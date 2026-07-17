// EntropyGate AI — public reader (vanilla JS, no build step).
// API base: same-origin /api/v1 (Cloudflare Pages Function proxies to Studio),
// or window.API_BASE override for custom-domain / direct deployments.
const API = (window.API_BASE && window.API_BASE.replace(/\/+$/, "")) || "/api/v1";

async function apiGet(path) {
  const resp = await fetch(API + path, { headers: { Accept: "application/json" } });
  if (!resp.ok) throw new Error("HTTP " + resp.status);
  const json = await resp.json();
  return json.data || {};
}

function esc(s) {
  if (s == null) return "";
  return String(s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
function fmtDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return "";
  return d.toLocaleString("zh-CN", { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}
function readingTime(text) {
  const n = (text || "").length;
  return Math.max(1, Math.round(n / 320));
}
function highlight(text, q) {
  const safe = esc(text);
  if (!q) return safe;
  const idx = safe.toLowerCase().indexOf(q.toLowerCase());
  if (idx < 0) return safe;
  return safe.slice(0, idx) + "<mark class='hl'>" + safe.slice(idx, idx + q.length) + "</mark>" + safe.slice(idx + q.length);
}

const BUCKET_LABEL = {
  essential: "头条必读", authoritative: "权威发布", credible: "可信源",
  signal: "信号", peripheral: "边缘",
};
const BUCKETS = [
  { key: "", label: "全部" },
  { key: "essential", label: "头条必读" },
  { key: "authoritative", label: "权威发布" },
  { key: "credible", label: "可信源" },
  { key: "signal", label: "信号" },
  { key: "peripheral", label: "边缘" },
];
function sourceName(a) {
  if (a.source && a.source.name) return a.source.name;
  return a.source_name || "未知来源";
}
function thumbUrl(a) { return a.thumbnail_url || a.image_url || ""; }
function bucketClass(a) {
  const b = a.editorial_bucket;
  return (b && ["essential","authoritative","credible","signal","peripheral"].includes(b)) ? "b-" + b : "b-credible";
}
function initial(a) {
  const s = (sourceName(a) || a.title || "?").trim();
  return s.charAt(0).toUpperCase();
}

/* ---------- Card (grid) ---------- */
function cardHtml(a, q) {
  const badges = [];
  if (a.is_breaking) badges.push("突发");
  else if (a.is_featured) badges.push("精选");
  const tags = (a.tags || []).slice(0, 3).map(t => `<span class="tag">${esc(t.name || t)}</span>`).join("");
  const summary = a.ai_summary || a.summary || a.excerpt || "";
  const thumb = thumbUrl(a);
  const media = thumb
    ? `<div class="media"><div class="ph ${bucketClass(a)}">${initial(a)}</div>` +
      `<img src="${esc(thumb)}" alt="" loading="lazy" onerror="this.remove()"></div>`
    : `<div class="media"><div class="ph ${bucketClass(a)}">${initial(a)}</div></div>`;
  const floatBadge = badges.length
    ? `<span class="badge-float">${badges[0]}</span>` : "";
  const rt = a.content ? ` · ${readingTime(a.content)} 分钟阅读` : "";
  const orig = a.url
    ? `<a class="orig" href="${esc(a.url)}" target="_blank" rel="noopener" onclick="event.stopPropagation()">查看原文 ↗</a>` : "";
  return `<article class="card">
    <a class="card-link" href="/article.html?id=${a.id}">
      ${media}
      ${floatBadge}
      <div class="body">
        <h3>${highlight(a.title, q)}</h3>
        ${summary ? `<p class="summary">${highlight(summary, q)}</p>` : ""}
        <div class="meta">
          <span class="src">${esc(sourceName(a))}</span><span class="dot-sep">·</span>
          <span>${esc(fmtDate(a.published_at || a.created_at))}</span>${rt}
        </div>
        ${tags ? `<div class="tags">${tags}</div>` : ""}
        <div style="margin-top:10px">${orig}</div>
      </div>
    </a>
  </article>`;
}

function skeletonGrid(n) {
  let s = "";
  for (let i = 0; i < n; i++) {
    s += `<div class="sk-card"><div class="media" style="aspect-ratio:16/9"></div>` +
         `<div class="body"><div class="sk-line w90"></div><div class="sk-line w70"></div>` +
         `<div class="sk-line w50"></div></div></div>`;
  }
  return s;
}

function renderFeedGrid(container, articles, q) {
  if (!articles || articles.length === 0) {
    container.innerHTML = `<div class="empty-guide">
      <div class="eg-icon">📡</div>
      <h3>暂时没有内容</h3>
      <p>采集系统正在抓取与整理最新的 AI 资讯，通常几分钟内就会有新内容上线。你可以稍后再来，或先看看其它栏目。</p>
      <a class="btn" href="/">返回首页</a>
    </div>`;
    return;
  }
  container.innerHTML = articles.map(a => cardHtml(a, q)).join("");
}
function showError(container, msg) {
  container.innerHTML = `<div class="error">加载失败：${esc(msg)}</div>`;
}

/* ---------- Hero / Featured ---------- */
function heroHtml(a) {
  const thumb = thumbUrl(a);
  const media = thumb
    ? `<div class="ph ${bucketClass(a)}">${initial(a)}</div><img class="bg" src="${esc(thumb)}" alt="" onerror="this.remove()">`
    : `<div class="ph ${bucketClass(a)}">${initial(a)}</div>`;
  const summary = a.ai_summary || a.summary || "";
  return `<a class="lead" href="/article.html?id=${a.id}">
    ${media}
    <div class="inner">
      <span class="kicker">★ 今日精选</span>
      <h2>${esc(a.title)}</h2>
      ${summary ? `<p class="summary">${esc(summary)}</p>` : ""}
      <span class="meta"><span>${esc(sourceName(a))}</span><span>·</span>
      <span>${esc(fmtDate(a.published_at || a.created_at))}</span></span>
    </div>
  </a>`;
}
function sideItemHtml(a, rank) {
  return `<a class="side-item" href="/article.html?id=${a.id}">
    <span class="rank">${rank}</span>
    <div class="si-body">
      <p class="si-title">${esc(a.title)}</p>
      <div class="si-meta">${esc(sourceName(a))} · ${esc(fmtDate(a.published_at || a.created_at))}</div>
    </div>
  </a>`;
}
async function loadFeatured(el) {
  try {
    const [featured, breaking] = await Promise.all([
      apiGet("/homepage/featured?fields=light"),
      apiGet("/homepage/breaking?fields=light"),
    ]);
    let f = Array.isArray(featured) ? featured : (featured.items || []);
    let b = Array.isArray(breaking) ? breaking : (breaking.items || []);
    if (!f.length && !b.length) {
      // Fallback: top stories by editorial score so the hero is never empty
      const data = await apiGet("/homepage/stories?page=1&page_size=5&fields=light");
      const items = data.items || [];
      if (!items.length) { el.style.display = "none"; return; }
      f = items.slice(0, 1);
      b = items.slice(1, 5);
    }
    const lead = f[0];
    const side = (b.length ? b : f.slice(1)).slice(0, 4);
    el.innerHTML = (lead ? heroHtml(lead) : "") +
      `<div class="hero-side"><div class="side-title">🔥 实时动态</div>${side.map((a, i) => sideItemHtml(a, i + 1)).join("")}</div>`;
    el.style.display = "grid";
  } catch (e) { el.style.display = "none"; }
}

function renderChips(el, active, onPick) {
  el.innerHTML = BUCKETS.map(b =>
    `<button class="chip ${b.key === active ? "active" : ""}" data-key="${b.key}">${b.label}</button>`).join("");
  el.querySelectorAll(".chip").forEach(btn => {
    btn.addEventListener("click", () => onPick(btn.dataset.key));
  });
}

/* ---------- Header search (shared) ---------- */
function bindSearch() {
  const form = document.querySelector(".search-form");
  if (!form) return;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = form.querySelector("input").value.trim();
    if (q) location.href = "/search.html?q=" + encodeURIComponent(q);
  });
}
function getParam(name) { return new URLSearchParams(location.search).get(name); }

/* ---------- Page initializers ---------- */
function initHome() {
  const feed = document.getElementById("feed");
  const featured = document.getElementById("featured");
  const chips = document.getElementById("chips");
  const prevBtn = document.getElementById("prev");
  const nextBtn = document.getElementById("next");
  const pageNo = document.getElementById("page-no");
  const PAGE_SIZE = 12;
  const state = { page: 1, bucket: "", totalPages: 1 };

  function load() {
    feed.innerHTML = skeletonGrid(6);
    prevBtn.disabled = true; nextBtn.disabled = true;
    const qs = `/homepage/stories?page=${state.page}&page_size=${PAGE_SIZE}` +
      (state.bucket ? `&bucket=${encodeURIComponent(state.bucket)}` : "") + "&fields=light";
    apiGet(qs).then(data => {
      const items = data.items || [];
      renderFeedGrid(feed, items, "");
      state.totalPages = data.total_pages || 1;
      prevBtn.disabled = state.page <= 1;
      nextBtn.disabled = state.page >= state.totalPages;
      if (pageNo) pageNo.textContent = `第 ${state.page} / ${state.totalPages} 页`;
      window.scrollTo({ top: 0, behavior: "smooth" });
    }).catch(e => showError(feed, e.message));
  }
  function pickBucket(key) {
    state.bucket = key; state.page = 1;
    renderChips(chips, state.bucket, pickBucket);
    load();
  }
  renderChips(chips, state.bucket, pickBucket);
  loadFeatured(featured);
  load();
  prevBtn.addEventListener("click", () => { if (state.page > 1) { state.page--; load(); } });
  nextBtn.addEventListener("click", () => { if (state.page < state.totalPages) { state.page++; load(); } });
}

function initSearch() {
  const feed = document.getElementById("feed");
  const sub = document.getElementById("sub");
  const prevBtn = document.getElementById("prev");
  const nextBtn = document.getElementById("next");
  const pageNo = document.getElementById("page-no");
  const q = (getParam("q") || "").trim();
  const input = document.querySelector(".search-form input");
  if (input) input.value = q;
  const PAGE_SIZE = 12;
  let page = 1, totalPages = 1;

  function load() {
    feed.innerHTML = skeletonGrid(6);
    prevBtn.disabled = true; nextBtn.disabled = true;
    if (!q) { feed.innerHTML = `<div class="empty-guide">
      <div class="eg-icon">🔍</div><h3>请输入搜索关键词</h3>
      <p>在上方搜索框中输入公司、技术或话题，即可检索 AI 资讯库。</p>
      <a class="btn" href="/">返回首页</a></div>`; return; }
    apiGet(`/search?q=${encodeURIComponent(q)}&page=${page}&page_size=${PAGE_SIZE}`).then(data => {
      const items = data.items || [];
      const total = data.total || 0;
      if (sub) sub.textContent = `“${q}” — 共 ${total} 条结果`;
      if (!items.length) {
        feed.innerHTML = `<div class="empty-guide">
          <div class="eg-icon">🔍</div><h3>没有找到与“${esc(q)}”相关的内容</h3>
          <p>换个关键词试试，或浏览<a href="/" style="color:var(--brand)">今日情报首页</a>。也可以检查拼写，或查看其它栏目。</p>
          <a class="btn" href="/">浏览首页</a></div>`;
        return;
      }
      renderFeedGrid(feed, items, q);
      totalPages = data.total_pages || 1;
      prevBtn.disabled = page <= 1;
      nextBtn.disabled = page >= totalPages;
      if (pageNo) pageNo.textContent = `第 ${page} / ${totalPages} 页`;
    }).catch(e => showError(feed, e.message));
  }
  load();
  prevBtn.addEventListener("click", () => { if (page > 1) { page--; load(); window.scrollTo({ top: 0, behavior: "smooth" }); } });
  nextBtn.addEventListener("click", () => { if (page < totalPages) { page++; load(); window.scrollTo({ top: 0, behavior: "smooth" }); } });
}

function initArticle() {
  const content = document.getElementById("content");
  const id = getParam("id");
  if (!id) { content.innerHTML = `<div class="error">缺少文章 ID</div>`; return; }
  content.innerHTML = `<div class="article-wrap"><div class="empty">加载中…</div></div>`;
  apiGet(`/articles/${id}`).then(a => {
    const src = (a.source && a.source.name) ? a.source.name : (a.source_name || "未知来源");
    const badges = [];
    if (a.is_breaking) badges.push('<span class="badge breaking">突发</span>');
    if (a.is_featured) badges.push('<span class="badge featured">精选</span>');
    const tags = (a.tags || []).map(t => `<span class="tag">${esc(t.name || t)}</span>`).join(" ");
    const thumb = thumbUrl(a);
    const hero = thumb
      ? `<img class="hero-img" src="${esc(thumb)}" alt="" onerror="this.outerHTML='<div class=\\'hero-ph ${bucketClass(a)}\\'>${initial(a)}</div>'">`
      : `<div class="hero-ph ${bucketClass(a)}">${initial(a)}</div>`;
    const aiSum = a.ai_summary
      ? `<div class="ai-summary"><span class="lbl">AI 摘要</span>${esc(a.ai_summary)}</div>` : "";
    const body = a.content || a.summary || "（无正文）";
    const orig = a.url ? `<a class="orig" href="${esc(a.url)}" target="_blank" rel="noopener">查看原文 ↗</a>` : "";
    document.title = `${esc(a.title)} · EntropyGate AI`;
    content.innerHTML = `<div class="article-wrap">
      <a class="back" href="/">← 返回首页</a>
      <article class="article">
        ${hero}
        <div class="pad">
          <h1>${esc(a.title)}</h1>
          <div class="meta">
            <span class="src">${esc(src)}</span><span>·</span>
            <span>${esc(fmtDate(a.published_at || a.created_at))}</span>
            ${badges.join(" ")}
          </div>
          ${aiSum}
          <div class="body">${esc(body)}</div>
          ${tags ? `<div class="tags" style="margin-top:22px">${tags}</div>` : ""}
          ${orig}
        </div>
      </article>
    </div>`;
  }).catch(e => {
    content.innerHTML = `<div class="article-wrap"><div class="error">加载失败：${esc(e.message)}</div></div>`;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  bindSearch();
  if (document.getElementById("featured")) initHome();
  else if (document.getElementById("sub")) initSearch();
  else if (document.getElementById("content")) initArticle();
});
