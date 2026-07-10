<script setup>
import { ref, onMounted, computed, h } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NDataTable, NButton, NSpace, NInput, NSelect,
  NPagination, useMessage, useDialog, NTag, NRate
} from 'naive-ui'
import { PlusOutlined, SearchOutlined, EditOutlined, DeleteOutlined } from '@vicons/antd'
import { getArticles, deleteArticle, publishArticle, batchRewriteArticles } from '@/api/article'
import { getSources } from '@/api/source'

const router = useRouter()
const message = useMessage()
const dialog = useDialog()

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')
const statusFilter = ref('approved')
const sourceFilter = ref(null)
const newsTypeFilter = ref(null)
const sortField = ref('-approved_at')
const sourceOptions = ref([])
const selectedIds = ref([])

const statusOptions = [
  { label: '待编辑', value: 'approved' },
  { label: '全部状态', value: null },
  { label: '已发布', value: 'published' },
  { label: '草稿', value: 'draft' },
  { label: '已下架', value: 'archived' },
  { label: '已废弃', value: 'discarded' }
]

const sortOptions = [
  { label: '发布时间 ↓', value: '-published_at' },
  { label: '发布时间 ↑', value: 'published_at' },
  { label: '质量分 ↓', value: '-quality_score' },
  { label: '相关性 ↓', value: '-relevance_score' },
  { label: '浏览量 ↓', value: '-view_count' },
]

const statusTypeMap = {
  published: 'success',
  approved: 'info',
  draft: 'default',
  archived: 'warning',
  discarded: 'error'
}

const statusLabelMap = {
  published: '已发布',
  approved: '待编辑',
  draft: '草稿',
  archived: '已下架',
  discarded: '已废弃'
}

const newsTypeMap = {
  new_model: { label: '新模型', icon: '🆕', type: 'success' },
  new_capability: { label: '新能力', icon: '🚀', type: 'primary' },
  agent_update: { label: 'Agent', icon: '🤖', type: 'warning' },
  api_update: { label: 'API', icon: '🔌', type: 'info' },
  open_access: { label: '开放', icon: '🌍', type: 'success' },
  restriction_change: { label: '限制', icon: '⚠️', type: 'error' },
  benchmark: { label: 'Benchmark', icon: '📊', type: 'default' },
  ecosystem: { label: '生态', icon: '📦', type: 'info' },
}

const newsTypeOptions = [
  { label: '全部类型', value: null },
  { label: '🆕 新模型', value: 'new_model' },
  { label: '🚀 新能力', value: 'new_capability' },
  { label: '🤖 Agent', value: 'agent_update' },
  { label: '🔌 API', value: 'api_update' },
  { label: '🌍 开放', value: 'open_access' },
  { label: '⚠️ 限制', value: 'restriction_change' },
  { label: '📊 Benchmark', value: 'benchmark' },
  { label: '📦 生态', value: 'ecosystem' },
]

function getImpactLevel(score) {
  if (score >= 8) return { label: '发布', color: 'success' }
  if (score >= 5) return { label: '观察', color: 'warning' }
  return { label: '忽略', color: 'default' }
}

function qualityColor(score) {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'default'
}

const columns = [
  { title: '标题', key: 'title', ellipsis: { tooltip: true } },
  {
    title: '新闻类型',
    key: 'news_type',
    width: 100,
    render: (row) => {
      const nt = newsTypeMap[row.news_type]
      if (!nt) return '-'
      return h(NTag, { size: 'small', type: nt.type }, {
        default: () => `${nt.icon} ${nt.label}`
      })
    }
  },
  {
    title: '来源',
    key: 'source_name',
    width: 130,
    ellipsis: { tooltip: true }
  },
  {
    title: '状态',
    key: 'status',
    width: 90,
    render: (row) => {
      return h(NTag, { size: 'small', type: statusTypeMap[row.status] || 'default' }, {
        default: () => statusLabelMap[row.status] || row.status
      })
    }
  },
  {
    title: '影响力',
    key: 'impact_score',
    width: 100,
    render: (row) => {
      const level = getImpactLevel(row.impact_score || 0)
      return h(NTag, { size: 'small', type: level.color }, {
        default: () => `${row.impact_score || 0}分 (${level.label})`
      })
    }
  },
  {
    title: '质量分',
    key: 'quality_score',
    width: 90,
    render: (row) => {
      const score = row.quality_score || 0
      return h(NTag, { size: 'small', type: qualityColor(score) }, {
        default: () => score
      })
    }
  },
  {
    title: '相关性',
    key: 'relevance_score',
    width: 90,
    render: (row) => {
      const score = row.relevance_score || 0
      return h(NTag, { size: 'small', type: qualityColor(score) }, {
        default: () => score
      })
    }
  },
  {
    title: '能力变化',
    key: 'capability_change',
    width: 150,
    ellipsis: { tooltip: true },
    render: (row) => {
      const cc = row.capability_change
      if (!cc || !cc.highlights || cc.highlights.length === 0) return '-'
      return cc.highlights.slice(0, 2).join(' | ')
    }
  },
  {
    title: '精选',
    key: 'is_featured',
    width: 70,
    render: (row) => row.is_featured ? '✓' : '-'
  },
  { title: '浏览', key: 'view_count', width: 70 },
  {
    title: '发布时间',
    key: 'published_at',
    width: 160,
    render: (row) => row.published_at ? new Date(row.published_at).toLocaleString() : '-'
  },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    render: (row) => {
      const buttons = [
        h(NButton, {
          size: 'small',
          type: 'primary',
          text: true,
          onClick: () => handleEdit(row)
        }, { default: () => '编辑' })
      ]
      // 待编辑文章显示"发布"按钮
      if (row.status === 'approved') {
        buttons.push(h(NButton, {
          size: 'small',
          type: 'success',
          text: true,
          onClick: () => handlePublish(row)
        }, { default: () => '发布' }))
      }
      buttons.push(h(NButton, {
        size: 'small',
        type: 'error',
        text: true,
        onClick: () => handleDelete(row)
      }, { default: () => '删除' }))
      return h(NSpace, { size: 'small' }, { default: () => buttons })
    }
  }
]

