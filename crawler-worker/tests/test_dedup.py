#!/usr/bin/env python3
"""Unit tests for crawler-worker distributed dedup (no network required).

Run with:  python -m unittest tests.test_dedup -v

``filter_new`` is a pure function. ``check_existing_urls`` talks to the Studio,
but we monkeypatch the low-level ``httpx.post`` so the tests never hit the
network — they verify the request shape and the graceful-degradation contract
(any failure => empty set, never an exception).
"""
import os
import sys
import unittest
from unittest import mock

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

import dedup  # noqa: E402


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text="", raise_on_json=False):
        self.status_code = status_code
        self._payload = payload if payload is not None else {}
        self.text = text
        self._raise_on_json = raise_on_json

    def json(self):
        if self._raise_on_json:
            raise ValueError("bad json")
        return self._payload


class TestFilterNew(unittest.TestCase):
    def test_keeps_unseen(self):
        planned = [{"url": "https://a"}, {"url": "https://b"}]
        kept, dropped = dedup.filter_new(planned, [])
        self.assertEqual(kept, planned)
        self.assertEqual(dropped, 0)

    def test_drops_existing(self):
        planned = [{"url": "https://a"}, {"url": "https://b"}, {"url": "https://c"}]
        kept, dropped = dedup.filter_new(planned, {"https://b"})
        self.assertEqual([p["url"] for p in kept], ["https://a", "https://c"])
        self.assertEqual(dropped, 1)

    def test_empty_existing_is_noop(self):
        planned = [{"url": "x"}]
        kept, dropped = dedup.filter_new(planned, set())
        self.assertEqual(kept, planned)
        self.assertEqual(dropped, 0)

    def test_missing_url_key_safe(self):
        planned = [{"title": "no url"}, {"url": "https://a"}]
        kept, dropped = dedup.filter_new(planned, {"https://a"})
        self.assertEqual(kept, [{"title": "no url"}])
        self.assertEqual(dropped, 1)

    def test_whitespace_normalised(self):
        planned = [{"url": "  https://a  "}]
        kept, dropped = dedup.filter_new(planned, {"https://a"})
        self.assertEqual(kept, [])
        self.assertEqual(dropped, 1)


class TestCheckExistingUrls(unittest.TestCase):
    def setUp(self):
        self.base = "https://studio.example.com"
        self.tok = "fake-token"

    def _call(self, fake):
        with mock.patch.object(dedup.httpx, "post", return_value=fake) as m:
            result = dedup.check_existing_urls(self.base, self.tok, ["https://a", "https://b"])
            # Verify the request was shaped correctly.
            args, kwargs = m.call_args
            self.assertEqual(args[0], f"{self.base}/api/v1/crawler/check-urls")
            self.assertEqual(kwargs["json"], {"urls": ["https://a", "https://b"]})
            self.assertEqual(kwargs["headers"]["X-Access-Token"], self.tok)
            return result

    def test_happy_path(self):
        fake = FakeResponse(200, {"code": 200, "data": {"existing": ["https://a"], "count": 1}})
        self.assertEqual(self._call(fake), {"https://a"})

    def test_empty_list_returns_empty_without_call(self):
        with mock.patch.object(dedup.httpx, "post") as m:
            self.assertEqual(dedup.check_existing_urls(self.base, self.tok, []), set())
            m.assert_not_called()

    def test_http_error_degrades(self):
        fake = FakeResponse(503, text="down")
        self.assertEqual(self._call(fake), set())

    def test_bad_envelope_code_degrades(self):
        fake = FakeResponse(200, {"code": 500, "message": "nope"})
        self.assertEqual(self._call(fake), set())

    def test_transport_exception_degrades(self):
        with mock.patch.object(dedup.httpx, "post", side_effect=RuntimeError("boom")):
            self.assertEqual(dedup.check_existing_urls(self.base, self.tok, ["u"]), set())

    def test_empty_existing_payload(self):
        fake = FakeResponse(200, {"code": 200, "data": {"existing": [], "count": 0}})
        self.assertEqual(self._call(fake), set())


if __name__ == "__main__":
    unittest.main()
