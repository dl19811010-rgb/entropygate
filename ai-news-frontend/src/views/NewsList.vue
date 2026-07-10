<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NButton, NTag, NPagination, NSelect, NInput } from 'naive-ui'
import { SearchOutlined } from '@vicons/antd'
import { getArticles } from '@/api/article'
import { getCategories, getTags } from '@/api/category'
import { logError } from '@/utils/log'

const route = useRoute()
const router = useRouter()

const articles = ref([])
const total = ref(0)
const page = ref(1)
const size = ref(12)
const loading = ref(false)
const categories = ref([])
const tags = ref([])
const keyword = ref('')
const selectedCategory = ref(null)
const selectedTag = ref(null)
const sortBy = ref('-published_at')

const sortOptions = [
  { label: '最新发布', value: '-published_at' },
  { label: '最多浏览', value: '-view_count' },
  { label: '最早发布', value: 'published_at' }
]

async function loadArticles() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      size: size.value,
      sort: sortBy.value
    }
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    if (selectedTag.value) {
      params.tag = selectedTag.value
    }
    if (keyword.value) {
      params.q = keyword.value
    }
    const res = await getArticles(params)
    articles.value = res.items || []
    total.value = res.total || 0
  } catch (e) {
    logError('加载文章失败:', e)
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  try {
    const res = await getCategories({ type: 'news' })
    categories.value = res || []
  } catch (e) {
    logError('加载分类失败:', e)
  }
}

async function loadTags() {
  try {
    const res = await getTags()
    tags.value = res || []
  } catch (e) {
    logError('加载标签失败:', e)
  }
}

function handlePageChange(p) {
  page.value = p
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleCategoryChange(value) {
  selectedCategory.value = value
  page.value = 1
}

function handleTagClick(tagSlug) {
  selectedTag.value = selectedTag.value === tagSlug ? null : tagSlug
  page.value = 1
}

function handleSearch() {
  page.value = 1
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

onMounted(() => {
  if (route.query.q) {
    keyword.value = route.query.q
  }
  loadCategories()
  loadTags()
  loadArticles()
})

watch([page, sortBy, selectedCategory, selectedTag, keyword], () => {
  loadArticles()
})
</script>

<template>
  <div class="news-list-page">
    <div class="page-inner">
      <div class="page-header">
        <div class="header-text">
          <h1 class="page-title">AI新动态</h1>
          <p class="page-desc">追踪全球AI前沿动态，掌握行业最新趋势</p>
        </div>
        <div class="header-search">
          <n-input
            v-model:value="keyword"
            placeholder="搜索文章..."
            @update:value="handleSearch"
          >
            <template #prefix>
              <search-outlined />
            </template>
          </n-input>
        </div>
      </div>

      <div class="content-wrap">
        <div class="main-content">
          <div class="articles-list">
            <article
              v-for="article in articles"
              :key="article.id"
              class="article-item"
              @click="router.push(`/article/${article.id}`)"
            >
              <div class="article-info">
                <div class="article-meta">
                  <span class="article-date">
                    {{ formatDate(article.published_at || article.created_at) }}
                  </span>
                  <span v-if="article.category_name" class="article-category">
                    {{ article.category_name }}
                  </span>
                  <span v-if="article.source_name" class="article-source">
                    {{ article.source_name }}
                  </span>
                </div>
                <h2 class="article-title">{{ article.title }}</h2>
                <p v-if="article.summary || article.ai_summary" class="article-summary">
                  {{ article.summary || article.ai_summary }}
                </p>
                <div class="article-footer">
                  <span class="view-count">{{ article.view_count || 0 }} 次阅读</span>
                  <span class="read-more">阅读全文 →</span>
                </div>
              </div>
            </article>

            <div v-if="!loading && articles.length === 0" class="empty-state">
              <p>暂无相关文章</p>
            </div>
          </div>

          <div v-if="total > size" class="pagination-wrap">
            <n-pagination
              v-model:page="page"
              :item-count="total"
              :page-size="size"
              :show-size-picker="false"
              @update:page="handlePageChange"
            />
          </div>
        </div>

        <aside class="sidebar">
          <div class="sidebar-section">
            <h3 class="sidebar-title">分类</h3>
            <div class="category-list">
              <a
                class="category-item"
                :class="{ active: !selectedCategory }"
                @click="handleCategoryChange(null)"
              >
                全部
              </a>
              <a
                v-for="cat in categories"
                :key="cat.id"
                class="category-item"
                :class="{ active: selectedCategory === cat.slug }"
                @click="handleCategoryChange(cat.slug)"
              >
                {{ cat.name }}
              </a>
            </div>
          </div>
          <div class="sidebar-section">
            <h3 class="sidebar-title">热门标签</h3>
            <div class="tag-cloud">
              <n-tag
                v-for="tag in tags.slice(0, 15)"
                :key="tag.id"
                :style="{ borderColor: tag.color + '40' }"
                class="tag-item"
                :class="{ active: selectedTag === tag.slug }"
                @click="handleTagClick(tag.slug)"
              >
                {{ tag.name }}
              </n-tag>
            </div>
          </div>
          <div class="sidebar-section">
            <h3 class="sidebar-title">排序</h3>
            <n-select
              v-model:value="sortBy"
              :options="sortOptions"
              style="width: 100%"
            />
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<style scoped>
.news-list-page {
  background: var(--bg-primary);
  min-height: calc(100vh - 64px);
}

.page-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.page-desc {
  font-size: 15px;
  color: var(--text-tertiary);
}

.header-search {
  width: 320px;
}

.content-wrap {
  display: grid;
  grid-template-columns: 1fr 240px;
  gap: 32px;
  align-items: flex-start;
}

.sidebar {
  position: sticky;
  top: 80px;
}

.sidebar-section {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.sidebar-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.category-item {
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.category-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.category-item.active {
  background: rgba(99, 102, 241, 0.08);
  color: var(--brand-primary);
  font-weight: 500;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: pointer;
  transition: all 0.2s;
}

.tag-item:hover {
  opacity: 0.8;
}

.tag-item.active {
  background: var(--brand-primary) !important;
  color: #fff !important;
  border-color: var(--brand-primary) !important;
}

.main-content {
  min-width: 0;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-item {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 28px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.article-item:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  transform: translateY(-2px);
  border-color: var(--border-color);
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 16px;
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

.article-source {
  font-size: 13px;
  color: var(--text-tertiary);
}

.article-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: 12px;
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
  margin-bottom: 16px;
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
  padding: 80px 20px;
  color: var(--text-tertiary);
  background: var(--bg-card);
  border-radius: 16px;
}

.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

@media (max-width: 960px) {
  .content-wrap {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
  }

  .sidebar-section {
    flex: 1;
    min-width: 200px;
    margin-bottom: 0;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-search {
    width: 100%;
  }
}
</style>
