#!/usr/bin/env python3
"""Weekly orphan-pruning for the R2 image bucket.

Why: the crawler only uploads to R2 when an article's original image is dead.
But an article may later be rejected in curation, or deleted, leaving an
orphaned object in R2 that still counts toward the 10 GB free-storage cap.
This job deletes every R2 object under `img/` that is NOT referenced by any
published article's `image_url`.

It is SAFE by default: set CLEANUP_DRYRUN=1 to only report what *would* be
deleted. Run weekly via cleanup.yml (cron) or manually (workflow_dispatch).

Needs: R2_ACCOUNT_ID / R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY / R2_BUCKET /
R2_PUBLIC_BASE  +  STUDIO_BASE_URL / STUDIO_ADMIN_PASSWORD.
"""
import os
import sys
import json
import logging
import hashlib
import hmac
from datetime import datetime, timezone
from urllib.parse import quote

import httpx

log = logging.getLogger("cleanup-r2")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

R2_ACCOUNT_ID = os.environ.get("R2_ACCOUNT_ID", "").strip()
R2_ACCESS_KEY_ID = os.environ.get("R2_ACCESS_KEY_ID", "").strip()
R2_SECRET_ACCESS_KEY = os.environ.get("R2_SECRET_ACCESS_KEY", "").strip()
R2_BUCKET = os.environ.get("R2_BUCKET", "entropygate-images").strip()
R2_PUBLIC_BASE = os.environ.get("R2_PUBLIC_BASE", "").strip().rstrip("/")
STUDIO_BASE = os.environ.get("STUDIO_BASE_URL", "").rstrip("/")
ADMIN_PASS = os.environ.get("STUDIO_ADMIN_PASSWORD", "")
DRYRUN = os.environ.get("CLEANUP_DRYRUN", "0") == "1"


