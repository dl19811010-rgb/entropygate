<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NButton, NSpace, NInput, NSelect, NModal, NImage,
  NPagination, useMessage, useDialog, NTag, NDivider, NPopover
} from 'naive-ui'
import { SearchOutlined, CheckCircleOutlined, CloseCircleOutlined, EditOutlined, LinkOutlined } from '@vicons/antd'
import { getArticles, approveArticle, rejectArticle, batchApproveArticles, getGroupedReview } from '@/api/article'
import { getAllCategories } from '@/api/category'

const router = useRouter()
const message = useMessage()
const dialog = useDialog()

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(12)
const searchKeyword = ref('')
const categoryFilter = ref(null)
const sourceFilter = ref(null)
const editorialFilter = ref('high')  // high(>=60) | mid(40-59) | low(<40) | all
const categories = ref([])
const sourceOptions = ref([{ label: '全部来源', value: null }])
const selectedIds = ref([])

// 预览弹窗
const previewId = ref(null)
const showPreview = ref(false)

// 驳回弹窗
const rejectReason = ref('')
const showRejectDialog = ref(false)
const rejectTarget = ref(null)

// 统计
const stats = ref({ draft: 0, approved: 0, total: 0 })
const tierStats = ref({ S: 0, A: 0, B: 0, C: 0, D: 0 })

// ESS v2 — 分组视图
const viewMode = ref('grouped')  // 'grouped' | 'flat'
const groupedData = ref(null)
const groupedLoading = ref(false)
const activeBucket = ref(null)

const categoryOptions = computed(() => [
  { label: '全部分类', value: null },
  ...categories.value.map(c => ({ label: c.name, value: c.slug }))
])

// ====== 辅助函数 ======

function getTranslatedTitle(row) {
  const extra = row.extra_data || {}
  return extra.translated_title || ''
}

function getOriginalTitle(row) {
  const extra = row.extra_data || {}
  return extra.original_title || row.title || ''
}

function getImages(row) {
  const extra = row.extra_data || {}
  return extra.images || []
}

function getImpactLevel(score) {
  if (score >= 8) return { label: '发布', color: '#10b981', bg: '#ecfdf5', icon: '🔴' }
  if (score >= 5) return { label: '观察', color: '#f59e0b', bg: '#fffbeb', icon: '🟡' }
  return { label: '忽略', color: '#9ca3af', bg: '#f9fafb', icon: '⚪' }
}

function getNewsTypeLabel(type) {
  const map = {
    new_model: '新模型', new_capability: '新能力', agent_update: 'Agent更新',
    api_update: 'API更新', open_access: '开放体验', restriction_change: '限制变更',
    benchmark: 'Benchmark', ecosystem: '生态更新'
  }
  return map[type] || type || '-'
}

function qualityLabel(score) {
  if (score >= 80) return { text: '优质', color: 'success' }
  if (score >= 60) return { text: '良好', color: 'info' }
  if (score >= 40) return { text: '一般', color: 'warning' }
  return { text: '低质', color: 'default' }
}

function getHighlights(row) {
  const cc = row.capability_change
  if (!cc || !cc.highlights || cc.highlights.length === 0) return []
  return cc.highlights
}

// 来源编辑等级
function getTierInfo(sourceName) {
  // 从前端映射快速判断（后端有完整数据）
  const sTier = ['OpenAI Blog', 'Anthropic News', 'Google DeepMind', 'Meta AI', 'xAI', 'Mistral AI']
  const aTier = ['DeepSeek', 'Perplexity', 'Cursor', 'Hugging Face', 'Qwen Blog', 'Google AI Blog', '月之暗面 Kimi Blog']
  const cTier = ['GitHub Changelog', 'Product Hunt AI', 'Runway']
  if (sTier.includes(sourceName)) return { tier: 'S', label: '核心', color: '#7c3aed', bg: '#f5f3ff' }
  if (aTier.includes(sourceName)) return { tier: 'A', label: '重要', color: '#2563eb', bg: '#eff6ff' }
  if (cTier.includes(sourceName)) return { tier: 'C', label: '背景', color: '#9ca3af', bg: '#f9fafb' }
  return { tier: 'B', label: '信号', color: '#0891b2', bg: '#ecfeff' }
}

// 编辑评分等级
function getEditorialLevel(score) {
  if (score >= 60) return { label: '高价值', color: '#10b981', bg: '#ecfdf5' }
  if (score >= 40) return { label: '中等', color: '#f59e0b', bg: '#fffbeb' }
  return { label: '低价值', color: '#9ca3af', bg: '#f9fafb' }
}

// ESS v2 — Bucket helpers
function getBucketLabel(bucket) {
  const map = {
    headline: '头条', major_release: '重大发布', capability: '能力变化',
    research: '研究前沿', industry: '行业动态', dev_tools: '开发者工具',
    infrastructure: '基础设施', archive: '存档'
  }
  return map[bucket] || bucket
}
function getBucketColor(bucket) {
  const map = {
    headline: '#dc2626', major_release: '#7c3aed', capability: '#2563eb',
    research: '#0891b2', industry: '#059669', dev_tools: '#6b7280',
    infrastructure: '#9ca3af', archive: '#d1d5db'
  }
  return map[bucket] || '#9ca3af'
}

