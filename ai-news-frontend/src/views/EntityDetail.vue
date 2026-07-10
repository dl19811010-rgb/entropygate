<template>
  <div class="entity-page">
    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <n-spin size="large" />
        <p>加载实体情报...</p>
      </div>

      <!-- Not Found -->
      <div v-else-if="!entity" class="empty-state">
        <file-tray-outline class="empty-icon" />
        <h2>实体未找到</h2>
        <p>该实体快照尚未生成，或 slug 不正确。</p>
        <n-button @click="router.push('/')">返回首页</n-button>
      </div>

      <!-- Entity Content -->
      <template v-else>
        <!-- Header -->
        <div class="entity-header">
          <div class="entity-type-badge">{{ entityTypeLabel }}</div>
          <h1 class="entity-name">{{ entityName }}</h1>
          <p class="entity-summary" v-if="summary">{{ summary }}</p>
          <div class="entity-actions">
            <router-link :to="`/timeline/${entityType}/${entitySlug}`" class="entity-action-link">
              <time-outline />
              查看时间线
            </router-link>
          </div>
        </div>

        <!-- Tabs -->
        <n-tabs v-model:value="activeTab" type="line" class="entity-tabs">
          <n-tab-pane name="overview" tab="概览">
            <div class="tab-content">
              <!-- Latest Events -->
              <div class="section" v-if="latestEvents.length">
                <h2 class="section-title">
                  <flash-outline />
                  <span>最新事件</span>
                </h2>
                <div class="event-list">
                  <div
                    v-for="event in latestEvents.slice(0, 6)"
                    :key="event.id || event.date"
                    class="event-card"
                  >
                    <div class="event-date">{{ formatDate(event.date || event.detected_at) }}</div>
                    <div class="event-title">{{ event.event || event.title }}</div>
                    <div class="event-type" v-if="event.type">{{ event.type }}</div>
                  </div>
                </div>
              </div>

              <!-- Capabilities -->
              <div class="section" v-if="capabilities.length">
                <h2 class="section-title">
                  <trending-up-outline />
                  <span>相关能力</span>
                </h2>
                <div class="capability-list">
                  <div
                    v-for="cap in capabilities.slice(0, 6)"
                    :key="cap.name || cap.id"
                    class="capability-card"
                    @click="goToEntity('capability', slugify(cap.name))"
                  >
                    <div class="cap-name">{{ cap.name }}</div>
                    <div class="cap-desc" v-if="cap.description">{{ cap.description }}</div>
                  </div>
                </div>
              </div>

              <!-- Knowledge -->
              <div class="section" v-if="knowledge.length">
                <h2 class="section-title">
                  <library-outline />
                  <span>知识</span>
                </h2>
                <div class="knowledge-list">
                  <div
                    v-for="(item, idx) in knowledge.slice(0, 6)"
                    :key="idx"
                    class="knowledge-card"
                  >
                    <div class="knowledge-title">{{ item.title || item.fact || item.statement }}</div>
                    <div class="knowledge-source" v-if="item.source">来源: {{ item.source }}</div>
                  </div>
                </div>
              </div>
            </div>
          </n-tab-pane>

          <n-tab-pane name="timeline" tab="时间线">
            <div class="tab-content">
              <div class="timeline-controls">
                <n-radio-group v-model:value="timelinePeriod" size="small">
                  <n-radio-button value="all">全部</n-radio-button>
                  <n-radio-button value="month">本月</n-radio-button>
                  <n-radio-button value="week">本周</n-radio-button>
                </n-radio-group>
              </div>
              <div class="timeline-list" v-if="filteredTimeline.length">
                <div
                  v-for="item in filteredTimeline"
                  :key="item.date || item.id"
                  class="timeline-item"
                >
                  <div class="timeline-dot"></div>
                  <div class="timeline-content">
                    <div class="timeline-date">{{ formatDate(item.date || item.detected_at) }}</div>
                    <div class="timeline-title">{{ item.event || item.title }}</div>
                    <div class="timeline-type" v-if="item.type">{{ item.type }}</div>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state">
                <p>该时间范围内无事件</p>
              </div>
            </div>
          </n-tab-pane>

          <n-tab-pane name="relations" tab="关系" v-if="relations.length">
            <div class="tab-content">
              <div class="relation-list">
                <div
                  v-for="rel in relations.slice(0, 10)"
                  :key="rel.entity || rel.name"
                  class="relation-card"
                  @click="goToEntity(rel.entity_type || 'company', slugify(rel.entity || rel.name))"
                >
                  <div class="relation-name">{{ rel.entity || rel.name }}</div>
                  <div class="relation-type">{{ rel.relation_type || rel.type }}</div>
                </div>
              </div>
            </div>
          </n-tab-pane>
        </n-tabs>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getEntity } from '@/api/entity'
