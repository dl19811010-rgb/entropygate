"""
采集内容过滤器 - EntropyGate AI 新动态版块

用途：在采集入库前对原始内容进行质量筛选，
      确保只有符合「AI新动态」定位的高价值内容进入审核队列。

使用方式：
    from scripts.filters import should_collect, FilterResult

    item = RawItem(title="...", summary="...", source_name="...")
    result = should_collect(item)
    if result.passed:
        save_to_draft(item)  # 入库待审核
    else:
        log_filtered(item, result.reason)  # 记录丢弃原因

测试：python scripts/filters.py
"""

from dataclasses import dataclass
from typing import Optional


# ============================================================
# 1. 关键词配置 - 核心界定规则（来自采集界定.txt）
# ============================================================

# 白名单：标题或摘要必须包含至少一个才考虑采集
# 分为三级权重：核心(3)、重要(2)、一般(1)
KEYWORD_WHITELIST = {
    # === 核心词（权重3）- 直接相关AI产品/模型/技术 ===
    "GPT": 3, "GPT-4": 3, "GPT-4o": 3, "GPT-5": 3,
    "Claude": 3, "Claude 3": 3, "Claude 3.5": 3, "Claude 3 Opus": 3,
    "Gemini": 3, "Gemini Pro": 3, "Gemini Ultra": 3,
    "LLM": 3, "大语言模型": 3, "大模型": 3,
    "ChatGPT": 3,

    # === 重要词（权重2）- AI领域关键概念 ===
    "人工智能": 2, "AIGC": 2, "AGI": 2,
    "机器学习": 2, "深度学习": 2, "神经网络": 2,
    "Transformer": 2, "Diffusion": 2,
    "多模态": 2, "智能体": 2, "AI Agent": 2,
    "Stable Diffusion": 2, "Midjourney": 2, "DALL·E": 2, "DALL-E": 2, "Sora": 2,
    "Cursor": 2, "Copilot": 2, "GitHub Copilot": 2,
    "开源": 2, "OpenAI": 2, "Anthropic": 2, "Google DeepMind": 2,
    "字节跳动": 2, "阿里": 2, "通义": 2, "百度": 2, "文心": 2,
    "智谱": 2, "月之暗面": 2, "Kimi": 2, "MiniMax": 2, "零一万物": 2,

    # === 一般词（权重1）- 可能相关的宽泛词汇 ===
    "发布": 1, "上线": 1, "更新": 1, "版本": 1, "新品": 1,
    "工具": 1, "产品": 1, "平台": 1, "框架": 1, "API": 1,
    "模型": 1, "训练": 1, "推理": 1, "微调": 1, "预训练": 1,
    "芯片": 1, "GPU": 1, "NVIDIA": 1, "算力": 1,
    "禁用": 1, "封禁": 1, "限制": 1, "合规": 1, "监管": 1, "政策": 1,
    "可用性": 1, "替代": 1, "国产": 1, "国内": 1,
    "机器人": 1, "自动驾驶": 1, "语音识别": 1, "图像生成": 1, "文本生成": 1,
}

# 黑名单：包含任意一个直接丢弃（无论白名单命中情况）
KEYWORD_BLACKLIST = [
    # 融资/IPO类（除非金额巨大且明确影响产品路线）
    "融资", "IPO", "上市", "财报", "股价", "并购", "收购", "亿美元融资",
    "估值", "轮融资", "天使轮", "A轮", "B轮", "C轮",
    # 招聘/人事
    "招聘", "求职", "面试", "内推", "offer", "入职", "离职", "裁员",
    "薪资", "工资", "年薪",
    # 非AI科技（明确排除）
    "电动车", "新能源汽车", "手机发布", "数码新品",
    "航天", "火箭", "卫星",
    # 纯社区噪音
    "求助", "请问大家", "有人知道吗", "怎么解决", "报错",
    "分享福利", "薅羊毛", "优惠券", "打折",
]


# ============================================================
# 2. 来源特定规则
# ============================================================

