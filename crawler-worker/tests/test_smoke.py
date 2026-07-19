#!/usr/bin/env python3
"""Lightweight self-test for crawler-worker modules (no network required).

Run with:  python -m unittest tests.test_smoke -v

These tests exist so the CI workflow fails fast when crawler code is broken,
instead of discovering it after a 5-minute Playwright/Chromium install on the
real crawl run. All network access is either stubbed or avoided.
"""
import importlib
import os
import sys
import unittest

# Make crawler-worker importable whether run from repo root or its own dir.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

import image_search as ims  # noqa: E402

_ENV_KEYS = (
    "IMAGE_SEARCH_PROVIDER",
    "UNSPLASH_ACCESS_KEY",
    "PEXELS_API_KEY",
    "AUTO_IMAGE_SEARCH",
)


def _reload(**env):
    """Reload image_search with a clean, controlled environment."""
    saved = {k: os.environ.pop(k, None) for k in _ENV_KEYS}
    for k, v in env.items():
        if v is not None:
            os.environ[k] = v
    try:
        return importlib.reload(ims)
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


class TestConfig(unittest.TestCase):
    def setUp(self):
        _reload()  # clean baseline

    def test_defaults(self):
        m = _reload(IMAGE_SEARCH_PROVIDER="wikimedia")
        self.assertTrue(m.enabled())
        self.assertEqual(m.provider_name(), "wikimedia")

    def test_unsplash_with_key(self):
        m = _reload(IMAGE_SEARCH_PROVIDER="unsplash", UNSPLASH_ACCESS_KEY="demo-key")
        self.assertEqual(m.provider_name(), "unsplash")

    def test_unsplash_without_key_degrades(self):
        m = _reload(IMAGE_SEARCH_PROVIDER="unsplash", UNSPLASH_ACCESS_KEY=None)
        self.assertEqual(m.provider_name(), "wikimedia")

    def test_pexels_with_key(self):
        m = _reload(IMAGE_SEARCH_PROVIDER="pexels", PEXELS_API_KEY="demo-key")
        self.assertEqual(m.provider_name(), "pexels")

    def test_pexels_without_key_degrades(self):
        m = _reload(IMAGE_SEARCH_PROVIDER="pexels", PEXELS_API_KEY=None)
        self.assertEqual(m.provider_name(), "wikimedia")

    def test_auto_disabled_off_values(self):
        for val in ("0", "false", "no", "off"):
            m = _reload(AUTO_IMAGE_SEARCH=val)
            self.assertFalse(m.enabled(), f"AUTO_IMAGE_SEARCH={val!r} should disable")


class TestSearchImages(unittest.TestCase):
    def setUp(self):
        _reload()

    def test_empty_query_no_network(self):
        # Early return before any HTTP; must not raise.
        self.assertEqual(ims.search_images(""), [])
        self.assertEqual(ims.search_images("   "), [])


class TestWikimediaParser(unittest.TestCase):
    """Verify Wikimedia result filtering without hitting the network.

    We monkeypatch the low-level _get so _search_wikimedia parses canned data.
    """

    def _fake_get(self, url, params, headers):
        return {
            "query": {
                "pages": [
                    # valid landscape jpeg -> kept
                    {
                        "title": "File:Valid.jpg",
                        "imageinfo": [
                            {
                                "mime": "image/jpeg",
                                "width": 2000,
                                "height": 1200,
                                "thumburl": "http://x/valid.jpg",
                                "extmetadata": {"LicenseShortName": {"value": "CC BY"}},
                            }
                        ],
                    },
                    # svg -> skipped
                    {
                        "title": "File:Bad.svg",
                        "imageinfo": [
                            {"mime": "image/svg+xml", "width": 512, "height": 512,
                             "url": "http://x/bad.svg"}
                        ],
                    },
                    # tiny icon -> skipped
                    {
                        "title": "File:Tiny.png",
                        "imageinfo": [
                            {"mime": "image/png", "width": 100, "height": 100,
                             "url": "http://x/tiny.png"}
                        ],
                    },
                    # valid but only `url` (no thumburl) -> kept via fallback
                    {
                        "title": "File:NoThumb.jpg",
                        "imageinfo": [
                            {"mime": "image/jpeg", "width": 1500, "height": 900,
                             "url": "http://x/notnumb.jpg"}
                        ],
                    },
                ]
            }
        }

    def test_filtering(self):
        orig = ims._get
        ims._get = self._fake_get
        try:
            hits = ims._search_wikimedia("test query", max_results=5)
        finally:
            ims._get = orig

        urls = [h["url"] for h in hits]
        self.assertIn("http://x/valid.jpg", urls)
        self.assertIn("http://x/notnumb.jpg", urls)
        self.assertNotIn("http://x/bad.svg", urls)
        self.assertNotIn("http://x/tiny.png", urls)
        self.assertTrue(any(h["license"] == "CC BY" for h in hits))


if __name__ == "__main__":
    unittest.main()
