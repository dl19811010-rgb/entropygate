"""
工具可用性追踪服务 - EntropyGate AI 核心差异化功能

用途：
  - 定期检测各AI工具的国内可用性状态
  - 状态变更时自动通知 + 记录变更日志
  - 为Availability.vue页面提供实时数据

设计原则：
  - 可用性是本站的核心差异化内容，必须保持准确和及时
  - 每个工具的检测频率根据其稳定性动态调整
  - 变更必须有来源和原因记录
"""

import json
import logging
import re
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================
# 检测方法定义
# ============================================================

class CheckMethod(Enum):
    HTTP_STATUS = "http_status"      # 检测HTTP状态码
    DNS_RESOLVE = "dns_resolve"      # 检测DNS是否解析
    PAGE_CONTENT = "page_content"    # 检测页面内容特征
    API_PROBE = "api_probe"          # 调用API接口探测
    MANUAL = "manual"                # 人工确认


# ============================================================
# 检测规则配置
# ============================================================

CHECK_RULES = {
    # 格式: domain -> { method, expected_patterns, url }
    "openai.com": {
        "method": CheckMethod.HTTP_STATUS,
        "check_url": "https://chat.openai.com",
        "expected_status": [200, 301, 302, 303],
        "block_indicators": ["access denied", "cloudflare", "403 forbidden"],
        "note": "需VPN或代理访问",
        "default_status": "needs_vpn",
        "check_interval_hours": 6,
    },
    "anthropic.com": {
        "method": CheckMethod.HTTP_STATUS,
        "check_url": "https://claude.ai",
        "expected_status": [200, 301, 302],
        "block_indicators": ["access denied", "unavailable in your country"],
        "note": "需VPN或代理访问",
        "default_status": "needs_vpn",
        "check_interval_hours": 6,
    },
    "gemini.google.com": {
        "method": CheckMethod.HTTP_STATUS,
        "check_url": "https://gemini.google.com",
        "expected_status": [200],
        "block_indicators": [],
        "note": "国内部分地区可直接访问",
        "default_status": "uncertain",
        "check_interval_hours": 12,
    },
    "kimi.moonshot.cn": {
        "method": CheckMethod.HTTP_STATUS,
        "check_url": "https://kimi.moonshot.cn",
        "expected_status": [200],
        "block_indicators": [],
        "note": "国内直接可用",
        "default_status": "available",
        "check_interval_hours": 24,
    },
    "midjourney.com": {
        "method": CheckMethod.PAGE_CONTENT,
        "check_url": "https://www.midjourney.com",
        "expected_patterns": ["login", "sign in"],
        "block_indicators": ["access denied", "not available"],
        "note": "通过Discord使用，Discord国内受限",
        "default_status": "restricted",
        "check_interval_hours": 24,
    },
}

# 默认规则（未匹配域名的工具）
DEFAULT_CHECK_RULE = {
    "method": CheckMethod.HTTP_STATUS,
    "check_interval_hours": 48,
    "default_status": "uncertain",
}


@dataclass
class AvailabilityCheckResult:
    """单次检测结果"""
    tool_id: str = ""
    tool_name: str = ""
    domain: str = ""
    old_status: str = ""
    new_status: str = ""
    changed: bool = False
    check_method: str = ""
    response_time_ms: int = 0
    http_status: int = 0
    details: str = ""
    checked_at: str = ""
    error: str = ""


