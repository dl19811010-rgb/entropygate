<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NGrid, NGi, NSpace, NTag, NIcon, NEmpty, NButton, NSpin } from 'naive-ui'
import {
  FileTextOutlined,
  ToolOutlined,
  FolderOpenOutlined,
  TagsOutlined,
  PlusOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  RiseOutlined,
  ThunderboltOutlined,
  DatabaseOutlined,
  BarChartOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  ClockCircleOutlined,
  PieChartOutlined,
  AppstoreOutlined,
  ApiOutlined,
  SafetyOutlined
} from '@vicons/antd'
import { getProductHealth, getRuntimeHealth } from '@/api/productDashboard'
import { logError } from '@/utils/log'

const router = useRouter()
const loading = ref(false)

const product = ref({
  metrics: {
    signals_24h: 0,
    signals_total: 0,
    facts_24h: 0,
    facts_total: 0,
    events_24h: 0,
    events_total: 0,
    capabilities_total: 0,
    articles_published_today: 0,
    review_queue: 0,
    active_sources: 0,
    last_refresh: '',
    headline: ''
  }
})

const runtime = ref({
  metrics: {
    replay_status: 'PASS',
    replay_deterministic_rate: 1.0,
    baseline_exists: false,
    certifications: 0,
    runtime_version: 'v1',
    runtime_api_changes: 0,
    platform_changes: 0,
    specification_age_days: 0,
    evidence_growth: 0
  }
})

// Product Health Cards
const productCards = computed(() => {
  const m = product.value.metrics || {}
  return [
    {
      title: 'Signals 24h',
      value: m.signals_24h || 0,
      total: m.signals_total || 0,
      icon: ThunderboltOutlined,
      color: '#f59e0b',
      bgColor: '#fffbeb'
    },
    {
      title: 'Facts 24h',
      value: m.facts_24h || 0,
      total: m.facts_total || 0,
      icon: FileTextOutlined,
      color: '#10b981',
      bgColor: '#ecfdf5'
    },
    {
      title: 'Events 24h',
      value: m.events_24h || 0,
      total: m.events_total || 0,
      icon: RiseOutlined,
      color: '#ef4444',
      bgColor: '#fef2f2'
    },
    {
      title: 'Capabilities',
      value: m.capabilities_total || 0,
      total: null,
      icon: AppstoreOutlined,
      color: '#6366f1',
      bgColor: '#eef2ff'
    }
  ]
})

// Operation Cards
const operationCards = computed(() => {
  const m = product.value.metrics || {}
  return [
    {
      title: '今日文章',
      value: m.articles_published_today || 0,
      icon: FileTextOutlined,
      action: () => router.push('/articles')
    },
    {
      title: '审核队列',
      value: m.review_queue || 0,
      icon: TagsOutlined,
      action: () => router.push('/articles/review')
    },
    {
      title: '活跃来源',
      value: m.active_sources || 0,
      icon: DatabaseOutlined,
      action: () => router.push('/sources')
    },
    {
      title: '数据采集',
      value: '监控',
      icon: BarChartOutlined,
      action: () => router.push('/crawler-monitor')
    }
  ]
})

// Runtime Health Cards
const runtimeCards = computed(() => {
  const m = runtime.value.metrics || {}
  return [
    {
      title: 'Replay',
      value: m.replay_status || 'PASS',
      detail: `确定性 ${Math.round((m.replay_deterministic_rate || 0) * 100)}%`,
      icon: CheckCircleOutlined,
      status: m.replay_status === 'PASS' ? 'success' : 'warning'
    },
    {
      title: 'Certifications',
      value: m.certifications || 0,
      detail: '已认证',
      icon: SafetyOutlined,
      status: 'success'
    },
    {
      title: 'Runtime API Changes',
      value: m.runtime_api_changes || 0,
      detail: '必须为 0',
      icon: ApiOutlined,
      status: m.runtime_api_changes === 0 ? 'success' : 'error'
    },
    {
      title: 'Platform Changes',
      value: m.platform_changes || 0,
      detail: '必须为 0',
      icon: PieChartOutlined,
      status: m.platform_changes === 0 ? 'success' : 'error'
    },
    {
      title: 'Spec Age',
      value: `${m.specification_age_days || 0}d`,
      detail: '自上次变更',
      icon: ClockCircleOutlined,
      status: 'default'
    },
    {
      title: 'Evidence',
      value: m.evidence_growth || 0,
      detail: '文件总数',
      icon: DatabaseOutlined,
      status: 'default'
    }
  ]
})

const quickActions = [
  { title: '新建文章', icon: FileTextOutlined, action: () => router.push('/articles/create') },
  { title: '新建工具', icon: ToolOutlined, action: () => router.push('/tools/create') },
  { title: '文章审核', icon: TagsOutlined, action: () => router.push('/articles/review') },
  { title: '采集监控', icon: DatabaseOutlined, action: () => router.push('/crawler-monitor') }
]

