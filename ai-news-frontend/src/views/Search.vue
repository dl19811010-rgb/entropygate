<template>
  <div class="search-page">
    <div class="container">
      <div class="search-hero">
        <h1 class="search-title">搜索情报</h1>
        <p class="search-desc">搜索公司、模型、能力、研究等实体</p>

        <div class="search-box-large" :class="{ focused: searchFocused }">
          <n-input
            v-model:value="keyword"
            placeholder="输入关键词搜索实体..."
            size="large"
            clearable
            @focus="searchFocused = true"
            @blur="handleBlur"
            @keydown.enter="handleSearch"
            @clear="handleClear"
            @update:value="handleInput"
          >
            <template #prefix>
              <search-outline class="search-icon" />
            </template>
            <template #suffix>
              <n-button type="primary" size="large" @click="handleSearch">搜索</n-button>
            </template>
          </n-input>
        </div>

        <!-- Autocomplete suggestions -->
        <div class="suggest-dropdown" v-if="showSuggestions && suggestions.length">
          <div
            v-for="s in suggestions"
            :key="s.id"
            class="suggest-item"
            @mousedown="goToSuggestion(s)"
          >
            <span class="suggest-type">{{ s.type }}</span>
            <span class="suggest-title">{{ s.title }}</span>
          </div>
        </div>

        <!-- Recent searches -->
        <div class="recent-searches" v-if="!hasSearched && recentSearches.length">
          <span class="recent-label">最近搜索：</span>
          <span
            v-for="word in recentSearches"
            :key="word"
            class="recent-word"
            @click="quickSearch(word)"
          >
            {{ word }}
          </span>
        </div>

        <!-- Hot searches -->
        <div class="hot-searches" v-if="!hasSearched">
          <span class="hot-label">热门：</span>
          <span
            v-for="word in hotWords"
            :key="word"
            class="hot-word"
            @click="quickSearch(word)"
          >
            {{ word }}
          </span>
        </div>
      </div>

      <!-- Search Results -->
      <div v-if="hasSearched" class="search-results">
        <div class="result-header">
          <h2>
            搜索 <span class="keyword">「{{ keyword }}」</span>
            <span class="count">共 {{ total }} 个结果</span>
          </h2>
        </div>

        <div v-if="loading" class="loading-state">
          <n-spin size="large" />
          <p>搜索中...</p>
        </div>

        <div v-else-if="results.length === 0" class="empty-state">
          <file-tray-outline class="empty-icon" />
          <p>没有找到相关实体</p>
          <p class="empty-hint">换个关键词试试吧</p>
        </div>

        <div v-else class="result-list">
          <div
            v-for="item in results"
            :key="item.id"
            class="result-card"
            @click="goToResult(item)"
          >
            <div class="result-type-badge">{{ item.type }}</div>
            <h3 class="result-title">{{ item.title }}</h3>
            <p class="result-summary" v-if="item.summary">{{ item.summary }}</p>
            <div class="result-meta">
              <span class="result-slug">{{ item.slug }}</span>
              <span class="result-score" v-if="item.match_score">匹配度 {{ item.match_score }}</span>
            </div>
            <div class="result-keywords" v-if="item.keywords?.length">
              <n-tag v-for="kw in item.keywords.slice(0, 5)" :key="kw" size="small">{{ kw }}</n-tag>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { search, searchSuggest } from '@/api/search'
import { logError } from '@/utils/log'
import {
  SearchOutline, FileTrayOutline
} from '@vicons/ionicons5'

const route = useRoute()
const router = useRouter()

const keyword = ref('')
const searchFocused = ref(false)
const hasSearched = ref(false)
const results = ref([])
const suggestions = ref([])
const showSuggestions = ref(false)
const loading = ref(false)
const total = ref(0)

const recentSearches = ref([])
const RECENT_KEY = 'eg_recent_searches'

const hotWords = [
  'OpenAI', 'Claude', 'GPT-4', '推理',
  'Midjourney', 'Sora', 'LLM', '多模态'
]

onMounted(() => {
  // Load recent searches
  try {
    const raw = localStorage.getItem(RECENT_KEY)
    if (raw) recentSearches.value = JSON.parse(raw)
  } catch (e) { /* ignore */ }

  if (route.query.q) {
    keyword.value = route.query.q
    doSearch()
  }
})

watch(() => route.query.q, (newQ, oldQ) => {
  if (newQ === oldQ) return
  const q = typeof newQ === 'string' ? newQ : ''
  if (q !== keyword.value) {
    keyword.value = q
    if (q) {
      doSearch()
    } else {
      hasSearched.value = false
      results.value = []
      total.value = 0
    }
  }
})

