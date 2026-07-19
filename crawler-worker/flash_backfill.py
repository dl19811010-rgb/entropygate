#!/usr/bin/env python3
"""Backfill flash_meta for existing articles by re-running the LLM rewrite.

The backend rewrite endpoint now returns a flash_meta JSON along with the
Chinese rewrite. This script iterates over approved articles that lack a
flash_meta or have a failed rewrite, calls POST /articles/{id}/rewrite, and
records progress. It runs on the GitHub Actions US runner so it can reach the
configured LLM endpoint (via the backend) without GFW issues.

Env:
  STUDIO_BASE_URL        e.g. https://entropygate.cc.cd
  STUDIO_ADMIN_PASSWORD  admin password
  MODE                   fill (default) or all
"""
import json
import logging
import os
import sys
import time

import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from backfill import api, login  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("flash-backfill")

MODE = os.environ.get("MODE", "fill").strip().lower()


def fetch_article_ids() -> list[int]:
    """Fetch approved article IDs. MODE=fill only targets those without flash_meta."""
    ids = []
    page = 1
    while True:
        st, js = api("GET", f"/articles?status=approved&page={page}&page_size=100&fields=light")
        if st != 200:
            log.error("fetch articles failed %s %s", st, js)
            raise SystemExit(1)
        items = (js.get("data") or {}).get("items") or []
        if not items:
            break
        for a in items:
            aid = a["id"]
            if MODE == "fill":
                meta = a.get("flash_meta") or ""
                if meta and meta.strip() and meta != "null":
                    continue
            ids.append(aid)
        if len(items) < 100:
            break
        page += 1
        time.sleep(0.2)
    return ids


def rewrite_one(aid: int, token: str) -> dict:
    st, js = api("POST", f"/articles/{aid}/rewrite", token=token)
    if st != 200:
        return {"ok": False, "status": st, "error": str(js)[:200]}
    data = (js or {}).get("data") or {}
    return {
        "ok": True,
        "has_flash_meta": bool(data.get("flash_meta")),
        "rewrite_status": data.get("rewrite_status"),
    }


def main():
    tok = login()
    log.info("login ok, token length %d", len(tok))
    ids = fetch_article_ids(tok)
    log.info("target articles: %d (mode=%s)", len(ids), MODE)

    done = fail = 0
    for i, aid in enumerate(ids, 1):
        log.info("[%d/%d] rewriting article %d", i, len(ids), aid)
        try:
            res = rewrite_one(aid, tok)
            if res["ok"]:
                done += 1
                log.info("  -> ok, flash_meta=%s", res["has_flash_meta"])
            else:
                fail += 1
                log.warning("  -> failed status=%s %s", res["status"], res["error"])
        except Exception as e:  # noqa: BLE001
            fail += 1
            log.error("  -> exception: %s", e)
        time.sleep(1.5)

    log.info("FLASH BACKFILL DONE mode=%s total=%d done=%d fail=%d", MODE, len(ids), done, fail)


if __name__ == "__main__":
    main()
