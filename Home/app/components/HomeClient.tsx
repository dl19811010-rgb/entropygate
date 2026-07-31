"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { fetchArticles, fetchArticleCount, formatTimeAgo } from "../lib/data";
import { Article } from "../types";
import { NewsGrid } from "./NewsGrid";

// 分类标签配色（对应 .eg-t-* 类）
const TAG_CLASS: Record<string, string> = {
  "大语言模型": "eg-t-ai",
  "智能体": "eg-t-model",
  "硬件": "eg-t-chip",
  "政策": "eg-t-policy",
  "研究": "eg-t-ai",
  "产品": "eg-t-product",
};
function tagClass(label: string): string {
  return TAG_CLASS[label] || "eg-t-ai";
}

// 把文章分类标签映射成展示标签（最多 2 个）
function articleTags(a: Article): string[] {
  if (a.tags && a.tags.length) return a.tags.slice(0, 2);
  if (a.categoryLabel) return [a.categoryLabel];
  return ["AI 情报"];
}

export function HomeClient() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [count, setCount] = useState<number>(0);
  const [activeCat, setActiveCat] = useState("all");
  const [subEmail, setSubEmail] = useState("");
  const [subOk, setSubOk] = useState(false);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    fetchArticles(1, 21)
      .then((list) => {
        if (!alive) return;
        setArticles(list);
        setError(null);
      })
      .catch(() => {
        if (!alive) return;
        setError("内容加载失败，请稍后刷新");
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    fetchArticleCount().then((c) => alive && setCount(c));
    return () => {
      alive = false;
    };
  }, []);

  const filtered = useMemo(() => {
    if (activeCat === "all") return articles;
    return articles.filter((a) => a.categorySlug === activeCat);
  }, [articles, activeCat]);

  // 精选：带封面或首篇 featured，否则取第一篇
  const featured = useMemo<Article | undefined>(() => {
    const f = articles.find((a) => a.featured && a.imageUrl);
    return f || articles.find((a) => a.featured) || articles[0];
  }, [articles]);

  // 主列表（去掉精选那篇）
  const feed = useMemo(
    () => (featured ? filtered.filter((a) => a.id !== featured.id) : filtered),
    [filtered, featured]
  );

  // 侧栏热门：前 5 篇
  const hot = useMemo(() => articles.slice(0, 5), [articles]);

  // 常用标签云（从 tags 聚合）
  const tagCloud = useMemo(() => {
    const freq: Record<string, number> = {};
    articles.forEach((a) => {
      (a.tags || []).forEach((t) => {
        freq[t] = (freq[t] || 0) + 1;
      });
    });
    return Object.entries(freq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([t]) => t);
  }, [articles]);

  const today = new Date().toISOString().slice(0, 10).replace(/-/g, ".");

  return (
    <div className="eg-page">
      {/* Hero + 实时情报 */}
      <section className="eg-hero">
        <div className="eg-hero-grid">
          <div>
            <div className="eg-badge">
              <span className="eg-pulse" />
              实时更新中
            </div>
            <h1>
              AI <span className="grad">情报快讯</span>
            </h1>
            <p className="eg-hero-desc">
              由 EntropyGate 编辑智能筛选，每日为你呈现最具影响力的 AI 情报与科技动态
            </p>
            <div className="eg-stats">
              <div>
                <div className="eg-stat-num">{loading ? "—" : count || articles.length}</div>
                <div className="eg-stat-label">已收录</div>
              </div>
              <div>
                <div className="eg-stat-num">{articles.length ? "每日" : "—"}</div>
                <div className="eg-stat-label">更新频率</div>
              </div>
              <div>
                <div className="eg-stat-num">实时</div>
                <div className="eg-stat-label">策展改写</div>
              </div>
            </div>
          </div>

          {/* 实时情报 ticker：取最新 4 篇 */}
          <div className="eg-ticker">
            <div className="eg-ticker-h">
              <span>实时情报</span>
              <time>{today}</time>
            </div>
            {loading ? (
              <div className="eg-tk-item">
                <div className="eg-tk-dot b" />
                <div className="eg-tk-txt" style={{ color: "var(--eg-text-3)" }}>
                  正在加载最新情报…
                </div>
              </div>
            ) : (
              articles.slice(0, 4).map((a, i) => {
                const dots = ["b", "g", "o", "b"];
                return (
                  <Link
                    key={a.id}
                    href={a.href || `/article?id=${a.id}`}
                    className="eg-tk-item"
                    style={{ textDecoration: "none" }}
                  >
                    <div className={`eg-tk-dot ${dots[i % dots.length]}`} />
                    <div>
                      <div className="eg-tk-txt">{a.title}</div>
                      <div className="eg-tk-meta">
                        <span>{a.categoryLabel || "AI 情报"}</span>
                        <span>{formatTimeAgo(a.publishedAt)}</span>
                      </div>
                    </div>
                  </Link>
                );
              })
            )}
          </div>
        </div>
      </section>

      {/* 分类条 */}
      <div className="eg-cat-bar">
        <div className="eg-cat-scroll">
          {[
            { slug: "all", label: "全部" },
            { slug: "llm", label: "大语言模型" },
            { slug: "agent", label: "智能体" },
            { slug: "hardware", label: "硬件" },
            { slug: "policy", label: "政策" },
            { slug: "research", label: "研究" },
            { slug: "product", label: "产品" },
          ].map((c) => (
            <button
              key={c.slug}
              className={`eg-cat-btn ${activeCat === c.slug ? "on" : ""}`}
              onClick={() => setActiveCat(c.slug)}
            >
              {c.label}
            </button>
          ))}
        </div>
      </div>

      {/* 主内容 */}
      <div className="eg-main">
        <div className="feed">
          <div className="eg-feed-h">
            <h2>最新情报</h2>
          </div>

          {error ? (
            <div className="eg-card" style={{ textAlign: "center" }}>
              <p style={{ color: "var(--eg-text-2)" }}>{error}</p>
              <button
                onClick={() => window.location.reload()}
                style={{
                  marginTop: 8,
                  color: "var(--eg-accent)",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                重新加载
              </button>
            </div>
          ) : (
            <>
              {/* 精选大卡 */}
              {featured && (
                <Link
                  href={featured.href || `/article?id=${featured.id}`}
                  className="eg-feat"
                  style={{ textDecoration: "none" }}
                >
                  <div className="eg-feat-img">
                    {featured.imageUrl ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={featured.imageUrl}
                        alt={featured.title}
                        loading="lazy"
                        onError={(e) => {
                          (e.currentTarget as HTMLImageElement).style.display = "none";
                        }}
                      />
                    ) : (
                      <div className="eg-feat-img-inner">
                        <div className="big">🤖</div>
                        <p>featured / {today}</p>
                      </div>
                    )}
                  </div>
                  <div className="eg-feat-body">
                    <div className="eg-feat-badge">★ 编辑精选</div>
                    <h3>{featured.title}</h3>
                    <p>{featured.description}</p>
                    <div className="eg-feat-meta">
                      <span>{featured.readTime}</span>
                      {Number(featured.viewCount) > 0 && (
                        <span>{Number(featured.viewCount).toLocaleString()} views</span>
                      )}
                    </div>
                  </div>
                </Link>
              )}

              {/* 文章卡列表：首页只保留 5 篇重要内容（带封面图） */}
              <NewsGrid articles={feed.slice(0, 5)} />

              {/* 查看更多 */}
              {!loading && feed.length > 5 && (
                <div className="eg-more-wrap">
                  <Link href="/category?slug=all" className="eg-more">
                    查看全部快讯 →
                  </Link>
                </div>
              )}

              {!loading && feed.length === 0 && (
                <div className="eg-card" style={{ textAlign: "center", color: "var(--eg-text-3)" }}>
                  该分类暂无内容
                </div>
              )}

              {loading && (
                <div className="eg-card" style={{ textAlign: "center", color: "var(--eg-text-3)" }}>
                  加载中…
                </div>
              )}
            </>
          )}
        </div>

        {/* 侧边栏 */}
        <aside className="eg-side">
          <div className="eg-sc">
            <h4>热门话题</h4>
            {hot.map((a, i) => (
              <Link
                key={a.id}
                href={a.href || `/article?id=${a.id}`}
                className="eg-hot"
                style={{ textDecoration: "none" }}
              >
                <span className={`eg-rn ${i < 3 ? "top" : "mid"}`}>{i + 1}</span>
                <span className="eg-ht">{a.title}</span>
                <span className="eg-hn">{Number(a.viewCount) > 0 ? Number(a.viewCount).toLocaleString() : "—"}</span>
              </Link>
            ))}
            {!hot.length && (
              <div className="eg-hot" style={{ color: "var(--eg-text-3)" }}>
                暂无数据
              </div>
            )}
          </div>

          <div className="eg-sc">
            <h4>情报分类</h4>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {[
                { slug: "llm", label: "大语言模型" },
                { slug: "agent", label: "智能体" },
                { slug: "hardware", label: "硬件" },
                { slug: "policy", label: "政策" },
                { slug: "research", label: "研究" },
                { slug: "product", label: "产品" },
              ].map((c) => (
                <Link
                  key={c.slug}
                  href={`/category?slug=${c.slug}`}
                  style={{
                    padding: "6px 12px",
                    borderRadius: 999,
                    fontSize: 13,
                    fontWeight: 500,
                    background: "rgba(99,102,241,0.08)",
                    color: "var(--eg-accent)",
                    textDecoration: "none",
                    border: "1px solid rgba(99,102,241,0.18)",
                  }}
                >
                  {c.label}
                </Link>
              ))}
            </div>
          </div>

          <div className="eg-sc">
            <h4>常用标签</h4>
            {tagCloud.length > 0 ? (
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {tagCloud.map((t) => (
                  <Link
                    key={t}
                    href={`/search?q=${encodeURIComponent(t)}`}
                    style={{
                      padding: "5px 10px",
                      borderRadius: 8,
                      fontSize: 13,
                      background: "var(--eg-surface)",
                      color: "var(--eg-text-2)",
                      textDecoration: "none",
                      border: "1px solid var(--eg-border)",
                    }}
                  >
                    {t}
                  </Link>
                ))}
              </div>
            ) : (
              <p style={{ color: "var(--eg-text-3)", fontSize: 13 }}>加载中…</p>
            )}
          </div>

          <div className="eg-sc eg-sub">
            <h4>订阅快讯</h4>
            <p>每日精选 AI 情报，直接送达邮箱。无广告，随时退订。</p>
            <div className="eg-sub-inp">
              <input
                type="email"
                placeholder="your@email.com"
                value={subEmail}
                onChange={(e) => setSubEmail(e.target.value)}
              />
              <button
                onClick={() => {
                  if (subEmail.includes("@")) setSubOk(true);
                }}
              >
                订阅
              </button>
            </div>
            {subOk && <div className="eg-sub-ok">✓ 已订阅，感谢关注！</div>}
          </div>

          <div className="eg-sc eg-about">
            <h4>关于 EntropyGate</h4>
            <p>
              由 AI 从业者与科技编辑共同维护，致力于为全球中文读者提供精准、及时的 AI
              行业情报。自动采集、策展与改写。
            </p>
          </div>
        </aside>
      </div>
    </div>
  );
}