# ── SigV4 (stdlib only) ───────────────────────────────────────────────────────
def _hmac(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _sig_key(key, datestamp, region, service):
    k = _hmac(("AWS4" + key).encode(), datestamp)
    k = _hmac(k, region)
    k = _hmac(k, service)
    k = _hmac(k, "aws4_request")
    return k


def _s3_request(method, bucket, key="", query="", body=b""):
    import http.client
    host = f"{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    path = f"/{bucket}"
    if key:
        path += "/" + key
    if query:
        path += "?" + query
    amz = datetime.now(timezone.utc)
    amzdate = amz.strftime("%Y%m%dT%H%M%SZ")
    datestamp = amzdate[:8]
    region, service = "auto", "s3"
    payload_hash = hashlib.sha256(body).hexdigest()
    signed = "host;x-amz-content-sha256;x-amz-date"
    canonical = "\n".join([
        method, path, "",
        f"host:{host}",
        f"x-amz-content-sha256:{payload_hash}",
        f"x-amz-date:{amzdate}",
        "", signed, payload_hash,
    ])
    scope = f"{datestamp}/{region}/{service}/aws4_request"
    sts = "\n".join([
        "AWS4-HMAC-SHA256", amzdate, scope,
        hashlib.sha256(canonical.encode()).hexdigest(),
    ])
    skey = _sig_key(R2_SECRET_ACCESS_KEY, datestamp, region, service)
    sig = hmac.new(skey, sts.encode(), hashlib.sha256).hexdigest()
    auth = (f"AWS4-HMAC-SHA256 Credential={R2_ACCESS_KEY_ID}/{scope}, "
            f"SignedHeaders={signed}, Signature={sig}")
    headers = {
        "Host": host,
        "X-Amz-Date": amzdate,
        "X-Amz-Content-Sha256": payload_hash,
        "Authorization": auth,
    }
    if body:
        headers["Content-Type"] = "application/octet-stream"
    conn = http.client.HTTPSConnection(host, 443, timeout=30)
    try:
        conn.request(method, path, body=body or None, headers=headers)
        resp = conn.getresponse()
        data = resp.read()
        return resp.status, data
    finally:
        conn.close()


def list_r2_keys():
    keys = []
    token = None
    while True:
        q = "list-type=2&prefix=img/"
        if token:
            q += "&continuation-token=" + quote(token, safe="")
        st, body = _s3_request("GET", R2_BUCKET, query=q)
        if st != 200:
            log.error("ListObjects failed HTTP %s: %s", st, body[:200])
            return keys
        text = body.decode("utf-8", "replace")
        # strip xml namespaces for simple parsing
        import xml.etree.ElementTree as ET
        root = ET.fromstring(text)
        for c in root.iter():
            if c.tag.endswith("Contents"):
                k = None
                for child in c:
                    if child.tag.endswith("Key"):
                        k = child.text
                if k:
                    keys.append(k)
        truncated = None
        nxt = None
        for c in root.iter():
            if c.tag.endswith("IsTruncated"):
                truncated = c.text
            if c.tag.endswith("NextContinuationToken"):
                nxt = c.text
        if truncated == "true" and nxt:
            token = nxt
        else:
            break
    return keys


def studio_token():
    r = httpx.post(f"{STUDIO_BASE}/api/v1/admin/auth/login",
                   json={"username": "admin", "password": ADMIN_PASS}, timeout=30)
    r.raise_for_status()
    return r.json().get("data", {}).get("token")


def referenced_r2_keys(token_val):
    ref = set()
    page = 1
    prefix = R2_PUBLIC_BASE + "/"
    while True:
        r = httpx.get(f"{STUDIO_BASE}/api/v1/articles",
                      headers={"X-Access-Token": token_val},
                      params={"page": page, "page_size": 100,
                              "sort_by": "published_at", "sort_dir": "desc"},
                      timeout=30)
        if r.status_code != 200:
            log.warning("list articles HTTP %s", r.status_code)
            break
        d = r.json()
        data = d.get("data", d)
        items = data.get("items", []) or []
        for it in items:
            u = (it.get("image_url") or "")
            if u.startswith(prefix):
                ref.add(u[len(prefix):])
        if len(items) < 100:
            break
        page += 1
        if page > 300:
            break
    return ref


def main():
    missing = [n for n, v in (("R2_ACCOUNT_ID", R2_ACCOUNT_ID),
                              ("R2_ACCESS_KEY_ID", R2_ACCESS_KEY_ID),
                              ("R2_SECRET_ACCESS_KEY", R2_SECRET_ACCESS_KEY),
                              ("R2_BUCKET", R2_BUCKET),
                              ("R2_PUBLIC_BASE", R2_PUBLIC_BASE),
                              ("STUDIO_BASE_URL", STUDIO_BASE),
                              ("STUDIO_ADMIN_PASSWORD", ADMIN_PASS)) if not v]
    if missing:
        log.error("missing env: %s", ", ".join(missing))
        sys.exit(1)

    keys = list_r2_keys()
    log.info("R2 objects under img/: %d", len(keys))
    if not keys:
        log.info("nothing to prune")
        sys.exit(0)

    tok = studio_token()
    ref = referenced_r2_keys(tok)
    log.info("referenced R2 keys (from published articles): %d", len(ref))

    orphans = [k for k in keys if k not in ref]
    log.info("orphans to delete: %d", len(orphans))
    if DRYRUN:
        for k in orphans[:50]:
            log.info("  [dryrun] would delete %s", k)
        if len(orphans) > 50:
            log.info("  ... and %d more", len(orphans) - 50)
        sys.exit(0)

    deleted = 0
    for k in orphans:
        st, _ = _s3_request("DELETE", R2_BUCKET, key=k)
        if 200 <= st < 300 or st == 404:
            deleted += 1
        else:
            log.warning("delete failed %s -> HTTP %s", k, st)
    log.info("deleted %d / %d orphans", deleted, len(orphans))
    sys.exit(0)


if __name__ == "__main__":
    main()