// ESS v3 — 从 narrative 中查找实体的 Story
function getStoryForEntity(entity) {
  if (!groupedData.value?.narratives) return ''
  for (const n of groupedData.value.narratives) {
    for (const s of n.stories || []) {
      if (s.entity === entity) return s.story
    }
  }
  return ''
}

function openSourceUrl(url) {
  if (url) window.open(url, '_blank')
}

function copySourceUrl(url) {
  if (!url) return
  navigator.clipboard.writeText(url).then(() => {
    message.success('链接已复制')
  }).catch(() => {
    message.warning('复制失败，请手动复制')
  })
}

// ====== 数据加载 ======

async function loadCategories() {
  try {
    const res = await getAllCategories()
    categories.value = res.data || []
  } catch (e) { /* ignore */ }
}

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      size: 200,  // 取足够多以支持客户端筛选
      status: 'draft',
      sort: '-editorial_score'
    }
    if (searchKeyword.value) params.q = searchKeyword.value
    if (categoryFilter.value) params.category = categoryFilter.value
    if (sourceFilter.value) params.source = sourceFilter.value

    const res = await getArticles(params)
    const allItems = res.data.items

    // 计算来源分布统计
    const tc = { S: 0, A: 0, B: 0, C: 0, D: 0 }
    allItems.forEach(item => {
      const ti = getTierInfo(item.source_name)
      tc[ti.tier] = (tc[ti.tier] || 0) + 1
    })
    tierStats.value = tc

    // 编辑价值筛选
    let filtered = allItems
    if (editorialFilter.value === 'high') {
      filtered = allItems.filter(item => (item.editorial_score || 0) >= 60)
    } else if (editorialFilter.value === 'mid') {
      filtered = allItems.filter(item => {
        const s = item.editorial_score || 0
        return s >= 40 && s < 60
      })
    } else if (editorialFilter.value === 'low') {
      filtered = allItems.filter(item => (item.editorial_score || 0) < 40)
    }

    total.value = filtered.length
    // 分页
    const start = (page.value - 1) * pageSize.value
    list.value = filtered.slice(start, start + pageSize.value)

    // 动态来源列表
    const sources = new Set()
    allItems.forEach(item => { if (item.source_name) sources.add(item.source_name) })
    sourceOptions.value = [
      { label: '全部来源', value: null },
      ...Array.from(sources).map(s => ({ label: s, value: s }))
    ]
  } catch (e) {
    message.error(e.message || '加载失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() { page.value = 1; loadData() }
function handleReset() { searchKeyword.value = ''; categoryFilter.value = null; sourceFilter.value = null; page.value = 1; loadData() }

// ESS v2 — 分组加载
async function loadGroupedData() {
  groupedLoading.value = true
  try {
    const res = await getGroupedReview(activeBucket.value)
    groupedData.value = res.data
  } catch (e) {
    message.error(e.message || '加载失败')
  } finally {
    groupedLoading.value = false
  }
}

function switchView(mode) {
  viewMode.value = mode
  if (mode === 'flat') loadData()
  else if (mode === 'narrative' || mode === 'grouped' || mode === 'events') loadGroupedData()
}

function filterByBucket(bucket) {
  activeBucket.value = activeBucket.value === bucket ? null : bucket
  loadGroupedData()
}

// ====== 操作 ======

async function handleApprove(row) {
  try {
    await approveArticle(row.id)
    message.success('审核通过，已进入待编辑列表')
    loadData()
  } catch (e) {
    message.error(e.message || '操作失败')
  }
}

function handleRejectClick(row) {
  rejectTarget.value = row
  rejectReason.value = ''
  showRejectDialog.value = true
}

async function confirmReject() {
  if (!rejectTarget.value) return
  try {
    await rejectArticle(rejectTarget.value.id, rejectReason.value || undefined)
    message.success('已驳回')
    showRejectDialog.value = false
    rejectTarget.value = null
    loadData()
  } catch (e) {
    message.error(e.message || '操作失败')
  }
}

function handleEdit(row) {
  router.push(`/articles/edit/${row.id}`)
}

async function handleBatchApprove() {
  if (selectedIds.value.length === 0) { message.warning('请先选择文章'); return }
  dialog.info({
    title: '确认批量通过',
    content: `确定要通过选中的 ${selectedIds.value.length} 篇文章吗？它们将进入「待编辑」列表`,
    positiveText: '通过',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await batchApproveArticles(selectedIds.value)
        message.success('批量通过完成')
        selectedIds.value = []
        loadData()
      } catch (e) { message.error(e.message || '操作失败') }
    }
  })
}