SOURCE_RULES = {
    "36氪": {
        "min_score": 4,
        "require_ai_keyword": True,
        "max_items_per_fetch": 8,
        "description": "泛科技媒体，需要严格过滤非AI内容"
    },
    "Reddit": {
        "min_score": 3,
        "exclude_patterns": [r"help\s+me", r"how\s+do\s*I"],
        "description": "社区讨论帖多，需过滤求助/水帖"
    },
    "Hacker News": {
        "min_score": 3,
        "require_summary": True,
        "description": "综合技术论坛，仅保留AI高相关内容"
    },
    "量子位": {
        "min_score": 2,
        "max_items_per_fetch": 15,
        "description": "垂直AI媒体，本身质量较高"
    },
    "机器之心": {
        "min_score": 2,
        "max_items_per_fetch": 15,
        "description": "垂直AI媒体"
    },
}


# ============================================================
# 3. 内容质量阈值
# ============================================================

MIN_TITLE_LENGTH = 10
MAX_TITLE_LENGTH = 200
MIN_SUMMARY_LENGTH = 20


# ============================================================
# 4. 数据结构
# ============================================================

@dataclass
class RawItem:
    """采集到的原始条目"""
    title: str
    summary: Optional[str] = None
    content: Optional[str] = None
    url: str = ""
    source_name: str = ""
    author: Optional[str] = None
    published_at: Optional[str] = None


@dataclass
class FilterResult:
    """过滤结果"""
    passed: bool
    reason: str = ""
    score: int = 0
    matched_keywords: list = None
    suggestions: list = None

    def __post_init__(self):
        if self.matched_keywords is None:
            self.matched_keywords = []
        if self.suggestions is None:
            self.suggestions = []


# ============================================================
# 5. 核心过滤函数
# ============================================================

def calculate_relevance_score(text: str) -> tuple:
    """计算文本与AI新动态的相关性得分"""
    text_lower = text.lower()
    score = 0
    matched = []
    for keyword, weight in KEYWORD_WHITELIST.items():
        if keyword.lower() in text_lower:
            score += weight
            matched.append(keyword)
    return score, matched


def check_blacklist(text: str) -> Optional[str]:
    """检查是否命中黑名单"""
    for kw in KEYWORD_BLACKLIST:
        if kw and kw.lower() in text.lower():
            return kw
    return None


def get_source_rule(source_name: str) -> dict:
    """获取来源特定的过滤规则"""
    if source_name in SOURCE_RULES:
        return SOURCE_RULES[source_name]
    for key, rule in SOURCE_RULES.items():
        if key in source_name or source_name in key:
            return rule
    return {"min_score": 3, "max_items_per_fetch": 10, "description": "默认规则"}


def should_collect(item: RawItem) -> FilterResult:
    """
    主过滤函数：判断一条采集内容是否应该进入审核队列

    过滤流程：
    1. 黑名单检查 → 直接丢弃
    2. 长度检查 → 太短则丢弃
    3. 白名单评分 → 不够分则丢弃
    4. 来源特定规则 → 按来源调整标准
    5. 返回结果（含得分和建议标签）
    """
    full_text = f"{item.title} {item.summary or ''} {item.content or ''}"

    # 第1步：黑名单优先
    black_kw = check_blacklist(full_text)
    if black_kw:
        return FilterResult(passed=False, reason=f"命中黑名单关键词: [{black_kw}]")

    # 第2步：长度检查
    if len(item.title) < MIN_TITLE_LENGTH:
        return FilterResult(passed=False, reason=f"标题过短 ({len(item.title)} < {MIN_TITLE_LENGTH})")
    if len(item.title) > MAX_TITLE_LENGTH:
        return FilterResult(passed=False, reason=f"标题过长")

    # 第3步：白名单评分
    score, matched = calculate_relevance_score(full_text)
    if score == 0:
        return FilterResult(passed=False, reason="未命中任何白名单关键词", score=0)

    # 第4步：来源特定规则
    source_rule = get_source_rule(item.source_name)
    min_score = source_rule.get("min_score", 3)

    if source_rule.get("require_ai_keyword"):
        core_kws = [kw for kw, w in KEYWORD_WHITELIST.items() if w >= 3]
        if not any(kw.lower() in full_text.lower() for kw in core_kws):
            return FilterResult(
                passed=False, reason=f"[{item.source_name}] 未命中核心AI关键词",
                score=score, matched_keywords=matched)

    if score < min_score:
        return FilterResult(
            passed=False, reason=f"相关性得分不足 ({score} < {min_score})",
            score=score, matched_keywords=matched)

    # 第5步：通过！生成建议标签
    suggestions = _generate_suggestions(score, matched, item)
    return FilterResult(
        passed=True, score=score,
        matched_keywords=matched, suggestions=suggestions)


