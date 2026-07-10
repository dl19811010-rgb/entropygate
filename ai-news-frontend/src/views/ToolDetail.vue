<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NTag, NButton, NCard } from 'naive-ui'
import { ArrowLeftOutlined, LinkOutlined, CheckCircleOutlined, ExclamationCircleOutlined, CloseCircleOutlined, InfoCircleOutlined, ClockCircleOutlined } from '@vicons/antd'
import { logError } from '@/utils/log'

const route = useRoute()
const router = useRouter()

const tool = ref(null)
const loading = ref(true)

const availabilityLabels = {
  available: '国内可用',
  restricted: '部分受限',
  blocked: '已被封禁',
  enterprise_only: '仅企业版',
  uncertain: '待核实'
}

const availabilityColors = {
  available: 'success',
  restricted: 'warning',
  blocked: 'error',
  enterprise_only: 'info',
  uncertain: 'default'
}

const availabilityIconMap = {
  available: CheckCircleOutlined,
  restricted: ExclamationCircleOutlined,
  blocked: CloseCircleOutlined,
  enterprise_only: InfoCircleOutlined,
  uncertain: ClockCircleOutlined
}

async function loadTool() {
  loading.value = true
  try {
    const { getToolBySlug } = await import('@/api/tool')
    const res = await getToolBySlug(route.params.slug)
    tool.value = res
  } catch (e) {
    logError('加载工具详情失败:', e)
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

onMounted(() => {
  loadTool()
})

watch(() => route.params.slug, () => {
  loadTool()
})
</script>

<template>
  <div class="tool-detail-page">
    <div class="page-inner">
      <button class="back-btn" @click="router.back()">
        <arrow-left-outlined />
        <span>返回工具库</span>
      </button>

      <div v-if="loading" class="loading-state">
        <p>加载中...</p>
      </div>

      <div v-else-if="tool" class="tool-detail">
        <div class="tool-header">
          <div class="tool-logo-lg">
            <span class="tool-letter">{{ tool.name ? tool.name.charAt(0) : '?' }}</span>
          </div>
          <div class="tool-head-info">
            <h1 class="tool-name">{{ tool.name }}</h1>
            <div class="tool-tags">
              <span v-if="tool.category_name" class="tool-category">{{ tool.category_name }}</span>
              <n-tag
                v-if="tool.pricing_model"
                size="small"
                round
              >
                {{ tool.pricing_model }}
              </n-tag>
              <span
                class="avail-badge"
                :class="tool.availability_status || 'uncertain'"
              >
                <component :is="availabilityIconMap[tool.availability_status] || ClockCircleOutlined" />
                {{ availabilityLabels[tool.availability_status] || '待核实' }}
              </span>
            </div>
            <p v-if="tool.description" class="tool-desc">{{ tool.description }}</p>
            <div class="tool-actions">
              <n-button
                v-if="tool.website_url"
                type="primary"
                size="large"
                @click="openWebsite(tool.website_url)"
              >
                <link-outlined style="margin-right:6px" />
                访问官网
              </n-button>
            </div>
          </div>
        </div>

        <div class="tool-body">
          <div class="main-section">
            <div v-if="tool.availability" class="info-card">
              <h2 class="card-title">可用性状态</h2>
              <div class="avail-detail">
                <div class="avail-status-row">
                  <span class="label">地区</span>
                  <span class="value">{{ tool.availability.region || '中国大陆' }}</span>
                </div>
                <div class="avail-status-row">
                  <span class="label">状态</span>
                  <span
                    class="status-tag"
                    :class="tool.availability.status || 'uncertain'"
                  >
                    {{ availabilityLabels[tool.availability.status] || '待核实' }}
                  </span>
                </div>
                <div v-if="tool.availability.access_method" class="avail-status-row">
                  <span class="label">访问方式</span>
                  <span class="value">{{ tool.availability.access_method }}</span>
                </div>
                <div v-if="tool.availability.restrictions" class="avail-status-row">
                  <span class="label">限制说明</span>
                  <span class="value">{{ tool.availability.restrictions }}</span>
                </div>
                <div v-if="tool.availability.last_verified_at" class="avail-status-row">
                  <span class="label">核实时间</span>
                  <span class="value">{{ formatDate(tool.availability.last_verified_at) }}</span>
                </div>
              </div>
            </div>

            <div v-if="tool.alternatives && tool.alternatives.length > 0" class="info-card">
              <h2 class="card-title">替代方案</h2>
              <div class="alt-list">
                <div
                  v-for="alt in tool.alternatives"
                  :key="alt.id"
                  class="alt-item"
                  @click="router.push(`/tools/${alt.alternative_tool?.slug}`)"
                >
                  <div class="alt-logo">
                    {{ alt.alternative_tool?.name?.charAt(0) || '?' }}
                  </div>
                  <div class="alt-info">
                    <h4>{{ alt.alternative_tool?.name }}</h4>
                    <p v-if="alt.comparison_summary">{{ alt.comparison_summary }}</p>
                  </div>
                  <span v-if="alt.is_recommended" class="recommend-badge">推荐</span>
                </div>
              </div>
            </div>
          </div>

          <div class="side-section">
            <div class="info-card">
              <h2 class="card-title">基本信息</h2>
              <div class="info-list">
                <div v-if="tool.company" class="info-row">
                  <span class="label">开发商</span>
                  <span class="value">{{ tool.company }}</span>
                </div>
                <div v-if="tool.launch_date" class="info-row">
                  <span class="label">发布时间</span>
                  <span class="value">{{ formatDate(tool.launch_date) }}</span>
                </div>
                <div v-if="tool.status" class="info-row">
                  <span class="label">产品状态</span>
                  <span class="value">{{ tool.status }}</span>
                </div>
                <div class="info-row">
                  <span class="label">添加时间</span>
                  <span class="value">{{ formatDate(tool.created_at) }}</span>
                </div>
              </div>
            </div>

            <div v-if="tool.tags && tool.tags.length > 0" class="info-card">
              <h2 class="card-title">相关标签</h2>
              <div class="tag-list">
                <n-tag
                  v-for="tag in tool.tags"
                  :key="tag.id"
                  size="small"
                  round
                  style="margin: 4px"
                >
                  {{ tag.name }}
                </n-tag>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="not-found">
        <h2>工具不存在</h2>
        <n-button type="primary" @click="router.push('/tools')">
          返回工具库
        </n-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tool-detail-page {
  background: var(--bg-primary);
  min-height: calc(100vh - 64px);
}

.page-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 24px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  background: var(--bg-tertiary);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  margin-bottom: 24px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: var(--border-color);
  color: var(--text-primary);
}

.loading-state,
.not-found {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-tertiary);
}

