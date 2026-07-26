# -*- coding: utf-8 -*-
"""封面文字排版层（两阶段合成第二阶段：AI 底图 + 程序化叠字）。

为什么存在（用户 2026-07-25 参考 5 张 YouTube 封面定方向）：
参考封面的"大字"从来不是图像模型画的——AI 直出文字必鬼画符（尤其中文）。
行业标准是**底图生成 + 后期排版**：字由程序绘制，永远正确、清晰、可控。
本模块就是那个排版引擎。

视觉规范（对标参考图）：
  - 超粗黑体：Noto Sans CJK SC Black（开源免费，运行时 CDN 下载缓存）
  - 撞色：主标题纯白 + highlight 词亮黄（YouTube 封面经典白/黄）
  - 深色粗描边：保证任何底图上的可读性
  - 左上安全区布局，文字区宽 58%（右侧留给底图视觉主体）
  - 换行 = DP 最小参差（balanced wrap）：拉丁词/highlight 词原子不拆，
    空格为首选断行点，多行宽度尽量均衡（不出现"长行+单字吊尾"）
  - 自适应暗纱：文字区底图过亮时自动垫一层半透明暗色圆角块

环境变量：
  COVER_TEXT_OVERLAY     0 关闭（退回纯 AI 底图），默认 1
  COVER_HEADLINE_COLOR   主标题色，默认 #FFFFFF
  COVER_HIGHLIGHT_COLOR  高亮色，默认 #FFD60A
  COVER_FONT_URL         自定义字体 URL（默认 jsdelivr 的 Noto Black）

任何一步失败都回退原图字节——叠字是增强，绝不能让生成链路翻车。
"""
import io
import logging
import os
import re

log = logging.getLogger("text_overlay")

_ENABLED = os.environ.get("COVER_TEXT_OVERLAY", "0") == "1"
_HEADLINE_COLOR = os.environ.get("COVER_HEADLINE_COLOR", "#FFFFFF")
_HIGHLIGHT_COLOR = os.environ.get("COVER_HIGHLIGHT_COLOR", "#FFD60A")
_STROKE_COLOR = "#0A0C14"

_FONT_URLS = [
    os.environ.get("COVER_FONT_URL", "").strip() or None,
    "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/"
    "SimplifiedChinese/NotoSansCJKsc-Black.otf",
    "https://fastly.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/"
    "SimplifiedChinese/NotoSansCJKsc-Black.otf",
    "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/"
    "SimplifiedChinese/NotoSansCJKsc-Black.otf",
]
_FONT_CACHE = os.path.join(
    os.environ.get("FONT_CACHE_DIR",
                   os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                ".font-cache")),
    "NotoSansCJKsc-Black.otf",
)

# 布局常量（1664x928 画布）
_MARGIN_X = 64
_MARGIN_Y = 56
_ZONE_RATIO = 0.58       # 文字区最大宽度占比
_SIZE_START = 156
_SIZE_MIN = 84
_SIZE_STEP = 10
_LINE_SPACING = 1.18
_MAX_LINES = 3
_SCRIM_LUMA = 125        # 文字区平均亮度超过此值则垫暗纱（中灰以上就垫）
_SCRIM_ALPHA = 118

_font_path_cache = None


def enabled() -> bool:
    return _ENABLED


def _ensure_font() -> str:
    """返回本地字体路径；没有就从镜像链下载（带缓存）。失败返回 ""。"""
    global _font_path_cache
    if _font_path_cache:
        return _font_path_cache
    if os.path.exists(_FONT_CACHE) and os.path.getsize(_FONT_CACHE) > 1_000_000:
        _font_path_cache = _FONT_CACHE
        return _font_path_cache
    os.makedirs(os.path.dirname(_FONT_CACHE), exist_ok=True)
    import httpx
    for url in [u for u in _FONT_URLS if u]:
        try:
            r = httpx.get(url, timeout=120, follow_redirects=True)
            if r.status_code == 200 and len(r.content) > 1_000_000:
                with open(_FONT_CACHE, "wb") as f:
                    f.write(r.content)
                _font_path_cache = _FONT_CACHE
                log.info("font cached from %s (%dMB)", url.split("/")[2],
                         len(r.content) // 1048576)
                return _font_path_cache
        except Exception as ex:  # noqa: BLE001
            log.warning("font download failed %s: %s", url.split("/")[2], ex)
    log.warning("no headline font available; overlay disabled for this run")
    return ""


# ── 单元化（拉丁词/highlight 原子，空格为断行提示）───────────────────────────
_ASCII_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9\-+./]*")


def _tokenize(headline: str, highlight):
    """切排版单元 [(text, is_highlight, is_break_hint)]。

    - highlight 词整体成为一个原子单元（绝不拆行、整体高亮）
    - 拉丁词/数字整体不拆
    - 空格成为零宽断行提示（不绘制，仅 DP 首选断点）
    - 其余 CJK/符号逐字
    """
    hl_words = sorted([w for w in (highlight or []) if w and w in headline],
                      key=len, reverse=True)
    units = []
    i = 0
    while i < len(headline):
        ch = headline[i]
        if ch.isspace():
            units.append(("", False, True))
            i += 1
            continue
        matched = None
        for w in hl_words:
            if headline.startswith(w, i):
                matched = w
                break
        if matched:
            units.append((matched, True, False))
            i += len(matched)
            continue
        m = _ASCII_WORD.match(headline, i)
        if m:
            units.append((m.group(0), False, False))
            i = m.end()
        else:
            units.append((ch, False, False))
            i += 1
    return [u for u in units if u[0] or u[2]]