async function loadDashboard() {
  loading.value = true
  try {
    const [prodRes, runRes] = await Promise.all([
      getProductHealth(),
      getRuntimeHealth()
    ])
    product.value = prodRes.data || product.value
    runtime.value = runRes.data || runtime.value
  } catch (e) {
    logError('加载 Dashboard 失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboard()
})
</script>

<template>
  <div class="dashboard-page">
    <n-spin :show="loading">
      <n-space vertical :size="20">
        <!-- Welcome Banner -->
        <n-card class="welcome-card" :bordered="false">
          <div class="welcome-content">
            <div class="welcome-text">
              <h2 class="welcome-title">EntropyGate AI 运营中心</h2>
              <p class="welcome-desc">
                {{ product.metrics.headline || '实时监控产品健康与 Runtime 稳定性' }}
              </p>
            </div>
            <div class="welcome-meta" v-if="product.metrics.last_refresh">
              <n-tag size="small" type="info">
                更新于 {{ product.metrics.last_refresh ? new Date(product.metrics.last_refresh).toLocaleString('zh-CN') : '' }}
              </n-tag>
            </div>
          </div>
        </n-card>

        <!-- Product Health -->
        <div class="section-header">
          <h3 class="section-title">产品健康</h3>
        </div>
        <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen">
          <n-gi v-for="(card, index) in productCards" :key="index" :span="1">
            <n-card class="stat-card" :bordered="false" hoverable>
              <div class="stat-header">
                <div class="stat-icon" :style="{ background: card.bgColor, color: card.color }">
                  <n-icon size="20">
                    <component :is="card.icon" />
                  </n-icon>
                </div>
              </div>
              <div class="stat-body">
                <div class="stat-value">{{ card.value }}</div>
                <div class="stat-label">{{ card.title }}</div>
                <div class="stat-total" v-if="card.total !== null">
                  累计 {{ card.total }}
                </div>
              </div>
            </n-card>
          </n-gi>
        </n-grid>

        <!-- Operations -->
        <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen">
          <n-gi v-for="(card, index) in operationCards" :key="index" :span="1">
            <n-card class="op-card" :bordered="false" hoverable @click="card.action">
              <div class="op-content">
                <n-icon size="24" class="op-icon">
                  <component :is="card.icon" />
                </n-icon>
                <div class="op-value">{{ card.value }}</div>
                <div class="op-label">{{ card.title }}</div>
              </div>
            </n-card>
          </n-gi>
        </n-grid>

        <!-- Quick Actions + Runtime -->
        <n-grid :cols="3" :x-gap="16" :y-gap="16" responsive="screen">
          <n-gi :span="1">
            <n-card class="section-card" :bordered="false" title="快捷操作">
              <n-grid :cols="2" :x-gap="12" :y-gap="12">
                <n-gi v-for="(action, index) in quickActions" :key="index">
                  <div class="quick-action-item" @click="action.action">
                    <div class="action-icon">
                      <n-icon size="20">
                        <component :is="action.icon" />
                      </n-icon>
                    </div>
                    <span class="action-label">{{ action.title }}</span>
                  </div>
                </n-gi>
              </n-grid>
            </n-card>
          </n-gi>

          <n-gi :span="2">
            <n-card class="section-card" :bordered="false" title="Runtime 健康">
              <template #header-extra>
                <n-tag size="small" :type="runtime.metrics.replay_status === 'PASS' ? 'success' : 'warning'">
                  {{ runtime.metrics.replay_status }}
                </n-tag>
              </template>

              <n-grid :cols="3" :x-gap="12" :y-gap="12">
                <n-gi v-for="(card, index) in runtimeCards" :key="index">
                  <div class="runtime-item" :class="`runtime-${card.status}`">
                    <div class="runtime-header">
                      <n-icon size="16">
                        <component :is="card.icon" />
                      </n-icon>
                      <span class="runtime-title">{{ card.title }}</span>
                    </div>
                    <div class="runtime-value">{{ card.value }}</div>
                    <div class="runtime-detail">{{ card.detail }}</div>
                  </div>
                </n-gi>
              </n-grid>
            </n-card>
          </n-gi>
        </n-grid>
      </n-space>
    </n-spin>
  </div>
</template>

<style scoped>
.dashboard-page {
  padding: 0;
}

.welcome-card {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  border-radius: var(--border-radius-xl);
  border: none;
}

.welcome-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.welcome-text {
  flex: 1;
}

.welcome-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: white;
}

.welcome-desc {
  font-size: 14px;
  margin: 0;
  opacity: 0.9;
  color: rgba(255, 255, 255, 0.9);
}

.welcome-meta {
  flex-shrink: 0;
}

.section-header {
  margin-bottom: 4px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.stat-card {
  border-radius: var(--border-radius-lg);
  cursor: default;
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-body {
  text-align: left;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 2px;
}

.stat-total {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* Op cards */
.op-card {
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
}

.op-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.op-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 8px 0;
}

.op-icon {
  color: var(--brand-primary);
}

.op-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.op-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Section card */
.section-card {
  border-radius: var(--border-radius-lg);
}

.quick-action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 8px;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.25s ease;
  background: var(--bg-hover);
}

.quick-action-item:hover {
  background: var(--gray-100);
}

.action-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  color: var(--text-primary);
  border: 1px solid var(--gray-100);
}

.action-label {
  font-size: 12px;
  color: var(--text-regular);
  font-weight: 500;
}

/* Runtime items */
.runtime-item {
  padding: 12px;
  border-radius: var(--border-radius-md);
  background: var(--bg-hover);
  border-left: 3px solid var(--border-color);
}

.runtime-success {
  border-left-color: #10b981;
  background: #ecfdf5;
}

.runtime-warning {
  border-left-color: #f59e0b;
  background: #fffbeb;
}

.runtime-error {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.runtime-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
  font-size: 12px;
  color: var(--text-secondary);
}

.runtime-title {
  font-weight: 500;
}

.runtime-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.runtime-detail {
  font-size: 11px;
  color: var(--text-tertiary);
}

@media (max-width: 1024px) {
  .stat-card {
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
}
</style>
