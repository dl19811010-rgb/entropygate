"""百度「普通收录」主动推送（GitHub Actions 版，美区出口）。

为什么在这里而不是 Studio 调度器：2026-07-26 实测 Studio 中国机房出口到
data.zz.baidu.com 链路被污染（https 证书主机名不匹配、http 返回假响应
"site init fail"），而本机（国内）与美区均正常。故推送迁移到 crawler 同款
GitHub Actions runner。

策略：新站日配额实测仅 ~10 条。从 Studio 公开 API 拉全部文章 id，升序取
last_id 之后的前 DAILY_CAP 条，分块 5 条 POST；整块成功才推进 last_id，
遇错即停（超配额/网络错误），明日继续。百度对重复 URL 幂等。

状态持久化：crawler-worker/baidu_push_state.json 随 workflow 提交回仓库。
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

SITE = "https://aientropygate.com"
PUSH_ENDPOINT = "http://data.zz.baidu.com/urls"  # 官方接口地址就是 http；https 证书无效
STUDIO = os.getenv("STUDIO_BASE_URL", "https://entropygate.cc.cd").rstrip("/")
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baidu_push_state.json")
DAILY_CAP = 10   # 实测新站配额 ~10 条/天，宁可少推不留失败
CHUNK = 5        # 整批超配额会被整体拒绝，小块推进
PAGE_SIZE = 100  # 后端 per_page 上限 ~200，留余量用 100
MAX_PAGES = 10


def log(msg, *args):
    print(f"[baidu-push] " + (msg % args if args else msg), flush=True)


def load_last_id() -> int:
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return int(json.load(f).get("last_id", 0))
    except Exception:
        return 0


def save_last_id(v: int) -> None:
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"last_id": v}, f)
    os.replace(tmp, STATE_FILE)


def http_json(url, timeout=30) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "entropygate-baidu-push/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_all_ids() -> list:
    """从 Studio 公开 API 拉取全部文章 id（fields=light 分页）。"""
    ids = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{STUDIO}/api/v1/articles?fields=light&per_page={PAGE_SIZE}&page={page}"
        try:
            j = http_json(url)
        except Exception as e:
            log("fetch page %s failed: %s", page, e)
            break
        items = (j.get("data") or {}).get("items") or []
        ids.extend(int(it["id"]) for it in items if it.get("id") is not None)
        if len(items) < PAGE_SIZE:
            break
    return sorted(set(ids))


def push_chunk(urls: list, token: str) -> dict:
    """推一批 URL。返回 {"ok":bool, "success":N, "remain":M, "resp":...}"""
    body = "\n".join(urls).encode("utf-8")
    req = urllib.request.Request(
        PUSH_ENDPOINT + f"?site={SITE}&token={token}",
        data=body, method="POST",
        headers={"Content-Type": "text/plain", "User-Agent": "curl/8.0 baidu-push"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            j = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            j = json.loads(e.read().decode("utf-8"))
        except Exception:
            j = {"http_status": e.code}
        return {"ok": False, "resp": j}
    except Exception as e:
        return {"ok": False, "resp": str(e)}
    if "success" in j:
        return {"ok": True, **j}
    return {"ok": False, "resp": j}


def main() -> int:
    token = os.getenv("BAIDU_PUSH_TOKEN", "").strip()
    if not token:
        log("BAIDU_PUSH_TOKEN not set, skip")
        return 0

    last = load_last_id()
    ids = fetch_all_ids()
    todo = [i for i in ids if i > last][:DAILY_CAP]
    log("total ids=%s, last_id=%s, todo=%s", len(ids), last, len(todo))
    if not todo:
        return 0

    pushed = 0
    for i in range(0, len(todo), CHUNK):
        chunk = todo[i : i + CHUNK]
        urls = [f"{SITE}/article?id={a}" for a in chunk]
        res = push_chunk(urls, token)
        if res.get("ok") and int(res.get("success", 0)) == len(chunk):
            save_last_id(chunk[-1])
            pushed += len(chunk)
            log("pushed %s ids up to %s (remain=%s)", len(chunk), chunk[-1], res.get("remain"))
            if int(res.get("remain", 1)) <= 0:
                log("remain=0, stop for today")
                break
            time.sleep(1)
            continue
        log("stop: %s", res.get("resp"))
        break

    log("done: pushed=%s, last_id=%s", pushed, load_last_id())
    return 0


if __name__ == "__main__":
    sys.exit(main())