.not-found h2 {
  color: var(--text-primary);
  margin-bottom: 16px;
}

.tool-detail {
  background: var(--bg-card);
  border-radius: 20px;
  overflow: hidden;
}

.tool-header {
  padding: 40px 48px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
  display: flex;
  gap: 28px;
  align-items: flex-start;
}

.tool-logo-lg {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.tool-letter {
  font-size: 36px;
  font-weight: 700;
  color: #fff;
}

.tool-head-info {
  flex: 1;
  min-width: 0;
}

.tool-name {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.tool-tags {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.tool-category {
  font-size: 13px;
  color: var(--text-secondary);
  background: var(--bg-card);
  padding: 4px 12px;
  border-radius: 20px;
}

.avail-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.avail-badge.available {
  background: #d1fae5;
  color: #059669;
}

.avail-badge.restricted {
  background: #fef3c7;
  color: #d97706;
}

.avail-badge.blocked {
  background: #fee2e2;
  color: #dc2626;
}

.avail-badge.enterprise_only {
  background: #e0e7ff;
  color: #4f46e5;
}

.avail-badge.uncertain {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.tool-desc {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 20px;
}

.tool-body {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 32px;
  padding: 32px 48px 48px;
}

.info-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
}

.info-card:last-child {
  margin-bottom: 0;
}

.card-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.avail-detail {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.avail-status-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.avail-status-row .label {
  font-size: 14px;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.avail-status-row .value {
  font-size: 14px;
  color: var(--text-primary);
  text-align: right;
}

.status-tag {
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-tag.available {
  background: #d1fae5;
  color: #059669;
}

.status-tag.restricted {
  background: #fef3c7;
  color: #d97706;
}

.status-tag.blocked {
  background: #fee2e2;
  color: #dc2626;
}

.status-tag.enterprise_only {
  background: #e0e7ff;
  color: #4f46e5;
}

.status-tag.uncertain {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.alt-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alt-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: #fff;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.alt-item:hover {
  border-color: var(--border-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.alt-logo {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  flex-shrink: 0;
}

.alt-info {
  flex: 1;
  min-width: 0;
}

.alt-info h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.alt-info p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
}

.recommend-badge {
  font-size: 11px;
  color: #fff;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
  flex-shrink: 0;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.info-row .label {
  font-size: 13px;
  color: var(--text-tertiary);
}

.info-row .value {
  font-size: 13px;
  color: var(--text-primary);
  text-align: right;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  margin: -4px;
}

@media (max-width: 960px) {
  .tool-body {
    grid-template-columns: 1fr;
  }

  .tool-header {
    padding: 28px 24px;
    flex-direction: column;
  }

  .tool-body {
    padding: 24px;
  }
}
</style>