async function loadSources() {
  try {
    const res = await getSources()
    sourceOptions.value = [
      { label: '全部来源', value: null },
      ...res.data.items.map(s => ({ label: s.name, value: s.name }))
    ]
  } catch (e) {
    // 忽略，不影响主流程
  }
}

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      size: pageSize.value,
      sort: sortField.value
    }
    if (searchKeyword.value) {
      params.q = searchKeyword.value
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    if (sourceFilter.value) {
      params.source = sourceFilter.value
    }
    if (newsTypeFilter.value) {
      params.news_type = newsTypeFilter.value
    }
    const res = await getArticles(params)
    list.value = res.data.items
    total.value = res.data.total
  } catch (e) {
    message.error(e.message || '加载失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  loadData()
}

function handleReset() {
  searchKeyword.value = ''
  statusFilter.value = null
  sourceFilter.value = null
  newsTypeFilter.value = null
  sortField.value = '-published_at'
  page.value = 1
  loadData()
}

function handleCreate() {
  router.push('/articles/create')
}

function handleEdit(row) {
  router.push(`/articles/edit/${row.id}`)
}

function handleDelete(row) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除文章「${row.title}」吗？`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await deleteArticle(row.id)
        message.success('删除成功')
        loadData()
      } catch (e) {
        message.error(e.message || '删除失败')
      }
    }
  })
}

async function handlePublish(row) {
  try {
    await publishArticle(row.id)
    message.success('发布成功')
    loadData()
  } catch (e) {
    message.error(e.message || '发布失败')
  }
}

async function handleBatchRewrite() {
  if (selectedIds.value.length === 0) {
    message.warning('请先勾选文章')
    return
  }
  dialog.info({
    title: '确认批量 AI 重写',
    content: `将使用 AI 对选中的 ${selectedIds.value.length} 篇文章进行翻译和重写，原文将保留在 extra_data 中。继续？`,
    positiveText: '开始重写',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        const res = await batchRewriteArticles(selectedIds.value)
        message.success(res.message || '批量重写完成')
        selectedIds.value = []
        loadData()
      } catch (e) {
        message.error(e.message || '批量重写失败')
      }
    }
  })
}

function handleCheck(rowKeys) {
  selectedIds.value = rowKeys
}

function handlePageChange(p) {
  page.value = p
  loadData()
}

function handlePageSizeChange(s) {
  pageSize.value = s
  page.value = 1
  loadData()
}

onMounted(() => {
  loadSources()
  loadData()
})
</script>

<template>
  <div class="article-list">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">文章管理</h2>
        <p class="page-desc">待编辑：审核通过待翻译重写 | 已发布：翻译完成已上线</p>
      </div>
      <n-space>
        <n-button
          v-if="selectedIds.length > 0"
          type="warning"
          @click="handleBatchRewrite"
        >
          批量 AI 重写 ({{ selectedIds.length }})
        </n-button>
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <plus-outlined />
          </template>
          新建文章
        </n-button>
      </n-space>
    </div>
    <n-card>
      <n-space vertical :size="16">
        <n-space :size="12" align="center" wrap>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索标题..."
            style="width: 200px"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <search-outlined />
            </template>
          </n-input>
          <n-select
            v-model:value="statusFilter"
            :options="statusOptions"
            style="width: 130px"
            @update:value="handleSearch"
          />
          <n-select
            v-model:value="sourceFilter"
            :options="sourceOptions"
            placeholder="全部来源"
            style="width: 160px"
            @update:value="handleSearch"
          />
          <n-select
            v-model:value="newsTypeFilter"
            :options="newsTypeOptions"
            placeholder="全部类型"
            style="width: 140px"
            @update:value="handleSearch"
          />
          <n-select
            v-model:value="sortField"
            :options="sortOptions"
            style="width: 140px"
            @update:value="handleSearch"
          />
          <n-button type="primary" @click="handleSearch">搜索</n-button>
          <n-button @click="handleReset">重置</n-button>
          <div style="flex: 1"></div>
        </n-space>

        <n-data-table
          :columns="columns"
          :data="list"
          :loading="loading"
          :bordered="false"
          :scroll-x="1100"
          :row-key="row => row.id"
          :checked-row-keys="selectedIds"
          @update:checked-row-keys="handleCheck"
        />

        <div v-if="total > 0" class="pagination-wrapper">
          <n-pagination
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 50, 100]"
            show-size-picker
            show-quick-jumper
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
          />
        </div>
      </n-space>
    </n-card>
  </div>
</template>

<style scoped>
.article-list {
  width: 100%;
  min-width: 0;
  padding: 0;
  overflow-x: auto;
}

:deep(.n-card) {
  width: 100%;
  min-width: 800px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header-left {
  min-width: 0;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.page-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}
</style>
