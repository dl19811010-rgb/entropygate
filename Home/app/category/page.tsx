"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Eye, Clock, TrendingUp, Hash, Mail, Newspaper, ChevronLeft, ChevronRight, WifiOff } from "lucide-react";
import {
  CATEGORIES,
  fetchAllArticles,
  formatTimeAgo,
  formatFullDate,
} from "../lib/data";
import { sourceStyle } from "../lib/sourceStyle";
import { Article } from "../types";

type SortKey = "earliest" | "newest" | "hot";

const PER_PAGE = 8;

function fmtViews(n: number): string {
  if (!n) return "0";
  return n >= 10000 ? (n / 10000).toFixed(1) + "万" : String(n);
}

function timeValue(a: Article): number {
  const t = new Date(a.publishedAt).getTime();
  return isNaN(t) ? 0 : t;
}

function CategoryInner() {
  const router = useRouter();
  const params = useSearchParams();
  const initialSlug = params.get("slug") || "all";

  const [all, setAll] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [cat, setCat] = useState(initialSlug);
  const [sort, setSort] = useState<SortKey>("newest");
  const [page, setPage] = useState(1);
  const [email, setEmail] = useState("");
  const [emailSent, setEmailSent] = useState(false);

  // 载入全部文章（一次拉取，后续分类/排序/分页全在前端完成）
  const [retryTick, setRetryTick] = useState(0);
  const loadArticles = () => {
    let alive = true;
    setLoading(true);
    setError(null);
    fetchAllArticles()
      .then((list) => { if (alive) { setAll(list); setError(null); } })
      .catch((e) => { if (alive) setError(e instanceof Error ? e : new Error(String(e))); })
      .finally(() => { if (alive) setLoading(false); });
    return () => { alive = false; };
  };
  useEffect(() => { return loadArticles(); }, [retryTick]);

  // URL slug 变化时同步筛选
  useEffect(() => {
    setCat(initialSlug);
    setPage(1);
  }, [initialSlug]);

  const info = CATEGORIES.find((c) => c.slug === cat) || { slug: "all", label: "全部" };

  // 分类筛选 + 排序
  const filtered = useMemo(() => {
    let data = cat === "all" ? all : all.filter((a) => a.categorySlug === cat);
    data = data.slice();
    if (sort === "hot") {
      data.sort((a, b) => (b.viewCount || 0) - (a.viewCount || 0));
    } else if (sort === "newest") {
      data.sort((a, b) => timeValue(b) - timeValue(a));
    } else {
      // earliest：更新越早的越靠前（本页的特色）
      data.sort((a, b) => timeValue(a) - timeValue(b));
    }
    return data;
  }, [all, cat, sort]);

  const total = filtered.length;
  const totalPages = Math.max(1, Math.ceil(total / PER_PAGE));
  const curPage = Math.min(page, totalPages);
  const pageData = filtered.slice((curPage - 1) * PER_PAGE, curPage * PER_PAGE);

  // 侧栏：最新 AI 日报（按阅读量取前 8）
  const ranks = useMemo(
    () => all.slice().sort((a, b) => (b.viewCount || 0) - (a.viewCount || 0)).slice(0, 8),
    [all]
  );

  // 侧栏：热门标签（跨文章标签词频）
  const hotTags = useMemo(() => {
    const freq = new Map<string, number>();
    all.forEach((a) => (a.tags || []).forEach((t) => {
      const k = t.trim();
      if (k) freq.set(k, (freq.get(k) || 0) + 1);
    }));
    return Array.from(freq.entries())
      .sort((x, y) => y[1] - x[1])
      .slice(0, 9);
  }, [all]);

  const changeCat = (slug: string) => {
    setCat(slug);
    setPage(1);
    // 同步 URL slug，保证刷新/分享/浏览器前进后退都能还原当前分类
    router.replace(slug === "all" ? "/category?slug=all" : `/category?slug=${slug}`, {
      scroll: false,
    });
  };

  // 分页窗口化：页数多时用 … 省略，避免平铺一长排页码
  const pageItems = useMemo<(number | "…")[]>(() => {
    if (totalPages <= 7) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }
    const out: (number | "…")[] = [1];
    if (curPage > 3) out.push("…");
    const s = Math.max(2, curPage - 1);
    const e = Math.min(totalPages - 1, curPage + 1);
    for (let i = s; i <= e; i++) out.push(i);
    if (curPage < totalPages - 2) out.push("…");
    out.push(totalPages);
    return out;
  }, [totalPages, curPage]);

  const onSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
    if (!ok) return;
    setEmailSent(true);
    // 暂无独立订阅后端，跳转到注册页完成订阅绑定
    setTimeout(() => router.push(`/register?email=${encodeURIComponent(email.trim())}`), 400);
  };

  return (
    <div className="max-w-[1400px] mx-auto px-6 pt-[92px] pb-16 grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_360px] gap-8">
      {/* ============ 主内容区 ============ */}
      <main className="min-w-0">
        {/* 标题 */}
        <div className="flex items-baseline justify-between gap-3 mb-5">
          <h1 className="text-[28px] leading-tight font-bold tracking-tight text-text-primary">
            {info.label}快讯
          </h1>
        </div>

        {/* 工具栏：分类筛选 + 排序 */}
        <div className="flex items-center justify-between gap-3 flex-wrap mb-5 p-4 bg-surface border border-border-light rounded-xl">
          <div className="flex items-center gap-1.5 flex-wrap">
            {CATEGORIES.map((c) => (
              <button
                key={c.slug}
                onClick={() => changeCat(c.slug)}
                className={`h-8 px-3.5 rounded-full text-xs font-medium border transition-colors ${
                  cat === c.slug
                    ? "bg-accent-light text-accent border-accent/25"
                    : "bg-transparent text-text-secondary border-border-light hover:text-text-primary hover:bg-surface-hover"
                }`}
              >
                {c.label}
              </button>
            ))}
          </div>
          <div className="flex items-center gap-2 text-xs text-text-secondary">
            <span className="hidden sm:inline">排序</span>
            <select
              value={sort}
              onChange={(e) => {
                setSort(e.target.value as SortKey);
                setPage(1);
              }}
              className="h-8 px-2.5 rounded-md border border-border-light bg-surface-hover text-text-primary text-xs outline-none focus:border-accent transition-colors"
            >
              <option value="newest">最新更新</option>
              <option value="hot">最热阅读</option>
              <option value="earliest">最早更新</option>
            </select>
          </div>
        </div>

        {/* 列表 */}
        {error ? (
          <div className="text-center py-20 bg-surface border border-border-light rounded-2xl">
            <WifiOff size={40} strokeWidth={1.5} className="mx-auto mb-3 text-text-tertiary" />
            <p className="text-base font-semibold text-text-secondary mb-1">加载失败</p>
            <p className="text-sm text-text-tertiary mb-4">{error.message || "无法加载快讯，请检查网络后重试"}</p>
            <button
              onClick={() => setRetryTick((t) => t + 1)}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-accent text-white rounded-xl text-sm font-medium transition-all duration-200 hover:bg-accent-hover"
            >
              重新加载
            </button>
          </div>
        ) : loading ? (
          <div className="flex flex-col gap-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="flex h-[180px] bg-surface border border-border-light rounded-2xl overflow-hidden">
                <div className="shrink-0 w-[280px] h-full skeleton" />
                <div className="flex-1 flex flex-col gap-3 p-4">
                  <div className="h-3 w-1/3 rounded skeleton" />
                  <div className="h-5 w-4/5 rounded skeleton" />
                  <div className="h-4 w-full rounded skeleton" />
                  <div className="h-4 w-2/3 rounded skeleton" />
                </div>
              </div>
            ))}
          </div>
        ) : pageData.length === 0 ? (
          <div className="text-center py-20 bg-surface border border-border-light rounded-2xl">
            <p className="text-base font-semibold text-text-secondary">该分类暂无快讯</p>
            <p className="text-sm text-text-tertiary mt-1">换个分类看看吧</p>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            {pageData.map((a) => {
              const st = sourceStyle(a.source);
              const img = (a.imageUrl || "").trim();
              const initial = (a.source || "AI").trim().charAt(0).toUpperCase();
              return (
                <Link
                  key={a.id}
                  href={a.href || `/article?id=${a.id}`}
                  className="group relative flex flex-col sm:flex-row sm:h-[180px] bg-surface rounded-2xl border border-border-light overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:border-border"
                >
                  {/* 悬浮左色条（对齐首页 .eg-card 质感） */}
                  <span
                    className="absolute top-0 left-0 w-[3px] h-full bg-transparent transition-colors duration-300 group-hover:bg-gradient-to-b group-hover:from-[var(--eg-accent)] group-hover:to-[var(--eg-purple)] z-10"
                    aria-hidden
                  />
                  {/* 左侧缩略图：与主页 NewsCard 同规格——280px 贴边、与卡同高；移动端上图下文 */}
                  <div className="relative w-full sm:w-[280px] sm:shrink-0 aspect-[16/9] sm:aspect-auto sm:h-full overflow-hidden bg-[var(--eg-accent-glow)]">
                    {img ? (
                      <img
                        src={img}
                        alt={a.title}
                        loading="lazy"
                        className="w-full h-full object-cover bg-black group-hover:scale-[1.05] transition-transform duration-500"
                        onError={(e) => {
                          const el = e.currentTarget;
                          const box = el.parentElement;
                          if (box) {
                            el.remove();
                            const ph = document.createElement("div");
                            ph.className =
                              "w-full h-full flex items-center justify-center text-2xl font-bold text-white";
                            ph.style.background = st.color;
                            ph.textContent = initial;
                            box.appendChild(ph);
                          }
                        }}
                      />
                    ) : (
                      <div
                        className="w-full h-full flex items-center justify-center text-2xl font-bold text-white"
                        style={{ background: st.color }}
                      >
                        {initial}
                      </div>
                    )}
                  </div>

                  {/* 右侧文字区（垂直节奏对齐主页 NewsCard；160px 卡高给 2 行标题+2 行摘要留足行距） */}
                  <div className="px-4 py-3 flex flex-col flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1 text-xs font-medium text-text-tertiary flex-wrap">
                      <span
                        className="px-2 py-0.5 rounded-md text-[11px] font-semibold shrink-0"
                        style={{ color: st.color, background: `${st.color}14` }}
                      >
                        {a.category}
                      </span>
                      <span className="truncate">{formatTimeAgo(a.publishedAt) || formatFullDate(a.publishedAt)}</span>
                      {a.breaking && (
                        <span className="px-1.5 py-0.5 rounded text-[11px] font-semibold bg-[#fdecec] text-[#d84545] shrink-0">
                          头条
                        </span>
                      )}
                    </div>
                    <h3 className="text-[15.5px] sm:text-[16px] font-bold leading-[1.4] mb-1 line-clamp-2 text-text-primary group-hover:text-accent transition-colors">
                      {a.title}
                    </h3>
                    <p className="text-[13px] leading-relaxed text-text-secondary line-clamp-2 flex-1">
                      {a.description}
                    </p>
                    <div className="flex items-center gap-3 pt-1.5 mt-auto text-xs text-text-tertiary">
                      <span className="flex items-center gap-1">
                        <Eye size={14} /> {fmtViews(a.viewCount || 0)}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock size={14} /> {a.readTime}
                      </span>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        )}

        {/* 底部：总数 + 分页（计数挪到这里，顶部不再重复，2026-07-26 用户反馈） */}
        {!loading && total > 0 && (
          <div className="flex items-center justify-between gap-3 mt-6 p-3 bg-surface border border-border-light rounded-lg">
            <span className="text-[13px] text-text-tertiary font-medium whitespace-nowrap pl-1">
              共 {total} 条{totalPages > 1 ? ` · 第 ${curPage}/${totalPages} 页` : ""}
            </span>
            {totalPages > 1 && (
              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={curPage <= 1}
                  className="min-w-8 h-8 px-1.5 rounded-md border border-border-light bg-surface text-text-secondary flex items-center justify-center transition-colors hover:bg-surface-hover disabled:opacity-40 disabled:cursor-not-allowed"
                  aria-label="上一页"
                >
                  <ChevronLeft size={16} />
                </button>
                {pageItems.map((n, i) =>
                  n === "…" ? (
                    <span
                      key={`gap-${i}`}
                      className="min-w-8 h-8 flex items-center justify-center text-text-tertiary select-none"
                    >
                      …
                    </span>
                  ) : (
                    <button
                      key={n}
                      onClick={() => setPage(n)}
                      aria-current={n === curPage ? "page" : undefined}
                      className={`min-w-8 h-8 rounded-md border text-[13px] font-medium flex items-center justify-center transition-colors ${
                        n === curPage
                          ? "bg-[var(--eg-accent)] text-white border-transparent"
                          : "bg-surface text-text-secondary border-border-light hover:bg-surface-hover"
                      }`}
                    >
                      {n}
                    </button>
                  )
                )}
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={curPage >= totalPages}
                  className="min-w-8 h-8 px-1.5 rounded-md border border-border-light bg-surface text-text-secondary flex items-center justify-center transition-colors hover:bg-surface-hover disabled:opacity-40 disabled:cursor-not-allowed"
                  aria-label="下一页"
                >
                  <ChevronRight size={16} />
                </button>
              </div>
            )}
          </div>
        )}
      </main>

      {/* ============ 右侧栏 ============ */}
      <aside className="flex flex-col gap-5 lg:sticky lg:top-[92px] h-fit">
        {/* 最新 AI 日报 */}
        <div className="bg-surface border border-border-light rounded-2xl p-5">
          <h2 className="flex items-center gap-2 text-[15px] font-semibold text-text-primary mb-4">
            <Newspaper size={18} className="text-accent" /> 热门 AI 日报
          </h2>
          <div className="flex flex-col gap-3">
            {(loading ? Array.from({ length: 6 }) : ranks).map((item, i) => {
              const a = item as Article | undefined;
              return (
                <Link
                  key={a ? a.id : i}
                  href={a ? a.href || `/article?id=${a.id}` : "#"}
                  className="group flex gap-3 items-start -m-1.5 p-1.5 rounded-lg transition-colors hover:bg-surface-hover"
                >
                  <span
                    className={`w-6 h-6 rounded-md text-xs font-bold flex items-center justify-center shrink-0 mt-0.5 ${
                      i < 3 ? "bg-accent-light text-accent" : "bg-surface-hover text-text-tertiary"
                    }`}
                  >
                    {i + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    {a ? (
                      <>
                        <div className="text-[13px] font-medium leading-snug text-text-primary line-clamp-2 group-hover:text-accent transition-colors">
                          {a.title}
                        </div>
                        <div className="text-[11px] text-text-tertiary mt-1">
                          {fmtViews(a.viewCount || 0)} 阅读
                        </div>
                      </>
                    ) : (
                      <div className="h-8 rounded skeleton" />
                    )}
                  </div>
                </Link>
              );
            })}
          </div>
        </div>

        {/* 热门标签 */}
        {hotTags.length > 0 && (
          <div className="bg-surface border border-border-light rounded-2xl p-5">
            <h2 className="flex items-center gap-2 text-[15px] font-semibold text-text-primary mb-4">
              <Hash size={18} className="text-accent" /> 热门标签
            </h2>
            <div className="flex flex-wrap gap-2">
              {hotTags.map(([t, c]) => (
                <Link
                  key={t}
                  href={`/search?q=${encodeURIComponent(t)}`}
                  className="h-7 px-3 rounded-full border border-border-light bg-surface-hover text-text-secondary text-xs flex items-center transition-colors hover:border-accent hover:text-accent"
                >
                  {t}
                  <span className="ml-1 opacity-60">{c}</span>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* 订阅 AI 日报 */}
        <div className="bg-surface border border-border-light rounded-2xl p-5">
          <h2 className="flex items-center gap-2 text-[15px] font-semibold text-text-primary mb-3">
            <Mail size={18} className="text-accent" /> 订阅 AI 日报
          </h2>
          <p className="text-[13px] text-text-secondary mb-3">
            每天早上 8 点，获取最新 AI 快讯摘要。
          </p>
          <form onSubmit={onSubscribe} className="flex flex-col gap-2.5">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="输入邮箱地址"
              className="w-full h-10 px-3 rounded-md border border-border-light bg-surface-hover text-text-primary text-[13px] outline-none transition-colors focus:border-accent"
            />
            <button
              type="submit"
              disabled={emailSent}
              className="w-full h-10 rounded-md bg-accent text-white text-sm font-medium flex items-center justify-center gap-1.5 transition-colors hover:bg-accent-hover disabled:opacity-60"
            >
              {emailSent ? "正在跳转…" : "立即订阅"}
            </button>
          </form>
        </div>
      </aside>
    </div>
  );
}

export default function CategoryPage() {
  return (
    <Suspense
      fallback={<div className="pt-[120px] text-center text-text-tertiary">加载中…</div>}
    >
      <CategoryInner />
    </Suspense>
  );
}
