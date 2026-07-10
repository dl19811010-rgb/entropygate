<template>
  <div class="article-detail-page">
    <div class="container detail-container">
      <main class="detail-main">
        <nav class="breadcrumb-nav">
          <router-link to="/">首页</router-link>
          <span class="sep">/</span>
          <router-link v-if="article?.category" :to="`/category/${article.category.slug || article.category.id}`">
            {{ article.category.name }}
          </router-link>
          <span class="sep" v-if="article?.category">/</span>
          <span class="current">文章详情</span>
        </nav>

        <div v-if="loading" class="loading-state">
          <n-spin size="large" />
          <p>加载中...</p>
        </div>

        <article v-else class="article-detail">
          <header class="article-header">
            <div class="article-cat" v-if="article.category">
              {{ article.category.name }}
            </div>
            <h1 class="article-title">{{ article.title }}</h1>
            <div class="article-meta">
              <span class="meta-item" v-if="article.source">
                <globe-outline />
                <span>{{ article.source.name }}</span>
              </span>
              <span class="meta-item">
                <time-outline />
                <span>{{ formatDate(article.publish_time || article.created_at) }}</span>
              </span>
              <span class="meta-item">
                <eye-outline />
                <span>{{ article.view_count || 0 }} 阅读</span>
              </span>
            </div>
          </header>

          <div class="article-cover" v-if="article.cover_image">
            <img :src="article.cover_image" :alt="article.title" class="cover-image" />
          </div>

          <div class="article-content">
            <div v-html="sanitizeHTML(article.content_html || article.content || mockContent)" class="prose"></div>
          </div>

          <div class="article-tags" v-if="article.tags && article.tags.length">
            <pricetag-outline class="tags-icon" />
            <div class="tags-list">
              <router-link 
                v-for="tag in article.tags" 
                :key="tag.id"
                :to="`/tag/${tag.slug || tag.id}`"
                class="tag-link"
              >
                #{{ tag.name }}
              </router-link>
            </div>
          </div>

          <div class="article-actions">
            <div class="action-buttons">
              <button class="action-btn like">
                <heart-outline />
                <span>点赞</span>
              </button>
              <button class="action-btn share">
                <share-outline />
                <span>分享</span>
              </button>
              <button class="action-btn bookmark">
                <bookmark-outline />
                <span>收藏</span>
              </button>
            </div>
          </div>
        </article>
      </main>

      <aside class="detail-side">
        <div class="sidebar-card author-card">
          <div class="author-avatar">
            <person-outline />
          </div>
          <div class="author-name">{{ article?.source?.name || 'AI 资讯' }}</div>
          <div class="author-desc">专注 AI 领域资讯分享</div>
          <n-button type="primary" block>关注</n-button>
        </div>

        <div class="sidebar-card">
          <div class="sidebar-header">
            <flame-outline class="sidebar-icon hot" />
            <h3>相关推荐</h3>
          </div>
          <div class="related-list">
            <div 
              v-for="item in relatedArticles" 
              :key="item.id"
              class="related-item"
              @click="goToArticle(item.id)"
            >
              <div class="related-img" :class="`placeholder-${item.id % 6}`">
                <image-outline />
              </div>
              <div class="related-info">
                <div class="related-title">{{ item.title }}</div>
                <div class="related-views">
                  <eye-outline />
                  {{ item.view_count || 0 }} 阅读
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticleDetail } from '@/api/article'
import { isMockEnabled } from '@/utils/mock'
import { logError } from '@/utils/log'
import { sanitizeHTML } from '@/utils/sanitize'
import {
  GlobeOutline, TimeOutline, EyeOutline, ImageOutline,
  PricetagOutline, HeartOutline, ShareOutline, BookmarkOutline,
  FlameOutline, PersonOutline
} from '@vicons/ionicons5'

const route = useRoute()
const router = useRouter()

const article = ref({})
const loading = ref(true)
const relatedArticles = ref([])

