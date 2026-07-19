#!/usr/bin/env python3
"""Backfill cover images for already-published articles via Unsplash/Pexels.

Reuses the crawler's ``image_search`` (Unsplash/Pexels/Wikimedia, with graceful
degradation) + ``image_host.upload_images`` (R2 mirror) so the resulting covers
are China-reachable. This is the retroactive counterpart to the crawler's
Pass-2 auto image search: it fixes covers for articles that are ALREADY in
Studio (the incremental crawler only touches freshly fetched items).

Modes:
  fill    -> only articles with NO cover (image_url empty)        [default]
  replace -> only articles that ALREADY have a cover (swap it out)
  all     -> both

Env: STUDIO_BASE_URL, STUDIO_ADMIN_PASSWORD, R2_*, AUTO_IMAGE_SEARCH,
      IMAGE_SEARCH_PROVIDER, UNSPLASH_ACCESS_KEY, PEXELS_API_KEY.
"""
import sys
import os
import time
import logging
import argparse

import httpx  # noqa: F401  (kept for parity with backfill.py imports)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("backfill-covers")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from image_host import upload_images, r2_enabled
import image_search as ims

# Reuse the exact Studio/R2 call patterns from backfill.py (no side effects on
# import because its logic lives under ``if __name__ == "__main__"``).
from backfill import api, login, fetch_all, is_r2

BASE = os.getenv("STUDIO_BASE_URL", "https://entropygate.cc.cd").rstrip("/") + "/api/v1"
ADMIN_U = "admin"
ADMIN_P = os.getenv("STUDIO_ADMIN_PASSWORD", "admin123")


def has_cover(a: dict) -> bool:
    return bool((a.get("image_url") or "").strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["fill", "replace", "all"], default="fill")
    args = ap.parse_args()
    mode = args.mode

    log.info("mode=%s r2_enabled=%s provider=%s enabled=%s",
             mode, r2_enabled(), ims.provider_name(), ims.enabled())
    if not ims.enabled():
        log.warning("AUTO_IMAGE_SEARCH disabled; nothing to search")
        return

    tok = login()
    arts = fetch_all()
    log.info("total articles=%d", len(arts))

    targets = []
    for a in arts:
        hc = has_cover(a)
        if mode == "fill" and hc:
            continue
        if mode == "replace" and not hc:
            continue
        targets.append(a)
    log.info("target articles (mode=%s)=%d", mode, len(targets))

    if not targets:
        log.info("nothing to do for mode=%s", mode)
        return

    # Search a cover for each target from its (rewritten) title.
    need = {}
    for a in targets:
        q = (a.get("rewritten_title") or a.get("title") or "")[:120]
        try:
            hits = ims.search_images(q, 1)
        except Exception as e:  # noqa: BLE001
            log.warning("search failed for %s: %s", a["id"], e)
            hits = []
        if hits:
            need[a["id"]] = hits[0]["url"]
            log.info("search #%s -> %s (%s)", a["id"], hits[0]["url"][:60], hits[0].get("source"))
        else:
            log.info("no hit for #%s", a["id"])
        time.sleep(0.3)

    log.info("searched covers=%d / targets=%d", len(need), len(targets))
    if not need:
        return

    hosted = upload_images(need)
    upd = fail = skip = 0
    for a in targets:
        if a["id"] not in need:
            continue
        final = hosted.get(a["id"])
        if not final or not is_r2(final):
            skip += 1
            continue
        if final == (a.get("image_url") or ""):
            skip += 1
            continue
        st, js = api("PUT", f"/articles/{a['id']}", token=tok, body={"image_url": final})
        if st == 200:
            upd += 1
        else:
            fail += 1
            log.warning("PUT /articles/%s failed %s %s", a["id"], st, str(js)[:140])
        time.sleep(0.2)

    log.info("COVER BACKFILL DONE mode=%s updated=%d failed=%d skip=%d",
             mode, upd, fail, skip)


if __name__ == "__main__":
    main()
