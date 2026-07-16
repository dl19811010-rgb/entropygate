// EntropyGate AI — public reader (vanilla JS, no build step).
// API 基地址：默认同源 /api/v1；分离部署时由 /config.js 注入 window.API_BASE
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
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function fmtDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return "";
  return d.toLocaleString("zh-CN", { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

function readingTime(text) {
  const n = (text || "").length;
  return Math.max(1, Math.round(n / 300));
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

function thumbUrl(a) {
  return a.thumbnail_url || a.image_url || "";
}

function cardHtml(a, q) {
  const badges = [];
  if (a.is_breaking) badges.push('<span class="badge breaking">突发</span>');
  if (a.is_featured) badges.push('<span class="badge featured">精选</span>');
  if (a.editorial_bucket && BUCKET_LABEL[a.editorial_bucket])
    badges.push(`<span class="badge">${BUCKET_LABEL[a.editorial_bucket]}</span>`);

  const tags = (a.tags || []).slice(0, 5)
    .map((t) => `<span class="tag">${esc(t.name || t)}</span>`).join("");

  const summary = a.ai_summary || a.summary || a.excerpt || "";
  const thumb = thumbUrl(a);
  const rt = a.content ? ` · ${readingTime(a.content)} 分钟阅读` : "";
  const orig = a.url
    ? `<a class="orig" href="${esc(a.url)}" target="_blank" rel="noopener">查看原文 ↗</a>`
    : "";

  const inner = `
    <h2><a href="/article.html?id=${a.id}">${highlight(a.title, q)}</a></h2>
    <div class="meta">
      <span>${esc(sourceName(a))}</span>
      <span>·</span>
      <span>${esc(fmtDate(a.published_at || a.created_at))}</span>
      ${rt}
      ${badges.join(" ")}
    </div>
    ${summary ? `<p class="summary">${highlight(summary, q)}</p>` : ""}
    ${tags ? `<div class="tags">${tags}</div>` : ""}
    <div style="margin-top:10px">${orig}</div>`;

  if (thumb) {
    return `<article class="card with-thumb">
      <img class="thumb" src="${esc(thumb)}" alt="" onerror="this.style.display='none'" />
      <div class="body">${inner}</div>
    </article>`;
  }
  return `<article class="card">${inner}</article>`;
}

function renderFeed(container, articles, q) {
  if (!articles || articles.length === 0) {
    container.innerHTML = `<div class="empty-guide">
      <div class="eg-icon">📡</div>
      <h3>暂时没有内容</h3>
      <p>采集系统正在抓取与整理最新的 AI 资讯，通常几分钟内就会有新内容上线。你可以稍后再来，或先看看其它栏目。</p>
      <a class="btn" href="/">返回首页</a>
    </div>`;
    return;
  }
  container.innerHTML = articles.map((a) => cardHtml(a, q)).join("");
}

function showError(container, msg) {
  container.innerHTML = `<div class="error">加载失败：${esc(msg)}</div>`;
}

// Featured / breaking strip
function leadHtml(a) {
  return `<a class="lead" href="/article.html?id=${a.id}">
    <span class="kicker">★ 今日精选</span>
    <h2>${esc(a.title)}</h2>
    <span class="meta">${esc(sourceName(a))} · ${esc(fmtDate(a.published_at || a.created_at))}</span>
  </a>`;
}

function sideHtml(list) {
  return list.map((a) => `<div class="item">
    <span class="tag">突发</span>
    <a href="/article.html?id=${a.id}">${esc(a.title)}</a>
    <div class="src">${esc(sourceName(a))}</div>
  </div>`).join("");
}

async function loadFeatured(el) {
  try {
    const [featured, breaking] = await Promise.all([
      apiGet("/homepage/featured?fields=light"),
      apiGet("/homepage/breaking?fields=light"),
    ]);
    const f = (featured.items || featured) || [];
    const b = (breaking.items || breaking) || [];
    if (!f.length && !b.length) { el.style.display = "none"; return; }
    const lead = f[0];
    const side = (b.length ? b : f.slice(1)).slice(0, 4);
    el.innerHTML = (lead ? leadHtml(lead) : "") + `<div class="side">${sideHtml(side)}</div>`;
    el.style.display = "grid";
  } catch (e) {
    el.style.display = "none";
  }
}

function renderChips(el, active, onPick) {
  el.innerHTML = BUCKETS.map(
    (b) => `<button class="chip ${b.key === active ? "active" : ""}" data-key="${b.key}">${b.label}</button>`
  ).join("");
  el.querySelectorAll(".chip").forEach((btn) => {
    btn.addEventListener("click", () => onPick(btn.dataset.key));
  });
}

// Header search (shared across pages)
function bindSearch() {
  const form = document.querySelector(".search-form");
  if (!form) return;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = form.querySelector("input").value.trim();
    if (q) location.href = "/search.html?q=" + encodeURIComponent(q);
  });
}

function getParam(name) {
  return new URLSearchParams(location.search).get(name);
}