function handleCheck(id) {
  const idx = selectedIds.value.indexOf(id)
  if (idx >= 0) selectedIds.value.splice(idx, 1)
  else selectedIds.value.push(id)
}

function handleSelectAll() {
  if (selectedIds.value.length === list.value.length) {
    selectedIds.value = []
  } else {
    selectedIds.value = list.value.map(item => item.id)
  }
}

// ====== 预览 ======
const previewArticle = computed(() => list.value.find(item => item.id === previewId.value))

function handlePreview(id) {
  previewId.value = id
  showPreview.value = true
}

function handlePageChange(p) { page.value = p; loadData() }
function handlePageSizeChange(s) { pageSize.value = s; page.value = 1; loadData() }

onMounted(() => {
  loadCategories()
  loadGroupedData()
})
</script>

<template>
  <div class="review-page">
    <!-- 头部 -->
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">文章审核</h2>
        <p class="page-desc">采集后自动翻译标题和内容，审核通过后进入待编辑 → AI重写加工 → 发布上线</p>
      </div>
      <n-space>
        <n-button-group size="small">
          <n-button :type="viewMode === 'events' ? 'primary' : 'default'" @click="switchView('events')">
            事件
          </n-button>
          <n-button :type="viewMode === 'narrative' ? 'primary' : 'default'" @click="switchView('narrative')">
            叙事
          </n-button>
          <n-button :type="viewMode === 'grouped' ? 'primary' : 'default'" @click="switchView('grouped')">
            分组
          </n-button>
          <n-button :type="viewMode === 'flat' ? 'primary' : 'default'" @click="switchView('flat')">
            卡片
          </n-button>
        </n-button-group>
        <n-button
          type="primary"
          :disabled="selectedIds.length === 0"
          @click="handleBatchApprove"
        >
          批量通过 ({{ selectedIds.length }})
        </n-button>
        <n-button size="small" text @click="handleSelectAll" v-if="viewMode === 'flat'">
          {{ selectedIds.length === list.length ? '取消全选' : '全选' }}
        </n-button>
      </n-space>
    </div>

    <!-- 筛选栏 -->
    <n-card size="small" style="margin-bottom:16px">
      <n-space vertical :size="12">
        <!-- 编辑价值筛选标签 -->
        <n-space :size="8" align="center">
          <span style="font-size:13px;font-weight:600;color:var(--text-secondary)">编辑价值:</span>
          <n-button
            :type="editorialFilter === 'high' ? 'primary' : 'default'"
            size="small"
            @click="editorialFilter = 'high'; page = 1; loadData()"
          >
            高价值 ≥60
          </n-button>
          <n-button
            :type="editorialFilter === 'mid' ? 'primary' : 'default'"
            size="small"
            @click="editorialFilter = 'mid'; page = 1; loadData()"
          >
            中等 40-59
          </n-button>
          <n-button
            :type="editorialFilter === 'low' ? 'primary' : 'default'"
            size="small"
            @click="editorialFilter = 'low'; page = 1; loadData()"
          >
            低价值 &lt;40
          </n-button>
          <n-button
            :type="editorialFilter === 'all' ? 'primary' : 'default'"
            size="small"
            @click="editorialFilter = 'all'; page = 1; loadData()"
          >
            全部
          </n-button>
          <div style="flex:1"></div>
          <!-- 来源分布 -->
          <n-space :size="6">
            <span style="font-size:11px;color:var(--text-secondary)">来源分布:</span>
            <n-tag v-for="t in ['S','A','B','C','D']" :key="t" size="small" :bordered="false"
              :style="{background:t==='S'?'#f5f3ff':t==='A'?'#eff6ff':t==='B'?'#ecfeff':t==='C'?'#f9fafb':'#fef2f2',color:t==='S'?'#7c3aed':t==='A'?'#2563eb':t==='B'?'#0891b2':t==='C'?'#9ca3af':'#ef4444'}">
              {{ t }}级 {{ tierStats[t] || 0 }}
            </n-tag>
          </n-space>
        </n-space>

        <n-space :size="12" align="center" wrap>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索标题..."
            style="width: 220px"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix><search-outlined /></template>
          </n-input>
          <n-select v-model:value="categoryFilter" :options="categoryOptions" style="width: 150px" @update:value="handleSearch" />
          <n-select v-model:value="sourceFilter" :options="sourceOptions" style="width: 170px" @update:value="handleSearch" />
          <n-button type="primary" size="small" @click="handleSearch">搜索</n-button>
          <n-button size="small" @click="handleReset">重置</n-button>
          <div style="flex:1"></div>
          <span style="font-size:13px;color:var(--text-secondary)">共 {{ total }} 篇</span>
        </n-space>
      </n-space>
    </n-card>

    <!-- 事件视图 -->
    <div v-if="viewMode === 'events'">
      <div v-if="groupedData && groupedData.strategic_events && groupedData.strategic_events.length" class="events-section">
        <h3 class="narrative-title">Strategic Events</h3>
        <div class="events-list">
          <div
            v-for="event in groupedData.strategic_events"
            :key="event.entity + '-' + event.event_type"
            class="event-card"
          >
            <!-- 头部 -->
            <div class="event-header">
              <span class="event-confidence" :style="{ color: event.confidence >= 75 ? '#10b981' : event.confidence >= 50 ? '#f59e0b' : '#9ca3af' }">
                {{ event.confidence >= 75 ? '★★★' : event.confidence >= 50 ? '★★☆' : '★☆☆' }}
                置信度 {{ event.confidence }}%
              </span>
              <span class="event-entity">{{ event.entity }}</span>
              <span class="event-count">{{ event.article_count }} 条证据</span>
            </div>

            <!-- 事件标题 -->
            <h3 class="event-title">{{ event.title }}</h3>

            <!-- 五个编辑问题 -->
            <div class="event-questions">
              <div class="eq-row">
                <span class="eq-label">为什么今天？</span>
                <span class="eq-answer">{{ event.why_today }}</span>
              </div>
              <div class="eq-row">
                <span class="eq-label">为什么重要？</span>
                <span class="eq-answer">{{ event.why_important }}</span>
              </div>
              <div class="eq-row">
                <span class="eq-label">改变了什么？</span>
                <span class="eq-answer">{{ event.whats_changing }}</span>
              </div>
              <div class="eq-row">
                <span class="eq-label">下一步？</span>
                <span class="eq-answer">{{ event.whats_next }}</span>
              </div>
            </div>

            <!-- 证据列表 -->
            <div class="event-evidence">
              <div class="evidence-label">Evidence</div>
              <div class="evidence-items">
                <span
                  v-for="ev in event.evidence"
                  :key="ev.id"
                  class="evidence-item"
                  :style="{ borderLeftColor: getBucketColor(ev.bucket) }"
                >
                  {{ ev.title }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="groupedLoading" class="loading-state">
        <n-spin size="large" /><p>加载中...</p>
      </div>
      <div v-else class="empty-state">
        <p>暂无足够的文章来识别战略事件（需要同一实体 >= 2 篇）</p>
      </div>
    </div>

    <!-- 叙事视图 -->
    <div v-if="viewMode === 'narrative'">
      <div v-if="groupedData && groupedData.narratives && groupedData.narratives.length" class="narrative-section">
        <h3 class="narrative-title">Today's Narrative</h3>
        <div class="narrative-list">
          <div
            v-for="n in groupedData.narratives"
            :key="n.trend_key"
            class="narrative-card"
          >
            <div class="narrative-header">
              <span class="narrative-trend">{{ n.trend_label || n.trend_key }}</span>
              <span class="narrative-stats">{{ n.total_entities }} 实体 · {{ n.total_evidence }} 证据</span>
            </div>
            <p v-if="n.trend_narrative" class="narrative-insight">{{ n.trend_narrative }}</p>
            <div class="narrative-stories">
              <div
                v-for="s in n.stories"
                :key="s.entity"
                class="narrative-story-item"
                :class="'sig-' + s.significance"
              >
                <span class="story-sig">
                  {{ s.significance === 'critical' ? '★★★' : s.significance === 'high' ? '★★☆' : '★☆☆' }}
                </span>
                <span class="story-text">{{ s.story }}</span>
                <span class="story-evidence">{{ s.evidence_count }} 条证据</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="groupedLoading" class="loading-state">
        <n-spin size="large" /><p style="margin-top:12px">加载中...</p>
      </div>
      <div v-else class="empty-state">
        <p>暂无叙事数据</p>
      </div>
    </div>

    <!-- 分组视图 -->
    <div v-if="viewMode === 'grouped'">
      <!-- Top Pick -->
      <div v-if="groupedData && groupedData.top_pick" class="top-pick-card">
        <div class="top-pick-badge">Today's Top Pick</div>
        <h2 class="top-pick-title">{{ groupedData.top_pick.title }}</h2>
        <div class="top-pick-questions">
          <div class="tpq-row">
            <span class="tpq-label">为什么重要</span>
            <span class="tpq-answer">{{ groupedData.top_pick.why_important }}</span>
          </div>
          <div class="tpq-row">
            <span class="tpq-label">改变了什么</span>
            <span class="tpq-answer">{{ groupedData.top_pick.whats_changing }}</span>
          </div>
          <div class="tpq-row">
            <span class="tpq-label">置信度</span>
            <span class="tpq-answer" :style="{ color: groupedData.top_pick.confidence >= 75 ? '#10b981' : '#f59e0b' }">
              {{ groupedData.top_pick.confidence }}%
            </span>
          </div>
        </div>
        <div class="top-pick-evidence">
          <span class="tp-ev-label">Evidence</span>
          <n-space :size="4">
            <n-tag v-for="ev in groupedData.top_pick.evidence.slice(0, 5)" :key="ev.id" size="small">
              {{ ev.title?.slice(0, 60) }}{{ (ev.title || '').length > 60 ? '...' : '' }}
            </n-tag>
          </n-space>
        </div>
      </div>

      <!-- Bucket 过滤栏 -->
      <n-card v-if="groupedData" size="small" style="margin-bottom:12px">
        <n-space :size="8" align="center">
          <span style="font-size:12px;color:var(--text-secondary)">栏目:</span>
          <n-button
            size="tiny"
            :type="!activeBucket ? 'primary' : 'default'"
            @click="activeBucket = null; loadGroupedData()"
          >全部</n-button>
          <n-button
            v-for="b in groupedData.buckets"
            :key="b.key"
            size="tiny"
            :type="activeBucket === b.key ? 'primary' : 'default'"
            @click="filterByBucket(b.key)"
          >{{ b.icon }} {{ b.label }}</n-button>
          <div style="flex:1"></div>
          <span style="font-size:12px;color:var(--text-secondary)">
            {{ groupedData.total_groups }} 个编辑单元 · {{ groupedData.total_articles }} 篇文章
          </span>
        </n-space>
      </n-card>

      <div v-if="groupedLoading" class="loading-state">
        <n-spin size="large" /><p>加载中...</p>
      </div>

      <!-- 实体分组 -->
      <div v-else-if="groupedData && groupedData.groups.length" class="grouped-sections">
        <section v-for="group in groupedData.groups" :key="group.entity" class="entity-group">
          <div class="group-header">
            <div class="group-header-left">
              <h3 class="group-entity-name">
                <span v-if="group.story_type" class="story-type-badge">Story</span>
                {{ group.story || (group.entity + ' Today') }}
              </h3>
              <span class="group-count">{{ group.article_count }} 条证据</span>
              <span v-if="group.confidence" class="group-conf" :style="{ color: group.confidence >= 75 ? '#10b981' : '#f59e0b' }">
                {{ group.confidence }}%
              </span>
            </div>
            <n-button size="small" type="primary" @click="group.articles.forEach(a => handleApprove(a))">
              全部通过
            </n-button>
          </div>
          <!-- Why Important -->
          <div v-if="group.why_important" class="group-story">
            为什么重要：{{ group.why_important }}
          </div>

          <div class="group-articles">
            <article
              v-for="a in group.articles"
              :key="a.id"
              class="group-article-item"
            >
              <div class="ga-left">
                <span
                  class="bucket-dot"
                  :style="{background: getBucketColor(a.editorial_bucket)}"
                ></span>
                <div class="ga-info">
                  <h4 class="ga-title" @click="handlePreview(a.id)">{{ getTranslatedTitle(a) || a.title }}</h4>
                  <div class="ga-meta">
                    <span class="ga-bucket-label">{{ getBucketLabel(a.editorial_bucket) }}</span>
                    <span v-if="a.recommendation_reasons && a.recommendation_reasons.length" class="ga-reasons">
                      <n-tag
                        v-for="(r, i) in a.recommendation_reasons.slice(0, 3)"
                        :key="i"
                        size="tiny"
                        :bordered="false"
                        style="background:#f0fdf4;color:#16a34a"
                      >{{ r }}</n-tag>
                    </span>
                    <span v-if="a.source_url" class="ga-source-link">
                      <n-button size="tiny" text type="primary" @click="openSourceUrl(a.source_url)">原文</n-button>
                    </span>
                  </div>
                </div>
              </div>
              <n-space :size="4">
                <n-button size="tiny" type="primary" @click="handleApprove(a)">通过</n-button>
                <n-button size="tiny" @click="handleRejectClick(a)">驳回</n-button>
                <n-button size="tiny" text @click="handleEdit(a)">编辑</n-button>
              </n-space>
            </article>
          </div>
        </section>
      </div>

      <div v-else-if="!groupedLoading" class="empty-state">
        <p>暂无待审核内容</p>
      </div>
    </div>

    <!-- 卡片视图 (flat) -->
    <div v-if="viewMode === 'flat' && loading" class="loading-state">
      <n-spin size="large" /><p style="margin-top:12px">加载中...</p>
    </div>

    <div v-else-if="viewMode === 'flat' && list.length === 0" class="empty-state">
      <p>暂无待审核文章</p>
    </div>

    <div v-else-if="viewMode === 'flat'" class="review-cards">
      <article
        v-for="article in list"
        :key="article.id"
        class="review-card"
        :class="{ selected: selectedIds.includes(article.id) }"
      >
        <!-- 选择框 -->
        <div class="card-check" @click.stop="handleCheck(article.id)">
          <div class="check-box" :class="{ checked: selectedIds.includes(article.id) }">
            <span v-if="selectedIds.includes(article.id)">✓</span>
          </div>
        </div>

        <!-- 图片区域 -->
        <div class="card-image" @click="handlePreview(article.id)">
          <img
            v-if="getImages(article).length > 0"
            :src="getImages(article)[0]"
            :alt="getTranslatedTitle(article) || article.title"
            @error="$event.target.style.display='none'"
          />
          <div v-else class="no-image">
            <span>无图片</span>
          </div>

          <!-- 等级角标 -->
          <div
            class="impact-badge"
            :style="{ background: getImpactLevel(article.impact_score).bg, color: getImpactLevel(article.impact_score).color }"
          >
            {{ getImpactLevel(article.impact_score).icon }}
            {{ getImpactLevel(article.impact_score).label }}
            · {{ article.impact_score || 0 }}分
          </div>
        </div>

        <!-- 信息区域 -->
        <div class="card-body">
          <!-- 标题 -->
          <div class="card-title-row">
            <h3 class="card-title-zh" @click="handlePreview(article.id)">
              {{ getTranslatedTitle(article) || article.title }}
            </h3>
            <span v-if="getTranslatedTitle(article) && getOriginalTitle(article) !== getTranslatedTitle(article)" class="card-title-en">
              {{ getOriginalTitle(article) }}
            </span>
          </div>

          <!-- 来源 -->
          <div class="card-source">
            <span
              class="tier-badge"
              :style="{background: getTierInfo(article.source_name).bg, color: getTierInfo(article.source_name).color}"
            >
              {{ getTierInfo(article.source_name).tier }}级
            </span>
            <span class="source-name">{{ article.source_name || '未知来源' }}</span>
            <template v-if="article.source_url">
              <n-button size="tiny" text type="primary" @click="openSourceUrl(article.source_url)">
                <link-outlined /> 打开原文
              </n-button>
              <n-button size="tiny" text @click="copySourceUrl(article.source_url)">复制链接</n-button>
            </template>
          </div>

          <!-- AI 评分条 -->
          <div class="card-scores">
            <n-tag
              size="small"
              :style="{background:getEditorialLevel(article.editorial_score).bg, color:getEditorialLevel(article.editorial_score).color, border:'none'}"
            >
              编辑 {{ article.editorial_score || 0 }}分
            </n-tag>
            <n-tag size="small" :type="qualityLabel(article.quality_score).color">
              质量 {{ article.quality_score || 0 }}
            </n-tag>
            <n-tag size="small" :type="article.relevance_score >= 70 ? 'success' : article.relevance_score >= 50 ? 'warning' : 'default'">
              相关 {{ article.relevance_score || 0 }}
            </n-tag>
            <n-tag v-if="article.news_type" size="small" type="info">
              {{ getNewsTypeLabel(article.news_type) }}
            </n-tag>
            <span v-if="article.created_at" class="card-date">{{ new Date(article.created_at).toLocaleDateString() }}</span>
          </div>

          <!-- AI 摘要 -->
          <div v-if="article.ai_summary" class="card-summary">
            📝 {{ article.ai_summary }}
          </div>

          <!-- 关键亮点 -->
          <div v-if="getHighlights(article).length" class="card-highlights">
            <div class="hl-label">关键变化</div>
            <div class="hl-list">
              <span v-for="(hl, i) in getHighlights(article)" :key="i" class="hl-tag">{{ hl }}</span>
            </div>
          </div>

          <!-- 内容预览 -->
          <div class="card-preview" @click="handlePreview(article.id)">
            {{ (article.content || article.summary || '').slice(0, 200) }}{{ (article.content || '').length > 200 ? '...' : '' }}
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="card-actions">
          <n-button size="small" type="primary" @click="handleApprove(article)">
            <check-circle-outlined /> 通过
          </n-button>
          <n-button size="small" @click="handleRejectClick(article)">
            <close-circle-outlined /> 驳回
          </n-button>
          <n-button size="small" text @click="handleEdit(article)">
            <edit-outlined /> 编辑
          </n-button>
        </div>
      </article>
    </div>

    <!-- 分页 -->
    <div v-if="total > pageSize" class="pagination-wrapper">
      <n-pagination
        v-model:page="page"
        :page-size="pageSize"
        :total="total"
        :page-sizes="[12, 24, 48]"
        show-size-picker
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
      />
    </div>

    <!-- 预览弹窗 -->
    <n-modal v-model:show="showPreview" title="文章完整预览" style="width: 800px">
      <n-card v-if="previewArticle" style="max-height:70vh;overflow-y:auto">
        <div v-if="getImages(previewArticle).length" style="margin-bottom:16px">
          <n-image
            v-for="(img, i) in getImages(previewArticle).slice(0, 3)"
            :key="i"
            :src="img"
            style="width:200px;height:120px;object-fit:cover;margin-right:8px;border-radius:8px"
          />
        </div>
        <h2 style="margin-bottom:4px">{{ getTranslatedTitle(previewArticle) || previewArticle.title }}</h2>
        <p v-if="getTranslatedTitle(previewArticle)" style="color:var(--text-secondary);font-size:13px;margin-bottom:12px">
          {{ getOriginalTitle(previewArticle) }}
        </p>
        <n-space :size="8" style="margin-bottom:12px">
          <n-tag size="small" :style="{color:getImpactLevel(previewArticle.impact_score).color}">
            {{ getImpactLevel(previewArticle.impact_score).icon }} {{ getImpactLevel(previewArticle.impact_score).label }} {{ previewArticle.impact_score || 0 }}分
          </n-tag>
          <n-tag size="small">{{ previewArticle.source_name }}</n-tag>
          <n-tag size="small" type="info">质量{{ previewArticle.quality_score || 0 }} 相关{{ previewArticle.relevance_score || 0 }}</n-tag>
        </n-space>
        <div v-if="previewArticle.ai_summary" style="padding:12px;background:var(--bg-tertiary,#f9fafb);border-radius:8px;margin-bottom:12px;font-size:14px;line-height:1.7">
          📝 {{ previewArticle.ai_summary }}
        </div>
        <div v-if="getHighlights(previewArticle).length" style="margin-bottom:12px">
          <strong style="font-size:13px">关键变化：</strong>
          <n-space :size="4" style="margin-top:4px">
            <n-tag v-for="(hl,i) in getHighlights(previewArticle)" :key="i" size="small" type="warning">{{ hl }}</n-tag>
          </n-space>
        </div>
        <n-divider />
        <div style="font-size:14px;line-height:1.9;white-space:pre-wrap;word-break:break-word">
          {{ previewArticle.content || previewArticle.summary || '无内容' }}
        </div>
        <div v-if="previewArticle.source_url" style="margin-top:16px">
          <a :href="previewArticle.source_url" target="_blank" style="color:var(--brand-primary)">查看原文 →</a>
        </div>
      </n-card>
    </n-modal>

    <!-- 驳回弹窗 -->
    <n-modal v-model:show="showRejectDialog" title="驳回理由" style="width:420px">
      <n-card>
        <p style="margin-bottom:12px">驳回「<strong>{{ rejectTarget?.title }}</strong>」</p>
        <n-input v-model:value="rejectReason" type="textarea" :rows="3" placeholder="驳回理由（选填）" />
        <n-space style="margin-top:16px" justify="end">
          <n-button @click="showRejectDialog = false">取消</n-button>
          <n-button type="error" @click="confirmReject">确认驳回</n-button>
        </n-space>
      </n-card>
    </n-modal>
  </div>
</template>

<style scoped>
.review-page {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.page-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
}

/* 卡片网格 */
.review-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
}

