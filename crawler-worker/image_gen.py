# -*- coding: utf-8 -*-
"""AI 文生图封面通道（ModelScope api-inference，Z-Image-Turbo）。

定位：图片阶梯中"无原图"时的首选——官方原图（正文 <img> / og:image）实在
拿不到时，与其用 Unsplash 风景素材图凑数，不如按文章主题生成一张贴题插画
（用户定夺 2026-07-24：AI 生成 > 风景图）。

接口模式（官方）：
  POST /v1/images/generations  (header X-ModelScope-Async-Mode: true)
    -> {"task_id": ...}
  GET  /v1/tasks/{task_id}     (header X-ModelScope-Task-Type: image_generation)
    -> task_status SUCCEED 时 output_images[0] 为临时图 URL（MS OSS，需尽快镜像）

实测（2026-07-24）：
  - size 用 "宽x高" 字符串（"1664x928"），width/height 字段会被忽略（出竖版图）；
  - 1664x928 横版约 15-25s/张，产出 PNG ~1.6MB；
  - num_inference_steps=9, guidance_scale=0.0 是官方推荐 turbo 档。

环境变量：
  MS_IMAGE_TOKEN   ModelScope token（默认回退 MS_TOKEN；都不设则通道关闭）
  IMAGE_GEN_MODEL  默认 Tongyi-MAI/Z-Image-Turbo
  IMAGE_GEN_SIZE   默认 1664x928（16:9 封面）
  IMAGE_GEN_MAX_PER_RUN  单次运行最多生成张数（默认 8，约 3-4 分钟）
  IMAGE_GEN_TIMEOUT      单张轮询最长秒数（默认 90）
"""
import logging
import os
import time

import httpx

log = logging.getLogger("image_gen")

BASE = "https://api-inference.modelscope.cn"
TOKEN = os.environ.get("MS_IMAGE_TOKEN") or os.environ.get("MS_TOKEN") or ""
MODEL = os.environ.get("IMAGE_GEN_MODEL", "Tongyi-MAI/Z-Image-Turbo")
SIZE = os.environ.get("IMAGE_GEN_SIZE", "1664x928")
MAX_PER_RUN = int(os.environ.get("IMAGE_GEN_MAX_PER_RUN", "8"))
POLL_TIMEOUT = int(os.environ.get("IMAGE_GEN_TIMEOUT", "90"))

# 运行内配额计数（模块级，worker 单次运行共享）
_used = 0

# 提示词包装：LLM 出的英文搜图 query 偏关键词风，包一层编辑部插画指令。
# 用户明确要求"不一定需要图片上有文字"——反向禁文字，避免鬼画符字母。
_PROMPT_TMPL = (
    "editorial technology news illustration: {q}. "
    "clean modern flat style, professional, wide composition, "
    "soft gradient background, no text, no letters, no watermark, no logo"
)


def enabled() -> bool:
    return bool(TOKEN)


def remaining() -> int:
    return max(0, MAX_PER_RUN - _used)


def generate_cover(query: str) -> str:
    """按主题 query 生成封面插画，返回 MS 临时图 URL（调用方负责镜像/落库）。
    失败返回 ""（配额耗尽/超时/API 错），调用方落下一通道。"""
    global _used
    if not enabled() or remaining() <= 0:
        return ""
    q = (query or "").strip() or "artificial intelligence technology"
    prompt = _PROMPT_TMPL.format(q=q[:300])
    h = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    try:
        r = httpx.post(
            f"{BASE}/v1/images/generations",
            json={
                "model": MODEL,
                "prompt": prompt,
                "size": SIZE,
                "num_inference_steps": 9,
                "guidance_scale": 0.0,
            },
            headers={**h, "X-ModelScope-Async-Mode": "true"},
            timeout=60,
        )
        if r.status_code != 200:
            log.warning("image-gen submit HTTP %s: %s", r.status_code, r.text[:160])
            return ""
        task_id = (r.json() or {}).get("task_id")
        if not task_id:
            log.warning("image-gen submit no task_id: %s", r.text[:160])
            return ""
    except Exception as ex:  # noqa: BLE001
        log.warning("image-gen submit failed: %s", ex)
        return ""

    _used += 1  # 提交成功即计额（失败的任务也烧 API 调用）
    t0 = time.time()
    while time.time() - t0 < POLL_TIMEOUT:
        time.sleep(4)
        try:
            g = httpx.get(
                f"{BASE}/v1/tasks/{task_id}",
                headers={**h, "X-ModelScope-Task-Type": "image_generation"},
                timeout=60,
            )
            d = g.json() or {}
        except Exception as ex:  # noqa: BLE001
            log.warning("image-gen poll failed: %s", ex)
            return ""
        st = d.get("task_status")
        if st == "SUCCEED":
            url = ((d.get("output_images") or [""])[0] or "").strip()
            if url:
                log.info("image-gen ok in %.0fs: %s", time.time() - t0, url[:100])
                return url
            log.warning("image-gen SUCCEED but empty output_images")
            return ""
        if st == "FAILED":
            log.warning("image-gen task FAILED: %s", str(d)[:200])
            return ""
    log.warning("image-gen timeout after %ds", POLL_TIMEOUT)
    return ""