class ToolAvailabilityTracker:
    """
    工具可用性追踪器
    
    功能：
    1. 单工具检测
    2. 批量检测
    3. 变更判定与通知
    4. 统计汇总
    """
    
    def __init__(self):
        self.rules = CHECK_RULES
        self.change_history = []  # 本次运行中的变更记录
    
    def get_rule(self, domain: str) -> dict:
        """获取域名对应的检测规则"""
        # 精确匹配
        if domain in self.rules:
            return self.rules[domain]
        # 子域名匹配
        for rule_domain, rule in self.rules.items():
            if domain.endswith(f".{rule_domain}") or domain == rule_domain:
                return rule
        return DEFAULT_CHECK_RULE
    
    def extract_domain(self, url: str) -> str:
        """从URL中提取域名"""
        if not url:
            return ""
        url = url.replace("https://", "").replace("http://", "").replace("www.", "")
        return url.split("/")[0].split(":")[0]
    
    async def check_single_tool(self, tool) -> AvailabilityCheckResult:
        """
        检测单个工具的可用性
        
        Args:
            tool: Tool对象或dict，需包含 official_url 和 availability_status 字段
        """
        import time
        start = time.time()
        
        result = AvailabilityCheckResult(
            tool_id=getattr(tool, 'id', tool.get('id', '')),
            tool_name=getattr(tool, 'name', tool.get('name', '')),
            checked_at=datetime.now().isoformat(),
        )
        
        url = getattr(tool, 'official_url', tool.get('official_url', ''))
        if not url:
            result.error = "无官方URL"
            result.new_status = getattr(tool, 'availability_status', tool.get('availability_status', 'uncertain'))
            return result
        
        domain = self.extract_domain(url)
        result.domain = domain
        rule = self.get_rule(domain)
        
        old_status = getattr(tool, 'availability_status', tool.get('availability_status', 'uncertain'))
        result.old_status = old_status
        result.check_method = rule["method"].value
        
        try:
            # 执行检测（模拟实现）
            new_status, details = await self._execute_check(url, rule)
            
            result.new_status = new_status
            result.details = details
            result.changed = (old_status != new_status)
            result.response_time_ms = int((time.time() - start) * 1000)
            
            if result.changed:
                self.change_history.append({
                    "tool_id": result.tool_id,
                    "tool_name": result.tool_name,
                    "old_status": old_status,
                    "new_status": new_status,
                    "domain": domain,
                    "details": details,
                    "checked_at": result.checked_at,
                })
                logger.info(f"[可用性变更] {result.tool_name}: {old_status} → {new_status} ({details})")
                
        except Exception as e:
            result.error = str(e)
            result.new_status = old_status  # 检测失败保持原状态
            logger.error(f"[可用性检测失败] {result.tool_name}: {e}")
        
        return result
    
    async def _execute_check(self, url: str, rule: dict) -> tuple:
        """
        执行具体的检测逻辑
        
        返回: (new_status, details)
        
        注意：这是框架代码，实际HTTP请求需要异步HTTP客户端（如aiohttp/httpx）
        当前返回基于规则的默认值，生产环境应替换为真实请求
        """
        method = rule.get("method")
        
        if method == CheckMethod.MANUAL:
            return rule.get("default_status", "uncertain"), "人工确认"
        
        # TODO: 生产环境替换为真实HTTP检测
        # 示例（使用 aiohttp）:
        #   async with aiohttp.ClientSession() as session:
        #       async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
        #           status = resp.status
        #           content = await resp.text()
        #           # 判断是否被封禁...
        
        # 当前：返回规则默认值（开发阶段）
        default_status = rule.get("default_status", "uncertain")
        note = rule.get("note", "")
        
        return default_status, f"规则默认值({note})"
    
    async def check_batch(self, tools: list) -> list[AvailabilityCheckResult]:
        """批量检测多个工具"""
        results = []
        for tool in tools:
            result = await self.check_single_tool(tool)
            results.append(result)
        return results
    
    def get_summary(self) -> dict:
        """获取本次检测的汇总统计"""
        total = len(self.change_history)
        by_new_status = {}
        for change in self.change_history:
            s = change["new_status"]
            by_new_status[s] = by_new_status.get(s, 0) + 1
        
        return {
            "total_changes": total,
            "by_new_status": by_new_status,
            "changes": self.change_history,
            "checked_at": datetime.now().isoformat(),
        }


# ============================================================
# 定时任务入口
# ============================================================

async def scheduled_availability_check():
    """
    定时任务：执行全量工具可用性检测
    
    由调度器定期调用（建议每6小时一次高频工具，每24小时一次稳定工具）
    """
    tracker = ToolAvailabilityTracker()
    
    # TODO: 从数据库获取所有已发布工具
    # tools = await db.query("SELECT * FROM tools WHERE status='published'")
    # results = await tracker.check_batch(tools)
    
    # 对于每个变更，更新数据库 + 发送通知
    # for result in results:
    #     if result.changed:
    #         await db.execute(
    #             "UPDATE tools SET availability_status=$1, last_checked_at=$2 WHERE id=$3",
    #             result.new_status, result.checked_at, result.tool_id
    #         )
    #         await log_availability_change(result)
    #         if result.new_status in ('blocked', 'available'):
    #             await send_availability_alert(result)
    
    pass


if __name__ == "__main__":
    import asyncio
    
    async def test_tracker():
        from models.tool import Tool, AvailabilityStatus
        
        tracker = ToolAvailabilityTracker()
        
        test_tools = [
            Tool(id="t1", name="ChatGPT", official_url="https://chat.openai.com",
                 availability_status=AvailabilityStatus.NEEDS_VPN.value),
            Tool(id="t2", name="Kimi K2", official_url="https://kimi.moonshot.cn",
                 availability_status=AvailabilityStatus.AVAILABLE.value),
            Tool(id="t3", name="Midjourney", official_url="https://www.midjourney.com",
                 availability_status=AvailabilityStatus.RESTRICTED.value),
        ]
        
        print("=== 可用性追踪测试 ===\n")
        results = await tracker.check_batch(test_tools)
        
        for r in results:
            icon = "⚠️" if r.changed else "✅"
            print(f"{icon} {r.tool_name}: {r.old_status} → {r.new_status} | 方法:{r.check_method} | 耗时:{r.response_time_ms}ms")
            if r.details:
                print(f"   备注: {r.details}")
        
        summary = tracker.get_summary()
        print(f"\n📊 汇总: 总变更{summary['total_changes']}条")
        if summary['by_new_status']:
            for status, count in summary['by_new_status'].items():
                print(f"   → {status}: {count}条")
    
    asyncio.run(test_tracker())
