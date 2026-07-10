"""
AI 辅助处理服务 - EntropyGate AI 新动态版块

用途：对采集入库的草稿文章进行 AI 自动处理，包括：
  - 摘要生成（提炼核心要点）
  - 智能分类（判断所属分类）
  - 标签提取（提取关键标签）
  - 质量评分（评估内容质量）
  - 相关度补充打分

使用方式：
    from app.services.ai_processor import AIProcessor
    
    processor = AIProcessor()
    result = await processor.process_draft(draft_article)
"""

import re
import json
from dataclasses import dataclass, field, asdict
from typing import Optional


# ============================================================
# 数据结构
# ============================================================

@dataclass
class ProcessResult:
    """AI 处理结果"""
    summary: str = ""              # 生成的摘要
    category_id: int = None        # 推荐分类ID
    category_name: str = ""        # 推荐分类名
    category_confidence: float = 0  # 分类置信度 (0-1)
    tags: list = field(default_factory=list)  # 提取的标签 [{id, name, slug}]
    quality_score: int = 0         # 质量分 (0-100)
    relevance_score: int = 0       # 相关度分 (0-100)
    content_type: str = ""         # 内容类型: release/policy/tutorial/research/other
    is_important: bool = False     # 是否为重点内容（可用性变化等）
    processing_time_ms: int = 0    # 处理耗时
    error: str = ""                # 错误信息


@dataclass
class DraftArticle:
    """草稿文章（输入）"""
    id: str
    title: str
    summary: str = ""
    content: str = ""
    content_text: str = ""         # 纯文本版本
    url: str = ""
    source_name: str = ""
    filter_score: int = 0          # 过滤器得分
    filter_keywords: list = field(default_factory=list)  # 过滤器命中的关键词
    filter_suggestions: list = field(default_factory=list)  # 过滤器建议


# ============================================================
# 分类规则引擎（基于关键词，无需调用外部AI）
# ============================================================

CATEGORY_RULES = {
    "大模型动态": {
        "id": 1,
        "slug": "llm-news",
        "keywords": ["GPT", "Claude", "Gemini", "ChatGPT", "LLM", "大语言模型", "大模型",
                     "GPT-4", "GPT-4o", "GPT-5", "Claude 3", "Claude 3.5",
                     "OpenAI", "Anthropic", "Google DeepMind",
                     "智谱", "Kimi", "月之暗面", "MiniMax", "零一万物", "通义", "文心"],
        "weight": 3,
        "description": "GPT/Claude/Gemini等大模型产品发布与更新"
    },
    "AI工具与应用": {
        "id": 2,
        "slug": "ai-tools",
        "keywords": ["Midjourney", "DALL·E", "DALL-E", "Stable Diffusion", "Sora",
                     "Cursor", "Copilot", "GitHub Copilot",
                     "工具", "平台", "框架", "API", "产品", "发布", "上线", "更新", "版本"],
        "weight": 2,
        "description": "AI工具发布、更新与使用指南"
    },
    "可用性追踪": {
        "id": 3,
        "slug": "availability",
        "keywords": ["禁用", "封禁", "限制", "合规", "监管", "政策", "可用性",
                     "替代", "国产", "国内", "访问", "使用", "支付", "订阅"],
        "weight": 4,  # 最高权重 — 核心差异化内容
        "description": "AI工具在国内的可用性状态变化"
    },
    "行业动态": {
        "id": 4,
        "slug": "industry",
        "keywords": ["融资", "收购", "合作", "投资", "企业", "公司", "行业", "市场",
                     "芯片", "GPU", "NVIDIA", "算力", "机器人", "自动驾驶"],
        "weight": 1,
        "description": "AI行业商业动态与技术趋势"
    },
    "技术研究": {
        "id": 5,
        "slug": "research",
        "keywords": ["论文", "研究", "arXiv", "突破", "算法", "训练", "推理",
                     "微调", "预训练", "Transformer", "Diffusion", "神经网络", "机器学习", "深度学习"],
        "weight": 2,
        "description": "AI学术研究与技术创新"
    }
}


