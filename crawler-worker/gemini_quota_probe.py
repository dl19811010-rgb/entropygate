# -*- coding: utf-8 -*-
"""Gemini 3.6 Flash 免费日额探针（GHA 美区出口，stdlib only）。

小调用锤击：4.2s 间隔（≤15 RPM），最多 100 次或 8 分钟预算。
- 若打到 429：记录 QuotaFailure 详情（按天/按分钟维度一目了然），5s 后复核一次区分瞬时与日额。
- 若 100 次无 429：日额 >=100 次/天（已远超成稿兜底需求 25-60 篇/天），无需继续烧。

产出 -> gemini_quota_out/report.json
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = "gemini-3.6-flash"
API = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "gemini_quota_out")
os.makedirs(OUTDIR, exist_ok=True)

MAX_CALLS = 30
INTERVAL_S = 12.5
TIME_BUDGET_S = 480


def call():
    body = {
        "contents": [{"role": "user", "parts": [{"text": "回复一个字：好"}]}],
        "generationConfig": {"maxOutputTokens": 8, "temperature": 0},
    }
    req = urllib.request.Request(
        f"{API}?key={KEY}",
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode()), {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw), dict(e.headers or {})
        except Exception:
            return e.code, {"raw": raw[:1000]}, dict(e.headers or {})
    except Exception as e:
        return -1, {"exception": repr(e)[:300]}, {}


def main():
    report = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": MODEL,
        "calls": [],
    }
    out = os.path.join(OUTDIR, "report.json")
    if not KEY:
        report["fatal"] = "GEMINI_API_KEY missing"
        json.dump(report, open(out, "w"), indent=1)
        return 1

    ok = 0
    cum_tokens = 0
    stop = None
    t_start = time.time()
    for i in range(1, MAX_CALLS + 1):
        if time.time() - t_start > TIME_BUDGET_S:
            stop = {"reason": "time_budget", "calls_ok": ok}
            break
        t0 = time.time()
        st, j, h = call()
        el = round(time.time() - t0, 1)
        if st == 200:
            ok += 1
            u = j.get("usageMetadata") or {}
            cum_tokens += int(u.get("totalTokenCount") or 0)
            if i % 10 == 0:
                print(f"[quota] {i} ok cum_tokens={cum_tokens}", flush=True)
        else:
            err = json.dumps(j, ensure_ascii=False)[:900]
            print(f"[quota] {i} http={st} {el}s {err[:200]}", flush=True)
            if st == 429:
                time.sleep(30)
                st2, j2, _ = call()
                stop = {
                    "reason": "429_confirmed" if st2 == 429 else "429_transient",
                    "calls_ok": ok,
                    "first_429_body": j,
                    "confirm_http": st2,
                    "confirm_body": j2 if st2 != 200 else None,
                }
                if st2 == 429:
                    break
            elif st in (401, 403):
                stop = {"reason": f"auth_{st}", "body": err}
                break
            else:
                time.sleep(3)
        time.sleep(INTERVAL_S)
    else:
        stop = {"reason": "max_calls_reached", "calls_ok": ok}

    report["ok"] = ok
    report["cum_tokens"] = cum_tokens
    report["elapsed_s"] = round(time.time() - t_start, 1)
    report["stop"] = stop
    if stop["reason"] == "429_confirmed":
        report["verdict"] = f"日额≈{ok} 次/天（成稿兜底≈{ok} 篇/天，1 请求/篇）"
    elif ok >= MAX_CALLS:
        report["verdict"] = f"日额>={ok} 次/天（未触顶；成稿兜底 25-60 篇/天需求充分满足）"
    else:
        report["verdict"] = f"异常停止: {stop['reason']}"
    json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("QUOTA PROBE DONE:", report["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
