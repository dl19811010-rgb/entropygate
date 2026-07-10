<template>
  <div class="list-page">
    <div class="container">
      <nav class="breadcrumb-nav">
        <router-link to="/">首页</router-link>
        <span class="sep">/</span>
        <span class="current">标签: {{ tag?.name || route.params.slug }}</span>
      </nav>

      <div class="page-header tag-header">
        <div class="tag-badge">#{{ tag?.name || route.params.slug }}</div>
        <p class="page-desc">查看关于 {{ tag?.name || route.params.slug }} 的所有文章</p>
      </div>

      <div class="content-grid">
        <main class="main-col">
          <div class="section-header">
            <h2 class="section-title">
              <newspaper-outline />
              <span>相关文章</span>
            </h2>
          </div>

          <div v-if="loading" class="loading-state">
            <n-spin size="large" />
            <p>加载中...</p>
          </div>

          <div v-else-if="articles.length === 0" class="empty-state">
            <file-tray-outline class="empty-icon" />
            <p>暂无相关文章</p>
          </div>

          <div v-else class="article-list">
            <article 
              v-for="article in articles" 
              :key="article.id"
              class="article-card"
              @click="goToArticle(article)"
            >
              <div class="article-image">
                <div class="image-placeholder" :class="`placeholder-${article.id % 6}`">
                  <image-outline />
                </div>
              </div>
              <div class="article-body">
                <h3 class="article-title">{{ article.title }}</h3>
                <p class="article-excerpt" v-if="article.summary">{{ article.summary }}</p>
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
                    <span>{{ article.view_count || 0 }}</span>
                  </span>
                </div>
              </div>
            </article>
          </div>

          <div class="pagination-wrapper" v-if="totalPages > 1">
            <n-pagination
              v-model:page="currentPage"
              :page-count="totalPages"
              :page-size="pageSize"
              @update:page="handlePageChange"
            />
          </div>
        </main>

        <aside class="side-col">
          <div class="sidebar-card">
            <div class="sidebar-header">
              <flame-outline class="sidebar-icon hot" />
              <h3>热门标签</h3>
            </div>
            <div class="tag-cloud">
              <router-link 
                v-for="t in hotTags" 
                :key="t.id"
                :to="`/tag/${t.slug || t.id}`"
                class="tag-cloud-item"
                :class="{ active: t.name === tag?.name }"
              >
                {{ t.name }}
              </router-link>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticleList } from '@/api/article'
import { getTagDetail } from '@/api/tag'
import { isMockEnabled } from '@/utils/mock'
import { logError } from '@/utils/log'
import {
  NewspaperOutline, GlobeOutline, TimeOutline, EyeOutline,
  ImageOutline, FileTrayOutline, FlameOutline
} from '@vicons/ionicons5'

const route = useRoute()
const router = useRouter()

const articles = ref([])
const hotTags = ref([])
const tag = ref(null)
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

onMounted(() => {
  loadTag()
  loadArticles()
  loadHotTags()
})

watch(() => route.params.slug, () => {
  currentPage.value = 1
  loadTag()
  loadArticles()
})

async function loadTag() {
  const slug = route.params.slug
  try {
    const res = await getTagDetail(slug)
    tag.value = res || resolveTagName(slug)
  } catch (e) {
    tag.value = resolveTagName(slug)
  }
}

function resolveTagName(slug) {
  const nameMap = {
    '1': 'ChatGPT',
    '2': 'GPT-4',
    '3': 'AI绘画',
    '4': '大语言模型',
    '5': 'Midjourney',
    '6': 'AIGC',
    '7': 'Claude',
    '8': '自动驾驶',
    '9': '机器学习',
    '10': 'Sora',
    'chatgpt': 'ChatGPT',
    'gpt-4': 'GPT-4',
    'ai-painting': 'AI绘画',
    'llm': '大语言模型',
    'midjourney': 'Midjourney',
    'aigc': 'AIGC',
    'claude': 'Claude',
    'autonomous': '自动驾驶',
    'ml': '机器学习',
    'sora': 'Sora'
  }
  return { name: nameMap[slug] || slug }
}

async function loadArticles() {
  loading.value = true
  try {
    const res = await getArticleList({
      page: currentPage.value,
      page_size: pageSize.value,
      tag_slug: route.params.slug
    })
    articles.value = filterArticles(res.items || res.list || [])
    total.value = res.total || 0
  } catch (e) {
    logError('加载标签文章失败:', e)
    articles.value = isMockEnabled() ? filterArticles(getMockArticles()) : []
    total.value = 20
  } finally {
    loading.value = false
  }
}

function isTestArticle(article) {
  if (!article || !article.title) return true
  const title = article.title.toLowerCase()
  return ['测试', 'test', 'delete', '删除'].some(p => title.includes(p.toLowerCase()))
}

function filterArticles(list) {
  return (list || []).filter(a => !isTestArticle(a))
}

