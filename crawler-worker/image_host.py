#!/usr/bin/env python3
"""Image host backed by Cloudflare R2 (S3-compatible).

Free tier: 10 GB storage + 10M Class-A ops + 1M Class-B ops + $0 egress / month.
The only hard cap is 10 GB STORED at any moment.

Cost-optimized, original-image-first strategy
---------------------------------------------
  * The crawler keeps the ORIGINAL article image URL as the primary
    `image_url` whenever that URL is reachable and serves a real image.
    This costs ZERO R2 storage and the lowest copyright exposure.
  * R2 is used ONLY as a fallback: when the original URL is dead / blocked
    at crawl time, we download it once and store it in R2, then point
    `image_url` at the R2 public URL.
  * Upload uses AWS SigV4 over the S3 API implemented with the stdlib only
    (no boto3 dependency, so it runs on the GitHub Actions runner as-is).

Public URL shape:  R2_PUBLIC_BASE + "/" + key
  e.g. https://pub-<hash>.r2.dev/img/2026/07/ab12cd34.jpg
R2_PUBLIC_BASE must be set AFTER enabling bucket public access in the
Cloudflare dashboard (R2 -> bucket -> Settings -> Public access -> toggle on).
If R2 creds / R2_PUBLIC_BASE are missing, upload_images() degrades gracefully
and simply returns the original URLs (the article still gets its image).

Dedup: a committed image_map.json ({article_url: final_url}) means we never
re-probe or re-upload an article we already resolved; re-runs reuse the URL.
"""
import os
import io
import json
import time
import logging
import hashlib
import hmac
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx

log = logging.getLogger("image-host")

HERE = os.path.dirname(os.path.abspath(__file__))

# ── R2 config (all required for R2 to be active) ──────────────────────────────
R2_ACCOUNT_ID = os.environ.get("R2_ACCOUNT_ID", "").strip()
R2_ACCESS_KEY_ID = os.environ.get("R2_ACCESS_KEY_ID", "").strip()
R2_SECRET_ACCESS_KEY = os.environ.get("R2_SECRET_ACCESS_KEY", "").strip()
R2_BUCKET = os.environ.get("R2_BUCKET", "entropygate-images").strip()
R2_PUBLIC_BASE = os.environ.get("R2_PUBLIC_BASE", "").strip().rstrip("/")
# Test-only: when set to 1/true/yes, force every image into R2 regardless of
# original reachability. Default off — never affects production behaviour.
R2_FORCE_UPLOAD = os.environ.get("R2_FORCE_UPLOAD", "").strip().lower() in ("1", "true", "yes")

# ── tuning ────────────────────────────────────────────────────────────────────
MAX_BYTES = int(os.environ.get("IMG_MAX_BYTES", str(8 * 1024 * 1024)))
DOWNLOAD_TIMEOUT = int(os.environ.get("IMG_DL_TIMEOUT", "30"))
PROBE_TIMEOUT = int(os.environ.get("IMG_PROBE_TIMEOUT", "10"))
MAP_FILE = os.path.join(HERE, "image_map.json")

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def r2_enabled() -> bool:
    return bool(R2_ACCOUNT_ID and R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY
                and R2_BUCKET and R2_PUBLIC_BASE)


# ── dedup map ─────────────────────────────────────────────────────────────────
def load_map() -> dict:
    try:
        with open(MAP_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_map(m: dict) -> None:
    tmp = MAP_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False)
    os.replace(tmp, MAP_FILE)


# ── helpers ───────────────────────────────────────────────────────────────────
def _ext(url: str, content_type: str) -> str:
    path = urlparse(url).path.lower()
    if "." in path.rsplit("/", 1)[-1]:
        ext = "." + path.rsplit(".", 1)[-1].split("?")[0][:5]
        if 2 <= len(ext) <= 5 and ext[1:].isalnum():
            return ext
    ct = (content_type or "").lower()
    if "jpeg" in ct or "jpg" in ct:
        return ".jpg"
    if "png" in ct:
        return ".png"
    if "webp" in ct:
        return ".webp"
    if "gif" in ct:
        return ".gif"
    if "svg" in ct:
        return ".svg"
    if "avif" in ct:
        return ".avif"
    return ".jpg"


_EXT_CT = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".avif": "image/avif",
}


def _ct_for_ext(ext: str) -> str:
    return _EXT_CT.get(ext, "application/octet-stream")


def _looks_like_image(head: bytes) -> bool:
    if not head:
        return False
    if head[:3] == b"\xff\xd8\xff":                      # JPEG
        return True
    if head[:8] == b"\x89PNG\r\n\x1a\n":                 # PNG
        return True
    if head[:6] in (b"GIF87a", b"GIF89a"):               # GIF
        return True
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":    # WEBP
        return True
    if head[:5].lstrip().startswith(b"<"):               # SVG / HTML fallback
        return True
    return False


def _rel_path(article_url: str, ext: str) -> str:
    """Deterministic, sharded path so re-runs are idempotent (overwrite same key)."""
    h = hashlib.sha1(article_url.encode("utf-8")).hexdigest()[:16]
    d = datetime.now(timezone.utc)
    return f"img/{d.year}/{d.month:02d}/{h}{ext}"


