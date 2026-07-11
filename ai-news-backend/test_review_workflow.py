import httpx
from datetime import datetime

BASE = "http://localhost:8000/api/v1"
ADMIN_BASE = "http://localhost:8000/api/v1/admin"


def get_token():
    r = httpx.post(f"{ADMIN_BASE}/auth/login", json={"username": "admin", "password": "admin123"})
    r.raise_for_status()
    return r.json()["data"]["access_token"]


def test_review_workflow():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 获取 3 篇草稿
    r = httpx.get(f"{BASE}/articles?status=draft&size=3", headers=headers)
    r.raise_for_status()
    drafts = r.json()["data"]["items"]
    if len(drafts) < 3:
        print(f"草稿不足 3 篇，仅有 {len(drafts)} 篇")
        return

    ids = [a["id"] for a in drafts]
    print(f"测试文章 IDs: {ids}")

    # 1. 单篇通过
    r = httpx.post(f"{BASE}/articles/{ids[0]}/approve", headers=headers)
    print(f"单篇通过: {r.status_code} {r.json().get('message')}")

    # 2. 单篇废弃
    r = httpx.post(f"{BASE}/articles/{ids[1]}/reject", headers=headers)
    print(f"单篇废弃: {r.status_code} {r.json().get('message')}")

    # 3. 批量通过
    r = httpx.post(f"{BASE}/articles/batch-approve", json=[ids[2]], headers=headers)
    print(f"批量通过: {r.status_code} {r.json().get('message')} updated={r.json()['data'].get('updated')}")

    # 4. 状态隔离检查
    for status in ["draft", "published", "discarded"]:
        r = httpx.get(f"{BASE}/articles?status={status}&size=100", headers=headers)
        items = r.json()["data"]["items"]
        ids_in_status = [a["id"] for a in items]
        print(f"{status} 列表: {len(items)} 篇")
        # 检查是否有串状态
        if status == "published":
            assert ids[0] in ids_in_status, "单篇通过的文章未出现在 published"
            assert ids[1] not in ids_in_status, "废弃文章出现在 published"
        elif status == "discarded":
            assert ids[1] in ids_in_status, "废弃文章未出现在 discarded"

    print("\n状态隔离检查通过")


if __name__ == "__main__":
    test_review_workflow()

