import { Article, CategoryInfo, SearchResult, User } from "../types";

// ========== API 基础地址 ==========
// 走同域 Cloudflare Pages 函数代理 /api/*（functions/api/[[route]].js -> entropygate.cc.cd/api/*）。
// 同源请求无浏览器 CORS 预检问题，可安全携带自定义头（X-Access-Token 等）；代理再服务端转发到后端。
// 优先用注入的 window.API_BASE，否则用 Next 注入的环境变量，最后回退到同域 /api/v1。
export const API_BASE: string =
  (typeof window !== "undefined" && (window as unknown as { API_BASE?: string }).API_BASE) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "/api/v1";

// ========== 分类（前端派生，用于筛选芯片） ==========
export const CATEGORIES: { slug: string; label: string }[] = [
  { slug: "all", label: "全部" },
  { slug: "llm", label: "大语言模型" },
  { slug: "agent", label: "智能体" },
  { slug: "hardware", label: "硬件" },
  { slug: "policy", label: "政策" },
  { slug: "research", label: "研究" },
  { slug: "product", label: "产品" },
];

// 后端未维护 category 字段，这里按来源派生分类，让筛选芯片可用
const SOURCE_CATEGORY: Record<string, string> = {
  "OpenAI Blog": "llm",
  OpenAI: "llm",
  Anthropic: "agent",
  "Google AI": "research",
  DeepMind: "research",
  Google: "research",
  "Meta AI": "llm",
  Meta: "llm",
  "Hugging Face": "llm",
  HF: "llm",
  NVIDIA: "hardware",
  "EU Commission": "policy",
  Apple: "product",
  Cursor: "product",
  "The Batch": "research",
  // 国内源分类映射（让筛选芯片对国内新闻生效）
  "量子位 (QbitAI)": "llm",
  "量子位": "llm",
  "智东西 (Zhidx)": "product",
  "智东西": "product",
  "InfoQ 中文": "research",
  InfoQ: "research",
  "36氪 (36Kr)": "product",
  "36氪": "product",
  "机器之心 (Jiqizhixin)": "research",
  "机器之心": "research",
  "AI Frontline": "llm",
  Kimi: "llm",
};

function deriveCategory(sourceName?: string): { slug: string; label: string } {
  const slug = (sourceName && SOURCE_CATEGORY[sourceName]) || "";
  if (!slug) return { slug: "", label: sourceName || "科技" };
  const c = CATEGORIES.find((x) => x.slug === slug);
  return { slug, label: c ? c.label : sourceName || "科技" };
}