def _line_width(line, font) -> float:
    return sum(font.getlength(u[0]) for u in line if u[0])


def _wrap_dp(units, font, max_w: int):
    """DP 最小参差换行：断点只取「断行提示处」或「任意单元边界」，
    代价 = 每行 (max_w - 行宽)^2 之和；超宽行代价无穷大。
    返回 [ [unit, ...], ... ]（≤_MAX_LINES 行）。"""
    n = len(units)
    # 前缀宽
    widths = [0.0] * (n + 1)
    for i, (t, _, _) in enumerate(units):
        widths[i + 1] = widths[i] + (font.getlength(t) if t else 0.0)

    def seg_w(i, j):  # units[i:j] 的宽度
        return widths[j] - widths[i]

    INF = float("inf")
    # dp[i] = (cost, breaks) 处理 units[i:] 的最优解
    dp = [None] * (n + 1)
    dp[n] = (0.0, [])
    for i in range(n - 1, -1, -1):
        best = (INF, None)
        for j in range(i + 1, n + 1):
            lines_used = 1 + (len(dp[j][1]) if dp[j][1] is not None else 99)
            if lines_used > _MAX_LINES:
                break
            w = seg_w(i, j)
            if w > max_w and j > i + 1:
                break  # 此行已超宽，再长无意义
            line_cost = (max_w - min(w, max_w)) ** 2
            # 非断行提示处断行加强惩罚：LLM 给的空格断点（语义边界）必须
            # 压过纯宽度均衡，否则 CJK 会从词中间断开（"助|理"式败笔）
            if j < n and not units[j - 1][2] and units[j][0]:
                line_cost += (max_w * 0.25) ** 2
            rest = dp[j]
            if rest[1] is None:
                continue
            total = line_cost + rest[0]
            if total < best[0]:
                best = (total, [j] + rest[1])
        dp[i] = best
    if dp[0][1] is None:  # 理论不可达（单单元行总放得下降级字号后）
        return [units]
    breaks = dp[0][1]
    lines, prev = [], 0
    for b in breaks:
        lines.append([u for u in units[prev:b] if u[0]])
        prev = b
    return [l for l in lines if l]


def apply_headline(img_bytes: bytes, headline: str, highlight=None) -> bytes:
    """底图字节 + 中文短标题 → 叠字后的 JPEG 字节。失败回退原字节。"""
    if not _ENABLED or not headline or not headline.strip():
        return img_bytes
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception as ex:  # noqa: BLE001
        log.warning("Pillow unavailable, skip overlay: %s", ex)
        return img_bytes
    font_path = _ensure_font()
    if not font_path:
        return img_bytes
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        W, H = img.size
        max_w = int(W * _ZONE_RATIO) - _MARGIN_X

        headline = headline.strip()
        units = _tokenize(headline, highlight or [])
        if not any(u[0] for u in units):
            return img_bytes

        # 自动缩字号：DP 换行后总行数与最宽行都放得下即采纳
        chosen = None
        for size in range(_SIZE_START, _SIZE_MIN - 1, -_SIZE_STEP):
            font = ImageFont.truetype(font_path, size)
            lines = _wrap_dp(units, font, max_w)
            if lines and max(_line_width(l, font) for l in lines) <= max_w:
                chosen = (font, lines, size)
                break
        if chosen is None:
            font = ImageFont.truetype(font_path, _SIZE_MIN)
            chosen = (font, _wrap_dp(units, font, max_w), _SIZE_MIN)
        font, lines, size = chosen
        stroke = max(5, size // 16)
        line_h = int(size * _LINE_SPACING)

        # 自适应暗纱：文字块区域平均亮度过高时垫一层半透明暗色圆角块
        text_block_w = max(_line_width(l, font) for l in lines)
        text_block_h = line_h * len(lines)
        zone = img.crop((_MARGIN_X - 24, _MARGIN_Y - 20,
                         min(W, _MARGIN_X + int(text_block_w) + 28),
                         min(H, _MARGIN_Y + text_block_h + 20)))
        luma = zone.resize((1, 1)).getpixel((0, 0))
        brightness = 0.299 * luma[0] + 0.587 * luma[1] + 0.114 * luma[2]
        if brightness > _SCRIM_LUMA:
            scrim = Image.new("RGBA", img.size, (0, 0, 0, 0))
            sd = ImageDraw.Draw(scrim)
            sd.rounded_rectangle(
                [_MARGIN_X - 28, _MARGIN_Y - 24,
                 min(W, _MARGIN_X + int(text_block_w) + 32),
                 min(H, _MARGIN_Y + text_block_h + 24)],
                radius=28, fill=(8, 10, 18, _SCRIM_ALPHA))
            img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")

        draw = ImageDraw.Draw(img)
        y = _MARGIN_Y
        for line in lines:
            x = _MARGIN_X
            for text, is_hl, _ in line:
                color = _HIGHLIGHT_COLOR if is_hl else _HEADLINE_COLOR
                draw.text((x, y), text, font=font, fill=color,
                          stroke_width=stroke, stroke_fill=_STROKE_COLOR)
                x += font.getlength(text)
            y += line_h

        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=88, optimize=True, progressive=True)
        log.info("overlay: %d chars, %d lines @%dpx%s -> %dKB",
                 len(headline), len(lines), size,
                 " +scrim" if brightness > _SCRIM_LUMA else "",
                 buf.tell() // 1024)
        return buf.getvalue()
    except Exception as ex:  # noqa: BLE001
        log.warning("overlay failed, keep original: %s", ex)
        return img_bytes
