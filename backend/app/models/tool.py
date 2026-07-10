"""
工具数据模型 - EntropyGate AI 工具指南版块

与文章模型的差异：
- 工具有静态属性（定价/分类/使用场景）+ 动态属性（可用性状态/版本更新）
- 核心差异化功能：可用性追踪 + 替代方案推荐
- 面向用户问题：「这个工具怎么用？国内能不能用？有替代品吗？」
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import uuid
from datetime import datetime


# ============================================================
# 枚举定义
# ============================================================

class ToolStatus(str, Enum):
    """工具状态"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"  # 已被更好的替代


class AvailabilityStatus(str, Enum):
    """可用性状态"""
    AVAILABLE = "available"           # 国内可用
    RESTRICTED = "restricted"         # 部分受限（需特殊方式）
    BLOCKED = "blocked"               # 已被封禁
    ENTERPRISE_ONLY = "enterprise_only"  # 仅企业版
    UNCERTAIN = "uncertain"           # 待核实
    NEEDS_VPN = "needs_vpn"           # 需要VPN
    NEEDS_PROXY = "needs_proxy"       # 需要代理


class PricingType(str, Enum):
    """定价类型"""
    FREE = "freemium"                 # 免费增值
    FREE_TIER = "free_tier"           # 有免费额度
    PAID = "paid"                    # 付费
    OPEN_SOURCE = "open_source"       # 开源可自部署
    CUSTOM = "custom"                 # 企业定制


class DifficultyLevel(str, Enum):
    """使用难度"""
    BEGINNER = "beginner"             # 新手友好
    INTERMEDIATE = "intermediate"     # 需要一定基础
    ADVANCED = "advanced"             # 需要专业背景


# ============================================================
# 使用场景标签体系
# ============================================================

USE_CASES = [
    {"id": "text-generation", "name": "文本生成", "icon": "✍️", "description": "文章写作、翻译、摘要、润色"},
    {"id": "code-assistant", "name": "编程辅助", "icon": "💻", "description": "代码生成、调试、解释、重构"},
    {"id": "image-generation", "name": "图像生成", "icon": "🎨", "description": "AI绘画、图片编辑、风格转换"},
    {"id": "voice-synthesis", "name": "语音合成", "icon": "🎙️", "description": "TTS、语音克隆、配音"},
    {"id": "data-analysis", "name": "数据分析", "icon": "📊", "description": "数据处理、可视化、报告生成"},
    {"id": "document-processing", "name": "文档处理", "icon": "📄", "description": "PDF处理、OCR、格式转换"},
    {"id": "video-generation", "name": "视频生成", "icon": "🎬", "description": "AI视频、剪辑、特效"},
    {"id": "search-research", "name": "搜索研究", "icon": "🔍", "description": "AI搜索、学术研究、信息聚合"},
    {"id": "productivity", "name": "效率办公", "icon": "⚡", "description": "会议纪要、日程管理、自动化流程"},
    {"id": "chatbot-agent", "name": "对话智能体", "icon": "🤖", "description": "客服机器人、个人助手、工作流Agent"},
]


# ============================================================
# 工具主模型
# ============================================================