function stripHtml(html?: string): string {
  if (!html) return "";
  return html
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function readTime(content?: string): string {
  const text = stripHtml(content || "");
  const mins = Math.max(1, Math.round(text.length / 350));
  return `${mins} 分钟阅读`;
}

// 后端内容多为纯文本（\n\n 分段）。若直接塞进 HTML 会变成一堵文字墙。
// 这里把纯文本转成带 <p> / <h2> / <h3> / <ul> 的结构，供 Tailwind prose 渲染。
function formatContentHtml(raw: string): string {
  if (!raw) return "";
  // 已有常见 HTML 块级标签则不再二次处理，避免破坏后端生成的 HTML
  if (/<(p|h[1-6]|div|ul|ol|blockquote|pre|table)[\s>]/i.test(raw)) {
    return raw;
  }

  // Markdown 标题
  let html = raw
    .replace(/^### (.*)$/gim, "<h3>$1</h3>")
    .replace(/^## (.*)$/gim, "<h2>$1</h2>")
    .replace(/^# (.*)$/gim, "<h1>$1</h1>");

  // 按空行分段
  return html
    .split(/\n\s*\n/)
    .map((block) => {
      const trimmed = block.trim();
      if (!trimmed) return "";
      if (trimmed.startsWith("<h")) return trimmed;
      // 段内单换行转 <br/>
      const inner = trimmed.replace(/\n/g, "<br/>");
      return `<p>${inner}</p>`;
    })
    .filter(Boolean)
    .join("\n");
}

// ========== 后端原始文章 → 前端 Article ==========
export function mapArticle(raw: Record<string, unknown>): Article {
  const id = String(raw.id);
  const title = (raw.rewritten_title as string) || (raw.title as string) || "";
  // 结构化快讯优先：flash_meta 是二次创作后的权威内容（content 列曾被误写入 flash_meta JSON，必须过滤）
  let flashMeta: Record<string, unknown> | undefined;
  if (raw.flash_meta) {
    try {
      const parsed =
        typeof raw.flash_meta === "string"
          ? JSON.parse(raw.flash_meta as string)
          : raw.flash_meta;
      if (parsed && typeof parsed === "object") {
        flashMeta = parsed as Record<string, unknown>;
      }
    } catch {
      flashMeta = undefined;
    }
  }
  const fmSections = flashMeta && Array.isArray(flashMeta.sections)
    ? (flashMeta.sections as { title: string; content: string }[])
    : [];
  const fmSummary = flashMeta && flashMeta.flash_summary ? String(flashMeta.flash_summary) : "";

  // FlashSpec（C+ 组件化快讯规格）：article 页优先走 flash-theme 渲染
  let flashSpec: Record<string, unknown> | undefined;
  if (raw.flash_spec) {
    try {
      const parsed =
        typeof raw.flash_spec === "string"
          ? JSON.parse(raw.flash_spec as string)
          : raw.flash_spec;
      if (parsed && typeof parsed === "object" && Array.isArray((parsed as any).blocks)) {
        flashSpec = parsed as Record<string, unknown>;
      }
    } catch {
      flashSpec = undefined;
    }
  }

  // 旧 content 列可能被误写入 flash_meta JSON，做安全过滤
  const rawContent =
    (raw.rewritten_content as string) ||
    (raw.content as string) ||
    (raw.preview as string) || "";
  const safeContent = rawContent.trim().startsWith("{") ? "" : rawContent;
  const structuredBody = fmSections.length
    ? fmSections.map((s) => `## ${s.title}\n\n${s.content}`).join("\n\n")
    : "";
  const formattedContent = structuredBody
    ? formatContentHtml(structuredBody)
    : formatContentHtml(safeContent);

  const summaryRaw = raw.summary as string | undefined;
  const aiSummaryRaw = raw.ai_summary as string | undefined;
  // 卡片描述优先级：kimi 导语(ai_summary) → 结构化快讯摘要 → 首段正文 → 旧 summary → 旧 content（已过滤 JSON）
  const description =
    (aiSummaryRaw ? stripHtml(aiSummaryRaw) : "") ||
    (fmSummary ? stripHtml(fmSummary) : "") ||
    (fmSections.length ? stripHtml(String(fmSections[0].content || "")) : "") ||
    (summaryRaw ? stripHtml(summaryRaw) : "") ||
    stripHtml(safeContent).slice(0, 140);
  const { slug: categorySlug, label: categoryLabel } = deriveCategory(
    raw.source_name as string | undefined
  );
  const publishedAt = (raw.published_at as string) || (raw.created_at as string) || "";
  const imageUrl =
    ((raw.image_url as string) || (raw.thumbnail_url as string) || "").trim() || "";
  const breaking = Number(raw.is_breaking) > 0;
  const featured = Number(raw.is_featured) > 0 || breaking;
  const tagsRaw = Array.isArray(raw.tags) && raw.tags.length ? (raw.tags as string[]) : [];
  const keywordsRaw = Array.isArray(raw.ai_keywords) ? (raw.ai_keywords as string[]) : [];
  const tags = tagsRaw.length ? tagsRaw : keywordsRaw;
  const sourceName = (raw.source_name as string) || "未知来源";

  return {
    id,
    slug: (raw.slug as string) || id,
    title,
    description,
    content: formattedContent,
    category: categoryLabel,
    categoryLabel,
    categorySlug,
    tags,
    source: sourceName,
    sourceIcon: sourceName.charAt(0).toUpperCase(),
    readTime: readTime(safeContent),
    publishedAt,
    imageUrl,
    featured,
    breaking,
    viewCount: Number(raw.view_count) || 0,
    flashMeta,
    flashSpec,
    // Kimi-K3 自包含 HTML 快讯页（新引擎产物，article 页最优先渲染）
    kimiHtml: typeof raw.kimi_html === "string" && raw.kimi_html.length > 1000
      ? (raw.kimi_html as string)
      : undefined,
    href: `/article?id=${id}`,
  };
}

// ========== 底层请求 ==========
// 自定义 API 错误类——携带 HTTP 状态码，让调用方能做差异化处理（如 429 限流、401 过期等）
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public path: string = ""
  ) {
    super(message);
    this.name = "ApiError";
  }
}

// 默认超时 15 秒（公开列表接口通常 <3s；搜索/文章详情可能稍长）
const FETCH_TIMEOUT_MS = 15_000;

async function apiGet(path: string, headers?: Record<string, string>): Promise<{ data: unknown }> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      headers: { Accept: "application/json", ...(headers || {}) },
      signal: controller.signal,
    });
    if (!res.ok) throw new ApiError(res.status, `API ${res.status} @ ${path}`, path);
    return (await res.json()) as { data: unknown };
  } finally {
    clearTimeout(timer);
  }
}

