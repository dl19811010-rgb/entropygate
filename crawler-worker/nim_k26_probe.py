# -*- coding: utf-8 -*-
"""NIM kimi-k2.6 探针（GHA 美区出口，stdlib only）。

三阶段：
1. 可用性：一次小调用（非流式），记录状态/延迟/完整响应头。
2. 真实成稿：复用 gemini_probe_payload.json 的 zh 文章 + 生产提示词（与 kimi_rewrite.py
   完全一致），SSE 流式，temperature=0.6（与生产 kimi_client.py 一致），记录 usage/延迟，
   产出 HTML 样本。
3. 额度锤击：小调用循环（1.6s 间隔，远低于 40 RPM 限制），直到 429 或达到上限，
   记录成功计数、累计 usage tokens、429 时的响应头与错误体——据此判断额度性质
   （按请求数 vs 按 token vs credit 制）。

产出 -> nim_out/: report.json / k26_zh_sample.html / hammer_log.jsonl
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "moonshotai/kimi-k2.6"
KEY = os.environ.get("NVIDIA_API_KEY", "").strip()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "nim_out")
os.makedirs(OUTDIR, exist_ok=True)

PAYLOAD_PATH = os.path.join(HERE, "gemini_probe_payload.json")

HAMMER_MAX_CALLS = 240
HAMMER_INTERVAL_S = 1.6
HAMMER_TIME_BUDGET_S = 720


def hdr_dict(r):
    return {k.lower(): v for k, v in r.headers.items()}


def post(body, timeout=120, stream=False):
    """返回 (status, headers, parsed_or_raw)。stream=True 时返回 SSE 聚合结果。"""
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        URL,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream" if stream else "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            h = hdr_dict(r)
            if not stream:
                return r.status, h, json.loads(r.read().decode())
            # SSE 聚合
            content_parts, reasoning_parts, usage = [], [], {}
            finish = None
            raw = b""
            while True:
                chunk = r.read1(65536) if hasattr(r, "read1") else r.read(65536)
                if not chunk:
                    break
                raw += chunk
            for line in raw.decode("utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                try:
                    ev = json.loads(payload)
                except Exception:
                    continue
                ch = (ev.get("choices") or [{}])[0]
                delta = ch.get("delta") or {}
                if delta.get("content"):
                    content_parts.append(delta["content"])
                if delta.get("reasoning_content"):
                    reasoning_parts.append(delta["reasoning_content"])
                if ch.get("finish_reason"):
                    finish = ch["finish_reason"]
                if ev.get("usage"):
                    usage = ev["usage"]
            return r.status, h, {
                "content": "".join(content_parts),
                "reasoning": "".join(reasoning_parts),
                "usage": usage,
                "finish_reason": finish,
            }
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            body_j = json.loads(raw)
        except Exception:
            body_j = {"raw": raw[:1500]}
        return e.code, {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}, body_j
    except Exception as e:
        return -1, {}, {"exception": repr(e)[:400]}


def strip_fences(html):
    h = (html or "").strip()
    if h.startswith("```"):
        h = re.sub(r"^```[a-zA-Z]*\s*", "", h)
        h = re.sub(r"\s*```\s*$", "", h)
    return h


def looks_complete(html):
    h = (html or "").strip()
    return len(h) >= 8000 and h.lower().rstrip().endswith("</html>")


def extract_h1(html):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html or "", re.I | re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()


def phase_availability(report):
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "用一句中文回答：1+1等于几？"}],
        "max_tokens": 32,
        "temperature": 0.6,
        "stream": False,
    }
    t0 = time.time()
    st, h, j = post(body, timeout=180)
    el = round(time.time() - t0, 1)
    rec = {"http": st, "elapsed_s": el, "headers": h}
    if st == 200:
        msg = (j.get("choices") or [{}])[0].get("message", {})
        rec["content"] = (msg.get("content") or "")[:200]
        rec["usage"] = j.get("usage")
    else:
        rec["error"] = json.dumps(j, ensure_ascii=False)[:1200]
    report["phase1_availability"] = rec
    print(f"[phase1] http={st} {el}s content={rec.get('content','')[:80]!r}", flush=True)
    return st == 200


def phase_rewrite(report):
    if not os.path.exists(PAYLOAD_PATH):
        report["phase2_rewrite"] = {"skipped": "payload not found"}
        return None
    payload = json.load(open(PAYLOAD_PATH, encoding="utf-8"))
    zh = next((a for a in payload["articles"] if a.get("slot") == "zh"), payload["articles"][0])
    source_text = (
        f"标题：{zh['title']}\n来源：{zh.get('source_name') or '未知'}\n\n{zh['content'][:12000]}"
    )
    user = payload["user_tmpl"].replace("{{BLUEPRINT}}", payload["blueprint"]).replace(
        "{{ARTICLE}}", source_text
    )
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": payload["system"]},
            {"role": "user", "content": user},
        ],
        "max_tokens": 32000,
        "temperature": 0.6,
        "stream": True,
    }
    last = None
    for attempt in range(2):
        t0 = time.time()
        st, h, j = post(body, timeout=900, stream=True)
        el = round(time.time() - t0, 1)
        if st == 200:
            html = strip_fences(j["content"])
            fname = "k26_zh_sample.html"
            open(os.path.join(OUTDIR, fname), "w", encoding="utf-8").write(html)
            rec = {
                "http": st,
                "elapsed_s": el,
                "usage": j.get("usage"),
                "finish_reason": j.get("finish_reason"),
                "reasoning_chars": len(j.get("reasoning") or ""),
                "html_len": len(html),
                "looks_complete": looks_complete(html),
                "h1": extract_h1(html),
                "file": fname,
            }
            report["phase2_rewrite"] = rec
            print(
                f"[phase2] http=200 {el}s html_len={rec['html_len']} "
                f"complete={rec['looks_complete']} usage={rec['usage']}",
                flush=True,
            )
            return rec
        last = {"http": st, "elapsed_s": el, "error": json.dumps(j, ensure_ascii=False)[:1200], "headers": h}
        print(f"[phase2] attempt{attempt} http={st} {el}s", flush=True)
        if st in (429, 500, 502, 503, 504):
            time.sleep(20 * (attempt + 1))
            continue
        break
    report["phase2_rewrite"] = last
    return None


def phase_hammer(report):
    log_path = os.path.join(OUTDIR, "hammer_log.jsonl")
    log = open(log_path, "w", encoding="utf-8")
    t_start = time.time()
    ok = 0
    cum_tokens = 0
    stop_info = None
    first_headers = None
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "回复一个字：好"}],
        "max_tokens": 8,
        "temperature": 0,
        "stream": False,
    }
    for i in range(1, HAMMER_MAX_CALLS + 1):
        if time.time() - t_start > HAMMER_TIME_BUDGET_S:
            stop_info = {"reason": "time_budget", "calls": i - 1}
            break
        t0 = time.time()
        st, h, j = post(body, timeout=60)
        el = round(time.time() - t0, 1)
        if first_headers is None:
            first_headers = h
        if st == 200:
            ok += 1
            u = j.get("usage") or {}
            cum_tokens += int(u.get("total_tokens") or 0)
            if i % 20 == 0:
                print(f"[hammer] {i} calls ok={ok} cum_tokens={cum_tokens}", flush=True)
            log.write(json.dumps({"i": i, "st": st, "el": el, "usage": u}, ensure_ascii=False) + "\n")
        else:
            err = json.dumps(j, ensure_ascii=False)[:800]
            log.write(json.dumps({"i": i, "st": st, "el": el, "err": err, "headers": h}, ensure_ascii=False) + "\n")
            print(f"[hammer] {i} http={st} {el}s err={err[:160]}", flush=True)
            if st == 429:
                # 5s 后确认一次，区分瞬时限流与日额耗尽
                time.sleep(5)
                st2, h2, j2 = post(body, timeout=60)
                if st2 == 429:
                    stop_info = {
                        "reason": "429_confirmed",
                        "calls_ok": ok,
                        "first_429_headers": h,
                        "first_429_body": json.loads(err) if err.startswith("{") else err,
                        "confirm_429_headers": h2,
                        "confirm_429_body": j2,
                    }
                    break
                else:
                    print(f"[hammer] 429 transient, confirm http={st2}, continue", flush=True)
            elif st in (401, 403):
                stop_info = {"reason": f"auth_{st}", "calls_ok": ok, "body": err}
                break
            else:
                time.sleep(3)
        log.flush()
        time.sleep(HAMMER_INTERVAL_S)
    else:
        stop_info = {"reason": "max_calls_reached", "calls_ok": ok}
    log.close()
    elapsed = round(time.time() - t_start, 1)
    report["phase3_hammer"] = {
        "calls_ok": ok,
        "cum_tokens": cum_tokens,
        "elapsed_s": elapsed,
        "first_call_headers": first_headers,
        "stop": stop_info,
    }
    print(f"[hammer DONE] ok={ok} cum_tokens={cum_tokens} stop={stop_info['reason']}", flush=True)


def derive_estimates(report):
    p2 = report.get("phase2_rewrite") or {}
    p3 = report.get("phase3_hammer") or {}
    est = {}
    if p2.get("usage"):
        u = p2["usage"]
        est["per_article_tokens"] = {
            "prompt": u.get("prompt_tokens"),
            "completion": u.get("completion_tokens"),
            "total": u.get("total_tokens"),
        }
    stop = (p3.get("stop") or {}).get("reason")
    ok = p3.get("calls_ok", 0)
    if stop == "429_confirmed":
        est["daily_request_cap_observed"] = ok
        est["note"] = "锤击在 429 处停止（两次确认）。若按请求计，成稿量≈该值/天；若按 token 计需看累计。"
        if est.get("per_article_tokens") and p3.get("cum_tokens"):
            est["daily_articles_by_token"] = round(
                p3["cum_tokens"] / max(est["per_article_tokens"]["total"] or 1, 1), 1
            )
    elif stop == "max_calls_reached":
        est["note"] = f"{ok} 次小调用无 429——日额未触顶，成稿兜底需求（25-60 篇/天）在请求数维度充分满足。"
        est["daily_request_cap_observed"] = f">={ok}"
    elif stop == "time_budget":
        est["note"] = f"时间预算内完成 {ok} 次无 429。"
        est["daily_request_cap_observed"] = f">={ok}"
    else:
        est["note"] = f"锤击异常停止: {stop}"
    report["estimates"] = est


def main():
    report = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": MODEL}
    out = os.path.join(OUTDIR, "report.json")
    if not KEY:
        report["fatal"] = "NVIDIA_API_KEY missing"
        json.dump(report, open(out, "w"), indent=1)
        print("FATAL: no key")
        return 1
    if not phase_availability(report):
        json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("FATAL: availability failed")
        return 1
    phase_rewrite(report)
    phase_hammer(report)
    derive_estimates(report)
    json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("PROBE DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