# ============================================================
# 标签库（从过滤器白名单扩展）
# ============================================================

TAG_LIBRARY = [
    {"name": "GPT", "slug": "gpt", "color": "#10a37f"},
    {"name": "Claude", "slug": "claude", "color": "#d97706"},
    {"name": "Gemini", "slug": "gemini", "color": "#4285f4"},
    {"name": "ChatGPT", "slug": "chatgpt", "color": "#10a37f"},
    {"name": "OpenAI", "slug": "openai", "color": "#10a37f"},
    {"name": "Anthropic", "slug": "anthropic", "color": "#d97706"},
    {"name": "Google DeepMind", "slug": "deepmind", "color": "#4285f4"},
    {"name": "Midjourney", "slug": "midjourney", "color": "#000000"},
    {"name": "Sora", "slug": "sora", "color": "#ec4899"},
    {"name": "Cursor", "slug": "cursor", "color": "#2d2d2d"},
    {"name": "国产替代", "slug": "domestic-alt", "color": "#ef4444"},
    {"name": "可用性变化", "slug": "availability", "color": "#f59e0b"},
    {"name": "开源", "slug": "open-source", "color": "#6366f1"},
    {"name": "大模型", "slug": "llm", "color": "#8b5cf6"},
    {"name": "图像生成", "slug": "image-gen", "color": "#ec4899"},
    {"name": "多模态", "slug": "multimodal", "color": "#14b8a6"},
    {"name": "AI Agent", "slug": "ai-agent", "color": "#f97316"},
]


# ============================================================
# 核心 AI 处理类
# ============================================================