.review-card {
  position: relative;
  background: var(--bg-card, #fff);
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
}

.review-card:hover {
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  border-color: var(--brand-primary, #6366f1);
}

.review-card.selected {
  border-color: var(--brand-primary, #6366f1);
  box-shadow: 0 0 0 2px rgba(99,102,241,0.15);
}

/* 选择框 */
.card-check {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 2;
  cursor: pointer;
}

.check-box {
  width: 22px;
  height: 22px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  font-size: 12px;
  transition: all 0.15s;
}

.check-box.checked {
  background: var(--brand-primary, #6366f1);
  border-color: var(--brand-primary, #6366f1);
  color: #fff;
}

/* 图片 */
.card-image {
  position: relative;
  height: 180px;
  background: var(--bg-tertiary, #f3f4f6);
  cursor: pointer;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  font-size: 14px;
}

.impact-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

/* 卡片主体 */
.card-body {
  padding: 14px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card-title-row {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.card-title-zh {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.5;
  margin: 0;
  cursor: pointer;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: var(--text-primary);
}

.card-title-zh:hover {
  color: var(--brand-primary, #6366f1);
}

.card-title-en {
  font-size: 12px;
  color: #9ca3af;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-source {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.source-name {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

.tier-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
  letter-spacing: 0.3px;
}

.card-scores {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.card-date {
  font-size: 11px;
  color: #9ca3af;
  margin-left: auto;
}

.card-summary {
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-highlights {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hl-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.hl-list {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.hl-tag {
  font-size: 11px;
  padding: 2px 8px;
  background: #fef3c7;
  color: #92400e;
  border-radius: 4px;
}

.card-preview {
  font-size: 12px;
  line-height: 1.6;
  color: #9ca3af;
  cursor: pointer;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  border-top: 1px solid var(--border-color, #f3f4f6);
  padding-top: 8px;
}

.card-preview:hover {
  color: var(--text-secondary);
}

/* 操作按钮 */
.card-actions {
  padding: 10px 14px;
  border-top: 1px solid var(--border-color, #f3f4f6);
  display: flex;
  gap: 8px;
}

/* 加载 & 空状态 */
.loading-state, .empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

/* 叙事卡片 */
.narrative-section {
  margin-bottom: 24px;
}

.narrative-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 16px 0;
  color: var(--text-primary);
}

.narrative-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.narrative-card {
  background: var(--bg-card, #fff);
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 12px;
  padding: 16px;
}

.narrative-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.narrative-trend {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.narrative-stats {
  font-size: 12px;
  color: var(--text-secondary);
}

.narrative-insight {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0 0 12px 0;
}

.narrative-stories {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.narrative-story-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  background: var(--bg-tertiary, #f9fafb);
}

.narrative-story-item.sig-critical {
  border-left: 3px solid #dc2626;
}

.narrative-story-item.sig-high {
  border-left: 3px solid #f59e0b;
}

.story-sig {
  font-size: 12px;
  flex-shrink: 0;
}

.story-text {
  font-size: 13px;
  color: var(--text-primary);
  flex: 1;
}

.story-evidence {
  font-size: 11px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

/* 战略事件 */
.events-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.event-card {
  background: var(--bg-card, #fff);
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 12px;
  padding: 20px;
}

.event-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.event-confidence {
  font-size: 13px;
  font-weight: 600;
}

.event-entity {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.event-count {
  font-size: 12px;
  color: var(--text-secondary);
  margin-left: auto;
}

.event-title {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.5;
  margin: 0 0 16px 0;
  color: var(--text-primary);
}

.event-questions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px;
  background: var(--bg-tertiary, #f9fafb);
  border-radius: 8px;
}

.eq-row {
  display: flex;
  gap: 12px;
  font-size: 13px;
  line-height: 1.6;
}

.eq-label {
  font-weight: 600;
  color: var(--text-secondary);
  flex-shrink: 0;
  min-width: 80px;
}

.eq-answer {
  color: var(--text-primary);
}

.event-evidence {
  border-top: 1px solid var(--border-color, #e5e7eb);
  padding-top: 12px;
}

.evidence-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.evidence-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.evidence-item {
  font-size: 12px;
  color: var(--text-secondary);
  padding: 4px 8px;
  border-left: 3px solid #9ca3af;
  background: var(--bg-tertiary, #f9fafb);
  border-radius: 0 4px 4px 0;
}

/* 分组视图 */
.grouped-sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Top Pick */
.top-pick-card {
  background: var(--bg-card, #fff);
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
}

.top-pick-badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  color: #dc2626;
  background: #fef2f2;
  padding: 2px 10px;
  border-radius: 999px;
  margin-bottom: 8px;
}

.top-pick-title {
  font-size: 20px;
  font-weight: 700;
  margin: 8px 0 16px;
  color: var(--text-primary);
  line-height: 1.4;
}

.top-pick-questions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px;
  background: var(--bg-tertiary, #f9fafb);
  border-radius: 8px;
}

.tpq-row {
  display: flex;
  gap: 12px;
  font-size: 13px;
  line-height: 1.6;
}

.tpq-label {
  font-weight: 600;
  color: var(--text-secondary);
  flex-shrink: 0;
  min-width: 80px;
}

.tpq-answer {
  color: var(--text-primary);
}

.top-pick-evidence {
  border-top: 1px solid var(--border-color, #e5e7eb);
  padding-top: 12px;
}

.tp-ev-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
  display: block;
}

/* Story badge */
.story-type-badge {
  font-size: 10px;
  font-weight: 700;
  color: #7c3aed;
  background: #f5f3ff;
  padding: 2px 8px;
  border-radius: 4px;
  margin-right: 8px;
  text-transform: uppercase;
   letter-spacing: 0.5px;
 }

 .entity-group {
  background: var(--bg-card, #fff);
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 12px;
  overflow: hidden;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: var(--bg-tertiary, #f9fafb);
  border-bottom: 1px solid var(--border-color, #e5e7eb);
}

.group-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.group-entity-name {
  font-size: 16px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.group-count {
  font-size: 12px;
  color: var(--text-secondary);
}

.group-conf {
  font-size: 11px;
  font-weight: 600;
}

.group-story {
  padding: 8px 18px;
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  background: var(--bg-tertiary, #f9fafb);
  border-bottom: 1px solid var(--border-color, #e5e7eb);
}

.group-articles {
  display: flex;
  flex-direction: column;
}

.group-article-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 18px;
  border-bottom: 1px solid var(--border-color, #f3f4f6);
  transition: background 0.15s;
}

.group-article-item:last-child {
  border-bottom: none;
}

.group-article-item:hover {
  background: var(--bg-hover, #f9fafb);
}

.ga-left {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.bucket-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 6px;
  flex-shrink: 0;
}

.ga-info {
  min-width: 0;
  flex: 1;
}

.ga-title {
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 4px 0;
  cursor: pointer;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: var(--text-primary);
}

.ga-title:hover {
  color: var(--brand-primary, #6366f1);
}

.ga-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.ga-bucket-label {
  font-size: 11px;
  color: var(--text-secondary);
  padding: 1px 6px;
  background: var(--bg-tertiary, #f3f4f6);
  border-radius: 4px;
}

.ga-reasons {
  display: flex;
  gap: 4px;
}

.ga-source-link {
  font-size: 12px;
}

/* 响应式 */
@media (max-width: 768px) {
  .review-cards {
    grid-template-columns: 1fr;
  }
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
