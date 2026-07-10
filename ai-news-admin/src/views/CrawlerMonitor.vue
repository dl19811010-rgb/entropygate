<script setup>
import { ref, onMounted, h, computed } from 'vue'
import {
  NCard, NGrid, NGi, NButton, NSpace, NTag, NIcon,
  NDataTable, useMessage, NProgress, NTooltip, NDescriptions,
  NDescriptionsItem, NSpin, NBadge
} from 'naive-ui'
import {
  CloudDownloadOutlined, FileAddOutlined,
  WarningOutlined, FileTextOutlined, ReloadOutlined,
  PlayCircleOutlined, CheckCircleOutlined, CloseCircleOutlined,
  ClockCircleOutlined, ThunderboltOutlined, DatabaseOutlined,
  SettingOutlined, ApiOutlined, SyncOutlined
} from '@vicons/antd'
import { getCrawlerStats, getCrawlerSourceStats, triggerSource, triggerAllSources, getRecentLogs } from '@/api/source'
import { getCeleryStatus, getSchedulerStatus, startScheduler, stopScheduler, getSourceHealth } from '@/api/operations'
import { logError } from '@/utils/log'

const message = useMessage()
const loading = ref(false)
const triggerLoading = ref({})
const schedulerActionLoading = ref(false)

// 采集系统状态
const celeryStatus = ref({
  worker_online: false,
  worker_count: 0,
  workers: [],
  beat_schedule: []
})
const schedulerStatus = ref({
  running: false,
  jobs: []
})
const sourceHealth = ref({
  total: 0,
  healthy: 0,
  degraded: 0,
  critical: 0,
  disabled: 0,
  sources: []
})

// 采集统计
const stats = ref({
  today: { found: 0, new: 0, failed: 0, pending: 0 },
  sources: []
})
const sourceStats = ref([])
const recentLogs = ref([])

// 系统状态卡片
const systemCards = computed(() => [
  {
    title: 'Celery Worker',
    value: celeryStatus.value.worker_online ? '在线' : '离线',
    sub: `${celeryStatus.value.worker_count} 个 Worker`,
    icon: SyncOutlined,
    status: celeryStatus.value.worker_online ? 'success' : 'error'
  },
  {
    title: 'Celery Beat',
    value: celeryStatus.value.beat_schedule.length > 0 ? '已配置' : '未配置',
    sub: `${celeryStatus.value.beat_schedule.length} 个定时任务`,
    icon: ClockCircleOutlined,
    status: celeryStatus.value.beat_schedule.length > 0 ? 'success' : 'warning'
  },
  {
    title: 'Pipeline 调度器',
    value: schedulerStatus.value.running ? '运行中' : '已停止',
    sub: `${schedulerStatus.value.jobs.length} 个 Pipeline 任务`,
    icon: ThunderboltOutlined,
    status: schedulerStatus.value.running ? 'success' : 'warning',
    actionable: true
  },
  {
    title: '今日采集',
    value: stats.value.today.found,
    sub: `新增 ${stats.value.today.new} · 失败 ${stats.value.today.failed}`,
    icon: CloudDownloadOutlined,
    status: 'default'
  }
])

// 数据源健康分布
const healthCards = computed(() => [
  { label: '健康', value: sourceHealth.value.healthy, color: '#10b981', bg: '#ecfdf5' },
  { label: '降级', value: sourceHealth.value.degraded, color: '#f59e0b', bg: '#fffbeb' },
  { label: '严重', value: sourceHealth.value.critical, color: '#ef4444', bg: '#fef2f2' },
  { label: '已禁用', value: sourceHealth.value.disabled, color: '#9ca3af', bg: '#f3f4f6' }
])

