<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NButton, NTag } from 'naive-ui'
import {
  FlashOutline, ConstructOutline, TrendingUpOutline,
  NewspaperOutline, SearchOutline
} from '@vicons/ionicons5'
import { getHomepageFeed } from '@/api/homepage'
import { getTools } from '@/api/tool'
import { logError } from '@/utils/log'

const router = useRouter()

const feedData = ref(null)
const feedLoading = ref(false)
const latestArticles = ref([])
const featuredTools = ref([])

// 将 feed 中的 major_events 转为卡片展示数据
const feedArticles = computed(() => {
  if (!feedData.value) return []
  const events = feedData.value.major_events || []
  return events.map((event) => ({
    id: event.id,
    title: event.title,
    date: event.detected_at,
    category: event.type,
    summary: '',
    entity_type: event.entity_type,
    entity_slug: event.entity_slug,
    score: event.score,
  }))
})

async function loadFeed() {
  feedLoading.value = true
  try {
    const res = await getHomepageFeed()
    feedData.value = res
    latestArticles.value = feedArticles.value
  } catch (e) {
    logError('加载首页情报失败:', e)
    feedData.value = null
    latestArticles.value = []
  } finally {
    feedLoading.value = false
  }
}

async function loadFeaturedTools() {
  try {
    const res = await getTools({ page: 1, size: 4, sort: '-view_count' })
    featuredTools.value = res.items || []
  } catch (e) {
    logError('加载热门工具失败:', e)
  }
}

function goToNews() {
  router.push('/news')
}

function goToTools() {
  router.push('/tools')
}

function goToArticle(id) {
  router.push(`/article/${id}`)
}

function goToEntity(type, slug) {
  if (type && slug) {
    router.push(`/entity/${type}/${slug}`)
  }
}

function goToTool(slug) {
  router.push(`/tools/${slug}`)
}

function goToSearch() {
  router.push('/search')
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// 事件类型中文映射
function eventTypeLabel(type) {
  const map = {
    model_release: '模型发布',
    feature_added: '新功能',
    price_change: '价格变动',
    partnership: '合作',
    funding: '融资',
    acquisition: '收购',
    regulation: '监管',
    research: '研究',
    benchmark: '基准测试',
  }
  return map[type] || type
}

onMounted(() => {
  loadFeed()
  loadFeaturedTools()
})
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-bg">
        <div class="hero-glow glow-1"></div>
        <div class="hero-glow glow-2"></div>
        <div class="hero-grid"></div>
      </div>
      <div class="container hero-content">
        <div class="hero-text">
          <div class="hero-badge">
            <span class="badge-dot"></span>
            AI 资讯平台
          </div>
          <h1 class="hero-title">探索 AI 领域的无限可能</h1>
          <p class="hero-desc">汇聚全球前沿人工智能资讯，掌握行业最新动态，发现实用 AI 工具。</p>
          <div class="hero-actions">
            <n-button type="primary" size="large" @click="goToNews">
              <template #icon><newspaper-outline /></template>
              浏览 AI 新动态
            </n-button>
            <n-button size="large" ghost @click="goToTools">
              <template #icon><construct-outline /></template>
              AI 工具库
            </n-button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="hero-card card-news" @click="goToNews">
            <div class="card-icon news"><flash-outline /></div>
            <div class="card-info">
              <div class="card-title">AI 新动态</div>
              <div class="card-desc">前沿资讯 · 行业趋势</div>
            </div>
          </div>
          <div class="hero-card card-tools" @click="goToTools">
            <div class="card-icon tools"><construct-outline /></div>
            <div class="card-info">
              <div class="card-title">AI 工具库</div>
              <div class="card-desc">实用工具 · 效率提升</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="content-section">
      <div class="container content-grid">
        <!-- Latest Articles -->
        <div class="main-col">
          <div class="section-header">
            <h2 class="section-title">
              <trending-up-outline />
              <span>最新动态</span>
            </h2>
            <a class="more-link" @click="goToNews">查看更多 →</a>
          </div>

          <div class="article-list">
            <article
              v-for="article in latestArticles"
              :key="article.id"
              class="article-card"
              :class="{ clickable: article.entity_type && article.entity_slug }"
              @click="article.entity_type && article.entity_slug ? goToEntity(article.entity_type, article.entity_slug) : null"
            >
              <div class="article-meta">
                <span class="article-date">{{ formatDate(article.date) }}</span>
                <span v-if="article.category" class="article-category">{{ eventTypeLabel(article.category) }}</span>
              </div>
              <h3 class="article-title">{{ article.title }}</h3>
              <div class="article-footer">
                <span class="view-count">热度 {{ article.score || 0 }}</span>
                <span v-if="article.entity_type && article.entity_slug" class="read-more">查看详情 →</span>
              </div>
            </article>

            <div v-if="!feedLoading && latestArticles.length === 0" class="empty-state">
              情报收集中，请稍后再来...
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <aside class="side-col">
          <div class="sidebar-card">
            <div class="sidebar-header">
              <construct-outline class="sidebar-icon" />
              <h3>热门工具</h3>
            </div>
            <div class="tool-list">
              <div
                v-for="tool in featuredTools"
                :key="tool.id"
                class="tool-item"
                @click="goToTool(tool.slug)"
              >
                <div class="tool-name">{{ tool.name }}</div>
                <div class="tool-views">{{ tool.view_count || 0 }} 次使用</div>
              </div>
              <div v-if="featuredTools.length === 0" class="empty-small">
                暂无工具
              </div>
            </div>
            <a class="sidebar-more" @click="goToTools">查看全部工具 →</a>
          </div>

          <div class="sidebar-card">
            <div class="sidebar-header">
              <search-outline class="sidebar-icon" />
              <h3>快速搜索</h3>
            </div>
            <n-button block @click="goToSearch">
              <template #icon><search-outline /></template>
              搜索文章和工具
            </n-button>
          </div>
        </aside>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
}

