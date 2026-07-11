"""Complete seed script — populates DB with admin, categories, tags, sources, tools, and sample articles.

Works with the actual Source model (editorial_tier values: s_tier, a_tier, b_tier, etc.)
"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, Base, engine
from app.models.admin import Admin
from app.models.article import Article
from app.models.source import Source
from app.models.category import Category
from app.models.tag import Tag
from app.models.tool import Tool
from app.utils.security import hash_password
from slugify import slugify


def seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ── Admin user ──────────────────────────────────────────
        if db.query(Admin).count() == 0:
            db.add(Admin(
                username="admin",
                password_hash=hash_password("admin123"),
                display_name="Super Admin",
                is_active=1,
                role="super_admin",
            ))
            print("[SEED] Admin user: admin / admin123")
        else:
            print("[SEED] Admin user already exists")

        # ── Categories ──────────────────────────────────────────
        categories_data = [
            ("ai-news", "AI 新闻", "AI 行业最新资讯", "newspaper"),
            ("models", "模型", "大语言模型与 AI 模型", "cube"),
            ("tools", "工具", "AI 工具与产品", "construct"),
            ("research", "研究", "AI 学术研究论文", "flask"),
        ]
        cat_map = {}
        for slug, name, desc, icon in categories_data:
            existing = db.query(Category).filter(Category.slug == slug).first()
            if not existing:
                c = Category(slug=slug, name=name, description=desc, icon=icon, sort_order=len(cat_map))
                db.add(c)
                db.flush()
                cat_map[slug] = c.id
                print(f"[SEED] Category: {name}")
            else:
                cat_map[slug] = existing.id
                print(f"[SEED] Category exists: {name}")

        # ── Tags ────────────────────────────────────────────────
        tags_data = [
            ("GPT", "#10a37f"), ("Claude", "#d97757"), ("LLM", "#6366f1"),
            ("OpenAI", "#10a37f"), ("Google", "#4285f4"), ("Meta", "#0866ff"),
            ("开源", "#f59e0b"), ("多模态", "#ec4899"), ("Agent", "#8b5cf6"),
            ("微调", "#06b6d4"), ("RAG", "#14b8a6"), ("Midjourney", "#7c3aed"),
        ]
        tag_map = {}
        for name, color in tags_data:
            slug = slugify(name)
            existing = db.query(Tag).filter(Tag.slug == slug).first()
            if not existing:
                t = Tag(name=name, slug=slug, color=color)
                db.add(t)
                db.flush()
                tag_map[name] = t.id
            else:
                tag_map[name] = existing.id
        print(f"[SEED] Tags: {len(tag_map)} total")

        # ── Sources ─────────────────────────────────────────────
        sources_data = [
            # S-tier: core intelligence
            ("OpenAI Blog", "https://openai.com/blog", "https://openai.com/blog/rss.xml", "s_tier", "核心 Intelligence", "en"),
            ("Anthropic News", "https://www.anthropic.com/news", "https://www.anthropic.com/rss.xml", "s_tier", "核心 Intelligence", "en"),
            ("Google DeepMind", "https://deepmind.google/blog/", "https://deepmind.google/blog/rss.xml", "s_tier", "核心 Intelligence", "en"),
            ("Meta AI", "https://ai.meta.com/blog/", "https://ai.meta.com/blog/rss/", "s_tier", "核心 Intelligence", "en"),
            ("xAI", "https://x.ai/blog", "https://x.ai/blog/rss.xml", "s_tier", "核心 Intelligence", "en"),
            ("Mistral AI", "https://mistral.ai/news/", "https://mistral.ai/feed.xml", "s_tier", "核心 Intelligence", "en"),
            # A-tier: AI products
            ("DeepSeek", "https://www.deepseek.com", "https://api-docs.deepseek.com/rss.xml", "a_tier", "AI 产品", "en"),
            ("Hugging Face", "https://huggingface.co/blog", "https://huggingface.co/blog/feed.xml", "a_tier", "AI 研究", "en"),
            ("Qwen Blog", "https://qwenlm.github.io/blog/", "https://qwenlm.github.io/blog/feed.xml", "a_tier", "AI 产品", "zh"),
            ("月之暗面 Kimi", "https://platform.moonshot.cn/blog", "https://platform.moonshot.cn/blog/rss.xml", "a_tier", "AI 产品", "zh"),
            # A-tier: Chinese media
            ("机器之心", "https://www.jiqizhixin.com", "https://rss.jiqizhixin.com/feed", "a_tier", "AI 媒体", "zh"),
            ("量子位", "https://www.qbitai.com", "https://www.qbitai.com/feed", "a_tier", "AI 媒体", "zh"),
            # B-tier: community / research signals
            ("Hacker News AI", "https://news.ycombinator.com", "https://news.ycombinator.com/rss", "b_tier", "社区信号", "en"),
            ("arXiv (cs.CL)", "https://arxiv.org/list/cs.CL/recent", "https://arxiv.org/rss/cs.CL", "b_tier", "AI 研究", "en"),
            ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/", "https://techcrunch.com/category/artificial-intelligence/feed/", "b_tier", "AI 媒体", "en"),
            ("VentureBeat AI", "https://venturebeat.com/category/ai/", "https://venturebeat.com/category/ai/feed/", "b_tier", "AI 媒体", "en"),
            ("Papers with Code", "https://paperswithcode.com", "https://paperswithcode.com/latest", "b_tier", "AI 研究", "en"),
        ]

        source_map = {}
        for name, url, feed_url, tier, role, lang in sources_data:
            slug = slugify(name)
            existing = db.query(Source).filter(Source.slug == slug).first()
            if not existing:
                tier_scores = {"s_tier": 92, "a_tier": 75, "b_tier": 60, "c_tier": 45, "d_tier": 30}
                tier_buckets = {"s_tier": "essential", "a_tier": "authoritative", "b_tier": "credible", "c_tier": "signal", "d_tier": "peripheral"}
                s = Source(
                    name=name, slug=slug, url=url, feed_url=feed_url,
                    feed_type="rss", language=lang, country="global" if lang == "en" else "cn",
                    category="AI", topic_focus="Artificial Intelligence",
                    editorial_tier=tier, editorial_role=role,
                    editorial_score=tier_scores.get(tier, 60.0),
                    editorial_bucket=tier_buckets.get(tier, "credible"),
                    credibility_score=tier_scores.get(tier, 60.0),
                    is_active=1, crawl_interval_minutes=30,
                    max_articles_per_fetch=20, status="active", health="healthy",
                )
                db.add(s)
                db.flush()
                source_map[name] = s.id
                print(f"[SEED] Source: [{tier}] {name}")
            else:
                source_map[name] = existing.id
        print(f"[SEED] Sources: {len(source_map)} total")

        # ── Tools ───────────────────────────────────────────────
        tools_data = [
            ("ChatGPT", "OpenAI 旗舰对话 AI，支持文本、图片、代码生成", "https://chat.openai.com", "对话助手", "freemium", True),
            ("Claude", "Anthropic 出品的 AI 助手，擅长长文本理解和分析", "https://claude.ai", "对话助手", "freemium", True),
            ("Midjourney", "AI 图像生成工具，以艺术品质著称", "https://www.midjourney.com", "图像生成", "paid", True),
            ("GitHub Copilot", "AI 编程助手，集成于 VS Code 和 JetBrains", "https://github.com/features/copilot", "编程开发", "paid", True),
            ("Cursor", "AI 原生代码编辑器，支持全项目上下文", "https://cursor.sh", "编程开发", "freemium", True),
            ("Stable Diffusion", "开源 AI 图像生成模型，可本地部署", "https://stability.ai", "图像生成", "free", True),
            ("Gemini", "Google 多模态 AI 助手，支持文本、图片、视频", "https://gemini.google.com", "对话助手", "freemium", True),
            ("Perplexity", "AI 搜索引擎，提供带引用的回答", "https://www.perplexity.ai", "搜索", "freemium", True),
            ("DALL-E 3", "OpenAI 的图像生成模型，集成于 ChatGPT", "https://openai.com/dall-e-3", "图像生成", "paid", False),
            ("Suno", "AI 音乐生成工具，支持完整歌曲创作", "https://suno.com", "音频生成", "freemium", False),
            ("Runway", "AI 视频生成和编辑平台", "https://runwayml.com", "视频生成", "freemium", False),
            ("LangChain", "构建 LLM 应用的开源框架", "https://python.langchain.com", "开发框架", "free", False),
        ]

        for name, desc, url, cat, pricing, featured in tools_data:
            slug = slugify(name)
            existing = db.query(Tool).filter(Tool.slug == slug).first()
            if not existing:
                t = Tool(
                    name=name, slug=slug, description=desc, url=url,
                    category=cat, tags=cat, pricing=pricing,
                    is_featured=1 if featured else 0, sort_order=0,
                )
                db.add(t)
        print(f"[SEED] Tools: {len(tools_data)} total")

        # ── Sample Articles ─────────────────────────────────────
        now = datetime.utcnow()
        articles_data = [
            {
                "title": "OpenAI 发布 GPT-5：多模态推理能力大幅提升",
                "summary": "OpenAI 正式发布 GPT-5 模型，在推理、编程和多模态理解方面实现显著突破，支持原生图像输入和输出。",
                "content": "OpenAI 今日正式发布 GPT-5，这是其旗舰语言模型的重大升级。新模型在推理能力、编程能力和多模态理解方面均实现了显著提升。\n\nGPT-5 支持原生图像输入与输出，能够在单次对话中处理文本、图像和代码。在 MMLU、HumanEval 和 MATH 等基准测试中，GPT-5 均取得了业界领先的成绩。\n\n关键改进包括：\n- 更强的长上下文理解能力（支持 128K token）\n- 改进的指令遵循和安全性\n- 原生多模态输入输出\n- 更低的 API 价格\n\nGPT-5 已向 ChatGPT Plus 用户和 API 开发者开放。",
                "source_name": "OpenAI Blog", "category_slug": "models", "lang": "zh",
                "tier": "s_tier", "bucket": "essential", "score": 95,
                "tags": ["GPT", "OpenAI", "LLM", "多模态"],
                "published_at": now - timedelta(hours=2),
                "is_featured": 1, "is_breaking": 1, "is_trending": 1,
                "ai_sentiment": "positive", "ai_summary": "OpenAI 发布 GPT-5 模型，推理和多模态能力大幅提升",
            },
            {
                "title": "Anthropic 推出 Claude 4：上下文窗口扩展至 500K",
                "summary": "Anthropic 发布 Claude 4 模型，将上下文窗口从 200K 扩展到 500K token，并增强了工具使用能力。",
                "content": "Anthropic 今日宣布推出 Claude 4 模型，这是 Claude 系列的最新版本。\n\n主要更新：\n- 上下文窗口从 200K 扩展到 500K token\n- 改进的工具使用和函数调用\n- 更强的代码生成和调试能力\n- 增强的安全性和对齐\n\nClaude 4 在多个基准测试中表现优异，特别是在长文档理解和代码生成任务上。Anthropic 同时推出了新的定价模型，使大规模部署更加经济。",
                "source_name": "Anthropic News", "category_slug": "models", "lang": "zh",
                "tier": "s_tier", "bucket": "essential", "score": 93,
                "tags": ["Claude", "LLM"],
                "published_at": now - timedelta(hours=5),
                "is_featured": 1, "is_trending": 1,
                "ai_sentiment": "positive", "ai_summary": "Anthropic 发布 Claude 4，上下文窗口扩展到 500K",
            },
            {
                "title": "Google DeepMind 发布 Gemini 2.0：原生多模态推理",
                "summary": "Google DeepMind 推出 Gemini 2.0 模型，实现原生多模态推理能力，支持文本、图像、音频和视频的统一处理。",
                "content": "Google DeepMind 正式发布 Gemini 2.0，标志着多模态 AI 的新里程碑。\n\nGemini 2.0 的核心突破：\n- 原生多模态推理（文本、图像、音频、视频）\n- 实时流式处理能力\n- 改进的 Agent 功能\n- 更高效的推理引擎\n\n该模型已在 Google AI Studio 和 Vertex AI 上线，开发者可以通过 API 调用。",
                "source_name": "Google DeepMind", "category_slug": "models", "lang": "zh",
                "tier": "s_tier", "bucket": "essential", "score": 91,
                "tags": ["Google", "LLM", "多模态"],
                "published_at": now - timedelta(hours=8),
                "is_trending": 1,
                "ai_sentiment": "positive", "ai_summary": "Google DeepMind 发布 Gemini 2.0 多模态模型",
            },
            {
                "title": "Meta 开源 Llama 4：405B 参数模型免费可用",
                "summary": "Meta 发布并开源 Llama 4 模型，包含 405B 参数版本，性能逼近 GPT-4 级别，完全免费开放。",
                "content": "Meta 今日宣布开源 Llama 4 系列模型，最大版本参数量达 405B，是迄今为止最大的开源语言模型之一。\n\nLlama 4 系列包含三个版本：\n- Llama 4 Scout (8B)：轻量级，适合边缘部署\n- Llama 4 Maverick (70B)：平衡性能与效率\n- Llama 4 Behemoth (405B)：旗舰级，性能媲美 GPT-4\n\n所有版本均采用 Apache 2.0 许可证，可免费用于商业用途。Meta 同时发布了量化版本，降低部署门槛。",
                "source_name": "Meta AI", "category_slug": "models", "lang": "zh",
                "tier": "s_tier", "bucket": "essential", "score": 90,
                "tags": ["Meta", "开源", "LLM"],
                "published_at": now - timedelta(hours=12),
                "is_featured": 1, "is_trending": 1,
                "ai_sentiment": "positive", "ai_summary": "Meta 开源 Llama 4 405B 参数模型",
            },
            {
                "title": "DeepSeek-V3 登顶开源模型排行榜，训练成本仅 557 万美元",
                "summary": "DeepSeek 发布 V3 模型，以极低训练成本实现 GPT-4 级别性能，引发行业关注。",
                "content": "中国 AI 公司 DeepSeek 发布了 DeepSeek-V3 模型，该模型以仅 557 万美元的训练成本实现了接近 GPT-4 的性能表现，引发业界广泛关注。\n\nDeepSeek-V3 的关键指标：\n- 671B 参数，37B 激活\n- 训练成本约 557 万美元（使用 2048 张 H800 GPU）\n- 在 MMLU、HumanEval 等基准测试中表现优异\n- 完全开源，支持商业使用\n\n该模型证明了高质量 AI 模型不一定需要巨额算力投入，对 AI 行业的成本结构产生了深远影响。",
                "source_name": "DeepSeek", "category_slug": "models", "lang": "zh",
                "tier": "a_tier", "bucket": "authoritative", "score": 85,
                "tags": ["开源", "LLM"],
                "published_at": now - timedelta(hours=18),
                "is_trending": 1,
                "ai_sentiment": "positive", "ai_summary": "DeepSeek-V3 以低成本实现高性能",
            },
            {
                "title": "Mistral AI 发布 Mistral Large 2：欧洲 AI 的新标杆",
                "summary": "法国 AI 公司 Mistral 发布旗舰模型 Mistral Large 2，在多语言和代码生成方面表现突出。",
                "content": "Mistral AI 发布了其最新旗舰模型 Mistral Large 2，进一步巩固了其作为欧洲领先 AI 公司的地位。\n\n主要特性：\n- 123B 参数，支持 80+ 种语言\n- 128K 上下文窗口\n- 强化的代码生成能力\n- 改进的函数调用和工具使用\n\nMistral Large 2 在多语言基准测试中表现优异，特别是在欧洲语言方面具有明显优势。",
                "source_name": "Mistral AI", "category_slug": "models", "lang": "zh",
                "tier": "s_tier", "bucket": "essential", "score": 87,
                "tags": ["LLM"],
                "published_at": now - timedelta(hours=24),
                "ai_sentiment": "positive", "ai_summary": "Mistral AI 发布 Mistral Large 2 多语言模型",
            },
            {
                "title": "Cursor 完成 9 亿美元融资，估值达 90 亿美元",
                "summary": "AI 代码编辑器 Cursor 母公司 Anysphere 完成 9 亿美元融资，估值飙升至 90 亿美元。",
                "content": "AI 代码编辑器 Cursor 的开发商 Anysphere 宣布完成 9 亿美元融资，公司估值达到 90 亿美元。本轮融资由 Thrive Capital 领投，A16z 和 Stripe 等参投。\n\nCursor 自 2023 年推出以来迅速增长，目前拥有超过 100 万开发者用户。该工具基于 VS Code 构建，集成了多种 AI 模型，支持代码补全、重构、调试等功能。\n\n此轮融资将用于扩大团队规模和加速产品开发。",
                "source_name": "TechCrunch AI", "category_slug": "ai-news", "lang": "zh",
                "tier": "b_tier", "bucket": "credible", "score": 78,
                "tags": ["Agent"],
                "published_at": now - timedelta(hours=30),
                "ai_sentiment": "positive", "ai_summary": "Cursor 完成 9 亿美元融资",
            },
            {
                "title": "Hugging Face 发布 SmolLM2：手机端运行的高效小模型",
                "summary": "Hugging Face 推出 SmolLM2 系列模型，参数量 135M-1.7B，专为边缘设备优化。",
                "content": "Hugging Face 发布了 SmolLM2 系列模型，包含 135M、360M 和 1.7B 三个版本，专为在手机和边缘设备上运行而设计。\n\nSmolLM2 的特点：\n- 1.7B 版本在多项基准测试中超越同类模型\n- 支持在普通智能手机上流畅运行\n- 完全开源，采用 Apache 2.0 许可证\n- 提供训练代码和数据集\n\n该系列模型为离线 AI 应用和隐私敏感场景提供了可行的解决方案。",
                "source_name": "Hugging Face", "category_slug": "models", "lang": "zh",
                "tier": "a_tier", "bucket": "authoritative", "score": 80,
                "tags": ["开源", "LLM"],
                "published_at": now - timedelta(hours=36),
                "ai_sentiment": "positive", "ai_summary": "Hugging Face 发布 SmolLM2 边缘模型",
            },
            {
                "title": "通义千问 Qwen2.5 发布：数学和编程能力大幅提升",
                "summary": "阿里通义千问发布 Qwen2.5 系列模型，在数学推理和代码生成方面实现显著进步。",
                "content": "阿里巴巴通义千问团队发布 Qwen2.5 系列模型，涵盖 0.5B 到 72B 多个规格。\n\nQwen2.5 主要改进：\n- 数学推理能力提升 20%+\n- 代码生成能力提升 15%+\n- 支持 29 种语言\n- 128K 上下文窗口\n- 改进的指令遵循能力\n\nQwen2.5-72B 在多个基准测试中达到或超越同级别开源模型，同时保持完全开源。",
                "source_name": "Qwen Blog", "category_slug": "models", "lang": "zh",
                "tier": "a_tier", "bucket": "authoritative", "score": 82,
                "tags": ["LLM", "开源"],
                "published_at": now - timedelta(hours=42),
                "is_trending": 1,
                "ai_sentiment": "positive", "ai_summary": "阿里发布 Qwen2.5 系列模型",
            },
            {
                "title": "AI Agent 框架 LangGraph 1.0 正式发布",
                "summary": "LangChain 团队发布 LangGraph 1.0，为构建可靠 AI Agent 提供状态管理和循环控制。",
                "content": "LangChain 团队正式发布 LangGraph 1.0，这是一个专为构建 AI Agent 应用设计的框架。\n\nLangGraph 1.0 核心功能：\n- 状态图（StateGraph）用于管理 Agent 工作流\n- 支持循环和条件分支\n- 内置人机交互节点\n- 持久化记忆和检查点\n- 流式输出支持\n\n该框架已被多个企业用于生产环境的 Agent 应用，包括客服自动化、数据分析助手等场景。",
                "source_name": "Hugging Face", "category_slug": "tools", "lang": "zh",
                "tier": "a_tier", "bucket": "authoritative", "score": 79,
                "tags": ["Agent", "开源"],
                "published_at": now - timedelta(hours=48),
                "ai_sentiment": "neutral", "ai_summary": "LangGraph 1.0 正式发布",
            },
            {
                "title": "机器之心：2025 年 AI 行业十大趋势预测",
                "summary": "从多模态到 Agent，从边缘部署到开源生态，盘点 2025 年 AI 领域最值得关注的十大趋势。",
                "content": "2025 年 AI 行业将迎来多项重要变化：\n\n1. 多模态成为标配\n2. AI Agent 走向生产环境\n3. 小模型和边缘部署加速\n4. 开源与闭源模型差距缩小\n5. AI 安全和对齐成为焦点\n6. 具身智能（Embodied AI）突破\n7. AI 科研助手普及\n8. 垂直领域 AI 应用爆发\n9. AI 监管框架逐步落地\n10. 算力效率持续优化\n\n这些趋势将共同塑造 2025 年的 AI 产业格局。",
                "source_name": "机器之心", "category_slug": "research", "lang": "zh",
                "tier": "a_tier", "bucket": "authoritative", "score": 76,
                "tags": ["LLM", "Agent", "多模态"],
                "published_at": now - timedelta(hours=60),
                "ai_sentiment": "neutral", "ai_summary": "2025 年 AI 十大趋势预测",
            },
            {
                "title": "arXiv 论文：思维链推理的可解释性研究取得突破",
                "summary": "最新研究表明，大语言模型的思维链推理过程可以通过探针技术进行可视化解释。",
                "content": "一项发表在 arXiv 上的最新研究揭示了 LLM 思维链（Chain-of-Thought）推理的内部机制。\n\n研究团队使用探针技术（probing）分析了多个主流模型在推理过程中的内部表示，发现：\n\n- 模型在生成推理步骤时，内部表示确实包含了任务相关的结构化信息\n- 推理步骤之间存在因果依赖关系\n- 模型的推理过程可以被可视化并验证\n\n这一发现对提升 AI 系统的可解释性和可信度具有重要意义。",
                "source_name": "arXiv (cs.CL)", "category_slug": "research", "lang": "zh",
                "tier": "b_tier", "bucket": "credible", "score": 72,
                "tags": ["LLM", "RAG"],
                "published_at": now - timedelta(hours=72),
                "ai_sentiment": "neutral", "ai_summary": "思维链推理可解释性研究突破",
            },
        ]

        for i, a_data in enumerate(articles_data):
            slug = slugify(a_data["title"])[:100]
            existing = db.query(Article).filter(Article.slug == slug).first()
            if existing:
                continue

            source_id = source_map.get(a_data["source_name"])
            category_id = cat_map.get(a_data["category_slug"])

            article = Article(
                title=a_data["title"],
                slug=slug,
                summary=a_data["summary"],
                content=a_data["content"],
                excerpt=a_data["summary"][:150],
                source_url=a_data.get("source_url", ""),
                source_name=a_data["source_name"],
                source_id=source_id,
                language=a_data["lang"],
                published_at=a_data["published_at"],
                fetched_at=now,
                category_id=category_id,
                relevance_score=float(a_data["score"]),
                quality_score=float(a_data["score"] - 5),
                credibility_score=float(a_data["score"] - 3),
                newsworthiness_score=float(a_data["score"]),
                editorial_score=float(a_data["score"]),
                editorial_bucket=a_data["bucket"],
                editorial_tier=a_data["tier"],
                review_status="approved",
                reviewed_by=1,
                reviewed_at=now,
                ai_summary=a_data.get("ai_summary", ""),
                ai_sentiment=a_data.get("ai_sentiment", "neutral"),
                ai_tags=",".join(a_data.get("tags", [])),
                ai_keywords=",".join(a_data.get("tags", [])),
                is_featured=a_data.get("is_featured", 0),
                is_trending=a_data.get("is_trending", 0),
                is_breaking=a_data.get("is_breaking", 0),
            )
            db.add(article)
            db.flush()

            # Add tags
            for tag_name in a_data.get("tags", []):
                tag_id = tag_map.get(tag_name)
                if tag_id:
                    from app.models.tag import article_tags
                    db.execute(article_tags.insert().values(article_id=article.id, tag_id=tag_id))

            print(f"[SEED] Article: {a_data['title'][:40]}...")

        db.commit()
        print("\n=== SEED COMPLETE ===")

        # Print summary
        print(f"\nAdmins:    {db.query(Admin).count()}")
        print(f"Categories: {db.query(Category).count()}")
        print(f"Tags:       {db.query(Tag).count()}")
        print(f"Sources:    {db.query(Source).count()}")
        print(f"Tools:      {db.query(Tool).count()}")
        print(f"Articles:   {db.query(Article).count()}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
