# -*- coding: utf-8 -*-
"""AI 文生图封面通道（ModelScope api-inference，provider 注册表制）。

定位：图片阶梯中"无原图"时的首选——官方原图（正文 <img> / og:image）实在
拿不到时，按文章的视觉导演 brief（/articles/generate-cover-brief）生成贴题
封面（用户定夺 2026-07-24：AI 生成 > 风景素材图）。

系统化设计（Supabase12 落地，2026-07-25）
-----------------------------------------
换模型迭代 = 改 PROVIDERS 一条注册项 / 设 IMAGE_GEN_PROVIDER 环境变量，
不动任何调用方代码：
  1. PROVIDERS      模型注册表。同平台（MS api-inference 异步任务制）的模型
                    只差 model/size/steps/guidance 四个参数。
  2. STYLE_PRESETS  风格注册表。全站统一视觉语言的三套英文风格后缀
                    （tech_photo / editorial_illustration / abstract_light），
                    由后端视觉导演 brief 的 style 字段选用。
  3. build_prompt   装配器：metaphor + style suffix + palette + 负面约束。
  4. postprocess    统一后处理（颗粒/暗角/冷调/JPEG），治塑料感、统一调性。
横评工具 eval_covers.py 用同一 brief 跑遍注册表出对比墙，人工打分定主力。

接口模式（官方）：
  POST /v1/images/generations  (header X-ModelScope-Async-Mode: true)
    -> {"task_id": ...}
  GET  /v1/tasks/{task_id}     (header X-ModelScope-Task-Type: image_generation)
    -> task_status SUCCEED 时 output_images[0] 为临时图 URL（MS OSS，需尽快镜像）

实测（2026-07-25， deploy 账号探针）：
  - Tongyi-MAI/Z-Image-Turbo  ✅ 15-25s/张（当前生产主力）
  - Tongyi-MAI/Z-Image        ✅ 质量档，细节明显更锐
  - Qwen/Qwen-Image           ✅ ~2min/张；具象编辑部插画很好，超抽象 prompt 会
                                出空渐变——必须配 brief 的具象隐喻场景
  - FLUX.1-schnell            ❌ 40212（MS api-inference 未上架，两个命名空间都试过）
  - size 必须 "宽x高" 字符串（"1664x928"），width/height 字段会被忽略（出竖版）

环境变量：
  MS_IMAGE_TOKEN   ModelScope token（默认回退 MS_TOKEN；都不设则通道关闭）
  IMAGE_GEN_PROVIDER  注册表键名，默认 zimage_turbo
  IMAGE_GEN_MODEL / IMAGE_GEN_SIZE / IMAGE_GEN_STEPS / IMAGE_GEN_GUIDANCE
                   对所选 provider 的单项覆盖（临时实验用，不写代码）
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
MAX_PER_RUN = int(os.environ.get("IMAGE_GEN_MAX_PER_RUN", "8"))
POLL_TIMEOUT = int(os.environ.get("IMAGE_GEN_TIMEOUT", "90"))

# ── 模型注册表 ────────────────────────────────────────────────────────────────
# 同平台模型只差这四个参数；新增模型 = 加一条注册项（先实测 model id 可用）。
PROVIDERS = {
    "zimage_turbo": {
        "model": "Tongyi-MAI/Z-Image-Turbo",
        "size": "1664x928",
        "steps": 9,
        "guidance": 0.0,
    },
    "zimage": {
        "model": "Tongyi-MAI/Z-Image",
        "size": "1664x928",
        "steps": 25,
        "guidance": 4.0,
    },
    "qwen_image": {
        "model": "Qwen/Qwen-Image",
        "size": "1664x928",
        "steps": 30,
        "guidance": 5.0,
    },
}

PROVIDER = os.environ.get("IMAGE_GEN_PROVIDER", "zimage_turbo").strip() or "zimage_turbo"

# ── 风格注册表（全站统一视觉语言）────────────────────────────────────────────
# 与后端 generate-cover-brief 的 style 三选一一一对应；构图/光影/质感各一句。
STYLE_PRESETS = {
    # 基础设施/芯片/算力/硬件：真实材质 + 电影感布光
    "tech_photo": (
        "cinematic editorial photograph, shallow depth of field, realistic materials "
        "and reflections, soft volumetric lighting, muted industrial color grading, "
        "wide 16:9 composition"
    ),
    # 观点/趋势/战略：高级杂志扁平插画，大留白 + 单强调色
    "editorial_illustration": (
        "premium editorial illustration for a technology magazine, flat geometric "
        "shapes with subtle grain texture, confident composition with generous "
        "negative space, muted duotone palette with one accent color, "
        "wide 16:9 composition"
    ),
    # 纯概念/框架/方法论：抽象光艺术，深底 + 发光渐变
    "abstract_light": (
        "abstract data-art render, flowing luminous gradients and fine particle "
        "lines, glass and light refraction, deep dark background, elegant "
        "minimalism, wide 16:9 composition"
    ),
}

DEFAULT_STYLE = "abstract_light"
DEFAULT_PALETTE = "deep blue and violet with one warm accent"

# 全站统一负面约束（内联进 prompt；Z-Image/Qwen-Image 均无独立 negative 字段）
_NEGATIVE = (
    "no text, no letters, no words, no watermark, no logo, "
    "no brand marks, no people faces"
)

# 运行内配额计数（模块级，worker 单次运行共享）
_used = 0


def enabled() -> bool:
    return bool(TOKEN)


def remaining() -> int:
    return max(0, MAX_PER_RUN - _used)


def provider_cfg(provider: str = None) -> dict:
    """解析 provider 配置：注册表条目 + 环境变量单项覆盖。"""
    name = (provider or PROVIDER).strip()
    cfg = dict(PROVIDERS.get(name) or PROVIDERS["zimage_turbo"])
    if os.environ.get("IMAGE_GEN_MODEL"):
        cfg["model"] = os.environ["IMAGE_GEN_MODEL"].strip()
    if os.environ.get("IMAGE_GEN_SIZE"):
        cfg["size"] = os.environ["IMAGE_GEN_SIZE"].strip()
    try:
        if os.environ.get("IMAGE_GEN_STEPS"):
            cfg["steps"] = int(os.environ["IMAGE_GEN_STEPS"])
        if os.environ.get("IMAGE_GEN_GUIDANCE"):
            cfg["guidance"] = float(os.environ["IMAGE_GEN_GUIDANCE"])
    except ValueError:
        log.warning("bad IMAGE_GEN_STEPS/GUIDANCE env, using provider defaults")
    cfg["provider"] = name if name in PROVIDERS else "zimage_turbo"
    return cfg


def build_prompt(brief) -> str:
    """装配生成 prompt：视觉隐喻 + 风格后缀 + 色板 + 负面约束。

    brief 可以是：
      dict  {metaphor, style, palette, headline?, highlight?}（后端视觉导演产出）
      str   旧式英文 query（端点不可用时的降级路径，套默认风格）

    叠字层开启且 brief 带 headline 时追加构图指令：底图左侧留暗色平静区域
    供文字排版（两阶段合成：字由 text_overlay 程序绘制，不由模型画）。
    """
    if isinstance(brief, str):
        brief = {"metaphor": brief, "style": DEFAULT_STYLE, "palette": DEFAULT_PALETTE}
    metaphor = (brief.get("metaphor") or "").strip() or \
        "a glowing neural network of connected light nodes above abstract data streams"
    style = (brief.get("style") or "").strip()
    suffix = STYLE_PRESETS.get(style) or STYLE_PRESETS[DEFAULT_STYLE]
    palette = (brief.get("palette") or "").strip() or DEFAULT_PALETTE
    composition = ""
    try:
        import text_overlay
        if text_overlay.enabled() and (brief.get("headline") or "").strip():
            composition = (
                " Composition: main subject weighted toward the right side, "
                "left half kept dark, calm and relatively empty for a headline "
                "text overlay."
            )
    except Exception:  # noqa: BLE001
        pass
    return (
        f"{metaphor[:400]}. {suffix}. "
        f"Color mood: {palette[:120]}.{composition} {_NEGATIVE}"
    )


def _submit(prompt: str, cfg: dict) -> str:
    """提交异步生图任务，返回 task_id（失败 ""）。"""
    h = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    try:
        r = httpx.post(
            f"{BASE}/v1/images/generations",
            json={
                "model": cfg["model"],
                "prompt": prompt,
                "size": cfg["size"],
                "num_inference_steps": cfg["steps"],
                "guidance_scale": cfg["guidance"],
            },
            headers={**h, "X-ModelScope-Async-Mode": "true"},
            timeout=60,
        )
        if r.status_code != 200:
            log.warning("image-gen[%s] submit HTTP %s: %s",
                        cfg["provider"], r.status_code, r.text[:160])
            return ""
        task_id = (r.json() or {}).get("task_id")
        if not task_id:
            log.warning("image-gen[%s] submit no task_id: %s",
                        cfg["provider"], r.text[:160])
            return ""
        return task_id
    except Exception as ex:  # noqa: BLE001
        log.warning("image-gen[%s] submit failed: %s", cfg["provider"], ex)
        return ""


def _poll(task_id: str, cfg: dict) -> str:
    """轮询任务至 SUCCEED，返回 MS 临时图 URL（失败 ""）。"""
    h = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
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
                log.info("image-gen[%s] ok in %.0fs", cfg["provider"], time.time() - t0)
                return url
            log.warning("image-gen SUCCEED but empty output_images")
            return ""
        if st == "FAILED":
            log.warning("image-gen task FAILED: %s", str(d)[:200])
            return ""
    log.warning("image-gen timeout after %ds", POLL_TIMEOUT)
    return ""


def _download(url: str) -> bytes:
    try:
        r = httpx.get(url, timeout=60, follow_redirects=True)
        if r.status_code == 200 and r.content and len(r.content) > 10_000:
            return r.content
        log.warning("image-gen download bad: HTTP %s size=%d",
                    r.status_code, len(r.content or b""))
    except Exception as ex:  # noqa: BLE001
        log.warning("image-gen download failed: %s", ex)
    return b""


def _generate(brief, provider: str = None):
    """生成 + 下载 + 统一后处理，返回 (字节, MS临时URL)（失败 (b"", "")）。

    提交成功即计额（失败的任务也烧 API 调用）。
    ms_url 一并返回：R2 直传失败时调用方可回退到调用方镜像路径（v1 行为）。
    """
    global _used
    if not enabled() or remaining() <= 0:
        return b"", ""
    cfg = provider_cfg(provider)
    prompt = build_prompt(brief)
    task_id = _submit(prompt, cfg)
    if not task_id:
        return b"", ""
    _used += 1
    ms_url = _poll(task_id, cfg)
    if not ms_url:
        return b"", ""
    raw = _download(ms_url)
    if not raw:
        return b"", ""
    try:
        import postprocess
        out = postprocess.cover_finish(raw)
        # 后处理内部失败会原样回退（可能是 PNG 原字节），调用方按魔数定格式
    except Exception as ex:  # noqa: BLE001
        log.warning("postprocess import/run failed, keep raw: %s", ex)
        out = raw
    # 第二阶段：程序化叠字（两阶段合成；brief 带 headline 时）
    if isinstance(brief, dict) and (brief.get("headline") or "").strip():
        try:
            import text_overlay
            out = text_overlay.apply_headline(
                out, brief["headline"], brief.get("highlight") or [])
        except Exception as ex:  # noqa: BLE001
            log.warning("text overlay failed, keep base image: %s", ex)
    return out, ms_url


def generate_image(brief, provider: str = None) -> bytes:
    """生成 + 后处理，返回图片字节（失败 b""）。供 eval_covers.py 横评落盘用。"""
    data, _ = _generate(brief, provider=provider)
    return data


def generate_cover(brief, article_url: str = "", provider: str = None) -> str:
    """全流程：生成 → 后处理 → 直传 R2（.jpg），返回最终 URL（失败 ""）。

    article_url 提供时用确定性 R2 key（sha1(article_url)，与 image_host 同
    规则）——重生成同 key 原地覆盖，URL 不变，DB 无需更新。
    R2 不可用/上传失败时：回退返回 MS 临时 URL，调用方走 need{} 旧路径
    由 image_host.upload_images 镜像（行为与 v1 一致，不浪费已烧的配额）。
    """
    cfg = provider_cfg(provider)
    data, ms_url = _generate(brief, provider=cfg["provider"])
    if not data:
        return ""

    is_jpeg = data[:3] == b"\xff\xd8\xff"
    ext = ".jpg" if is_jpeg else ".png"
    try:
        import image_host
        if article_url and image_host.r2_enabled():
            key = image_host._rel_path(article_url, ext)  # 同包复用确定性分片规则
            ct = "image/jpeg" if is_jpeg else "image/png"
            if image_host.upload_object(key, data, ct):
                url = f"{image_host.R2_PUBLIC_BASE}/{key}"
                log.info("image-gen[%s] -> R2 %s (%dKB)",
                         cfg["provider"], key, len(data) // 1024)
                return url
            log.warning("image-gen R2 upload failed, fall back to caller mirror path")
    except Exception as ex:  # noqa: BLE001
        log.warning("image-gen R2 direct upload error: %s", ex)

    return ms_url  # 调用方镜像（v1 兼容路径）