class AIProcessor:
    """
    AI 内容处理器
    
    支持两种模式：
    1. 规则模式（默认）：纯本地规则，无需外部 API，速度快
    2. LLM 模式：调用 OpenAI/其他 LLM API，质量更高但需配置 API Key
    """
    
    def __init__(self, mode="rule", api_key=None, model=None):
        """
        初始化处理器
        
        Args:
            mode: "rule" (纯规则) 或 "llm" (调用LLM API)
            api_key: LLM API 密钥（mode=llm 时需要）
            model: LLM 模型名称（如 gpt-4o-mini）
        """
        self.mode = mode
        self.api_key = api_key
        self.model = model or "gpt-4o-mini"
    
    async def process_draft(self, draft: DraftArticle) -> ProcessResult:
        """
        处理一条草稿文章（主入口）
        
        返回完整的处理结果，包含摘要、分类、标签、质量分等
        """
        import time
        start = time.time()
        
        try:
            if self.mode == "rule":
                result = await self._process_with_rules(draft)
            else:
                result = await self._process_with_llm(draft)
            
            result.processing_time_ms = int((time.time() - start) * 1000)
            return result
            
        except Exception as e:
            return ProcessResult(error=str(e))
    
    async def _process_with_rules(self, draft: DraftArticle) -> ProcessResult:
        """纯规则模式处理（无需外部API）"""
        text = f"{draft.title} {draft.summary} {draft.content_text}".lower()
        title_lower = draft.title.lower()
        
        result = ProcessResult()
        
        # 1. 摘要生成（基于原文摘要或截取正文）
        result.summary = self._generate_summary(draft)
        
        # 2. 分类判断
        cat_result = self._classify(text, draft.title)
        result.category_id = cat_result["id"]
        result.category_name = cat_result["name"]
        result.category_confidence = cat_result["confidence"]
        
        # 3. 标签提取
        result.tags = self._extract_tags(text, draft.filter_keywords)
        
        # 4. 质量评分
        result.quality_score = self._score_quality(draft, text)
        
        # 5. 相关度评分（结合过滤器得分和自身评估）
        result.relevance_score = self._score_relevance(draft, result)
        
        # 6. 内容类型判断
        result.content_type = self._detect_content_type(title_lower, text)
        
        # 7. 是否为重点内容
        result.is_important = (
            result.content_type == "availability" or
            result.quality_score >= 80 or
            draft.filter_score >= 8
        )
        
        return result
    
    async def _process_with_llm(self, draft: DraftArticle) -> ProcessResult:
        """LLM 模式处理（需配置 API Key）"""
        # TODO: 对接 OpenAI / 其他 LLM API
        # 当前降级为规则模式
        return await self._process_with_rules(draft)
    
    # -----------------------------------------------------------
    # 各子任务实现（规则模式）
    # -----------------------------------------------------------
    
    def _generate_summary(self, draft: DraftArticle) -> str:
        """生成摘要（优先使用源摘要，否则从正文截取）"""
        if draft.summary and len(draft.summary) >= 30:
            # 已有摘要，清理后返回
            return draft.summary.strip()[:300]
        
        if draft.content_text:
            # 从正文前200字生成
            text = draft.content_text.replace('\n', ' ').strip()
            if len(text) > 200:
                return text[:200].rsplit(' ', 1)[0] + '…'
            return text
        
        # 最差情况：用标题
        return draft.title
    
    def _classify(self, text: str, title: str) -> dict:
        """基于关键词的分类判断"""
        best_match = None
        best_score = 0
        
        for cat_name, rule in CATEGORY_RULES.items():
            score = 0
            matched_keywords = []
            
            for kw in rule["keywords"]:
                if kw.lower() in text:
                    score += rule["weight"]
                    matched_keywords.append(kw)
            
            if score > best_score:
                best_score = score
                best_match = {
                    "id": rule["id"],
                    "name": cat_name,
                    "slug": rule["slug"],
                    "confidence": min(score / 20, 1.0),  # 归一化到 0-1
                    "matched_kw": matched_keywords
                }
        
        if not best_match:
            # 默认分类
            return {
                "id": 1,
                "name": "大模型动态",
                "slug": "llm-news",
                "confidence": 0.3,
                "matched_kw": []
            }
        
        return best_match
    
    def _extract_tags(self, text: str, filter_keywords: list) -> list:
        """从文本中提取匹配的标签"""
        tags = []
        seen = set()
        
        # 先从过滤器命中的关键词中找标签
        for kw in filter_keywords:
            for tag in TAG_LIBRARY:
                if kw.lower() in tag["name"].lower() or tag["slug"] in kw.lower():
                    if tag["slug"] not in seen:
                        tags.append({**tag, "id": tag["slug"]})
                        seen.add(tag["slug"])
        
        # 再从 TAG_LIBRARY 中查找
        for tag in TAG_LIBRARY:
            if tag["slug"] not in seen and tag["name"].lower() in text:
                tags.append({**tag, "id": tag["slug"]})
                seen.add(tag["slug"])
        
        # 限制最多8个标签
        return tags[:8]
    
    def _score_quality(self, draft: DraftArticle, text: str) -> int:
        """质量评分 (0-100)"""
        score = 50  # 基础分
        
        # 标题质量 (+0 ~ +20)
        if len(draft.title) >= 20:
            score += 10
        elif len(draft.title) >= 12:
            score += 5
        
        if not draft.title.startswith(' ') and not draft.title.endswith(' '):
            score += 5
        
        # 有摘要 (+10)
        if draft.summary and len(draft.summary) >= 30:
            score += 10
        
        # 有正文内容 (+15)
        if draft.content_text and len(draft.content_text) >= 100:
            score += 15
        
        # 来源可信度 (+0 ~ +10)
        trusted_sources = ["量子位", "机器之心", "AI科技评论", "OpenAI Blog", "Anthropic Blog"]
        if draft.source_name in trusted_sources:
            score += 10
        elif draft.source_name in ["36氪", "Hacker News"]:
            score += 5
        
        # 过滤器得分映射 (+0 ~ +15)
        score += min(draft.filter_score * 1.5, 15)
        
        return min(int(score), 100)
    
    def _score_relevance(self, draft: DraftArticle, result: ProcessResult) -> int:
        """相关度综合评分 (0-100)"""
        base = draft.filter_score * 7  # 过滤器得分映射到 0~70 分范围
        
        # 分类置信度加成
        base += int(result.category_confidence * 15)
        
        # 标签数量加成
        base += min(len(result.tags) * 2, 15)
        
        return min(base, 100)
    
    def _detect_content_type(self, title_lower: str, text: str) -> str:
        """检测内容类型"""
        combined = f"{title_lower} {text}"
        
        if any(kw in combined for kw in ["禁用", "封禁", "限制", "合规", "监管", "可用性", "支付", "订阅"]):
            return "availability"
        if any(kw in combined for kw in ["发布", "上线", "推出", "开源", "更新", "版本"]):
            return "release"
        if any(kw in combined for kw in ["论文", "研究", "arXiv", "突破", "算法"]):
            return "research"
        if any(kw in combined for kw in ["教程", "指南", "如何", "使用", "技巧", "方法"]):
            return "tutorial"
        
        return "other"


