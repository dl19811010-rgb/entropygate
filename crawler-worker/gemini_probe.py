# -*- coding: utf-8 -*-
"""Gemini 成稿质量探针（GHA 美区出口，stdlib only）。

流程：
1. GET /v1beta/models 枚举 key 可用模型 -> gemini_out/models.json
2. 选主测模型：优先 gemini-3.6-flash，回退 3.5-flash，再回退任一 flash 文本模型；
   检测 thinking 支持（名称含 think 或 Model 资源 thinking 字段为真）。
3. 用生产提示词（AST 提取的 SYSTEM + USER_TMPL + 蓝本，与 kimi_rewrite.py 完全一致）
   对 zh / en 两篇原始报道各跑一次 generateContent（非流式，maxOutputTokens=65536）。
4. 若支持 thinking，加测一篇 zh（thinkingBudget=8192）做对比。
5. 产出 -> gemini_out/: models.json / probe_report.json / out_{model}_{slot}.html
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta"
KEY = os.environ.get("GEMINI_API_KEY", "").strip()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "gemini_out")
os.makedirs(OUTDIR, exist_ok=True)

PAYLOAD = json.load(open(os.path.join(HERE, "gemini_probe_payload.json"), encoding="utf-8"))

SKIP_MODEL = re.compile(r"image|tts|audio|live|robotics|embedding|aqa", re.I)
SAFETY = [
    {"category": c, "threshold": "BLOCK_NONE"}
    for c in (
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_DANGEROUS_CONTENT",
        "HARM_CATEGORY_CIVIC_INTEGRITY",
    )
]


def http(method, url, body=None, timeout=660):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw[:2000]}


def list_models():
    out, page = [], None
    while True:
        url = f"{API}/models?key={KEY}&pageSize=100"
        if page:
            url += f"&pageToken={page}"
        st, j = http("GET", url, timeout=120)
        if st != 200:
            return st, j, []
        out += j.get("models") or []
        page = j.get("nextPageToken")
        if not page:
            break
    return 200, None, out


def pick_primary(models):
    names = [
        m["name"].split("/")[-1]
        for m in models
        if "generateContent" in (m.get("supportedGenerationMethods") or [])
    ]
    text_models = [n for n in names if not SKIP_MODEL.search(n)]
    for pat in (r"gemini-3[.-]6-flash", r"gemini-3[.-]5-flash", r"gemini-.*flash"):
        cands = sorted(n for n in text_models if re.search(pat, n, re.I))
        if cands:
            return cands[0], text_models
    return (text_models[0] if text_models else None), text_models


def supports_thinking(model_obj, name):
    if model_obj and model_obj.get("thinking"):
        return True
    return bool(re.search(r"think", name, re.I))


def gen(model, system, user, thinking_budget=0):
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "safetySettings": SAFETY,
        "generationConfig": {
            "maxOutputTokens": 65536,
            "temperature": float(PAYLOAD.get("temperature", 0.6)),
        },
    }
    if thinking_budget:
        body["generationConfig"]["thinkingConfig"] = {
            "thinkingBudget": thinking_budget,
            "includeThoughts": False,
        }
    url = f"{API}/models/{model}:generateContent?key={KEY}"
    last = None
    for attempt in range(3):
        t0 = time.time()
        st, j = http("POST", url, body=body)
        elapsed = round(time.time() - t0, 1)
        if st == 200:
            return st, j, elapsed
        last = (st, j, elapsed)
        if st in (429, 500, 502, 503, 504):
            time.sleep(20 * (attempt + 1))
            continue
        break
    return last[0], last[1], last[2]


def resp_text(j):
    parts = (((j.get("candidates") or [{}])[0].get("content") or {}).get("parts")) or []
    return "".join(p.get("text", "") for p in parts)


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


def run_one(model, slot, article, thinking_budget=0):
    source_text = (
        f"标题：{article['title']}\n来源：{article.get('source_name') or '未知'}\n\n"
        f"{article['content'][:12000]}"
    )
    user = PAYLOAD["user_tmpl"].replace("{{BLUEPRINT}}", PAYLOAD["blueprint"]).replace(
        "{{ARTICLE}}", source_text
    )
    system = PAYLOAD["system"]
    if PAYLOAD.get("system_addendum"):
        system = system + "\n\n" + PAYLOAD["system_addendum"]
    st, j, elapsed = gen(model, system, user, thinking_budget)
    rec = {
        "model": model,
        "slot": slot,
        "article_id": article["id"],
        "thinking_budget": thinking_budget,
        "http": st,
        "elapsed_s": elapsed,
    }
    if st != 200:
        rec["error"] = json.dumps(j, ensure_ascii=False)[:1500]
        return rec
    html = strip_fences(resp_text(j))
    cand = (j.get("candidates") or [{}])[0]
    usage = j.get("usageMetadata") or {}
    fname = f"out_{model.replace('.', '-')}_{slot}{'_think' if thinking_budget else ''}.html"
    open(os.path.join(OUTDIR, fname), "w", encoding="utf-8").write(html)
    rec.update(
        finish_reason=cand.get("finishReason"),
        prompt_tokens=usage.get("promptTokenCount"),
        output_tokens=usage.get("candidatesTokenCount"),
        thoughts_tokens=usage.get("thoughtsTokenCount"),
        html_len=len(html),
        looks_complete=looks_complete(html),
        h1=extract_h1(html),
        tail40=html[-40:],
        file=fname,
    )
    return rec


def main():
    report = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "runs": []}
    if not KEY:
        report["fatal"] = "GEMINI_API_KEY missing"
        json.dump(report, open(os.path.join(OUTDIR, "probe_report.json"), "w"), indent=1)
        return 1

    st, err, models = list_models()
    if st != 200:
        report["fatal"] = f"list_models http={st}: {json.dumps(err, ensure_ascii=False)[:1500]}"
        json.dump(report, open(os.path.join(OUTDIR, "probe_report.json"), "w"), indent=1)
        return 1

    json.dump(models, open(os.path.join(OUTDIR, "models.json"), "w"), ensure_ascii=False, indent=1)
    primary, text_models = pick_primary(models)
    by_name = {m["name"].split("/")[-1]: m for m in models}
    think_names = [n for n in text_models if re.search(r"think", n, re.I)]
    report["text_models"] = text_models
    report["think_named_models"] = think_names
    report["primary"] = primary
    report["primary_thinking_flag"] = bool(by_name.get(primary, {}).get("thinking")) if primary else False
    print(f"primary={primary} think_named={think_names} text_models={len(text_models)}")

    if not primary:
        report["fatal"] = "no usable text model"
        json.dump(report, open(os.path.join(OUTDIR, "probe_report.json"), "w"), indent=1)
        return 1

    for a in PAYLOAD["articles"]:
        rec = run_one(primary, a["slot"], a)
        report["runs"].append(rec)
        print(json.dumps({k: rec.get(k) for k in ("slot", "http", "elapsed_s", "html_len", "looks_complete", "h1")}, ensure_ascii=False))

    # thinking 对比测：主模型支持思考 或 存在独立 thinking 命名模型
    think_model = primary if report["primary_thinking_flag"] else (think_names[0] if think_names else None)
    if think_model:
        zh = next((a for a in PAYLOAD["articles"] if a["slot"] == "zh"), None)
        if zh:
            rec = run_one(think_model, "zh", zh, thinking_budget=8192)
            report["runs"].append(rec)
            print(json.dumps({k: rec.get(k) for k in ("slot", "http", "elapsed_s", "html_len", "looks_complete", "h1")}, ensure_ascii=False))

    json.dump(report, open(os.path.join(OUTDIR, "probe_report.json"), "w"), ensure_ascii=False, indent=1)
    ok = all(r.get("looks_complete") for r in report["runs"] if r.get("http") == 200)
    print("PROBE DONE, all_complete =", ok)
    return 0


if __name__ == "__main__":
    sys.exit(main())
