"""
文章管理增强 API - EntropyGate AI 新动态版块

新增接口：
- GET /api/v1/articles/today-stats — 今日内容生产统计
- POST /api/v1/articles/batch-approve — 批量通过
- POST /api/v1/articles/:id/process-ai — 触发AI处理
- GET /api/v1/articles/review/stats — 审核队列统计
- GET /api/v1/dashboard/stats — Dashboard统计(含趋势)

注意：这是后端 API 设计参考，实际实现需对接您的后端框架（FastAPI/Django/Flask等）
"""

from datetime import datetime, timedelta


def json_success(data=None, message="success"):
    return {"code": 200, "message": message, "data": data}

def json_error(message="error", code=400):
    return {"code": code, "message": message, "data": None}


def get_today_stats():
    """GET /api/v1/articles/today-stats — 今日内容生产统计"""
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # TODO: 替换为真实数据库查询
    mock_data = {
        "fetched": 42,
        "filtered": 24,
        "reviewed": 18,
        "published": 15,
        "discarded": 3,
        "filter_rate": round((42 - 24) / 42, 2) if 42 > 0 else 0,
        "approve_rate": round(15 / 18, 2) if 18 > 0 else 0,
        "date": today_start.isoformat(),
        "_note": "当前为模拟数据，请替换为数据库查询"
    }
    return json_success(mock_data)


def get_review_stats():
    """GET /api/v1/articles/review/stats — 审核队列统计"""
    mock_data = {
        "total_pending": 23,
        "high_score_count": 8,
        "availability_change_count": 3,
        "by_category": {
            "大模型动态": 10,
            "AI工具与应用": 6,
            "可用性追踪": 3,
            "行业动态": 3,
            "技术研究": 1
        },
        "by_source": {
            "量子位": {"passed": 6, "filtered": 2},
            "机器之心": {"passed": 5, "filtered": 1},
            "36氪": {"passed": 3, "filtered": 5},
            "Hacker News": {"passed": 4, "filtered": 2}
        },
        "avg_wait_minutes": 85.5,
        "_note": "当前为模拟数据"
    }
    return json_success(mock_data)


def batch_approve_articles(article_ids: list, admin_id: int):
    """POST /api/v1/articles/batch-approve — 批量通过文章"""
    results = {"success_count": 0, "failed_ids": [], "errors": []}
    for aid in article_ids:
        try:
            # TODO: UPDATE articles SET status='published' WHERE id=aid
            results["success_count"] += 1
        except Exception as e:
            results["failed_ids"].append(aid)
            results["errors"].append({"id": aid, "error": str(e)})
    return json_success(results, f"成功发布 {results['success_count']} 篇")


def trigger_ai_process(article_id: int):
    """POST /api/v1/articles/{id}/process-ai — 手动触发AI处理"""
    return json_success({
        "article_id": article_id,
        "status": "processing",
        "message": "AI处理已触发，请稍后刷新查看结果",
        "_note": "需对接 ai_processor.py"
    })


def get_dashboard_stats():
    """GET /api/v1/dashboard/stats — Dashboard统计(含趋势数据)"""
    # 返回含 article_trend/tool_trend/pending_count 的数据
    # 用于修复 Dashboard.vue 的假数据问题
    mock_stats = {
        "article_count": 156,
        "tool_count": 48,
        "category_count": 12,
        "tag_count": 36,
        "pending_count": 23,
        "article_trend": 8.5,
        "tool_trend": 3.2,
        "category_trend": None,
        "today_published": 5,
        "today_fetched": 42,
        "today_filtered": 24,
        "_note": "当前为模拟数据，请替换为真实聚合查询"
    }
    return json_success(mock_stats)


if __name__ == "__main__":
    import json
    print("=== API 测试 ===\n")
    print("1. 今日统计:")
    print(json.dumps(get_today_stats(), indent=2, ensure_ascii=False))
    print("\n2. 审核队列统计:")
    print(json.dumps(get_review_stats(), indent=2, ensure_ascii=False))
    print("\n3. Dashboard统计:")
    print(json.dumps(get_dashboard_stats(), indent=2, ensure_ascii=False))