@dataclass
class Tool:
    """AI工具完整数据模型"""
    
    # ====== 基础信息 ======
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""                          # 工具名称
    slug: str = ""                           # URL标识
    logo_url: str = ""                       # Logo图标
    tagline: str = ""                        # 一句话描述
    description: str = ""                   # 详细介绍
    official_url: str = ""                  # 官方网站
    
    # ====== 分类与标签 ======
    category_id: int = None                 # 分类ID
    category_name: str = ""                 # 分类名称
    category_slug: str = ""
    tags: list = field(default_factory=list)  # [{id, name, slug}]
    use_cases: list = field(default_factory=list)  # 使用场景IDs (来自USE_CASES)
    
    # ====== 定价信息 ======
    pricing_type: str = PricingType.FREE.value
    price_from: str = ""                    # 起步价格，如 "$20/月"
    price_details: str = ""                 # 详细定价说明
    has_free_tier: bool = False            # 是否有免费层
    free_tier_limits: str = ""             # 免费层限制说明
    
    # ====== 可用性信息（核心差异化）=====
    availability_status: str = AvailabilityStatus.UNCERTAIN.value
    availability_note: str = ""            # 可用性备注
    access_method: str = ""                # 访问方式说明（如"需手机号注册"/"需科学上网"）
    last_checked_at: str = ""              # 最后核实时间
    next_check_scheduled: str = ""         # 下次计划检查时间
    
    # ====== 使用难度 ======
    difficulty: str = DifficultyLevel.BEGINNER.value
    learning_curve: str = ""               # 学习曲线描述
    
    # ====== 版本与更新 ======
    latest_version: str = ""               # 最新版本号
    update_frequency: str = ""             # 更新频率（如"每周"/"按需"）
    changelog_url: str = ""                # 更新日志链接
    
    # ====== 平台支持 ======
    platforms: list = field(default_factory=list)  # ["web", "ios", "android", "api", "desktop"]
    api_available: bool = False            # 是否提供API
    api_docs_url: str = ""                 # API文档地址
    
    # ====== 评分与统计 ======
    rating_avg: float = 0                  # 平均评分(0-5)
    rating_count: int = 0                  # 评分人数
    view_count: int = 0                    # 浏览数
    like_count: int = 0                    # 收藏数
    
    # ====== 内容字段 ======
    features: list = field(default_factory=list)   # 核心功能列表 [str]
    pros: list = field(default_factory=list)       # 优点列表 [str]
    cons: list = field(default_factory.list)       # 缺点列表 [str]
    best_for: str = ""                      # 最适合人群
    not_recommended_for: str = ""          # 不推荐场景
    quick_start_guide: str = ""            # 快速上手指南(HTML/Markdown)
    tutorial_links: list = field(default_factory.list)  # 教程链接 [{title, url}]
    
    # ====== 替代方案 ======
    alternatives: list = field(default_factory.list)  # [{tool_id, tool_name, reason}]
    is_alternative_of: list = field(default_factory.list)  # 反向关联
    
    # ====== 状态与管理 ======
    status: str = ToolStatus.DRAFT.value
    is_featured: bool = False              # 是否推荐
    is_top_picked: bool = False            # 是否精选
    sort_order: int = 0                     # 排序权重
    
    # ====== SEO ======
    seo_title: str = ""
    seo_description: str = ""
    
    # ====== 时间戳 ======
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    published_at: str = ""
    
    # ====== 方法 ======
    
    def to_api_dict(self) -> dict:
        """前端展示用（过滤内部字段）"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "logo_url": self.logo_url,
            "tagline": self.tagline,
            "official_url": self.official_url,
            "category": {
                "id": self.category_id,
                "name": self.category_name,
                "slug": self.category_slug,
            } if self.category_id else None,
            "tags": self.tags,
            "use_cases": self.use_cases,
            "pricing": {
                "type": self.pricing_type,
                "price_from": self.price_from,
                "has_free_tier": self.has_free_tier,
            },
            "availability": {
                "status": self.availability_status,
                "note": self.availability_note,
                "access_method": self.access_method,
                "last_checked": self.last_checked_at,
            },
            "difficulty": self.difficulty,
            "rating": self.rating_avg,
            "view_count": self.view_count,
            "platforms": self.platforms,
            "is_featured": self.is_featured,
            "alternatives_count": len(self.alternatives),
            "features": self.features[:6],  # 只返回前6个核心功能
            "best_for": self.best_for,
            "updated_at": self.updated_at,
        }
    
    def to_admin_dict(self) -> dict:
        """管理后台用（含所有内部字段）"""
        base = self.to_api_dict()
        base.update({
            "_internal": {
                "description": self.description,
                "price_details": self.price_details,
                "free_tier_limits": self.free_tier_limits,
                "learning_curve": self.learning_curve,
                "latest_version": self.latest_version,
                "update_frequency": self.update_frequency,
                "api_available": self.api_available,
                "api_docs_url": self.api_docs_url,
                "pros": self.pros,
                "cons": self.cons,
                "not_recommended_for": self.not_recommended_for,
                "quick_start_guide": self.quick_start_guide[:200] if self.quick_start_guide else "",
                "tutorial_links": self.tutorial_links,
                "alternatives": self.alternatives,
                "status": self.status,
                "sort_order": self.sort_order,
                "rating_count": self.rating_count,
                "like_count": self.like_count,
            }
        })
        return base


# ============================================================
# 可用性变更记录（用于追踪历史）
# ============================================================

@dataclass
class AvailabilityChange:
    """可用性状态变更记录"""
    id: int = 0
    tool_id: str = ""
    old_status: str = ""
    new_status: str = ""
    reason: str = ""                        # 变更原因
    source: str = ""                        # 信息来源
    changed_by: int = None                  # 操作人ID
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# 工具对比数据结构
# ============================================================

@dataclass
class ToolComparisonRow:
    """工具对比表的行数据"""
    feature: str = ""                       # 对比维度名称
    values: dict = field(default_factory=dict)  # {tool_id: value_string}


def generate_comparison_matrix(tools: list[Tool]) -> tuple[list[str], list[ToolComparisonRow]]:
    """
    生成工具对比矩阵
    
    返回: (工具列表, 对比行列表)
    """
    if len(tools) < 2:
        return tools, []
    
    rows = []
    
    # 基础信息行
    rows.append(ToolComparisonRow(
        feature="定价",
        values={t.id: f"{t.pricing_type} | {t.price_from or '免费'}" for t in tools}
    ))
    rows.append(ToolComparisonRow(
        feature="可用性",
        values={t.id: t.availability_status for t in tools}
    ))
    rows.append(ToolComparisonRow(
        feature="使用难度",
        values={t.id: t.difficulty for t in tools}
    ))
    rows.append(ToolComparisonRow(
        feature="平台",
        values={t.id: ", ".join(t.platforms) if t.platforms else "-" for t in tools}
    ))
    rows.append(ToolComparisonRow(
        feature="API",
        values={t.id: "✅ 有" if t.api_available else "❌ 无" for t in tools}
    ))
    rows.append(ToolComparisonRow(
        feature="免费层",
        values={t.id: t.free_tier_limits or ("✅ 有" if t.has_free_tier else "❌ 无") for t in tools}
    ))
    rows.append(ToolComparisonRow(
        feature="最适合",
        values={t.id: (t.best_for or "-")[:30] for t in tools}
    ))
    rows.append(ToolComparisonRow(
        feature="评分",
        values={t.id: f"{t.rating_avg}/5 ({t.rating_count}评)" if t.rating_count > 0 else "暂无评分" for t in tools}
    ))
    
    # 功能对比行（取所有工具的功能并集）
    all_features = set()
    for t in tools:
        all_features.update(t.features[:8])  # 最多取前8个功能
    
    for feat in sorted(all_features):
        rows.append(ToolComparisonRow(
            feature=feat,
            values={t.id: ("✅" if feat in t.features else "❌") for t in tools}
        ))
    
    return tools, rows


if __name__ == "__main__":
    # 测试数据模型
    t1 = Tool(
        name="ChatGPT", slug="chatgpt",
        tagline="OpenAI推出的对话式AI助手",
        category_name="文本生成",
        pricing_type=PricingType.FREE_TIER.value,
        price_from="$20/月",
        has_free_tier=True,
        free_tier_limits="GPT-4o mini 免费有限制",
        availability_status=AvailabilityStatus.NEEDS_VPN.value,
        access_method="需科学上网或使用镜像站",
        difficulty=DifficultyLevel.BEGINNER.value,
        platforms=["web", "ios", "android", "api"],
        api_available=True,
        features=["多轮对话", "代码生成", "数据分析", "文件上传", "联网搜索", "GPTs商店", "DALL·E绘图", "记忆功能"],
        pros=["生态最成熟", "回答质量高", "插件丰富"],
        cons=["国内无法直接访问", "高峰期可能排队"],
        best_for="通用场景、编程辅助、写作",
        rating_avg=4.5, rating_count=12500,
    )
    
    t2 = Tool(
        name="Kimi", slug="kimi-k2",
        tagline="月之暗面推出的国产AI助手",
        category_name="文本生成",
        pricing_type=PricingType.FREE_TIER.value,
        price_from="免费",
        has_free_tier=True,
        free_tier_limits="每日免费额度充足",
        availability_status=AvailabilityStatus.AVAILABLE.value,
        access_method="直接访问，手机号注册",
        difficulty=DifficultyLevel.BEGINNER.value,
        platforms=["web", "ios", "android", "api"],
        api_available=True,
        features=["超长上下文(200K)", "文件解析", "联网搜索", "代码能力", "多模态输入", "深度搜索"],
        pros=["国内直接可用", "超长上下文", "免费额度大"],
        cons":["英文能力略弱于GPT-4", "偶尔不稳定"],
        best_for="长文档分析、学术论文、国产替代",
        rating_avg=4.2, rating_count=3200,
    )
    
    print("=== 工具模型测试 ===")
    print(f"Tool1: {t1.name} | 可用性: {t1.availability_status} | 定价: {t1.pricing_type}")
    
    tools, rows = generate_comparison_matrix([t1, t2])
    print(f"\n=== 对比矩阵 ({len(tools)} 个工具, {len(rows)} 个维度) ===")
    for row in rows:
        vals = " | ".join([f"{row.values[t.id]:<25}" for t in tools])
        print(f"  {row.feature:<12} {vals}")
