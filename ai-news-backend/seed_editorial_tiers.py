"""给所有活跃 Source 分配编辑等级 (S/A/B/C/D) 和角色

基于以下原则：
    - Intelligence over Information
    - 不是所有来源都平等
    - 首页容量有限 → 编辑必须做选择
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.core.database import SessionLocal
from app.models.source import Source

db = SessionLocal()

# 编辑等级定义
# S: 核心 Intelligence — 模型发布、能力升级、Agent
# A: 重要产品更新 — AI 产品/框架关键更新
# B: 信号观察 — 社区/研究信号，有条件采
# C: 技术背景 — 基础设施更新，默认不进入首页
# D: 低优先级 — 非 AI 核心，仅留档

TIER_MAP = {
    # === S 级: 核心 Intelligence ===
    "OpenAI Blog":           ("S", "核心 Intelligence"),
    "Anthropic News":        ("S", "核心 Intelligence"),
    "Google DeepMind":       ("S", "核心 Intelligence"),
    "Meta AI":               ("S", "核心 Intelligence"),
    "xAI":                   ("S", "核心 Intelligence"),
    "Mistral AI":            ("S", "核心 Intelligence"),

    # === A 级: AI 产品/工具 ===
    "DeepSeek":              ("A", "AI 产品"),
    "Perplexity":            ("A", "AI 产品"),
    "Cursor":                ("A", "AI 产品"),
    "Replit":                ("A", "AI 产品"),
    "Vercel AI":             ("A", "AI 产品"),
    "Hugging Face":          ("A", "AI 研究"),
    "Qwen Blog":             ("A", "AI 产品"),
    "月之暗面 Kimi Blog":    ("A", "AI 产品"),
    "Google AI Blog":        ("A", "核心 Intelligence"),

    # === B 级: 社区/研究信号 ===
    "arXiv (cs.CL)":         ("B", "AI 研究"),
    "Hacker News AI":        ("B", "社区信号"),
    "Reddit r/MachineLearning": ("B", "社区信号"),
    "Reddit r/LocalLLaMA":     ("B", "社区信号"),
    "GitHub Trending AI":    ("B", "社区信号"),
    "Papers with Code":      ("B", "AI 研究"),
    "HuggingFace Daily":     ("B", "AI 研究"),
    "TechCrunch AI":         ("B", "AI 媒体"),
    "VentureBeat AI":        ("B", "AI 媒体"),

    # === C 级: 技术背景（默认不进入首页） ===
    "GitHub Changelog":      ("C", "基础设施"),
    "GitHub: Trending":      ("C", "基础设施"),
    "Product Hunt AI":       ("C", "社区信号"),
    "Runway":                ("C", "AI 产品"),
    "Microsoft AI":          ("C", "核心 Intelligence"),  # feed 已失效

    # === D 级: 低优先级 ===
    "Cloudflare AI":         ("D", "基础设施"),
}

try:
    updated = 0
    sources = db.query(Source).filter(Source.deleted_at.is_(None)).all()

    for source in sources:
        if source.name in TIER_MAP:
            tier, role = TIER_MAP[source.name]
            source.editorial_tier = tier
            source.editorial_role = role
            updated += 1
        elif source.is_active:
            # 活跃但未在映射表中的，默认为 B 级（保守策略）
            if not source.editorial_tier or source.editorial_tier == 'C':
                source.editorial_tier = 'B'
                source.editorial_role = '社区信号'
                updated += 1

    db.commit()

    print(f"\n=== 已更新 {updated} 个 Source 的编辑等级 ===\n")
    active = db.query(Source).filter(Source.is_active == True, Source.deleted_at.is_(None)).all()
    print(f"{'来源':<25} {'等级':<5} {'基础分':<8} {'角色'}")
    print("-" * 65)
    for s in sorted(active, key=lambda x: (x.editorial_tier or 'Z', x.name)):
        print(f"{s.name:<25} {s.editorial_tier or 'C':<5} {s.editorial_score_base if hasattr(s, 'editorial_score_base') else '':<8} {s.editorial_role or '-'}")

    # 分布统计
    from collections import Counter
    tier_counts = Counter(s.editorial_tier for s in active)
    print(f"\n=== 来源分布 ===")
    for tier in ['S', 'A', 'B', 'C', 'D']:
        count = tier_counts.get(tier, 0)
        bar = '█' * count
        print(f"  {tier} 级 ({count}): {bar}")

finally:
    db.close()