# ============================================================
# 批量处理
# ============================================================

async def process_batch(drafts: list[DraftArticle], processor=None) -> list[ProcessResult]:
    """批量处理多条草稿"""
    if processor is None:
        processor = AIProcessor(mode="rule")
    
    results = []
    for draft in drafts:
        result = await processor.process_draft(draft)
        results.append({
            "draft_id": draft.id,
            "result": asdict(result)
        })
    
    return results


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    import asyncio
    
    test_drafts = [
        DraftArticle(
            id="test-001",
            title="GPT-5即将发布？OpenAI最新动态深度解析",
            summary="据爆料，OpenAI正在测试下一代大模型，预计将在年内发布。新模型在推理能力和多模态理解方面有显著提升。",
            source_name="量子位",
            filter_score=13,
            filter_keywords=["GPT", "GPT-5", "大模型", "OpenAI", "发布"]
        ),
        DraftArticle(
            id="test-002",
            title="国内用户注意：ChatGPT Plus支付方式变更",
            summary="OpenAI调整了订阅支付渠道，国内用户受影响，可能需要寻找替代方案。",
            source_name="Hacker News",
            filter_score=9,
            filter_keywords=["GPT", "ChatGPT", "OpenAI", "国内"]
        ),
        DraftArticle(
            id="test-003",
            title="Midjourney V7实测：图像生成质量迎来质的飞跃",
            summary="我们深度体验了最新版本的Midjourney V7...",
            source_name="AI科技评论",
            filter_score=4,
            filter_keywords=["Midjourney", "版本", "图像生成"]
        ),
    ]
    
    async def run_test():
        processor = AIProcessor(mode="rule")
        
        print("=" * 60)
        print("AI 辅助处理测试 - EntropyGate AI")
        print("=" * 60)
        
        for draft in test_drafts:
            print(f"\n📄 {draft.title[:40]}...")
            result = await processor.process_draft(draft)
            
            if result.error:
                print(f"   ❌ 错误: {result.error}")
                continue
            
            print(f"   📝 摘要: {result.summary[:60]}...")
            print(f"   📂 分类: {result.category_name} ({result.category_confidence:.0%})")
            print(f"   🏷️  标签: {', '.join([t['name'] for t in result.tags[:5]])}")
            print(f"   ⭐ 质量分: {result.quality_score}/100")
            print(f"   🎯 相关度: {result.relevance_score}/100")
            print(f"   🔖 类型: {result.content_type}")
            print(f"   ⚡ 重点: {'是 ⭐' if result.is_important else '否'}")
            print(f"   ⏱️  耗时: {result.processing_time_ms}ms")
    
    asyncio.run(run_test())