def download(url: str) -> tuple:
    """Return (bytes, ext) or (None, None) on failure."""
    try:
        with httpx.Client(
            timeout=DOWNLOAD_TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": _USER_AGENT, "Accept": "image/*,*/*;q=0.8"},
        ) as c:
            r = c.get(url)
        if r.status_code != 200:
            log.warning("img download HTTP %s: %s", r.status_code, url)
            return None, None
        data = r.content
        if not data or len(data) > MAX_BYTES:
            log.warning("img skip size=%d: %s", len(data), url)
            return None, None
        if not _looks_like_image(data[:16]):
            log.warning("img not an image (magic=%r): %s", data[:8], url)
            return None, None
        ext = _ext(url, r.headers.get("content-type", ""))
        return data, ext
    except Exception as e:
        log.warning("img download error %s: %s", url, e)
        return None, None


def probe_image(url: str) -> bool:
    """True => original URL is usable, keep it (no R2 storage needed)."""
    try:
        with httpx.Client(
            timeout=PROBE_TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": _USER_AGENT, "Accept": "image/*,*/*;q=0.8"},
        ) as c:
            r = c.get(url)
        if r.status_code != 200:
            return False
        ct = r.headers.get("content-type", "").lower()
        if ct.startswith("image/"):
            return True
        return _looks_like_image(r.content[:16])
    except Exception:
        return False


# ── AWS SigV4 (stdlib only) for R2 S3 PUT ─────────────────────────────────────
def _hmac(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _sig_key(key: str, datestamp: str, region: str, service: str) -> bytes:
    k = _hmac(("AWS4" + key).encode("utf-8"), datestamp)
    k = _hmac(k, region)
    k = _hmac(k, service)
    k = _hmac(k, "aws4_request")
    return k


def _s3_put(key: str, data: bytes, content_type: str):
    """PUT object to R2. Returns (status_code, body_text)."""
    import http.client
    host = f"{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    path = f"/{R2_BUCKET}/{key}"
    amz = datetime.now(timezone.utc)
    amzdate = amz.strftime("%Y%m%dT%H%M%SZ")
    datestamp = amzdate[:8]
    region, service = "auto", "s3"
    payload_hash = hashlib.sha256(data).hexdigest()

    signed_headers = "host;x-amz-content-sha256;x-amz-date"
    canonical = "\n".join([
        "PUT", path, "",
        f"host:{host}",
        f"x-amz-content-sha256:{payload_hash}",
        f"x-amz-date:{amzdate}",
        "", signed_headers, payload_hash,
    ])
    scope = f"{datestamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join([
        "AWS4-HMAC-SHA256", amzdate, scope,
        hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    ])
    signing_key = _sig_key(R2_SECRET_ACCESS_KEY, datestamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"),
                         hashlib.sha256).hexdigest()
    auth = (f"AWS4-HMAC-SHA256 Credential={R2_ACCESS_KEY_ID}/{scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}")

    headers = {
        "Host": host,
        "X-Amz-Date": amzdate,
        "X-Amz-Content-Sha256": payload_hash,
        "Content-Type": content_type,
        "Authorization": auth,
    }
    conn = http.client.HTTPSConnection(host, 443, timeout=30)
    try:
        conn.request("PUT", path, body=data, headers=headers)
        resp = conn.getresponse()
        body = resp.read().decode("utf-8", "replace")
        return resp.status, body
    finally:
        conn.close()


def upload_object(key: str, data: bytes, content_type: str) -> bool:
    st, body = _s3_put(key, data, content_type)
    if 200 <= st < 300:
        return True
    log.warning("R2 PUT %s -> HTTP %s: %s", key, st, body[:160])
    return False


# ── public API ────────────────────────────────────────────────────────────────
def upload_images(need: dict) -> dict:
    """need: {article_url: original_image_url}. Returns {article_url: final_url}.

    Resolution order per article:
      * already resolved before  -> reuse (dedup map)
      * R2 not configured         -> keep original URL (graceful)
      * original URL reachable    -> keep original URL (zero R2 storage)
      * original dead             -> download + store in R2 (fallback)
      * download also fails       -> keep original URL as last resort
    """
    have = load_map()
    out: dict = {}

    if not r2_enabled():
        for a, orig in need.items():
            out[a] = have.get(a, orig)
        log.info("img: R2 not configured -> keeping %d original url(s)", len(out))
        return out

    to_resolve: dict = {}
    for a, orig in need.items():
        if not orig or not str(orig).startswith("http"):
            out[a] = orig
            continue
        if a in have:
            out[a] = have[a]
        else:
            to_resolve[a] = orig

    r2_hosted = 0
    for a, orig in to_resolve.items():
        if R2_FORCE_UPLOAD or probe_image(orig):
            final = orig                      # original usable (or force mode) -> no R2 storage
        else:
            data, ext = download(orig)
            if data is None:
                final = orig                  # can't rehost; keep original
            else:
                key = _rel_path(a, ext)
                if upload_object(key, data, _ct_for_ext(ext)):
                    final = f"{R2_PUBLIC_BASE}/{key}"
                    r2_hosted += 1
                else:
                    final = orig
        out[a] = final
        have[a] = final

    if to_resolve:
        save_map(have)
    log.info("img: %d newly hosted on R2 (force=%s) / %d resolved this run",
             r2_hosted, R2_FORCE_UPLOAD, len(to_resolve))
    return out


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("r2_enabled:", r2_enabled())
