#!/usr/bin/env python3
"""Distributed dedup helpers for the crawler-worker.

The worker keeps a local ``seen_urls.json`` purely for *speed* (so it does not
re-fetch the full article text it has already processed). That file is NOT
authoritative when several crawl jobs run in parallel — each job starts from
its own snapshot and commits back independently, so two runners can both decide
a URL is "new" and both POST it.

The authoritative source of truth is the Studio backend: exactly one article
row exists per unique source URL. We therefore:

  1. Ask the backend which candidate URLs already have an article via
     ``POST /api/v1/crawler/check-urls`` (``check_existing_urls``) BEFORE we
     spend bandwidth fetching full text / searching cover images for them.
  2. Rely on the backend's idempotent-by-URL ingest (articles.create_article
     returns the existing row instead of inserting a duplicate) so that even a
     race between two workers that both POST the same URL cannot create two
     articles.

``filter_new`` is a pure, network-free function so it is trivially unit-testable
in CI without touching the backend.
"""
import logging

import httpx

logger = logging.getLogger("crawler.dedup")


def filter_new(planned, existing_urls):
    """Drop planned items whose URL already exists in the backend.

    Args:
        planned: list of dicts, each expected to carry a ``"url"`` key.
        existing_urls: iterable of URL strings already present server-side.

    Returns:
        (kept, dropped):
            kept   — subset of ``planned`` whose URL is NOT in ``existing_urls``.
            dropped — number of items removed.
    """
    known = set(existing_urls or [])
    kept = []
    dropped = 0
    for p in planned:
        url = (p.get("url") or "").strip()
        if url and url in known:
            dropped += 1
            continue
        kept.append(p)
    return kept, dropped


def check_existing_urls(base_url, tok, urls, timeout=30):
    """Query the Studio for which of ``urls`` already have an article.

    Returns a ``set`` of existing URLs. On ANY failure (HTTP error, bad
    envelope, transport exception) returns an EMPTY set so the caller falls back
    to local-only dedup — the backend still dedups on ingest, so an empty result
    here is safe, merely less efficient. Dedup is a best-effort optimisation and
    must never abort a crawl run.
    """
    if not urls:
        return set()
    try:
        r = httpx.post(
            f"{base_url.rstrip('/')}/api/v1/crawler/check-urls",
            json={"urls": urls},
            headers={"X-Access-Token": tok, "Content-Type": "application/json"},
            timeout=timeout,
        )
        if r.status_code != 200:
            logger.warning("check-urls HTTP %s: %s", r.status_code, r.text[:160])
            return set()
        body = r.json()
        if body.get("code") not in (None, 200, "200"):
            logger.warning(
                "check-urls code=%s: %s", body.get("code"), body.get("message")
            )
            return set()
        data = body.get("data") or {}
        return set(data.get("existing") or [])
    except Exception as ex:  # noqa: BLE001 - best-effort dedup must not fail the run
        logger.warning("check-urls failed (treating all as new): %s", ex)
        return set()