def _generate_suggestions(score: int, matched: list, item: RawItem) -> list:
    """根据命中的关键词和得分，为审核人员生成建议标签"""
    suggestions = []

    if score >= 10:
        suggestions.append("🔥 高度推荐 - 核心AI动态")
    elif score >= 6:
        suggestions.append("✅ 推荐 - 明确相关")
    elif score >= 4:
        suggestions.append("⚠️ 一般相关 - 建议快速审核")
    else:
        suggestions.append("💡 低相关 - 可考虑放宽标准")

    text_lower = f"{item.title} {item.summary or ''}".lower()

    # 内容类型判断
    if any(kw in text_lower for kw in ["发布", "上线", "推出", "开源", "更新"]):
        suggestions.append("类型: 产品/模型发布")
    elif any(kw in text_lower for kw in ["禁用", "封禁", "限制", "合规", "监管"]):
        suggestions.append("类型: 可用性/政策变化 ⭐重点")
    elif any(kw in text_lower for kw in ["论文", "研究", "arXiv", "突破"]):
        suggestions.append("类型: 学术进展")
    elif any(kw in text_lower for kw in ["教程", "指南", "如何", "使用", "技巧"]):
        suggestions.append("类型: 实用教程")

    # 来源可信度提示
    if item.source_name in ["量子位", "机器之心"]:
        suggestions.append(f"来源: {item.source_name}(垂直媒体 ✓)")
    elif item.source_name in ["36氪", "Hacker News", "Reddit"]:
        suggestions.append(f"来源: {item.source_name}(需人工确认)")

    return suggestions


# ============================================================
# 6. 批量处理工具函数
# ============================================================

def filter_batch(items: list) -> tuple:
    """
    批量过滤一组采集条目
    返回: (通过列表, [(未通过条目, 过滤结果)])
    """
    passed = []
    filtered = []
    for item in items:
        result = should_collect(item)
        if result.passed:
            item._filter_score = result.score
            item._filter_suggestions = result.suggestions
            item._filter_keywords = result.matched_keywords
            passed.append(item)
        else:
            filtered.append((item, result))
    return passed, filtered


# ============================================================
# 7. 测试入口
# ============================================================

if __name__ == "__main__":
    test_cases = [
        RawItem(title="GPT-5即将发布？OpenAI最新动态深度解析",
               summary="据爆料，OpenAI正在测试下一代大模型...", source_name="量子位"),
        RawItem(title="某AI公司完成B轮融资3亿美元",
               summary="本轮融资将用于扩大团队规模...", source_name="36氪"),
        RawItem(title="Midjourney V7实测：图像生成质量迎来质的飞跃",
               summary="我们深度体验了最新版本的Midjourney...", source_name="AI科技评论"),
        RawItem(title="求助：如何配置CUDA环境？",
               summary="我的显卡是RTX 3060，一直报错...", source_name="Reddit"),
        RawItem(title="特斯拉新款电动车发布，续航提升20%",
               summary="特斯拉今日正式发布了2025款Model Y...", source_name="36氪"),
        RawItem(title="Anthropic发布Claude 3.5 Sonnet，编程能力大幅提升",
               summary="Anthropic今天宣布了Claude系列的最新版本...", source_name="机器之心"),
        RawItem(title="国内用户注意：ChatGPT Plus支付方式变更",
               summary="OpenAI调整了订阅支付渠道，国内用户受影响...", source_name="Hacker News"),
    ]

    print("=" * 60)
    print("采集过滤器测试 - EntropyGate AI 新动态版块")
    print("=" * 60)

    passed_count = 0
    for item in test_cases:
        result = should_collect(item)
        status = "✅ 通过" if result.passed else "❌ 过滤"
        print(f"\n{status} | 得分: {result.score}")
        print(f"  标题: {item.title}")
        print(f"  来源: {item.source_name}")
        if not result.passed:
            print(f"  原因: {result.reason}")
        else:
            print(f"  关键词: {', '.join(result.matched_keywords[:5])}")
            print(f"  建议: {result.suggestions[0] if result.suggestions else ''}")
        if result.passed:
            passed_count += 1

    print(f"\n{'=' * 60}")
    print(f"总计: {len(test_cases)} | 通过: {passed_count} | "
          f"过滤: {len(test_cases) - passed_count} | "
          f"通过率: {passed_count/len(test_cases)*100:.1f}%")
