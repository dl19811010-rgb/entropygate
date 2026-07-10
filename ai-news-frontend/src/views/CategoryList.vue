<template>
  <div class="list-page">
    <div class="container">
      <nav class="breadcrumb-nav">
        <router-link to="/">首页</router-link>
        <span class="sep">/</span>
        <span class="current">{{ category?.name || '分类' }}</span>
      </nav>

      <div class="page-header">
        <h1 class="page-title">{{ category?.name || '分类文章' }}</h1>
        <p class="page-desc" v-if="category?.description">{{ category.description }}</p>
      </div>

      <div class="content-grid">
        <main class="main-col">
          <div class="section-header">
            <h2 class="section-title">
              <newspaper-outline />
              <span>全部文章</span>
            </h2>
          </div>

          <div v-if="showNewsTypes" class="news-type-filter">
            <button
              v-for="nt in newsTypes"
              :key="nt.key"
              :class="['type-btn', { active: newsTypeFilter === nt.key }]"
              @click="handleNewsTypeChange(nt.key)"
            >
              <span class="type-icon">{{ nt.icon }}</span>
              <span class="type-label">{{ nt.label }}</span>
            </button>
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
              <h3>热门文章</h3>
            </div>
            <div class="hot-list">
              <div 
                v-for="(article, index) in hotArticles" 
                :key="article.id"
                class="hot-item"
                @click="goToArticle(article)"
              >
                <div class="hot-rank" :class="`rank-${index + 1}`">{{ index + 1 }}</div>
                <div class="hot-info">
                  <div class="hot-title">{{ article.title }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="sidebar-card">
            <div class="sidebar-header">
              <pricetag-outline class="sidebar-icon tag" />
              <h3>热门标签</h3>
            </div>
            <div class="tag-cloud">
              <router-link 
                v-for="tag in hotTags" 
                :key="tag.id"
                :to="`/tag/${tag.slug || tag.id}`"
                class="tag-cloud-item"
              >
                {{ tag.name }}
              </router-link>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticleList } from '@/api/article'
import { getCategoryDetail } from '@/api/category'
import { getMockArticleList, getMockHotArticles } from '@/data/mockArticles'
import { isMockEnabled } from '@/utils/mock'
import { logError } from '@/utils/log'
import {
  NewspaperOutline, GlobeOutline, TimeOutline, EyeOutline,
  ImageOutline, FileTrayOutline, FlameOutline, PricetagOutline
} from '@vicons/ionicons5'

const route = useRoute()
const router = useRouter()

const articles = ref([])
const hotArticles = ref([])
const hotTags = ref([])
const category = ref(null)
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)
const newsTypeFilter = ref(null)

const newsTypes = [
  { key: null, label: '全部', icon: '📋' },
  { key: 'new_model', label: '新模型', icon: '🆕' },
  { key: 'new_capability', label: '新能力', icon: '🚀' },
  { key: 'agent_update', label: 'Agent', icon: '🤖' },
  { key: 'api_update', label: 'API/SDK', icon: '🔌' },
  { key: 'open_access', label: '开放体验', icon: '🌍' },
  { key: 'restriction_change', label: '限制与故障', icon: '⚠️' },
  { key: 'benchmark', label: 'Benchmark', icon: '📊' },
  { key: 'ecosystem', label: '生态更新', icon: '📦' },
]

const showNewsTypes = computed(() => {
  const slug = route.params.slug
  return slug === 'ai-news' || slug === '1'
})

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

onMounted(() => {
  loadCategory()
  loadArticles()
  loadHotArticles()
  loadHotTags()
})

watch(() => route.params.slug, () => {
  currentPage.value = 1
  loadCategory()
  loadArticles()
})

async function loadCategory() {
  const slug = route.params.slug
  try {
    const res = await getCategoryDetail(slug)
    category.value = res || resolveCategoryName(slug)
  } catch (e) {
    category.value = resolveCategoryName(slug)
  }
}

function resolveCategoryName(slug) {
  const categoryMap = {
    '1': { name: 'AI新动态', description: '针对国内用户有实际价值的新工具、新技术与行业动态' },
    '2': { name: 'AI工具指南', description: '解决 AI 难使用的问题，提供实用工具教程与使用技巧' },
    'ai-news': { name: 'AI新动态', description: '针对国内用户有实际价值的新工具、新技术与行业动态' },
    'ai-tools': { name: 'AI工具指南', description: '解决 AI 难使用的问题，提供实用工具教程与使用技巧' }
  }
  return categoryMap[slug] || { name: slug, description: '' }
}

async function loadArticles() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      category_slug: route.params.slug
    }
    if (newsTypeFilter.value) {
      params.news_type = newsTypeFilter.value
    }
    const res = await getArticleList(params)
    articles.value = filterArticles(res.items || res.list || [])
    total.value = res.total || 0
  } catch (e) {
    logError('加载分类文章失败:', e)
    if (!isMockEnabled()) {
      articles.value = []
      total.value = 0
    } else {
      const mock = getMockArticleList({
        category_slug: route.params.slug,
        page: currentPage.value,
        page_size: pageSize.value
      })
      articles.value = filterArticles(mock.items)
      total.value = mock.total
    }
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

function loadHotArticles() {
  hotArticles.value = getMockHotArticles(5)
}

function loadHotTags() {
  hotTags.value = [
    { id: 1, name: 'ChatGPT' },
    { id: 2, name: 'GPT-4' },
    { id: 3, name: 'AI绘画' },
    { id: 4, name: '大语言模型' },
    { id: 5, name: 'Midjourney' },
    { id: 6, name: 'AIGC' },
    { id: 7, name: 'Claude' }
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

function handleNewsTypeChange(type) {
  newsTypeFilter.value = type
  currentPage.value = 1
  loadArticles()
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

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  word-break: break-word;
  overflow-wrap: break-word;
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

.news-type-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-lg);
}

.type-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-full);
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.type-btn:hover {
  border-color: var(--border-light);
  background: var(--bg-secondary);
}

.type-btn.active {
  border-color: var(--brand-primary);
  background: rgba(99, 102, 241, 0.1);
  color: var(--brand-primary);
}

.type-icon {
  font-size: 14px;
}

.type-label {
  white-space: nowrap;
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
.sidebar-icon.tag { color: #8b5cf6; }
.sidebar-icon {
  width: var(--icon-sm);
  height: var(--icon-sm);
}

.hot-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hot-item {
  display: flex;
  gap: 12px;
  cursor: pointer;
  transition: opacity var(--transition-fast);
}

.hot-item:hover { opacity: 0.8; }

.hot-rank {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 700;
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.hot-rank.rank-1 {
  background: linear-gradient(135deg, #ef4444, #f87171);
  color: white;
}

.hot-rank.rank-2 {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  color: white;
}

.hot-rank.rank-3 {
  background: linear-gradient(135deg, #10b981, #34d399);
  color: white;
}

.hot-info { 
  flex: 1; 
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hot-title {
  font-size: 13px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
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

.tag-cloud-item:hover {
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
  .page-title {
    font-size: 22px;
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
