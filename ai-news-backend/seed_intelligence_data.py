import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.services.intelligence_service import CapabilityService, IntelligencePipeline
from app.models.article import Article

def seed_capabilities():
    db = SessionLocal()
    cap_service = CapabilityService(db)

    core_capabilities = [
        {
            "name": "Memory",
            "slug": "memory",
            "type": "cognitive",
            "description": "模型能够记住用户信息和对话历史",
            "status": "mature",
            "domain": "memory",
            "category": "long-term",
            "version": "1.0",
            "maturity_score": 85,
            "adoption_score": 80,
            "truth_score": 90,
        },
        {
            "name": "MCP (Model Context Protocol)",
            "slug": "mcp",
            "type": "protocol",
            "description": "AI模型上下文交互的开放协议，支持工具调用和上下文共享",
            "status": "active",
            "domain": "tool-use",
            "category": "protocol",
            "version": "2.0",
            "maturity_score": 70,
            "adoption_score": 75,
            "truth_score": 85,
        },
        {
            "name": "Agent Framework",
            "slug": "agent-framework",
            "type": "system",
            "description": "支持自主代理执行的框架系统，包括规划、执行、反思能力",
            "status": "mature",
            "domain": "agent",
            "category": "autonomous",
            "version": "2.0",
            "maturity_score": 75,
            "adoption_score": 70,
            "truth_score": 80,
        },
        {
            "name": "Computer Use",
            "slug": "computer-use",
            "type": "execution",
            "description": "AI模型直接操作计算机界面的能力，包括点击、输入、浏览等",
            "status": "active",
            "domain": "tool-use",
            "category": "computer-control",
            "version": "1.0",
            "maturity_score": 55,
            "adoption_score": 45,
            "truth_score": 75,
        },
        {
            "name": "Long-term Memory",
            "slug": "long-term-memory",
            "type": "cognitive",
            "description": "跨会话的长期记忆能力，能够持久化用户偏好和知识",
            "status": "active",
            "domain": "memory",
            "category": "long-term",
            "version": "1.0",
            "parent_id": None,
            "maturity_score": 70,
            "adoption_score": 60,
            "truth_score": 80,
        },
        {
            "name": "Tool Use",
            "slug": "tool-use",
            "type": "execution",
            "description": "模型调用外部工具和API的能力",
            "status": "mature",
            "domain": "tool-use",
            "category": "general",
            "version": "2.0",
            "maturity_score": 90,
            "adoption_score": 85,
            "truth_score": 95,
        },
    ]

    created_count = 0
    for cap_data in core_capabilities:
        existing = cap_service.get_by_slug(cap_data["slug"])
        if not existing:
            cap_service.create_from_dict(cap_data)
            created_count += 1
            print(f"  + 创建 Capability: {cap_data['name']}")
        else:
            print(f"  = 已存在: {cap_data['name']}")

    print(f"\nCapability 导入完成: 新增 {created_count} 个")
    db.close()
    return created_count


def test_pipeline_with_existing_articles():
    db = SessionLocal()
    pipeline = IntelligencePipeline(db)

    articles = db.query(Article).filter(
        Article.status == "published"
    ).order_by(Article.published_at.desc()).limit(3).all()

    print(f"\n找到 {len(articles)} 篇已发布文章，测试转化为 Event...")

    for article in articles:
        try:
            event = pipeline.ingest_article_to_event(article)
            print(f"  ✓ {article.title[:50]} -> Event: {event.id} (score: {event.overall_score})")
        except Exception as e:
            print(f"  ✗ {article.title[:50]} -> 失败: {e}")

    db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("P0 数据验证脚本")
    print("=" * 50)

    print("\n[1/2] 导入核心 Capability...")
    seed_capabilities()

    print("\n[2/2] 测试文章 → Event 转化链路...")
    test_pipeline_with_existing_articles()

    print("\n" + "=" * 50)
    print("验证完成！")
    print("=" * 50)

