# -*- coding: utf-8 -*-
"""AI 封面统一后处理（Supabase12 杠杆 3：治"塑料感/AI 味"）。

只做 AI 生成图——官方原图/截图不动（那是真实世界质感，不需要"落地"）。
三件事：
  1. 轻微胶片颗粒（高斯噪声，强度很低，肉眼仅觉"不那么塑料"）
  2. 轻暗角（径向渐晕，把注意力收向画面中心）
  3. 统一冷调（压 R 提 B 几个点，整站色调一致）

顺带把 1.6MB PNG 转 ~250KB JPEG（quality=86）：列表页流量直接打一折。
纯 Pillow 实现，无 numpy 依赖（GitHub runner pip install Pillow 即可）。
"""
import io
import logging
import os
import random

log = logging.getLogger("postprocess")

_ENABLED = os.environ.get("COVER_POSTPROCESS", "1") == "1"
_JPEG_QUALITY = int(os.environ.get("COVER_JPEG_QUALITY", "86"))
_GRAIN = float(os.environ.get("COVER_GRAIN_STRENGTH", "6"))      # 0-255 噪声幅度
_VIGNETTE = float(os.environ.get("COVER_VIGNETTE_STRENGTH", "0.18"))  # 边缘压暗比例
_COOL_R = float(os.environ.get("COVER_COOL_R", "0.97"))          # R 通道乘子
_COOL_B = float(os.environ.get("COVER_COOL_B", "1.04"))          # B 通道乘子


def enabled() -> bool:
    return _ENABLED


def cover_finish(png_bytes: bytes) -> bytes:
    """PNG/JPEG 字节 → 后处理后的 JPEG 字节。任何一步失败都回退原字节。"""
    if not _ENABLED:
        return png_bytes
    try:
        from PIL import Image, ImageEnhance, ImageFilter  # noqa: WPS433
    except Exception as ex:  # noqa: BLE001
        log.warning("Pillow unavailable, skip postprocess: %s", ex)
        return png_bytes
    try:
        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        w, h = img.size

        # ① 冷调：R 微压、B 微提（点操作 LUT，快）
        lut = [min(255, int(i * _COOL_R)) for i in range(256)]
        lut += [i for i in range(256)]
        lut += [min(255, int(i * _COOL_B)) for i in range(256)]
        img = img.point(lut)

        # ② 胶片颗粒：叠加一层低强度高斯噪声（Image.effect_noise 出 L 图）
        if _GRAIN > 0:
            noise = Image.effect_noise((w, h), _GRAIN * 4).point(
                lambda i: int((i - 128) * (_GRAIN / 32.0) + 128)
            )
            img = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.06)

        # ③ 暗角：径向渐变 mask，边缘向黑收
        if _VIGNETTE > 0:
            mask = Image.new("L", (w, h), 0)
            # 用椭圆渐变：中心 255（保留）→ 边缘 0（压暗）
            grad = Image.radial_gradient("L").resize((max(w, h) * 2, max(w, h) * 2))
            grad = grad.crop(((grad.width - w) // 2, (grad.height - h) // 2,
                              (grad.width - w) // 2 + w, (grad.height - h) // 2 + h))
            # radial_gradient 中心 0 边缘 255，反转让中心亮
            mask = grad.point(lambda i: 255 - i)
            black = Image.new("RGB", (w, h), (8, 10, 18))
            img = Image.composite(img, black, mask.point(
                lambda i: 255 - int((255 - i) * _VIGNETTE)))

        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=_JPEG_QUALITY, optimize=True, progressive=True)
        out = buf.getvalue()
        log.info("postprocess: %dKB -> %dKB (grain=%.0f vig=%.2f)",
                 len(png_bytes) // 1024, len(out) // 1024, _GRAIN, _VIGNETTE)
        return out
    except Exception as ex:  # noqa: BLE001
        log.warning("postprocess failed, keep original: %s", ex)
        return png_bytes
