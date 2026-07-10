<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NButton, NSelect } from 'naive-ui'
import { getTools } from '@/api/tool'
import { getDashboardAvailability } from '@/api/dashboard'
import { logError } from '@/utils/log'

const router = useRouter()

const availabilityStats = ref({})
const tools = ref([])
const loading = ref(false)
const filterStatus = ref(null)

const availabilityLabels = {
  available: '国内可用',
  restricted: '部分受限',
  blocked: '已被封禁',
  enterprise_only: '仅企业版',
  uncertain: '待核实'
}

const statusOptions = [
  { label: '全部', value: null },
  { label: '国内可用', value: 'available' },
  { label: '部分受限', value: 'restricted' },
  { label: '已被封禁', value: 'blocked' },
  { label: '仅企业版', value: 'enterprise_only' },
  { label: '待核实', value: 'uncertain' }
]

async function loadStats() {
  try {
    const res = await getDashboardAvailability()
    availabilityStats.value = res.availability || {}
  } catch (e) {
    logError('加载可用性统计失败:', e)
  }
}

async function loadTools() {
  loading.value = true
  try {
    const params = { page: 1, size: 50 }
    if (filterStatus.value) {
      params.availability = filterStatus.value
    }
    const res = await getTools(params)
    tools.value = res.items || []
  } catch (e) {
    logError('加载工具失败:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStats()
  loadTools()
})
</script>

<template>
  <div class="availability-page">
    <div class="page-inner">
      <div class="page-header">
        <h1 class="page-title">国内可用性指南</h1>
        <p class="page-desc">主流AI工具国内访问状态实时追踪，附替代方案推荐</p>
      </div>

      <div class="stats-grid">
        <div
          v-for="(count, status) in availabilityStats"
          :key="status"
          class="stat-card"
          :class="status"
        >
          <div class="stat-header">
            <span :class="['status-dot', status]"></span>
            <span class="status-label">{{ availabilityLabels[status] || status }}</span>
          </div>
          <span class="stat-number">{{ count }}</span>
          <span class="stat-unit">款工具</span>
        </div>
      </div>

      <div class="toolbar">
        <div class="toolbar-left">
          <h2 class="section-title">工具列表</h2>
        </div>
        <div class="toolbar-right">
          <n-select
            v-model:value="filterStatus"
            :options="statusOptions"
            style="width: 160px"
            @update:value="loadTools"
          />
        </div>
      </div>

      <div class="tools-table">
        <table>
          <thead>
            <tr>
              <th>工具名称</th>
              <th>分类</th>
              <th>可用性状态</th>
              <th>访问方式</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="tool in tools"
              :key="tool.id"
              class="tool-row"
              @click="router.push(`/tools/${tool.slug}`)"
            >
              <td>
                <div class="tool-cell">
                  <div class="tool-logo-sm">
                    {{ tool.name ? tool.name.charAt(0) : '?' }}
                  </div>
                  <span class="tool-name">{{ tool.name }}</span>
                </div>
              </td>
              <td>{{ tool.category_name || '-' }}</td>
              <td>
                <span
                  class="status-badge"
                  :class="tool.availability_status || 'uncertain'"
                >
                  {{ availabilityLabels[tool.availability_status] || '待核实' }}
                </span>
              </td>
              <td>{{ tool.availability?.access_method || '-' }}</td>
              <td>
                <n-button text type="primary" size="small">
                  查看详情
                </n-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.availability-page {
  background: var(--bg-primary);
  min-height: calc(100vh - 64px);
}

.page-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.page-desc {
  font-size: 16px;
  color: var(--text-tertiary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
  border-top: 4px solid transparent;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.stat-card.available {
  border-top-color: #10b981;
}

.stat-card.restricted {
  border-top-color: #f59e0b;
}

.stat-card.blocked {
  border-top-color: #ef4444;
}

.stat-card.enterprise_only {
  border-top-color: #6366f1;
}

.stat-card.uncertain {
  border-top-color: var(--text-tertiary);
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 12px;
}

.status-dot {
  width: 10px;
  height: 10px;
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

.status-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-number {
  font-size: 40px;
  font-weight: 700;
  color: var(--text-primary);
  display: block;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-unit {
  font-size: 13px;
  color: var(--text-tertiary);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.tools-table {
  background: var(--bg-card);
  border-radius: 16px;
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--bg-primary);
}

th {
  padding: 16px 20px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-color);
}

td {
  padding: 16px 20px;
  border-bottom: 1px solid var(--bg-tertiary);
  font-size: 14px;
  color: var(--text-primary);
}

.tool-row {
  cursor: pointer;
  transition: background 0.2s;
}

.tool-row:hover {
  background: var(--bg-primary);
}

.tool-row:last-child td {
  border-bottom: none;
}

.tool-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.tool-logo-sm {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
}

.tool-name {
  font-weight: 500;
  color: var(--text-primary);
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.available {
  background: #d1fae5;
  color: #059669;
}

.status-badge.restricted {
  background: #fef3c7;
  color: #d97706;
}

.status-badge.blocked {
  background: #fee2e2;
  color: #dc2626;
}

.status-badge.enterprise_only {
  background: #e0e7ff;
  color: #4f46e5;
}

.status-badge.uncertain {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

@media (max-width: 960px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .tools-table {
    overflow-x: auto;
  }
}
</style>