/* Hero */
.hero-section {
  position: relative;
  padding: 100px 0 80px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.hero-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.12;
}

.glow-1 {
  width: 400px;
  height: 400px;
  background: #6366f1;
  top: -100px;
  left: -100px;
}

.glow-2 {
  width: 300px;
  height: 300px;
  background: #8b5cf6;
  bottom: -80px;
  right: 10%;
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(99, 102, 241, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99, 102, 241, 0.04) 1px, transparent 1px);
  background-size: 50px 50px;
}

.hero-content {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
  gap: 60px;
  align-items: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 999px;
  font-size: 13px;
  color: var(--brand-primary);
  margin-bottom: 20px;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--brand-primary);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.hero-title {
  font-size: 42px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 20px;
  letter-spacing: -0.5px;
}

.hero-desc {
  font-size: 17px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 32px;
  max-width: 500px;
}

.hero-actions {
  display: flex;
  gap: 12px;
}

.hero-visual {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hero-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.hero-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  border-color: var(--border-light);
}

.card-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  font-size: 24px;
  color: white;
  flex-shrink: 0;
}

.card-icon.news {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.card-icon.tools {
  background: linear-gradient(135deg, #10b981, #34d399);
}

.card-info {
  min-width: 0;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.card-desc {
  font-size: 13px;
  color: var(--text-tertiary);
}

/* Content */
.content-section {
  padding: 60px 0 80px;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: 40px;
  align-items: start;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 22px;
  font-weight: 700;
}

.section-title svg {
  color: var(--brand-primary);
  width: 1em;
  height: 1em;
}

.more-link {
  font-size: 14px;
  color: var(--brand-primary);
  cursor: pointer;
  transition: opacity 0.2s;
}

.more-link:hover {
  opacity: 0.8;
}

/* Article List */
.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  border-color: var(--border-light);
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.article-date {
  font-size: 13px;
  color: var(--text-tertiary);
}

.article-category {
  font-size: 12px;
  color: var(--brand-primary);
  background: rgba(99, 102, 241, 0.1);
  padding: 2px 10px;
  border-radius: 20px;
}

.article-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-summary {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 14px;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.view-count {
  font-size: 13px;
  color: var(--text-tertiary);
}

.read-more {
  font-size: 13px;
  color: var(--brand-primary);
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-tertiary);
  background: var(--bg-card);
  border-radius: 16px;
}

/* Sidebar */
.side-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 80px;
}

.sidebar-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 20px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-header h3 {
  font-size: 16px;
  font-weight: 600;
}

.sidebar-icon {
  width: 18px;
  height: 18px;
  color: var(--brand-primary);
}

.tool-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tool-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.tool-item:hover {
  background: var(--bg-tertiary);
}

.tool-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.tool-views {
  font-size: 12px;
  color: var(--text-tertiary);
}

.empty-small {
  text-align: center;
  padding: 20px;
  color: var(--text-tertiary);
  font-size: 13px;
}

.sidebar-more {
  display: block;
  text-align: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
  font-size: 13px;
  color: var(--brand-primary);
  cursor: pointer;
  transition: opacity 0.2s;
}

.sidebar-more:hover {
  opacity: 0.8;
}

/* Responsive */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  .side-col {
    position: static;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  }
  .hero-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  .hero-title {
    font-size: 32px;
  }
}

@media (max-width: 640px) {
  .hero-section {
    padding: 60px 0 40px;
  }
  .hero-title {
    font-size: 28px;
  }
  .hero-desc {
    font-size: 15px;
  }
  .hero-actions {
    flex-direction: column;
  }
  .hero-actions .n-button {
    width: 100%;
  }
  .content-section {
    padding: 40px 0 60px;
  }
  .section-title {
    font-size: 18px;
  }
}
</style>