const mockContent = `
  <p>人工智能技术正在以前所未有的速度发展，从大语言模型到图像生成，从自动驾驶到科学研究，AI 正在深刻改变我们的生活和工作方式。</p>
  
  <h2>大模型技术的最新进展</h2>
  
  <p>近年来，大语言模型（Large Language Models, LLMs）取得了突破性进展。GPT 系列、Claude、Gemini 等模型不断刷新性能上限，在自然语言理解、代码生成、逻辑推理等任务上展现出惊人的能力。</p>
  
  <p>这些模型不仅在规模上不断扩大，在架构设计、训练方法、对齐技术等方面也在持续创新。多模态能力的加入，让 AI 能够同时理解文本、图像、音频等多种形式的信息。</p>
  
  <h2>AIGC 内容创作革命</h2>
  
  <p>AIGC（AI Generated Content）正在重塑内容创作的方式。从文字到图像，从音频到视频，AI 生成内容的质量和效率都在快速提升。</p>
  
  <ul>
    <li><strong>文本生成</strong>：文章写作、代码生成、创意构思</li>
    <li><strong>图像生成</strong>：Midjourney、DALL·E、Stable Diffusion</li>
    <li><strong>视频生成</strong>：Sora、Runway、Pika</li>
    <li><strong>音频生成</strong>：音乐创作、语音合成、声音克隆</li>
  </ul>
  
  <h2>AI Agent 与自动化</h2>
  
  <p>AI Agent 被认为是下一代人机交互范式。通过将大语言模型作为核心控制器，结合各种工具和能力，AI Agent 能够自主完成复杂的任务。</p>
  
  <p>从个人助理到企业自动化，从科研助手到创意伙伴，AI Agent 的应用场景正在不断扩展。我们正在见证从"工具"到"代理"的转变。</p>
  
  <h2>未来展望</h2>
  
  <p>AI 技术的发展速度令人惊叹。未来，我们有望看到更强大的模型、更丰富的应用、更深入的融合。同时，AI 伦理、安全、治理等问题也需要我们共同关注和努力。</p>
  
  <p>让我们一起期待 AI 带来的无限可能！</p>
`

onMounted(async () => {
  await loadArticle()
  loadRelatedArticles()
})

async function loadArticle() {
  loading.value = true
  try {
    const res = await getArticleDetail(route.params.id)
    article.value = res || {}
  } catch (e) {
    logError('加载文章详情失败:', e)
    article.value = isMockEnabled() ? getMockArticle() : {}
  } finally {
    loading.value = false
  }
}

function loadRelatedArticles() {
  relatedArticles.value = filterArticles([
    { id: 1, title: 'GPT-5 即将发布？OpenAI 最新动态深度解析', view_count: 15420 },
    { id: 2, title: 'Midjourney V7 实测：图像生成质量迎来质的飞跃', view_count: 8930 },
    { id: 3, title: 'Anthropic 发布 Claude 3 Opus，性能直逼 GPT-4', view_count: 12050 },
    { id: 4, title: '2024 年 AI Agent 发展趋势与技术架构解析', view_count: 6780 },
    { id: 5, title: 'Sora 之后，视频生成领域还有哪些玩家？', view_count: 9520 }
  ])
}

function isTestArticle(article) {
  if (!article || !article.title) return true
  const title = article.title.toLowerCase()
  return ['测试', 'test', 'delete', '删除'].some(p => title.includes(p.toLowerCase()))
}

function filterArticles(list) {
  return (list || []).filter(a => !isTestArticle(a))
}

function getMockArticle() {
  return {
    id: route.params.id,
    title: '2024 年人工智能发展趋势深度解析',
    summary: '本文从大模型、AIGC、AI Agent 等多个维度，深入分析 2024 年人工智能领域的发展趋势和未来展望。',
    content: mockContent,
    category: { id: 1, name: '大模型', slug: 'llm' },
    source: { name: 'EntropyGate AI' },
    publish_time: new Date(Date.now() - 86400000).toISOString(),
    view_count: 12345,
    tags: [
      { id: 1, name: '人工智能' },
      { id: 2, name: '大模型' },
      { id: 3, name: 'AIGC' },
      { id: 4, name: 'AI Agent' }
    ]
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function goToArticle(id) {
  router.push(`/article/${id}`)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.article-detail-page {
  padding: var(--spacing-xl) 0;
}

.detail-container {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: var(--spacing-xl);
  align-items: start;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: var(--spacing-lg);
  min-width: 0;
  overflow: hidden;
}

.breadcrumb-nav a {
  color: var(--text-secondary);
  transition: color var(--transition-fast);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
  max-width: 200px;
}

.breadcrumb-nav a:hover {
  color: var(--brand-primary);
}

.breadcrumb-nav .sep {
  color: var(--border-light);
  flex-shrink: 0;
}

.breadcrumb-nav .current {
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.article-detail {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-2xl);
}

.article-header {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-xl);
  border-bottom: 1px solid var(--border-color);
}

.article-cat {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(99, 102, 241, 0.15);
  color: var(--brand-primary);
  border-radius: var(--border-radius-full);
  font-size: 13px;
  font-weight: 500;
  margin-bottom: var(--spacing-md);
}

.article-title {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: var(--spacing-md);
  word-break: break-word;
  overflow-wrap: break-word;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-md) var(--spacing-lg);
  font-size: 14px;
  color: var(--text-tertiary);
  min-width: 0;
  overflow: hidden;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  min-width: 0;
  flex-shrink: 0;
  max-width: 100%;
}

.meta-item span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
}