// 公开列表/搜索走轻量序列化（fields=light）。
// 重要：必须用“查询参数”而非自定义请求头（如 X-Fields）。
// 原因——浏览器发送自定义头会触发 CORS 预检(OPTIONS)，而上游网关(Studio/Cloudflare)
// 的 access-control-allow-headers 固定白名单不含 X-Fields，会拦截预检，导致前端拿不到数据、
// 文章列表整片空白。查询参数不触发预检，且真实用户访问无 CDN 挑战。admin 端不发该参数，仍取全文。
function extractItems(payload: unknown): Record<string, unknown>[] {
  if (Array.isArray(payload)) return payload as Record<string, unknown>[];
  const data = payload as { items?: unknown; list?: unknown };
  if (Array.isArray(data.items)) return data.items as Record<string, unknown>[];
  if (Array.isArray(data.list)) return data.list as Record<string, unknown>[];
  return [];
}

// ========== 对外数据接口 ==========
export async function fetchArticles(page = 1, pageSize = 21): Promise<Article[]> {
  try {
    const json = await apiGet(`/articles?page=${page}&page_size=${pageSize}&fields=light&status=approved,published`);
    return extractItems(json.data).map(mapArticle);
  } catch (e) {
    // ApiError（含 429/5xx 等）或网络错误统一向上抛，让页面层决定展示策略
    throw e;
  }
}

// 全量拉取（快讯页客户端筛选/排序/分页用）：先取第1页获取总数，再并行取剩余页，上限 1000 篇。
// 优化：串行10页耗时10-20s，改为1页串行+剩余页并行，降至2-3s。
export async function fetchAllArticles(): Promise<Article[]> {
  // 先取第1页，同时获知总数
  const firstPage = await apiGet(
    "/articles?page=1&page_size=100&fields=light&status=approved,published"
  );
  const firstItems = (firstPage.data as { items?: Article[] } | undefined)?.items ?? [];
  const total = (firstPage.data as { total?: number } | undefined)?.total ?? 0;

  if (firstItems.length < 100 || total <= 100) return firstItems;

  // 计算剩余页数，并行拉取（上限 5 页 = 500 篇，足够分类筛选）
  const totalPages = Math.min(5, Math.ceil(total / 100));
  const restPages = Array.from({ length: totalPages - 1 }, (_, i) => i + 2);
  const restResults = await Promise.all(
    restPages.map((page) => fetchArticles(page, 100))
  );

  return [firstItems, ...restResults].flat();
}

// 仅取已审核文章总数，用于 Hero 动态展示收录量（轻量：page_size=1）
export async function fetchArticleCount(): Promise<number> {
  try {
    const json = await apiGet(
      `/articles?page=1&page_size=1&fields=light&status=approved,published`
    );
    const data = json.data as { total?: number } | undefined;
    return typeof data?.total === "number" ? data.total : 0;
  } catch {
    return 0;
  }
}

export async function fetchArticle(id: string): Promise<Article | null> {
  try {
    const json = await apiGet(`/articles/${encodeURIComponent(id)}`);
    return mapArticle(json.data as Record<string, unknown>);
  } catch {
    return null;
  }
}

export async function trackArticleView(id: string): Promise<number> {
  try {
    const res = await fetch(`${API_BASE}/articles/${encodeURIComponent(id)}/view`, {
      method: "POST",
      headers: { Accept: "application/json" },
    });
    if (!res.ok) return 0;
    const json = (await res.json()) as { data?: { view_count?: number } };
    return json.data?.view_count || 0;
  } catch {
    return 0;
  }
}

export async function fetchSearch(q: string): Promise<Article[]> {
  if (!q.trim()) return [];
  try {
    const json = await apiGet(
      `/search?q=${encodeURIComponent(q)}&page=1&page_size=30&fields=light`
    );
    return extractItems(json.data).map(mapArticle);
  } catch (e) {
    throw e;
  }
}

