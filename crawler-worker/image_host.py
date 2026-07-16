#!/usr/bin/env python3
"""Image host backed by a Cloudflare Pages + GitHub repo (free, no card).

Pipeline (per crawler run):
  1. Download each new article's cover image on the GitHub Actions runner
     (US egress can reach origins the China Studio cannot).
  2. Push ALL new images to the `entropygate-images` repo in ONE Git commit
     via the Git Data API (blob -> tree -> commit -> ref update). This triggers
     exactly one Cloudflare Pages build instead of one per image.
  3. Return the CDN URL `https://images.aientropygate.com/<path>` for each
     article so the worker can store it as `image_url`.

Dedup: a committed `image_map.json` ({article_url: pages_url}) means we never
re-download or re-upload an image we already hosted, and re-runs reuse the URL.

The mapping is idempotent: each article gets a deterministic filename derived
from its URL hash, so re-pushing overwrites the same object (safe).
"""
import os
import io
import json
import time
import logging
import hashlib
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx

log = logging.getLogger("image-host")

HERE = os.path.dirname(os.path.abspath(__file__))

IMG_REPO = os.environ.get("IMG_REPO", "dl19811010-rgb/entropygate-images")
IMG_BRANCH = os.environ.get("IMG_BRANCH", "main")
IMG_BASE = os.environ.get("IMG_BASE", "https://images.aientropygate.com").rstrip("/")
GITHUB_API = "https://api.github.com"

# Skip absurdly large files; keeps Pages builds fast and within limits.
MAX_BYTES = int(os.environ.get("IMG_MAX_BYTES", str(8 * 1024 * 1024)))
DOWNLOAD_TIMEOUT = int(os.environ.get("IMG_DL_TIMEOUT", "30"))
MAP_FILE = os.path.join(HERE, "image_map.json")

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def _gh_headers() -> dict:
    tok = os.environ.get("GITHUB_PAT", "")
    h = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "entropygate-crawler",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


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


def _ext(url: str, content_type: str) -> str:
    """Pick a file extension from the URL path and/or Content-Type."""
    path = urlparse(url).path.lower()
    # strip query/fragment already gone in path
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


def _rel_path(article_url: str, ext: str) -> str:
    """Deterministic, sharded path so re-runs are idempotent."""
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
        # crude magic-byte check so we don't host HTML error pages
        head = data[:8]
        if not (
            head[:3] == b"\xff\xd8\xff"            # JPEG
            or head[:8] == b"\x89PNG\r\n\x1a\n"     # PNG
            or head[:6] in (b"GIF87a", b"GIF89a")   # GIF
            or head[:4] == b"RIFF"                  # WEBP (RIFF....WEBP)
            or head[:5] == b"%PDF-"                 # (ignore pdf)
        ):
            # allow webp (RIFF....WEBP) and svg
            if not (head[:4] == b"RIFF" and data[8:12] == b"WEBP") and not data[:5].lstrip().startswith(b"<"):
                log.warning("img not an image (magic=%r): %s", head, url)
                return None, None
        ext = _ext(url, r.headers.get("content-type", ""))
        return data, ext
    except Exception as e:
        log.warning("img download error %s: %s", url, e)
        return None, None


# ── GitHub Git Data API helpers ──────────────────────────────────────────────
def _api_get(path: str) -> dict:
    r = httpx.get(f"{GITHUB_API}{path}", headers=_gh_headers(), timeout=30)
    r.raise_for_status()
    return r.json()


def _api_post(path: str, json_body: dict) -> dict:
    r = httpx.post(f"{GITHUB_API}{path}", headers=_gh_headers(), json=json_body, timeout=30)
    r.raise_for_status()
    return r.json()


def _api_patch(path: str, json_body: dict) -> dict:
    r = httpx.patch(f"{GITHUB_API}{path}", headers=_gh_headers(), json=json_body, timeout=30)
    r.raise_for_status()
    return r.json()


def _resolve_base() -> tuple:
    """Return (commit_sha, tree_sha) for IMG_BRANCH head."""
    ref = _api_get(f"/repos/{IMG_REPO}/git/refs/heads/{IMG_BRANCH}")
    commit_sha = ref["object"]["sha"]
    commit = _api_get(f"/repos/{IMG_REPO}/git/commits/{commit_sha}")
    return commit_sha, commit["tree"]["sha"]


def _push_batch(items: list) -> dict:
    """items: list of (rel_path, bytes). Returns {rel_path: cdn_url}."""
    if not items:
        return {}
    commit_sha, base_tree = _resolve_base()
    entries = []
    for rel_path, data in items:
        blob = _api_post(
            f"/repos/{IMG_REPO}/git/blobs",
            {"content": base64_encode(data), "encoding": "base64"},
        )
        entries.append(
            {"path": rel_path, "mode": "100644", "type": "blob", "sha": blob["sha"]}
        )
    tree = _api_post(
        f"/repos/{IMG_REPO}/git/trees",
        {"base_tree": base_tree, "tree": entries},
    )
    new_commit = _api_post(
        f"/repos/{IMG_REPO}/git/commits",
        {
            "message": f"chore: host {len(items)} cover image(s) via crawler",
            "tree": tree["sha"],
            "parents": [commit_sha],
        },
    )
    _api_patch(
        f"/repos/{IMG_REPO}/git/refs/heads/{IMG_BRANCH}",
        {"sha": new_commit["sha"]},
    )
    return {p: f"{IMG_BASE}/{p}" for p, _ in items}


def base64_encode(data: bytes) -> str:
    import base64
    return base64.b64encode(data).decode("ascii")


def upload_images(need: dict) -> dict:
    """need: {article_url: original_image_url}. Returns {article_url: cdn_url}.

    Reuses any previously hosted URL from the committed map; downloads and
    uploads only the new ones (batched into a single commit).
    """
    have = load_map()
    out: dict = {}
    to_fetch: dict = {}  # article_url -> original_image_url (not yet hosted)
    for article_url, orig in need.items():
        if not orig or not str(orig).startswith("http"):
            continue
        if article_url in have:
            out[article_url] = have[article_url]
        else:
            to_fetch[article_url] = orig

    if not to_fetch:
        return out

    batch = []  # (rel_path, bytes, article_url)
    for article_url, orig in to_fetch.items():
        data, ext = download(orig)
        if data is None:
            continue
        rel = _rel_path(article_url, ext)
        batch.append((rel, data, article_url))

    if batch:
        try:
            paths = _push_batch([(p, d) for p, d, _ in batch])
            for rel, _d, article_url in batch:
                if rel in paths:
                    out[article_url] = paths[rel]
                    have[article_url] = paths[rel]
            save_map(have)
            log.info("img hosted %d new / %d requested", len(paths), len(batch))
        except Exception as e:
            log.warning("img batch push failed: %s", e)
            # fall back: keep original URLs so the article still has an image
            for _rel, _d, article_url in batch:
                if article_url not in out:
                    out[article_url] = to_fetch[article_url]

    return out


if __name__ == "__main__":
    # smoke test: host a tiny PNG
    logging.basicConfig(level=logging.INFO)
    png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xcf"
        b"\xc0\xf0\x1f\x00\x05\x05\x02\x00\x9d\xc5\xd7\xd3\x00\x00\x00\x00IEND"
        b"\xaeB`\x82"
    )
    res = upload_images({"https://example.com/smoke": "data-bin"})
    print("result:", res)