function loadHotTags() {
  hotTags.value = [
    { id: 1, name: 'ChatGPT' },
    { id: 2, name: 'GPT-4' },
    { id: 3, name: 'AI绘画' },
    { id: 4, name: '大语言模型' },
    { id: 5, name: 'Midjourney' },
    { id: 6, name: 'AIGC' },
    { id: 7, name: 'Claude' },
    { id: 8, name: '自动驾驶' },
    { id: 9, name: '机器学习' },
    { id: 10, name: 'Sora' }
  ]
}

function goToArticle(article) {
  router.push(`/article/${article.id}`)
}

function handlePageChange(page) {
  currentPage.value = page
  loadArticles()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}

function getMockArticles() {
  return [
    {
      id: 1,
      title: 'GPT-5 即将发布？OpenAI 最新动态深度解析',
      summary: '近期关于 GPT-5 的传闻不断，本文从多个角度分析 OpenAI 下一代大模型的可能特性。',
      source: { name: 'AI 科技评论' },
      publish_time: new Date(Date.now() - 3600000).toISOString(),
      view_count: 15420
    },
    {
      id: 2,
      title: 'Midjourney V7 实测：图像生成质量迎来质的飞跃',
      summary: 'Midjourney 最新版本 V7 在图像细节、文本生成方面都有显著提升。',
      source: { name: '设计前沿' },
      publish_time: new Date(Date.now() - 7200000).toISOString(),
      view_count: 8930
    },
    {
      id: 3,
      title: 'Anthropic 发布 Claude 3 Opus，性能直逼 GPT-4',
      summary: 'Claude 3 系列正式发布，长文本处理能力更是其核心优势。',
      source: { name: '机器之心' },
      publish_time: new Date(Date.now() - 86400000).toISOString(),
      view_count: 12050
    },
    {
      id: 4,
      title: '2024 年 AI Agent 发展趋势与技术架构解析',
      summary: 'AI Agent 被认为是下一代人机交互范式，本文深入分析其核心组件。',
      source: { name: 'PaperWeekly' },
      publish_time: new Date(Date.now() - 172800000).toISOString(),
      view_count: 6780
    }
  ]
}
</script>

<style scoped>
.list-page {
  padding: var(--spacing-xl) 0;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-tertiary);
  margin-bottom: var(--spacing-lg);
}

.breadcrumb-nav a {
  color: var(--text-secondary);
  transition: color var(--transition-fast);
}

.breadcrumb-nav a:hover {
  color: var(--brand-primary);
}

.breadcrumb-nav .sep {
  color: var(--border-light);
}

.breadcrumb-nav .current {
  color: var(--text-primary);
}

.tag-header {
  margin-bottom: var(--spacing-xl);
}

.tag-badge {
  display: inline-block;
  padding: 8px 18px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: var(--border-radius-full);
  font-size: 20px;
  font-weight: 600;
  color: var(--brand-primary);
  margin-bottom: var(--spacing-md);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.page-desc {
  font-size: 15px;
  color: var(--text-secondary);
  word-break: break-word;
  overflow-wrap: break-word;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: var(--spacing-xl);
  align-items: start;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  min-width: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  min-width: 0;
}

.section-title span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
}

.section-title svg {
  color: var(--brand-primary);
  flex-shrink: 0;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.article-card {
  display: grid;
  grid-template-columns: minmax(120px, 180px) 1fr;
  gap: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.article-card:hover {
  border-color: var(--border-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.article-image {
  aspect-ratio: 16/10;
  border-radius: var(--border-radius-md);
  overflow: hidden;
  background: var(--bg-tertiary);
  min-width: 0;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: var(--text-tertiary);
  background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary));
}

.article-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.article-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;
  margin-bottom: var(--spacing-sm);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color var(--transition-fast);
  word-break: break-word;
}

.article-card:hover .article-title {
  color: var(--brand-primary);
}

.article-excerpt {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: var(--spacing-md);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  font-size: 13px;
  color: var(--text-tertiary);
  margin-top: auto;
  min-width: 0;
  overflow: hidden;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
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

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-xl);
}

.side-col {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
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

.sidebar-icon.hot { color: #ef4444; }
.sidebar-icon {
  width: var(--icon-sm);
  height: var(--icon-sm);
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-cloud-item {
  padding: 4px 10px;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-full);
  font-size: 13px;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.tag-cloud-item:hover,
.tag-cloud-item.active {
  background: var(--brand-primary);
  color: white;
}

.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: var(--text-tertiary);
  gap: var(--spacing-md);
}

.empty-icon {
  font-size: 40px;
  opacity: 0.5;
}

@media (max-width: 1100px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .side-col {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  }
}

@media (max-width: 768px) {
  .article-card {
    grid-template-columns: minmax(100px, 160px) 1fr;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
  }
}

@media (max-width: 640px) {
  .article-card {
    grid-template-columns: 100px 1fr;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm);
  }
  .article-image {
    aspect-ratio: 1/1;
  }
  .tag-badge {
    font-size: 16px;
  }
  .article-title {
    font-size: 14px;
  }
  .article-excerpt {
    -webkit-line-clamp: 1;
  }
  .article-meta {
    gap: var(--spacing-sm);
    font-size: 12px;
  }
  .side-col {
    grid-template-columns: 1fr;
  }
}
</style>