async function handleInput(val) {
  if (!val || val.length < 1) {
    showSuggestions.value = false
    suggestions.value = []
    return
  }
  try {
    const data = await searchSuggest(val, 8)
    suggestions.value = data.suggestions || []
    showSuggestions.value = suggestions.value.length > 0
  } catch (e) {
    showSuggestions.value = false
  }
}

function handleBlur() {
  // Delay hiding so click on suggestion works
  setTimeout(() => {
    showSuggestions.value = false
  }, 150)
}

function handleSearch() {
  if (!keyword.value.trim()) return
  router.replace({ path: '/search', query: { q: keyword.value } })
  doSearch()
}

function handleClear() {
  hasSearched.value = false
  results.value = []
  total.value = 0
}

function quickSearch(word) {
  keyword.value = word
  handleSearch()
}

function goToSuggestion(s) {
  if (!s.type || !s.slug) return
  saveRecentSearch(s.title || s.slug)
  router.push(`/entity/${s.type}/${s.slug}`)
}

function goToResult(item) {
  if (!item.type || !item.slug) return
  saveRecentSearch(keyword.value)
  router.push(`/entity/${item.type}/${item.slug}`)
}

function saveRecentSearch(q) {
  if (!q) return
  const list = [q, ...recentSearches.value.filter(x => x !== q)].slice(0, 8)
  recentSearches.value = list
  try {
    localStorage.setItem(RECENT_KEY, JSON.stringify(list))
  } catch (e) { /* ignore */ }
}

async function doSearch() {
  hasSearched.value = true
  loading.value = true
  showSuggestions.value = false
  try {
    const data = await search(keyword.value, 20)
    results.value = data.results || []
    total.value = data.total || 0
    if (keyword.value) saveRecentSearch(keyword.value)
  } catch (e) {
    logError('搜索失败:', e)
    results.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.search-page {
  padding: var(--spacing-2xl) 0;
}

.search-hero {
  text-align: center;
  max-width: 700px;
  margin: 0 auto var(--spacing-2xl);
  position: relative;
}

.search-title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  background: var(--brand-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.search-desc {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
}

.search-box-large {
  margin-bottom: var(--spacing-lg);
  position: relative;
}

.search-box-large :deep(.n-input) {
  height: 52px;
  border-radius: var(--border-radius-full) !important;
  font-size: 16px;
}

.search-icon {
  width: var(--icon-lg);
  height: var(--icon-lg);
  color: var(--text-tertiary);
}

/* Suggest dropdown */
.suggest-dropdown {
  position: absolute;
  left: 0;
  right: 0;
  top: calc(100% + 4px);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  z-index: 100;
  text-align: left;
  overflow: hidden;
}

.suggest-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 10px 16px;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.suggest-item:hover {
  background: var(--bg-hover);
}

.suggest-type {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--brand-primary);
  background: rgba(99, 102, 241, 0.08);
  padding: 2px 8px;
  border-radius: var(--border-radius-sm);
  flex-shrink: 0;
}

.suggest-title {
  font-size: 14px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Recent + Hot */
.recent-searches, .hot-searches {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  max-width: 520px;
  margin: 0 auto var(--spacing-md);
  justify-content: center;
}

.recent-label, .hot-label {
  color: var(--text-tertiary);
  white-space: nowrap;
}

.recent-word, .hot-word {
  padding: 6px 12px;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-full);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 13px;
}

.recent-word:hover, .hot-word:hover {
  background: var(--brand-primary);
  color: white;
}

/* Results */
.search-results {
  max-width: 800px;
  margin: 0 auto;
  min-height: 300px;
  padding-bottom: var(--spacing-2xl);
}

.result-header {
  margin-bottom: var(--spacing-lg);
}

.result-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.result-header .keyword {
  color: var(--brand-primary);
  font-weight: 700;
}

.result-header .count {
  font-size: 14px;
  font-weight: normal;
  color: var(--text-tertiary);
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.result-card {
  padding: var(--spacing-lg);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.result-card:hover {
  border-color: var(--border-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.result-type-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--brand-primary);
  background: rgba(99, 102, 241, 0.08);
  padding: 2px 8px;
  border-radius: var(--border-radius-sm);
  margin-bottom: 8px;
}

.result-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
  line-height: 1.4;
}

.result-summary {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 8px;
}

.result-score {
  color: var(--brand-primary);
  font-weight: 500;
}

.result-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
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
  opacity: 0.4;
}

.empty-hint {
  font-size: 13px;
  opacity: 0.7;
}

@media (max-width: 640px) {
  .search-title {
    font-size: 28px;
  }
  .result-header h2 {
    font-size: 16px;
  }
}
</style>
