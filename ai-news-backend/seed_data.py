import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from app.core.database import SessionLocal, engine, Base
from app.models import *
from app.models.category import Category
from app.models.tag import Tag
from app.models.admin import Admin, Role, Permission
from app.models.source import Source
from app.utils.security import hash_password


def init_seed_data():
    db = SessionLocal()
    try:
        news_categories = [
            {"name": "大模型", "slug": "llm", "type": "news", "sort_order": 1},
            {"name": "AI编程", "slug": "ai-coding", "type": "news", "sort_order": 2},
            {"name": "AI视频", "slug": "ai-video", "type": "news", "sort_order": 3},
            {"name": "AI图像", "slug": "ai-image", "type": "news", "sort_order": 4},
            {"name": "AI办公", "slug": "ai-office", "type": "news", "sort_order": 5},
            {"name": "机器人", "slug": "robotics", "type": "news", "sort_order": 6},
            {"name": "行业动态", "slug": "industry", "type": "news", "sort_order": 7},
            {"name": "政策监管", "slug": "policy", "type": "news", "sort_order": 8},
        ]

        tool_categories = [
            {"name": "AI聊天", "slug": "chatbot", "type": "tool", "sort_order": 1},
            {"name": "AI编程", "slug": "code-assistant", "type": "tool", "sort_order": 2},
            {"name": "AI绘画", "slug": "image-generation", "type": "tool", "sort_order": 3},
            {"name": "AI视频", "slug": "video-generation", "type": "tool", "sort_order": 4},
            {"name": "AI搜索", "slug": "ai-search", "type": "tool", "sort_order": 5},
            {"name": "AI写作", "slug": "writing", "type": "tool", "sort_order": 6},
        ]

        for cat_data in news_categories + tool_categories:
            existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
                print(f"创建分类: {cat_data['name']}")

        tags = [
            {"name": "国内可用", "slug": "cn-available", "type": "availability", "color": "#10B981"},
            {"name": "需魔法", "slug": "need-proxy", "type": "availability", "color": "#F59E0B"},
            {"name": "企业版可用", "slug": "enterprise-only", "type": "availability", "color": "#6366F1"},
            {"name": "已被封禁", "slug": "blocked", "type": "availability", "color": "#EF4444"},
            {"name": "OpenAI", "slug": "openai", "type": "company", "color": "#10A37F"},
            {"name": "Anthropic", "slug": "anthropic", "type": "company", "color": "#D97757"},
            {"name": "Google", "slug": "google", "type": "company", "color": "#4285F4"},
            {"name": "字节跳动", "slug": "bytedance", "type": "company", "color": "#3C8CFF"},
            {"name": "阿里巴巴", "slug": "alibaba", "type": "company", "color": "#FF6A00"},
        ]

        for tag_data in tags:
            existing = db.query(Tag).filter(Tag.slug == tag_data["slug"]).first()
            if not existing:
                tag = Tag(**tag_data)
                db.add(tag)
                print(f"创建标签: {tag_data['name']}")

        permissions = [
            {"name": "查看文章", "code": "article:read", "module": "article", "type": "api", "sort_order": 1},
            {"name": "创建文章", "code": "article:create", "module": "article", "type": "api", "sort_order": 2},
            {"name": "编辑文章", "code": "article:update", "module": "article", "type": "api", "sort_order": 3},
            {"name": "删除文章", "code": "article:delete", "module": "article", "type": "api", "sort_order": 4},

            {"name": "查看工具", "code": "tool:read", "module": "tool", "type": "api", "sort_order": 1},
            {"name": "创建工具", "code": "tool:create", "module": "tool", "type": "api", "sort_order": 2},
            {"name": "编辑工具", "code": "tool:update", "module": "tool", "type": "api", "sort_order": 3},
            {"name": "删除工具", "code": "tool:delete", "module": "tool", "type": "api", "sort_order": 4},

            {"name": "查看分类", "code": "category:read", "module": "category", "type": "api", "sort_order": 1},
            {"name": "创建分类", "code": "category:create", "module": "category", "type": "api", "sort_order": 2},
            {"name": "编辑分类", "code": "category:update", "module": "category", "type": "api", "sort_order": 3},
            {"name": "删除分类", "code": "category:delete", "module": "category", "type": "api", "sort_order": 4},

            {"name": "查看标签", "code": "tag:read", "module": "tag", "type": "api", "sort_order": 1},
            {"name": "创建标签", "code": "tag:create", "module": "tag", "type": "api", "sort_order": 2},
            {"name": "编辑标签", "code": "tag:update", "module": "tag", "type": "api", "sort_order": 3},
            {"name": "删除标签", "code": "tag:delete", "module": "tag", "type": "api", "sort_order": 4},

            {"name": "查看管理员", "code": "admin:read", "module": "admin", "type": "api", "sort_order": 1},
            {"name": "创建管理员", "code": "admin:create", "module": "admin", "type": "api", "sort_order": 2},
            {"name": "编辑管理员", "code": "admin:update", "module": "admin", "type": "api", "sort_order": 3},
            {"name": "删除管理员", "code": "admin:delete", "module": "admin", "type": "api", "sort_order": 4},

            {"name": "查看角色", "code": "role:read", "module": "role", "type": "api", "sort_order": 1},
            {"name": "创建角色", "code": "role:create", "module": "role", "type": "api", "sort_order": 2},
            {"name": "编辑角色", "code": "role:update", "module": "role", "type": "api", "sort_order": 3},
            {"name": "删除角色", "code": "role:delete", "module": "role", "type": "api", "sort_order": 4},

            {"name": "查看权限", "code": "permission:read", "module": "permission", "type": "api", "sort_order": 1},
            {"name": "管理权限", "code": "permission:manage", "module": "permission", "type": "api", "sort_order": 2},

            {"name": "数据采集管理", "code": "crawler:manage", "module": "crawler", "type": "api", "sort_order": 1},

            {"name": "系统设置", "code": "system:manage", "module": "system", "type": "api", "sort_order": 1},

            {"name": "查看审计日志", "code": "audit:read", "module": "audit", "type": "api", "sort_order": 1},
        ]

        for perm_data in permissions:
            existing = db.query(Permission).filter(Permission.code == perm_data["code"]).first()
            if not existing:
                perm = Permission(**perm_data)
                db.add(perm)
                print(f"创建权限: {perm_data['name']}")

        db.commit()

        roles = [
            {
                "name": "超级管理员",
                "code": "super_admin",
                "description": "拥有所有权限",
                "sort_order": 1,
                "is_super": True
            },
            {
                "name": "内容编辑",
                "code": "content_editor",
                "description": "管理文章、工具、分类和标签",
                "sort_order": 2,
                "perms": [
                    "article:read", "article:create", "article:update", "article:delete",
                    "tool:read", "tool:create", "tool:update", "tool:delete",
                    "category:read", "category:create", "category:update", "category:delete",
                    "tag:read", "tag:create", "tag:update", "tag:delete",
                    "crawler:manage"
                ]
            },
            {
                "name": "运营人员",
                "code": "operator",
                "description": "查看内容和数据",
                "sort_order": 3,
                "perms": [
                    "article:read", "tool:read",
                    "category:read", "tag:read",
                    "audit:read"
                ]
            },
        ]

        for role_data in roles:
            existing = db.query(Role).filter(Role.code == role_data["code"]).first()
            if not existing:
                is_super = role_data.pop("is_super", False)
                perms = role_data.pop("perms", [])
                role = Role(**role_data)
                if perms:
                    perm_objs = db.query(Permission).filter(Permission.code.in_(perms)).all()
                    role.permissions = perm_objs
                db.add(role)
                print(f"创建角色: {role_data['name']}")

        db.commit()

        super_admin = db.query(Admin).filter(Admin.username == "admin").first()
        if not super_admin:
            super_role = db.query(Role).filter(Role.code == "super_admin").first()
            admin = Admin(
                username="admin",
                password_hash=hash_password("admin123"),
                name="超级管理员",
                is_super=True,
                status="active",
            )
            if super_role:
                admin.roles = [super_role]
            db.add(admin)
            db.commit()
            print("创建超级管理员: admin / admin123")

        # 简化后的内容分类
        simplified_categories = [
            {
                "name": "AI新动态",
                "slug": "ai-news",
                "type": "news",
                "description": "针对国内用户有实际价值的新工具、新技术与行业动态",
                "sort_order": 1,
            },
            {
                "name": "AI工具指南",
                "slug": "ai-tools",
                "type": "news",
                "description": "解决 AI 难使用的问题，提供实用工具教程与使用技巧",
                "sort_order": 2,
            },
        ]
        for cat_data in simplified_categories:
            existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
                print(f"创建分类: {cat_data['name']}")
        db.commit()

        # 默认信息源
        ai_news_cat = db.query(Category).filter(Category.slug == "ai-news").first()
        default_sources = [
            {
                "name": "量子位",
                "url": "https://www.qbitai.com",
                "type": "rss",
                "parser_type": "rss",
                "fetch_interval": 30,
                "is_active": True,
                "auto_publish": False,
                "ai_preprocess": True,
                "dedup_strategy": "url",
                "config": {"rss_url": "https://www.qbitai.com/rss", "language": "zh"},
            },
            {
                "name": "36氪 AI",
                "url": "https://36kr.com",
                "type": "rss",
                "parser_type": "rss",
                "fetch_interval": 60,
                "is_active": True,
                "auto_publish": False,
                "ai_preprocess": True,
                "dedup_strategy": "title",
                "config": {
                    "rss_url": "https://36kr.com/feed",
                    "language": "zh",
                    "keyword_filter": ["AI", "人工智能", "大模型", "GPT", "LLM", "ChatGPT", "Claude", "Gemini"],
                    "max_items": 30
                },
            },
            {
                "name": "机器之能",
                "url": "https://www.syncedreview.com",
                "type": "rss",
                "parser_type": "rss",
                "fetch_interval": 60,
                "is_active": True,
                "auto_publish": False,
                "ai_preprocess": True,
                "dedup_strategy": "title",
                "config": {"rss_url": "https://www.syncedreview.com/feed", "language": "en"},
            },
            {
                "name": "Hacker News AI",
                "url": "https://news.ycombinator.com",
                "type": "api",
                "parser_type": "api_hn",
                "fetch_interval": 60,
                "is_active": True,
                "auto_publish": False,
                "ai_preprocess": True,
                "dedup_strategy": "title",
                "config": {"language": "en"},
            },
            {
                "name": "Reddit r/MachineLearning",
                "url": "https://reddit.com/r/MachineLearning",
                "type": "api",
                "parser_type": "api_reddit",
                "fetch_interval": 60,
                "is_active": True,
                "auto_publish": False,
                "ai_preprocess": True,
                "dedup_strategy": "title",
                "config": {"subreddit": "MachineLearning", "language": "en"},
            },
        ]

        for src_data in default_sources:
            existing = db.query(Source).filter(Source.name == src_data["name"]).first()
            if not existing:
                source = Source(**src_data)
                if ai_news_cat:
                    source.category_id = ai_news_cat.id
                db.add(source)
                print(f"创建信息源: {src_data['name']}")

        db.commit()

        print("\n种子数据初始化完成!")
        print("超级管理员账号: admin / admin123")

    finally:
        db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    init_seed_data()

