<template>
  <div class="timeline-page">
    <div class="container">
      <div class="timeline-header">
        <h1 class="timeline-title">
          <time-outline />
          <span>{{ pageTitle }}</span>
        </h1>
        <p class="timeline-desc">探索 AI 世界的时间线，追踪事件、发布和能力演进</p>
      </div>

      <!-- Period Filter -->
      <div class="period-filter">
        <n-radio-group v-model:value="period" size="medium" @update:value="loadTimeline">
          <n-radio-button value="today">今日</n-radio-button>
          <n-radio-button value="week">本周</n-radio-button>
          <n-radio-button value="month">本月</n-radio-button>
          <n-radio-button value="all">全部</n-radio-button>
        </n-radio-group>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <n-spin size="large" />
        <p>加载时间线...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="entries.length === 0" class="empty-state">
        <file-tray-outline class="empty-icon" />
        <p>该时间范围内暂无事件</p>
      </div>

      <!-- Timeline -->
      <div v-else class="timeline-body">
        <div class="timeline-list">
          <div
            v-for="(item, index) in entries"
            :key="index"
            class="timeline-item"
            @click="goToEntity(item)"
          >
            <div class="timeline-marker">
              <div class="timeline-dot" :class="getTypeClass(item.type)"></div>
              <div class="timeline-line" v-if="index < entries.length - 1"></div>
            </div>
            <div class="timeline-content">
              <div class="timeline-date">{{ formatDate(item.date) }}</div>
              <h3 class="timeline-event-title">{{ item.title || item.event }}</h3>
              <div class="timeline-meta">
                <n-tag v-if="item.type" size="small" :type="getTagType(item.type)">{{ item.type }}</n-tag>
                <span class="timeline-subject" v-if="item.subject">{{ item.subject }}</span>
              </div>
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
import { getTimeline, getEntityTimeline } from '@/api/timeline'
import { logError } from '@/utils/log'
import {
  TimeOutline, FileTrayOutline
} from '@vicons/ionicons5'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const entries = ref([])
const period = ref('all')

const entityType = computed(() => route.params.type)
const entitySlug = computed(() => route.params.slug)

const isEntityTimeline = computed(() => !!entityType.value && !!entitySlug.value)

const pageTitle = computed(() => {
  if (isEntityTimeline.value) {
    return `${entitySlug.value} 的时间线`
  }
  return '情报时间线'
})

onMounted(() => {
  // Parse period from query
  if (route.query.period) {
    period.value = route.query.period
  }
  loadTimeline()
})

watch(() => route.query.period, (newPeriod) => {
  if (newPeriod && newPeriod !== period.value) {
    period.value = newPeriod
    loadTimeline()
  }
})

watch(() => [route.params.type, route.params.slug], () => {
  loadTimeline()
})

async function loadTimeline() {
  loading.value = true
  try {
    let data
    if (isEntityTimeline.value) {
      data = await getEntityTimeline(entityType.value, entitySlug.value)
      entries.value = data.timeline || []
    } else {
      data = await getTimeline(period.value)
      entries.value = data.entries || []
    }
  } catch (e) {
    logError('加载时间线失败:', e)
    entries.value = []
  } finally {
    loading.value = false
  }
}

function goToEntity(item) {
  if (item.entity_type && item.entity_slug) {
    router.push(`/entity/${item.entity_type}/${item.entity_slug}`)
  }
}

function getTypeClass(type) {
  const t = (type || '').toLowerCase()
  if (t.includes('release')) return 'dot-release'
  if (t.includes('research')) return 'dot-research'
  if (t.includes('funding')) return 'dot-funding'
  if (t.includes('benchmark')) return 'dot-benchmark'
  return 'dot-default'
}

function getTagType(type) {
  const t = (type || '').toLowerCase()
  if (t.includes('release')) return 'success'
  if (t.includes('research')) return 'info'
  if (t.includes('funding')) return 'error'
  if (t.includes('benchmark')) return 'warning'
  return 'default'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  const timeStr = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  const dateStr2 = date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })

  if (days === 0) return `今天 ${timeStr}`
  if (days === 1) return `昨天 ${timeStr}`
  if (days < 7) return `${days}天前`
  return `${dateStr2}`
}
</script>

<style scoped>
.timeline-page {
  padding: var(--spacing-xl) 0 var(--spacing-2xl);
  min-height: 60vh;
}

.timeline-header {
  margin-bottom: var(--spacing-xl);
  text-align: center;
}

.timeline-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
}

.timeline-title svg {
  color: var(--brand-primary);
  width: 1em;
  height: 1em;
}

.timeline-desc {
  font-size: 15px;
  color: var(--text-secondary);
}

.period-filter {
  display: flex;
  justify-content: center;
  margin-bottom: var(--spacing-xl);
}

.timeline-body {
  max-width: 720px;
  margin: 0 auto;
}

.timeline-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.timeline-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md) 0;
  cursor: pointer;
  transition: background var(--transition-fast);
  border-radius: var(--border-radius-lg);
}

.timeline-item:hover {
  background: var(--bg-hover);
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 24px;
  flex-shrink: 0;
  padding-top: 4px;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--brand-primary);
  border: 2px solid var(--bg-primary);
  box-shadow: 0 0 0 2px var(--brand-primary);
}

.dot-release { background: #10b981; box-shadow: 0 0 0 2px #10b981; }
.dot-research { background: #6366f1; box-shadow: 0 0 0 2px #6366f1; }
.dot-funding { background: #ef4444; box-shadow: 0 0 0 2px #ef4444; }
.dot-benchmark { background: #f59e0b; box-shadow: 0 0 0 2px #f59e0b; }
.dot-default { background: #9ca3af; box-shadow: 0 0 0 2px #9ca3af; }

.timeline-line {
  flex: 1;
  width: 2px;
  background: var(--border-color);
  margin-top: 4px;
  min-height: 40px;
}

.timeline-content {
  flex: 1;
  min-width: 0;
  padding-bottom: var(--spacing-md);
}

.timeline-date {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 4px;
}

.timeline-event-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
  line-height: 1.5;
}

.timeline-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.timeline-subject {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--text-tertiary);
  gap: var(--spacing-md);
}

.empty-icon {
  font-size: 40px;
  opacity: 0.4;
}

@media (max-width: 640px) {
  .timeline-title {
    font-size: 22px;
  }
}
</style>