export async function fetchRelated(current: Article, limit = 5): Promise<Article[]> {
  const all = await fetchArticles(1, 100);
  const others = all.filter((a) => a.id !== current.id);
  const sameCat = others.filter(
    (a) => a.categorySlug && a.categorySlug === current.categorySlug
  );
  const rest = others.filter(
    (a) => !(a.categorySlug && a.categorySlug === current.categorySlug)
  );
  return [...sameCat, ...rest].slice(0, limit);
}

// ========== 兼容旧接口名（页面/组件可能引用） ==========
export const getHomeArticles = fetchArticles;
export const getArticlesByCategory = async (slug: string): Promise<Article[]> => {
  const all = await fetchArticles(1, 60);
  if (slug === "all" || !slug) return all;
  return all.filter((a) => a.categorySlug === slug);
};
export const getArticleById = fetchArticle;
export const getRelatedArticles = fetchRelated;
export const searchArticles = fetchSearch;

// ========== 分类信息（带数量，可选） ==========
export function getCategories(): CategoryInfo[] {
  return CATEGORIES.map((c) => ({
    slug: c.slug,
    title: c.label,
    count: 0,
    weeklyCount: 0,
  }));
}

// ========== 时间格式化 ==========
export function formatTimeAgo(dateString: string): string {
  if (!dateString) return "";
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return "";
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffHours / 24);

  if (diffHours < 1) return "刚刚";
  if (diffHours < 24) return `${diffHours} 小时前`;
  if (diffDays < 7) return `${diffDays} 天前`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} 周前`;
  return `${Math.floor(diffDays / 30)} 月前`;
}

export function formatFullDate(dateString: string): string {
  if (!dateString) return "";
  const d = new Date(dateString);
  if (isNaN(d.getTime())) return "";
  return d.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

// ========== 鉴权（真实后端 API，token 存 localStorage） ==========
const TOKEN_KEY = "eg_token";
const USER_KEY = "eg_user";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}
export function setToken(t: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, t);
}
export function clearToken(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
}

function mapUser(raw: Record<string, unknown> | undefined): User {
  if (!raw) return { id: "", username: "", email: "", avatar: null, createdAt: "" };
  return {
    id: String(raw.id ?? ""),
    username: (raw.username as string) || (raw.displayName as string) || "",
    email: (raw.email as string) || "",
    avatar: (raw.avatar as string) || null,
    createdAt: (raw.createdAt as string) || "",
    displayName: (raw.displayName as string) || undefined,
    bio: (raw.bio as string) || undefined,
  };
}

// 通用鉴权请求：自动附带 token，按后端 {code,message,data} 结构处理错误
async function apiAuth<T = unknown>(path: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    Accept: "application/json",
    ...(init?.headers as Record<string, string> | undefined),
  };
  const token = getToken();
  if (token) headers["X-Access-Token"] = token;
  const res = await fetch(`${API_BASE}${path}`, { ...init, headers });
  let json: Record<string, unknown> | null = null;
  try {
    json = (await res.json()) as Record<string, unknown>;
  } catch {
    /* ignore parse errors */
  }
  // HTTP 层 401 → token 过期/无效，清除本地会话并提示重新登录
  if (res.status === 401) {
    clearToken();
    setCurrentUser(null);
    throw new Error("登录已过期，请重新登录");
  }
  if (!res.ok) {
    const msg =
      (json && ((json.message as string) || (json.detail as string))) ||
      `请求失败 (${res.status})`;
    throw new Error(msg);
  }
  // 后端统一信封：HTTP 200 + code 区分成败
  if (json && typeof json.code === "number" && json.code !== 200) {
    throw new Error((json.message as string) || "请求失败");
  }
  return (json ? (json.data as T) : (null as unknown as T));
}

export async function login(identifier: string, password: string): Promise<User> {
  const data = await apiAuth<{ token: string; user: Record<string, unknown> }>(
    "/auth/login",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ identifier, password }),
    }
  );
  const user = mapUser(data.user);
  setToken(data.token);
  setCurrentUser(user);
  return user;
}

export async function register(payload: {
  username: string;
  email: string;
  password: string;
  displayName?: string;
  turnstileToken?: string;
}): Promise<User> {
  const data = await apiAuth<{ token: string; user: Record<string, unknown> }>(
    "/auth/register",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }
  );
  const user = mapUser(data.user);
  setToken(data.token);
  setCurrentUser(user);
  return user;
}

// 请求密码重置邮件（后端统一回成功，不暴露邮箱是否已注册）
export async function forgotPassword(email: string): Promise<void> {
  await apiAuth("/auth/forgot-password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
}

// 用邮件里的令牌完成密码重置
export async function resetPassword(token: string, newPassword: string): Promise<void> {
  await apiAuth("/auth/reset-password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token, new_password: newPassword }),
  });
}

// 重发邮箱验证邮件（邮箱未验证的用户）
export async function resendVerifyEmail(email: string): Promise<void> {
  await apiAuth("/auth/resend-verify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
}

// 用 token 校验当前会话，刷新本地用户信息；token 失效则清空
export async function fetchMe(): Promise<User | null> {
  const token = getToken();
  if (!token) return null;
  try {
    const data = await apiAuth<{ user: Record<string, unknown> }>("/auth/me");
    const user = mapUser(data.user);
    setCurrentUser(user);
    return user;
  } catch {
    clearToken();
    setCurrentUser(null);
    return null;
  }
}

export function getCurrentUser(): User | null {
  if (typeof window === "undefined") return null;
  try {
    const s = localStorage.getItem(USER_KEY);
    return s ? (JSON.parse(s) as User) : null;
  } catch {
    return null;
  }
}

export function setCurrentUser(user: User | null): void {
  if (typeof window === "undefined") return;
  if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
  else localStorage.removeItem(USER_KEY);
}

export function isLoggedIn(): boolean {
  return getCurrentUser() !== null;
}

export function logout(): void {
  clearToken();
  setCurrentUser(null);
}

// 兼容旧调用名
export const mockLogin = login;
export const mockRegister = register;

// ========== 第三方登录（OAuth: GitHub / Google） ==========
export async function startOAuth(provider: "github" | "google"): Promise<void> {
  const res = await fetch(`${API_BASE}/auth/oauth/${provider}/login`, {
    headers: { Accept: "application/json" },
    // The backend binds the OAuth `state` to an HttpOnly cookie for CSRF
    // protection; the browser only stores that cross-origin Set-Cookie if
    // the request is made with credentials.
    credentials: "include",
  });
  let json: Record<string, unknown> | null = null;
  try {
    json = (await res.json()) as Record<string, unknown>;
  } catch {
    /* ignore parse errors */
  }
  const code = json && typeof json.code === "number" ? json.code : null;
  const dataObj = (json?.data as Record<string, unknown> | undefined) || {};
  if (!res.ok || code !== 200 || !dataObj.url) {
    throw new Error((json?.message as string) || "社交登录暂不可用，请稍后再试");
  }
  window.location.href = dataObj.url as string;
}

// 登录页挂载时调用：若 URL 带 ?token= 则落地为本地会话并跳首页
export async function consumeOAuthCallback(): Promise<boolean> {
  if (typeof window === "undefined") return false;
  const params = new URLSearchParams(window.location.search);

  // 后端 OAuth 失败会回跳 ?oauth_error=xxx —— 必须显式提示，否则用户会
  // 静静停在登录页（表现为"没报错也没登录"）。
  const oauthError = params.get("oauth_error");
  if (oauthError) {
    const url = new URL(window.location.href);
    url.searchParams.delete("oauth_error");
    url.searchParams.delete("token");
    url.searchParams.delete("provider");
    window.history.replaceState({}, "", url.pathname + url.search);
    throw new Error(oauthErrorMessage(oauthError));
  }

  const token = params.get("token");
  if (!token) return false;
  setToken(token);
  const url = new URL(window.location.href);
  url.searchParams.delete("token");
  url.searchParams.delete("provider");
  window.history.replaceState({}, "", url.pathname + url.search);
  try {
    await fetchMe();
  } catch {
    clearToken();
  }
  window.location.href = "/";
  return true;
}

function oauthErrorMessage(code: string): string {
  switch (code) {
    case "token_exchange_failed":
      return "第三方登录失败：授权交换超时，请稍后重试";
    case "no_access_token":
      return "第三方登录失败：未获取到访问令牌";
    case "userinfo_failed":
      return "第三方登录失败：无法获取账号信息";
    case "not_configured":
      return "第三方登录未配置";
    case "missing_code":
      return "第三方登录失败：缺少授权码";
    default:
      return "第三方登录失败，请稍后重试";
  }
}

// ========== HTML 净化（仅浏览器端执行，避免构建期触碰 window） ==========
export async function sanitizeHtml(html: string): Promise<string> {
  if (!html) return "";
  if (typeof window === "undefined") return html;
  try {
    const mod = await import("dompurify");
    const DOMPurify = mod.default;
    return DOMPurify.sanitize(html, {
      ADD_TAGS: ["img", "picture", "source", "figure", "figcaption"],
      ADD_ATTR: ["target", "rel", "srcset", "sizes"],
    }) as string;
  } catch {
    return html;
  }
}

// ========== 评论（AI 审核 + 登录用户） ==========
// Cloudflare Turnstile site key（公开，可安全内嵌；secret 仅存后端 secrets）。
// 为空时组件不渲染 widget（本地开发/未配置场景自动放行）。
export const TURNSTILE_SITE_KEY = "0x4AAAAAAD9jq-8sv_jkZLgS";

export interface CommentAuthor {
  username: string;
  display_name: string;
  avatar: string | null;
}

export interface ArticleComment {
  id: number;
  article_id: number;
  user_id: number;
  content: string;
  created_at: string;
  parent_id?: number | null;
  replies?: ArticleComment[];
  article_title?: string;
  author?: CommentAuthor;
}

export interface CommentPage {
  items: ArticleComment[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export async function fetchComments(
  articleId: string | number,
  page = 1,
  pageSize = 20
): Promise<CommentPage> {
  // _t 缓存破坏：/api 边缘代理对匿名 GET 有 60s 缓存，不带它会拿到评论前的旧列表
  const res = await fetch(
    `${API_BASE}/articles/${articleId}/comments?page=${page}&page_size=${pageSize}&_t=${Date.now()}`,
    { headers: { Accept: "application/json" }, cache: "no-store" }
  );
  const json = await res.json();
  if (!res.ok || json.code !== 200) {
    throw new Error(json.message || "评论加载失败");
  }
  return json.data as CommentPage;
}

export async function postComment(
  articleId: string | number,
  content: string,
  parentId?: number
): Promise<ArticleComment> {
  const data = await apiAuth<{ comment: ArticleComment }>(
    `/articles/${articleId}/comments`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(parentId ? { content, parent_id: parentId } : { content }),
    }
  );
  return data.comment;
}

export async function deleteComment(commentId: number): Promise<void> {
  await apiAuth(`/comments/${commentId}`, { method: "DELETE" });
}

// 我的评论（个人中心）：跨文章，带 article_title
export async function fetchMyComments(page = 1, pageSize = 20): Promise<CommentPage> {
  return apiAuth<CommentPage>(`/comments/mine?page=${page}&page_size=${pageSize}&_t=${Date.now()}`);
}

// ========== 通知（回复提醒） ==========
export interface AppNotification {
  id: number;
  type: string;
  article_id: number | null;
  comment_id: number | null;
  is_read: boolean;
  created_at: string;
  actor?: CommentAuthor;
  article_title?: string;
  excerpt?: string;
}

export interface NotificationPage {
  items: AppNotification[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export async function fetchNotifications(page = 1, pageSize = 20): Promise<NotificationPage> {
  return apiAuth<NotificationPage>(`/notifications?page=${page}&page_size=${pageSize}&_t=${Date.now()}`);
}

export async function fetchUnreadCount(): Promise<number> {
  const d = await apiAuth<{ count: number }>(`/notifications/unread_count?_t=${Date.now()}`);
  return d.count || 0;
}

export async function markAllNotificationsRead(): Promise<void> {
  await apiAuth(`/notifications/read`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ all: true }),
  });
}

// ========== 头像 ==========
export async function uploadAvatar(dataUrl: string): Promise<User> {
  const d = await apiAuth<{ avatar: string; user: Record<string, unknown> }>(
    `/auth/avatar`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dataUrl }),
    }
  );
  const user = mapUser(d.user);
  setCurrentUser(user);
  return user;
}

export async function deleteAvatar(): Promise<User> {
  const d = await apiAuth<{ user: Record<string, unknown> }>(`/auth/avatar`, {
    method: "DELETE",
  });
  const user = mapUser(d.user);
  setCurrentUser(user);
  return user;
}
