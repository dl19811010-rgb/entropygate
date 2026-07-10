"""
全链路处理流水线 - EntropyGate AI 新动态版块

将采集→过滤→整理→AI辅助→排队待审 串联成完整流水线

使用方式：
    from app.services.pipeline import run_pipeline
    
    result = await run_pipeline(raw_items)
    # result 包含：采集统计、过滤统计、入库数量、AI处理结果等
"""

import time
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """流水线执行结果"""
    total_input: int = 0              # 输入条目数
    filtered_out: int = 0             # 被过滤掉的
    passed_filter: int = 0            # 通过过滤的
    stored_as_draft: int = 0          # 成功入库为草稿
    ai_processed: int = 0             # AI处理完成的
    errors: list = field(default_factory=list)  # 错误列表
    duration_ms: int = 0              # 总耗时
    details: list = field(default_factory=list)  # 每条的处理详情


async def run_pipeline(raw_items: list, config: dict = None) -> PipelineResult:
    """
    执行完整的内容处理流水线
    
    Args:
        raw_items: RawItem 列表（来自采集器）
        config: 配置选项 {
            "skip_filter": bool,         # 是否跳过过滤
            "skip_ai": bool,             # 是否跳过AI处理
            "auto_approve_high_score": bool,  # 是否自动通过高分文章(>=10)
            "dry_run": bool,             # 试运行（不入库）
        }
    
    Returns:
        PipelineResult
    """
    start = time.time()
    cfg = config or {}
    result = PipelineResult(total_input=len(raw_items))
    
    # 延迟导入避免循环依赖
    from scripts.filters import should_collect, filter_batch
    from services.ai_processor import AIProcessor, process_batch
    from models.article import create_from_raw_item, apply_ai_result
    
    logger.info(f"[Pipeline] 开始处理 {len(raw_items)} 条原始内容")
    
    # ====== 第1步：过滤 ======
    if cfg.get("skip_filter"):
        passed_items = raw_items
        result.filtered_out = 0
        result.passed_filter = len(raw_items)
    else:
        passed_items, filtered_pairs = filter_batch(raw_items)
        result.filtered_out = len(filtered_pairs)
        result.passed_filter = len(passed_items)
        
        # 记录过滤原因统计
        reason_counts = {}
        for item, fr in filtered_pairs:
            reason = fr.reason[:40]
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        result.details.append({"step": "filter", "reason_counts": reason_counts})
    
    logger.info(f"[Pipeline] 过滤完成: {result.passed_filter}/{result.total_input} 通过")
    
    if not passed_items:
        result.duration_ms = int((time.time() - start) * 1000)
        return result
    
    # ====== 第2步：入库为草稿 ======
    drafts = []
    for item in passed_items:
        try:
            article = create_from_raw_item(item)
            
            if cfg.get("dry_run"):
                drafts.append(article)
                result.stored_as_draft += 1
            else:
                # TODO: save_to_db(article)
                drafts.append(article)
                result.stored_as_draft += 1
                
        except Exception as e:
            result.errors.append({"item": item.title[:30], "step": "store", "error": str(e)})
    
    logger.info(f"[Pipeline] 入库完成: {result.stored_as_draft} 条草稿")
    
    # ====== 第3步：AI辅助处理 ======
    if cfg.get("skip_ai") or not drafts:
        result.duration_ms = int((time.time() - start) * 1000)
        return result
    
    processor = AIProcessor(mode="rule")
    
    for draft in drafts:
        try:
            from services.ai_processor import DraftArticle as AIDraft
            
            ai_draft = AIDraft(
                id=draft.id,
                title=draft.title,
                summary=draft.summary,
                content_text=draft.content_text,
                source_name=draft.source_name,
                filter_score=draft.filter_score,
                filter_keywords=draft.filter_keywords,
                filter_suggestions=draft.filter_suggestions,
            )
            
            proc_result = await processor.process_draft(ai_draft)
            
            if proc_result.error:
                result.errors.append({"item": draft.title[:30], "step": "ai", "error": proc_result.error})
                continue
            
            apply_ai_result(draft, proc_result)
            result.ai_processed += 1
            
            if not cfg.get("dry_run"):
                # TODO: update_in_db(draft)
                pass
                
        except Exception as e:
            result.errors.append({"item": draft.title[:30], "step": "ai", "error": str(e)})
    
    logger.info(f"[Pipeline] AI处理完成: {result.ai_processed}/{len(drafts)} 条")
    
    # ====== 第4步：自动通过高分（可选）=====
    if cfg.get("auto_approve_high_score") and not cfg.get("dry_run"):
        high_score_ids = [
            d.id for d in drafts 
            if d.filter_score >= 10 or d.ai_is_important
        ]
        if high_score_ids:
            # TODO: batch_update_status(high_score_ids, 'pending_review')
            logger.info(f"[Pipeline] 自动标记高优: {len(high_score_ids)} 条")
    
    result.duration_ms = int((time.time() - start) * 1000)
    
    # 汇总信息
    result.details.append({
        "step": "summary",
        "input": result.total_input,
        "filtered": result.filtered_out,
        "stored": result.stored_as_draft,
        "ai_processed": result.ai_processed,
        "errors": len(result.errors),
        "duration_ms": result.duration_ms
    })
    
    logger.info(f"[Pipeline] 完成! 总耗时: {result.duration_ms}ms")
    return result


# ============================================================
# 定时任务入口
# ============================================================

async def scheduled_crawl_and_process(source_configs: list = None):
    """
    定时任务：采集 + 全链路处理
    
    由调度器（如 APScheduler / Celery Beat）定期调用
    """
    # TODO: 
    # 1. 调用各来源采集器获取 raw_items
    # 2. 调用 run_pipeline(raw_items)
    # 3. 记录执行日志
    # 4. 发送通知（如有异常或高优内容）
    pass


if __name__ == "__main__":
    import asyncio
    from scripts.filters import RawItem
    
    async def test_pipeline():
        test_items = [
            RawItem(title="GPT-5即将发布？OpenAI最新动态深度解析",
                   summary="据爆料，OpenAI正在测试下一代大模型...", source_name="量子位"),
            RawItem(title="某AI公司完成B轮融资3亿美元",
                   summary="本轮融资将用于扩大团队规模...", source_name="36氪"),
            RawItem(title="Anthropic发布Claude 3.5 Sonnet，编程能力大幅提升",
                   summary="Anthropic今天宣布了Claude系列的最新版本...", source_name="机器之心"),
            RawItem(title="国内用户注意：ChatGPT Plus支付方式变更",
                   summary="OpenAI调整了订阅支付渠道...", source_name="Hacker News"),
        ]
        
        print("=" * 60)
        print("全链路流水线测试 - EntropyGate AI")
        print("=" * 60)
        
        result = await run_pipeline(test_items, config={"dry_run": True})
        
        print(f"\n📊 流水线结果:")
        print(f"   输入: {result.total_input}")
        print(f"   过滤掉: {result.filtered_out}")
        print(f"   通过: {result.passed_filter}")
        print(f"   入库: {result.stored_as_draft}")
        print(f"   AI处理: {result.ai_processed}")
        print(f"   错误: {len(result.errors)}")
        print(f"   耗时: {result.duration_ms}ms")
        
        if result.details:
            for detail in result.details:
                print(f"\n   📋 {detail.get('step', '?')}: {detail}")
    
    asyncio.run(test_pipeline())
