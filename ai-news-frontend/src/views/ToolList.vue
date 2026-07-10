<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NButton, NTag, NPagination, NSelect, NInput } from 'naive-ui'
import { SearchOutlined } from '@vicons/antd'
import { getTools } from '@/api/tool'
import { getCategories, getTags } from '@/api/category'
import { logError } from '@/utils/log'

const route = useRoute()
const router = useRouter()

const tools = ref([])
const total = ref(0)
const page = ref(1)
const size = ref(12)
const loading = ref(false)
const categories = ref([])
const keyword = ref('')
const selectedCategory = ref(null)
const selectedAvailability = ref(null)

const availabilityOptions = [
  { label: '全部状态', value: null },
  { label: '国内可用', value: 'available' },
  { label: '部分受限', value: 'restricted' },
  { label: '已被封禁', value: 'blocked' },
  { label: '仅企业版', value: 'enterprise_only' },
  { label: '待核实', value: 'uncertain' }
]

const availabilityLabels = {
  available: '国内可用',
  restricted: '部分受限',
  blocked: '已被封禁',
  enterprise_only: '仅企业版',
  uncertain: '待核实'
}

async function loadTools() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      size: size.value
    }
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    if (selectedAvailability.value) {
      params.availability = selectedAvailability.value
    }
    if (keyword.value) {
      params.q = keyword.value
    }
    const res = await getTools(params)
    tools.value = res.items || []
    total.value = res.total || 0
  } catch (e) {
    logError('加载工具失败:', e)
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  try {
    const res = await getCategories({ type: 'tool' })
    categories.value = res || []
  } catch (e) {
    logError('加载分类失败:', e)
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

function handleSearch() {
  page.value = 1
}

onMounted(() => {
  loadCategories()
  loadTools()
})

watch([page, selectedCategory, selectedAvailability, keyword], () => {
  loadTools()
})
</script>

<template>
  <div class="tool-list-page">
    <div class="page-inner">
      <div class="page-header">
        <div class="header-text">
          <h1 class="page-title">AI工具库</h1>
          <p class="page-desc">精选全球优质AI工具，附国内可用性评估</p>
        </div>
        <div class="header-search">
          <n-input
            v-model:value="keyword"
            placeholder="搜索工具..."
            @update:value="handleSearch"
          >
            <template #prefix>
              <search-outlined />
            </template>
          </n-input>
        </div>
      </div>

      <div class="filter-bar">
        <div class="filter-group">
          <span class="filter-label">可用性：</span>
          <div class="filter-tags">
            <button
              v-for="opt in availabilityOptions"
              :key="opt.value || 'all'"
              class="filter-tag"
              :class="{ active: selectedAvailability === opt.value }"
              @click="selectedAvailability = opt.value; page = 1"
            >
              <span v-if="opt.value" :class="['status-dot', opt.value]"></span>
              {{ opt.label }}
            </button>
          </div>
        </div>
      </div>

      <div class="content-wrap">
        <aside class="sidebar">
          <div class="sidebar-section">
            <h3 class="sidebar-title">工具分类</h3>
            <div class="category-list">
              <a
                class="category-item"
                :class="{ active: !selectedCategory }"
                @click="handleCategoryChange(null)"
              >
                全部工具
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
        </aside>

        <div class="main-content">
          <div class="tools-grid">
            <div
              v-for="tool in tools"
              :key="tool.id"
              class="tool-card"
              @click="router.push(`/tools/${tool.slug}`)"
            >
              <div class="tool-header">
                <div class="tool-logo">
                  <span class="tool-letter">{{ tool.name ? tool.name.charAt(0) : '?' }}</span>
                </div>
                <span
                  class="tool-status"
                  :class="tool.availability_status || 'uncertain'"
                >
                  {{ availabilityLabels[tool.availability_status] || '待核实' }}
                </span>
              </div>
              <h3 class="tool-name">{{ tool.name }}</h3>
              <p class="tool-desc">{{ tool.description }}</p>
              <div class="tool-footer">
                <span v-if="tool.category_name" class="tool-category">
                  {{ tool.category_name }}
                </span>
                <span v-if="tool.pricing_model" class="tool-pricing">
                  {{ tool.pricing_model }}
                </span>
              </div>
            </div>

            <div v-if="!loading && tools.length === 0" class="empty-state">
              <p>暂无相关工具</p>
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
      </div>
    </div>
  </div>
</template>

<style scoped>
.tool-list-page {
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
  margin-bottom: 24px;
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

.filter-bar {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 24px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
  flex-shrink: 0;
}

.filter-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  border-radius: 20px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tag:hover {
  border-color: var(--border-light);
  color: var(--text-primary);
}

.filter-tag.active {
  background: rgba(99, 102, 241, 0.08);
  border-color: var(--brand-primary);
  color: var(--brand-primary);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.available {
  background: #10b981;
}

.status-dot.restricted {
  background: #f59e0b;
}

.status-dot.blocked {
  background: #ef4444;
}

.status-dot.enterprise_only {
  background: #6366f1;
}

.status-dot.uncertain {
  background: var(--text-tertiary);
}

.content-wrap {
  display: grid;
  grid-template-columns: 220px 1fr;
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

.tools-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.tool-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--bg-tertiary);
}

.tool-card:hover {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
  border-color: var(--border-color);
}

.tool-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.tool-logo {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-letter {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
}

.tool-status {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 500;
}

.tool-status.available {
  background: #d1fae5;
  color: #059669;
}

.tool-status.restricted {
  background: #fef3c7;
  color: #d97706;
}

.tool-status.blocked {
  background: #fee2e2;
  color: #dc2626;
}

.tool-status.enterprise_only {
  background: #e0e7ff;
  color: #4f46e5;
}

.tool-status.uncertain {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.tool-name {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.tool-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 16px;
  min-height: 42px;
}

.tool-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--bg-tertiary);
}

.tool-category {
  font-size: 12px;
  color: var(--text-tertiary);
}

.tool-pricing {
  font-size: 12px;
  color: var(--brand-primary);
  background: rgba(99, 102, 241, 0.08);
  padding: 2px 8px;
  border-radius: 10px;
}

.empty-state {
  grid-column: 1 / -1;
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
  }

  .tools-grid {
    grid-template-columns: repeat(2, 1fr);
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

@media (max-width: 640px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }
}
</style>