import { logError } from '@/utils/log'
import {
  FlashOutline, TrendingUpOutline, LibraryOutline, FileTrayOutline, TimeOutline
} from '@vicons/ionicons5'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const entity = ref(null)
const activeTab = ref('overview')
const timelinePeriod = ref('all')

const entityType = computed(() => route.params.type)
const entitySlug = computed(() => route.params.slug)

const entityTypeLabel = computed(() => {
  const map = { company: '公司', model: '模型', capability: '能力', research: '研究' }
  return map[entityType.value] || entityType.value
})

const entityName = computed(() => {
  return entity.value?.entity?.name || entity.value?.entity?.title || entitySlug.value
})

const summary = computed(() => {
  return entity.value?.summary || entity.value?.entity?.description || ''
})

const latestEvents = computed(() => {
  return entity.value?.latest_events || entity.value?.events || []
})

const capabilities = computed(() => {
  return entity.value?.capabilities || []
})

const knowledge = computed(() => {
  return entity.value?.knowledge || []
})

const relations = computed(() => {
  return entity.value?.relations || []
})

const timeline = computed(() => {
  return entity.value?.timeline || []
})

const filteredTimeline = computed(() => {
  const items = timeline.value
  if (timelinePeriod.value === 'all') return items

  const now = new Date()
  const cutoff = new Date()
  if (timelinePeriod.value === 'month') {
    cutoff.setMonth(now.getMonth() - 1)
  } else if (timelinePeriod.value === 'week') {
    cutoff.setDate(now.getDate() - 7)
  }

  return items.filter(item => {
    const d = new Date(item.date || item.detected_at)
    return d >= cutoff
  })
})

onMounted(() => {
  loadEntity()
})

watch(() => [route.params.type, route.params.slug], () => {
  loadEntity()
})

async function loadEntity() {
  if (!entityType.value || !entitySlug.value) return
  loading.value = true
  try {
    const data = await getEntity(entityType.value, entitySlug.value)
    entity.value = data || null
  } catch (e) {
    logError('加载实体失败:', e)
    entity.value = null
  } finally {
    loading.value = false
  }
}

function goToEntity(type, slug) {
  if (!type || !slug) return
  router.push(`/entity/${type}/${slug}`)
}

function slugify(str) {
  if (!str) return ''
  return str.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.entity-page {
  padding: var(--spacing-xl) 0;
  min-height: 60vh;
}

.entity-header {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.entity-type-badge {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: var(--border-radius-full);
  font-size: 12px;
  font-weight: 600;
  color: var(--brand-primary);
  text-transform: uppercase;
  margin-bottom: var(--spacing-md);
}

.entity-name {
  font-size: 32px;
  font-weight: 800;
  margin-bottom: var(--spacing-md);
  letter-spacing: -0.5px;
}

.entity-summary {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 700px;
  margin-bottom: var(--spacing-md);
}

.entity-actions {
  display: flex;
  gap: var(--spacing-md);
}

.entity-action-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-full);
  font-size: 14px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.entity-action-link:hover {
  background: var(--brand-primary);
  color: white;
  border-color: var(--brand-primary);
}

.entity-tabs :deep(.n-tabs-nav) {
  margin-bottom: var(--spacing-lg);
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.section {
  margin-bottom: var(--spacing-lg);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: var(--spacing-md);
}

.section-title svg {
  color: var(--brand-primary);
  width: 1em;
  height: 1em;
}

/* Event list */
.event-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.event-card {
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
}

.event-date {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 4px;
}

.event-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.event-type {
  font-size: 12px;
  color: var(--brand-primary);
}

/* Capability */
.capability-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--spacing-md);
}

.capability-card {
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.capability-card:hover {
  border-color: var(--border-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cap-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.cap-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Knowledge */
.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.knowledge-card {
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
}

.knowledge-title {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: 4px;
}

.knowledge-source {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* Timeline */
.timeline-controls {
  margin-bottom: var(--spacing-md);
}

.timeline-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  position: relative;
  padding-left: 24px;
}

.timeline-list::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border-color);
}

.timeline-item {
  position: relative;
  padding-bottom: var(--spacing-md);
}

.timeline-dot {
  position: absolute;
  left: -22px;
  top: 4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--brand-primary);
  border: 2px solid var(--bg-primary);
}

.timeline-date {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 4px;
}

.timeline-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.timeline-type {
  font-size: 12px;
  color: var(--brand-primary);
}

/* Relations */
.relation-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.relation-card {
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.relation-card:hover {
  border-color: var(--border-light);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.relation-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.relation-type {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* Loading / Empty */
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
  font-size: 48px;
  opacity: 0.5;
}

.empty-state h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.empty-state p {
  font-size: 14px;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .entity-name {
    font-size: 24px;
  }
  .capability-list {
    grid-template-columns: 1fr;
  }
  .relation-list {
    grid-template-columns: 1fr;
  }
}
</style>
