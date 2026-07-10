"""
文章数据模型扩展 - EntropyGate AI 新动态版块

扩展字段说明：
- filter_* 字段：由采集过滤器(filters.py)附加
- ai_* 字段：由AI处理器(ai_processor.py)附加
- status 状态机：draft → published / discarded

与现有数据库表的对应关系（如使用SQLAlchemy/Django ORM）：
  这些字段可作为 Article 模型的扩展列，
  或作为 JSON 字段存储在 extra_data 列中。
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import uuid
from datetime import datetime


class ArticleStatus(str, Enum):
    """文章状态枚举"""
    DRAFT = "draft"           # 草稿（待审核）
    PENDING_REVIEW = "pending_review"  # 待人工审核（AI已处理完）
    PUBLISHED = "published"   # 已发布
    DISCARDED = "discarded"   # 已废弃
    ARCHIVED = "archived"     # 已归档


class ContentType(str, Enum):
    """内容类型"""
    RELEASE = "release"       # 产品/模型发布
    AVAILABILITY = "availability"  # 可用性变化
    POLICY = "policy"         # 政策法规
    TUTORIAL = "tutorial"     # 教程指南
    RESEARCH = "research"     # 学术研究
    OTHER = "other"           # 其他


@dataclass
class Article:
    """
    完整文章模型（含扩展字段）
    
    设计原则：
    - 基础字段：与现有系统兼容
    - filter_* 字段：采集阶段写入，只读
    - ai_* 字段：AI处理后写入，可人工修改
    - audit_* 字段：审核阶段写入
    """
    
    # ====== 基础字段 ======
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    slug: str = ""                          # URL友好的标识
    summary: str = ""                       # 摘要（人工或AI生成）
    content: str = ""                       # 正文HTML
    content_text: str = ""                  # 纯文本版本
    cover_image: str = ""                   # 封面图URL
    url: str = ""                           # 原文链接
    
    # ====== 来源信息 ======
    source_id: int = None                   # 来源ID（关联Source表）
    source_name: str = ""                   # 来源名称（冗余存储，避免JOIN）
    source_url: str = ""                    # 来源URL
    author: str = ""                        # 原作者
    published_at_original: str = ""         # 原文发布时间
    
    # ====== 分类与标签 ======
    category_id: int = None                 # 分类ID
    category_slug: str = ""                 # 分类slug
    category_name: str = ""                 # 分类名称（冗余）
    tag_ids: list = field(default_factory=list)  # 标签ID列表
    tags: list = field(default_factory=list)      # 标签详情[{id,name,slug,color}]
    
    # ====== 状态 ======
    status: str = ArticleStatus.DRAFT.value
    priority: int = 0                       # 审核优先级（越高越优先）
    is_top: bool = False                    # 是否置顶
    is_featured: bool = False               # 是否推荐
    
    # ====== 统计 ======
    view_count: int = 0                     # 浏览数
    like_count: int = 0                     # 点赞数
    
    # ====== 过滤器字段（采集阶段写入）=====
    filter_score: int = 0                   # 过滤器相关性得分
    filter_keywords: list = field(default_factory=list)  # 命中的关键词
    filter_suggestions: list = field(default_factory=list)  # 过滤器建议标签
    
    # ====== AI处理字段（AI阶段写入）=====
    ai_summary: str = ""                    # AI生成的摘要
    ai_quality_score: int = 0               # AI质量分(0-100)
    ai_relevance_score: int = 0             # AI相关度分(0-100)
    ai_content_type: str = ""               # AI判断的内容类型
    ai_category_id: int = None              # AI推荐的分类
    ai_category_confidence: float = 0       # AI分类置信度
    ai_is_important: bool = False           # AI是否标记为重点
    ai_processed_at: str = ""               # AI处理时间
    ai_processing_time_ms: int = 0          # AI处理耗时(ms)
    
    # ====== 审核字段（人工审核阶段写入）=====
    reviewed_by: int = None                 # 审核人ID
    reviewed_at: str = ""                   # 审核时间
    reject_reason: str = ""                 # 废弃原因
    edit_notes: str = ""                    # 编辑备注
    
    # ====== 发布字段 ======
    published_at: str = ""                  # 发布时间
    published_by: int = None                # 发布人ID
    seo_title: str = ""                     # SEO标题
    seo_description: str = ""               # SEO描述
    
    # ====== 时间戳 ======
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # ====== 方法 ======
    
    def to_api_dict(self) -> dict:
        """转换为API响应格式（过滤内部字段）"""
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "content_html": self.content,
            "cover_image": self.cover_image,
            "url": self.url,
            "source": {
                "name": self.source_name,
                "url": self.source_url
            } if self.source_name else None,
            "category": {
                "id": self.category_id,
                "slug": self.category_slug,
                "name": self.category_name
            } if self.category_id else None,
            "tags": self.tags,
            "status": self.status,
            "view_count": self.view_count,
            "published_at": self.published_at or self.published_at_original,
            "created_at": self.created_at,
            
            # 审核页需要的扩展字段
            "filter_score": self.filter_score,
            "filter_suggestions": self.filter_suggestions,
            "ai_summary": self.ai_summary,
            "ai_quality_score": self.ai_quality_score,
            "ai_is_important": self.ai_is_important,
        }
    
    def to_admin_dict(self) -> dict:
        """转换为管理后台完整格式（含所有内部字段）"""
        base = self.to_api_dict()
        base.update({
            "_internal": {
                "filter_keywords": self.filter_keywords,
                "ai_relevance_score": self.ai_relevance_score,
                "ai_content_type": self.ai_content_type,
                "ai_category_confidence": self.ai_category_confidence,
                "ai_processed_at": self.ai_processed_at,
                "reviewed_by": self.reviewed_by,
                "reviewed_at": self.reviewed_at,
                "reject_reason": self.reject_reason,
                "priority": self.priority,
                "is_top": self.is_top,
                "is_featured": self.is_featured,
            }
        })
        return base


# ============================================================
# 工厂函数
# ============================================================

def create_from_raw_item(raw_item, filter_result=None) -> Article:
    """
    从采集原始条目创建文章草稿
    
    Args:
        raw_item: RawItem 对象（来自 filters.py）
        filter_result: FilterResult 对象（可选，已计算好的过滤结果）
    """
    article = Article(
        title=raw_item.title,
        summary=raw_item.summary or "",
        content="",  # HTML内容后续填充
        content_text=raw_item.content or "",
        url=raw_item.url,
        source_name=raw_item.source_name,
        author=raw_item.author,
        published_at_original=raw_item.published_at or "",
        status=ArticleStatus.DRAFT.value,
    )
    
    if filter_result and filter_result.passed:
        article.filter_score = filter_result.score
        article.filter_keywords = filter_result.matched_keywords
        article.filter_suggestions = filter_result.suggestions
        # 基于过滤器得分设置初始优先级
        article.priority = filter_result.score
    
    return article


def apply_ai_result(article: Article, process_result) -> Article:
    """将AI处理结果应用到文章对象"""
    article.ai_summary = process_result.summary
    article.ai_quality_score = process_result.quality_score
    article.ai_relevance_score = process_result.relevance_score
    article.ai_content_type = process_result.content_type
    article.ai_is_important = process_result.is_important
    article.ai_processed_at = datetime.now().isoformat()
    article.ai_processing_time_ms = process_result.processing_time_ms
    
    # 如果没有手动设置分类，使用AI推荐
    if not article.category_id and process_result.category_id:
        article.category_id = process_result.category_id
        # TODO: 从CATEGORY_RULES获取slug和name
    
    # 合并AI提取的标签
    if process_result.tags and not article.tags:
        article.tags = process_result.tags
        article.tag_ids = [t.get("id") or t.get("slug") for t in process_result.tags]
    
    # 更新摘要（如果没有更好的摘要）
    if not article.summary or len(article.summary) < 20:
        article.summary = process_result.summary
    
    # 更新状态为待审核
    if article.status == ArticleStatus.DRAFT.value:
        article.status = ArticleStatus.PENDING_REVIEW.value
    
    article.updated_at = datetime.now().isoformat()
    
    return article


if __name__ == "__main__":
    # 测试数据模型
    from app.services.filters import RawItem, should_collect
    
    raw = RawItem(
        title="Anthropic发布Claude 3.5 Sonnet，编程能力大幅提升",
        summary="Anthropic今天宣布了Claude系列的最新版本...",
        source_name="机器之心"
    )
    
    fr = should_collect(raw)
    article = create_from_raw_item(raw, fr)
    
    print("=== 文章模型测试 ===")
    print(f"ID: {article.id}")
    print(f"Title: {article.title}")
    print(f"Status: {article.status}")
    print(f"Filter Score: {article.filter_score}")
    print(f"Keywords: {article.filter_keywords}")
    print(f"Suggestions: {article.filter_suggestions}")
    print(f"\nAPI Dict keys: {list(article.to_api_dict().keys())}")