.article-cover {
  width: 100%;
  max-height: 240px;
  aspect-ratio: 16/9;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  margin-bottom: var(--spacing-xl);
  background: var(--bg-tertiary);
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
  background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary));
}

.cover-placeholder svg {
  width: var(--icon-xl);
  height: var(--icon-xl);
  flex-shrink: 0;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.article-content {
  font-size: 16px;
  line-height: 1.9;
  color: var(--text-secondary);
}

.article-content :deep(h2) {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin: var(--spacing-2xl) 0 var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
}

.article-content :deep(p) {
  margin-bottom: var(--spacing-md);
}

.article-content :deep(ul) {
  margin-bottom: var(--spacing-md);
  padding-left: var(--spacing-lg);
  list-style: disc;
}

.article-content :deep(li) {
  margin-bottom: var(--spacing-sm);
}

.article-content :deep(strong) {
  color: var(--text-primary);
  font-weight: 600;
}

.article-tags {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--border-color);
  min-width: 0;
}

.tags-icon {
  width: var(--icon-md);
  height: var(--icon-md);
  color: var(--brand-primary);
  margin-top: 4px;
  flex-shrink: 0;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  min-width: 0;
}

.tag-link {
  padding: 6px 12px;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-full);
  font-size: 13px;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.tag-link:hover {
  background: var(--brand-primary);
  color: white;
}

.article-actions {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--border-color);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  justify-content: center;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-full);
  font-size: 14px;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.action-btn:hover {
  border-color: var(--brand-primary);
  color: var(--brand-primary);
  transform: translateY(-1px);
}

.detail-side {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  position: sticky;
  top: calc(var(--header-height) + 24px);
}

.sidebar-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  min-width: 0;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  min-width: 0;
}

.sidebar-header h3 {
  font-size: 16px;
  font-weight: 600;
}

.sidebar-icon.hot {
  color: #ef4444;
}

.author-card {
  text-align: center;
}

.author-avatar {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--spacing-md);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--brand-gradient);
  border-radius: 50%;
  font-size: var(--icon-xl);
  color: white;
}

.author-avatar svg {
  width: 28px;
  height: 28px;
}

.author-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.author-desc {
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: var(--spacing-md);
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  display: flex;
  gap: 12px;
  cursor: pointer;
  transition: opacity var(--transition-fast);
}

.related-item:hover {
  opacity: 0.8;
}

.related-img {
  width: 64px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-sm);
  color: var(--text-tertiary);
  font-size: var(--icon-sm);
  flex-shrink: 0;
}

.related-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.related-title {
  font-size: 13px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
}

.related-views {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--text-tertiary);
  gap: var(--spacing-md);
}

@media (max-width: 1100px) {
  .detail-container {
    grid-template-columns: 1fr;
  }
  
  .detail-side {
    position: static;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  }
}

@media (max-width: 640px) {
  .article-detail {
    padding: var(--spacing-lg);
  }
  
  .article-title {
    font-size: 22px;
  }
  
  .article-meta {
    gap: var(--spacing-sm);
    font-size: 13px;
  }
  
  .article-cover {
    aspect-ratio: 16/9;
  }
  
  .breadcrumb-nav a {
    max-width: 120px;
  }
  
  .action-btn {
    padding: 8px 16px;
    font-size: 13px;
  }
  
  .detail-side {
    grid-template-columns: 1fr;
  }
}
</style>