// 来源统计表格列
const sourceColumns = [
  { title: '来源名称', key: 'name', width: 180, ellipsis: { tooltip: true } },
  { title: '类型', key: 'parser_type', width: 100 },
  {
    title: '今日采集',
    key: 'today',
    width: 160,
    render: (row) => h('span', null, `${row.today.found} / 新${row.today.new} / 败${row.today.failed}`)
  },
  {
    title: '累计采集',
    key: 'total',
    width: 160,
    render: (row) => h('span', null, `${row.total.found} / 新${row.total.new} / 败${row.total.failed}`)
  },
  {
    title: '文章状态',
    key: 'articles',
    width: 200,
    render: (row) => {
      return h(NSpace, { size: 4, wrap: true }, {
        default: () => [
          h(NTag, { size: 'small', type: 'success' }, { default: () => `已发${row.articles.published}` }),
          h(NTag, { size: 'small', type: 'warning' }, { default: () => `待审${row.articles.draft}` }),
          h(NTag, { size: 'small', type: 'error' }, { default: () => `废弃${row.articles.discarded}` })
        ]
      })
    }
  },
  {
    title: '采纳率',
    key: 'adoption_rate',
    width: 120,
    render: (row) => h(NProgress, {
      type: 'line',
      percentage: row.adoption_rate,
      indicatorPlacement: 'inside',
      status: row.adoption_rate >= 50 ? 'success' : row.adoption_rate >= 20 ? 'warning' : 'error'
    })
  },
  {
    title: '状态',
    key: 'last_fetch_status',
    width: 100,
    render: (row) => {
      const statusMap = {
        completed: { type: 'success', text: '正常' },
        failed: { type: 'error', text: '失败' },
        pending: { type: 'default', text: '待采集' },
        running: { type: 'warning', text: '采集中' }
      }
      const s = statusMap[row.last_fetch_status] || statusMap.pending
      return h(NTag, { size: 'small', type: s.type }, { default: () => s.text })
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    fixed: 'right',
    render: (row) => {
      return h(NButton, {
        size: 'small',
        type: 'primary',
        ghost: true,
        loading: triggerLoading.value[row.id],
        disabled: !row.is_active,
        onClick: () => handleTrigger(row)
      }, { default: () => '手动采集', icon: () => h(PlayCircleOutlined) })
    }
  }
]

// 最近采集日志列
const logColumns = [
  {
    title: '时间',
    key: 'created_at',
    width: 160,
    render: (row) => {
      if (!row.created_at) return '-'
      const d = new Date(row.created_at)
      return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
    }
  },
  { title: '来源', key: 'source_name', width: 180, ellipsis: { tooltip: true } },
  {
    title: '状态',
    key: 'status',
    width: 80,
    render: (row) => {
      const map = {
        completed: { type: 'success', text: '成功' },
        failed: { type: 'error', text: '失败' },
        running: { type: 'warning', text: '进行中' }
      }
      const s = map[row.status] || { type: 'default', text: row.status }
      return h(NTag, { size: 'small', type: s.type }, { default: () => s.text })
    }
  },
  { title: '发现', key: 'items_found', width: 60 },
  { title: '新增', key: 'items_new', width: 60 },
  { title: '重复', key: 'items_duplicate', width: 60 },
  {
    title: '耗时',
    key: 'duration',
    width: 80,
    render: (row) => row.duration ? `${row.duration}s` : '-'
  },
  {
    title: '错误信息',
    key: 'error_message',
    ellipsis: { tooltip: true },
    render: (row) => row.error_message ? h('span', { style: 'color: #ef4444; font-size: 12px' }, row.error_message) : '-'
  }
]

// Pipeline 任务名映射
const pipelineJobNames = {
  'incremental_pipeline': '增量 Pipeline',
  'daily_pipeline': '全量日报 Pipeline',
  'entity_refresh': '实体快照刷新',
  'search_index': '搜索索引重建',
  'daily_report': '每日情报报告'
}

async function loadAll() {
  loading.value = true
  try {
    const [statsRes, sourceRes, celeryRes, schedRes, healthRes, logsRes] = await Promise.all([
      getCrawlerStats(),
      getCrawlerSourceStats(),
      getCeleryStatus(),
      getSchedulerStatus(),
      getSourceHealth(),
      getRecentLogs(20)
    ])
    stats.value = statsRes.data || stats.value
    sourceStats.value = sourceRes.data || []
    celeryStatus.value = celeryRes.data || celeryStatus.value
    schedulerStatus.value = schedRes.data || schedulerStatus.value
    sourceHealth.value = healthRes.data || sourceHealth.value
    recentLogs.value = logsRes.data || []
  } catch (e) {
    message.error(e.message || '加载数据失败')
    logError('采集监控加载失败', e)
  } finally {
    loading.value = false
  }
}

async function handleTrigger(row) {
  triggerLoading.value[row.id] = true
  try {
    await triggerSource(row.id)
    message.success('采集任务已触发')
    loadAll()
  } catch (e) {
    message.error(e.message || '触发失败')
  } finally {
    triggerLoading.value[row.id] = false
  }
}

async function handleTriggerAll() {
  try {
    await triggerAllSources()
    message.success('已触发全部来源采集')
    setTimeout(() => loadAll(), 3000)
  } catch (e) {
    message.error(e.message || '触发失败')
  }
}

async function handleSchedulerAction() {
  schedulerActionLoading.value = true
  try {
    if (schedulerStatus.value.running) {
      await stopScheduler()
      message.success('Pipeline 调度器已停止')
    } else {
      await startScheduler()
      message.success('Pipeline 调度器已启动')
    }
    const res = await getSchedulerStatus()
    schedulerStatus.value = res.data || schedulerStatus.value
  } catch (e) {
    message.error(e.message || '操作失败')
  } finally {
    schedulerActionLoading.value = false
  }
}

function formatTime(timeStr) {
  if (!timeStr || timeStr === 'None') return '-'
  const d = new Date(timeStr)
  if (isNaN(d.getTime())) return '-'
  return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function getBeatScheduleLabel(key) {
  const map = {
    'fetch-high-priority': '高优采集',
    'fetch-medium-priority': '常规采集',
    'fetch-low-priority': '低频采集',
    'health-check-failed-sources': '失败源巡检'
  }
  return map[key] || key
}

onMounted(() => {
  loadAll()
})
</script>

<template>
  <div class="crawler-monitor-page">
    <n-spin :show="loading">
      <n-space vertical :size="20">
        <!-- 页面头部 -->
        <div class="page-header">
          <div>
            <h2 class="page-title">采集系统监控</h2>
            <p class="page-desc">实时查看采集系统运行状态、调度配置、数据源健康与采集日志</p>
          </div>
          <n-space>
            <n-button @click="loadAll">
              <template #icon><reload-outlined /></template>
              刷新
            </n-button>
            <n-button type="primary" @click="handleTriggerAll">
              <template #icon><play-circle-outlined /></template>
              全部采集
            </n-button>
          </n-space>
        </div>

        <!-- 系统运行状态 -->
        <div class="section-header">
          <h3 class="section-title">系统运行状态</h3>
        </div>
        <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen">
          <n-gi v-for="(card, index) in systemCards" :key="index" :span="1">
            <n-card class="system-card" :bordered="false">
              <div class="system-card-body">
                <div class="system-icon" :class="`status-${card.status}`">
                  <n-icon size="24">
                    <component :is="card.icon" />
                  </n-icon>
                </div>
                <div class="system-info">
                  <div class="system-value" :class="`text-${card.status}`">{{ card.value }}</div>
                  <div class="system-label">{{ card.title }}</div>
                  <div class="system-sub">{{ card.sub }}</div>
                </div>
                <div v-if="card.actionable" class="system-action">
                  <n-button
                    size="small"
                    :type="schedulerStatus.running ? 'error' : 'success'"
                    :loading="schedulerActionLoading"
                    @click="handleSchedulerAction"
                  >
                    {{ schedulerStatus.running ? '停止' : '启动' }}
                  </n-button>
                </div>
              </div>
            </n-card>
          </n-gi>
        </n-grid>

        <!-- 采集调度配置 + Pipeline 任务 -->
        <n-grid :cols="2" :x-gap="16" :y-gap="16" responsive="screen">
          <!-- Celery Beat 调度 -->
          <n-gi :span="1">
            <n-card title="Celery Beat 采集调度" :bordered="false">
              <template #header-extra>
                <n-tag size="small" :type="celeryStatus.worker_online ? 'success' : 'error'">
                  {{ celeryStatus.worker_online ? `Worker 在线 (${celeryStatus.worker_count})` : 'Worker 离线' }}
                </n-tag>
              </template>
              <div class="schedule-list">
                <div v-for="task in celeryStatus.beat_schedule" :key="task.key" class="schedule-item">
                  <div class="schedule-info">
                    <div class="schedule-name">{{ task.name }}</div>
                    <div class="schedule-detail">{{ task.schedule }}</div>
                  </div>
                  <n-tag size="small" :type="task.priority === 'high' ? 'error' : task.priority === 'medium' ? 'warning' : task.priority === 'low' ? 'info' : 'default'">
                    {{ task.priority === 'high' ? '高优' : task.priority === 'medium' ? '常规' : task.priority === 'low' ? '低频' : '巡检' }}
                  </n-tag>
                </div>
                <div v-if="celeryStatus.beat_schedule.length === 0" class="empty-hint">
                  未配置 Beat 调度任务
                </div>
              </div>
              <div v-if="celeryStatus.workers.length > 0" class="worker-info">
                <n-descriptions size="small" :column="1" label-placement="left" bordered>
                  <n-descriptions-item v-for="w in celeryStatus.workers" :key="w.name" :label="w.name">
                    {{ w.pool }} · 并发 {{ w.processes }}
                  </n-descriptions-item>
                </n-descriptions>
              </div>
            </n-card>
          </n-gi>

          <!-- APScheduler Pipeline 任务 -->
          <n-gi :span="1">
            <n-card title="Pipeline 调度任务" :bordered="false">
              <template #header-extra>
                <n-tag size="small" :type="schedulerStatus.running ? 'success' : 'warning'">
                  {{ schedulerStatus.running ? '运行中' : '已停止' }}
                </n-tag>
              </template>
              <div class="schedule-list">
                <div v-if="schedulerStatus.jobs.length === 0" class="empty-hint">
                  Pipeline 调度器未启动，点击上方"启动"按钮开始运行
                </div>
                <div v-for="job in schedulerStatus.jobs" :key="job.id" class="schedule-item">
                  <div class="schedule-info">
                    <div class="schedule-name">{{ pipelineJobNames[job.id] || job.name }}</div>
                    <div class="schedule-detail">{{ job.trigger }}</div>
                  </div>
                  <div class="schedule-next">
                    <n-tooltip trigger="hover">
                      <template #trigger>
                        <n-tag size="small" type="info">
                          下次: {{ formatTime(job.next_run_time) }}
                        </n-tag>
                      </template>
                      {{ job.next_run_time }}
                    </n-tooltip>
                  </div>
                </div>
              </div>
            </n-card>
          </n-gi>
        </n-grid>

        <!-- 数据源健康概览 -->
        <div class="section-header">
          <h3 class="section-title">数据源健康概览</h3>
        </div>
        <n-grid :cols="4" :x-gap="16" :y-gap="16" responsive="screen">
          <n-gi v-for="(card, index) in healthCards" :key="index" :span="1">
            <n-card class="health-card" :bordered="false" :style="{ background: card.bg }">
              <div class="health-body">
                <div class="health-value" :style="{ color: card.color }">{{ card.value }}</div>
                <div class="health-label">{{ card.label }}</div>
              </div>
            </n-card>
          </n-gi>
        </n-grid>

        <!-- 最近采集日志 -->
        <n-card title="最近采集日志" :bordered="false">
          <n-data-table
            :columns="logColumns"
            :data="recentLogs"
            :scroll-x="900"
            :pagination="{ pageSize: 8 }"
            size="small"
          />
        </n-card>

        <!-- 来源统计详情 -->
        <n-card title="来源统计详情" :bordered="false">
          <n-data-table
            :columns="sourceColumns"
            :data="sourceStats"
            :loading="loading"
            :scroll-x="1100"
            :pagination="{ pageSize: 10 }"
          />
        </n-card>
      </n-space>
    </n-spin>
  </div>
</template>

<style scoped>
.crawler-monitor-page {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: var(--text-primary);
}

.page-desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
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

/* 系统状态卡片 */
.system-card {
  border-radius: var(--border-radius-lg, 12px);
}

.system-card-body {
  display: flex;
  align-items: center;
  gap: 14px;
  position: relative;
}

.system-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.status-success {
  background: #ecfdf5;
  color: #10b981;
}

.status-error {
  background: #fef2f2;
  color: #ef4444;
}

.status-warning {
  background: #fffbeb;
  color: #f59e0b;
}

.status-default {
  background: #f3f4f6;
  color: #6b7280;
}

.system-info {
  flex: 1;
  min-width: 0;
}

.system-value {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 2px;
}

.text-success { color: #10b981; }
.text-error { color: #ef4444; }
.text-warning { color: #f59e0b; }
.text-default { color: #6b7280; }

.system-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.system-sub {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 2px;
}

.system-action {
  position: absolute;
  top: 0;
  right: 0;
}

/* 调度列表 */
.schedule-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.schedule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: var(--bg-hover, #f9fafb);
  border-radius: 8px;
  transition: background 0.2s;
}

.schedule-item:hover {
  background: var(--gray-100, #f3f4f6);
}

.schedule-info {
  flex: 1;
}

.schedule-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.schedule-detail {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 2px;
}

.schedule-next {
  flex-shrink: 0;
}

.empty-hint {
  text-align: center;
  padding: 24px;
  color: var(--text-tertiary);
  font-size: 13px;
}

.worker-info {
  margin-top: 16px;
}

/* 健康卡片 */
.health-card {
  border-radius: var(--border-radius-lg, 12px);
}

.health-body {
  text-align: center;
  padding: 8px 0;
}

.health-value {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.2;
}

.health-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
  }
}
</style>
