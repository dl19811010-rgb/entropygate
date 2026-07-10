<script setup>
import { ref, onMounted, h } from 'vue'
import {
  NCard, NDataTable, NButton, NSpace, NInput, NSelect,
  NPagination, useMessage, NModal, NDescriptions, NDescriptionsItem,
  NTag
} from 'naive-ui'
import { SearchOutlined } from '@vicons/antd'
import { getAuditLogs, getAuditLog } from '@/api/auditLog'

const message = useMessage()

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')
const actionFilter = ref(null)

const showDetail = ref(false)
const detailData = ref(null)

const actionOptions = [
  { label: '全部操作', value: null },
  { label: '创建', value: 'create' },
  { label: '更新', value: 'update' },
  { label: '删除', value: 'delete' },
  { label: '登录', value: 'login' },
  { label: '登出', value: 'logout' }
]

const actionTypeMap = {
  create: { text: '创建', type: 'success' },
  update: { text: '更新', type: 'warning' },
  delete: { text: '删除', type: 'error' },
  login: { text: '登录', type: 'info' },
  logout: { text: '登出', type: 'default' }
}

const columns = [
  { title: '操作人', key: 'operator', width: 140 },
  {
    title: '操作类型',
    key: 'action',
    width: 100,
    render: (row) => {
      const info = actionTypeMap[row.action] || {}
      return h(NTag, { type: info.type || 'default' }, {
        default: () => info.text || row.action
      })
    }
  },
  { title: '资源类型', key: 'model_name', width: 140 },
  { title: '资源ID', key: 'record_id', width: 180, ellipsis: { tooltip: true } },
  { title: 'IP地址', key: 'operator_ip', width: 140 },
  {
    title: '操作时间',
    key: 'created_at',
    width: 180,
    render: (row) => new Date(row.created_at).toLocaleString()
  },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row) => {
      return h(NButton, {
        size: 'small',
        type: 'primary',
        text: true,
        onClick: () => handleViewDetail(row)
      }, { default: () => '详情' })
    }
  }
]

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      size: pageSize.value
    }
    if (searchKeyword.value) {
      params.operator = searchKeyword.value
    }
    if (actionFilter.value) {
      params.action = actionFilter.value
    }
    const res = await getAuditLogs(params)
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
  actionFilter.value = null
  page.value = 1
  loadData()
}

async function handleViewDetail(row) {
  try {
    const res = await getAuditLog(row.id)
    detailData.value = res.data
    showDetail.value = true
  } catch (e) {
    message.error(e.message || '加载详情失败')
  }
}

function handlePageChange(p) {
  page.value = p
  loadData()
}

function formatJson(obj) {
  if (!obj) return '-'
  if (typeof obj === 'string') {
    try {
      const parsed = JSON.parse(obj)
      return JSON.stringify(parsed, null, 2)
    } catch (e) {
      return obj
    }
  }
  try {
    return JSON.stringify(obj, null, 2)
  } catch (e) {
    return String(obj)
  }
}


onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="audit-log-list">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">审计日志</h2>
        <p class="page-desc">查看系统操作记录，追踪管理行为</p>
      </div>
    </div>
    <n-card>
      <n-space vertical :size="16">
        <n-space :size="12" align="center">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索操作人..."
            style="width: 240px"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <search-outlined />
            </template>
          </n-input>
          <n-select
            v-model:value="actionFilter"
            :options="actionOptions"
            style="width: 160px"
            @update:value="handleSearch"
          />
          <n-button type="primary" @click="handleSearch">搜索</n-button>
          <n-button @click="handleReset">重置</n-button>
        </n-space>

        <n-data-table
          :columns="columns"
          :data="list"
          :loading="loading"
          :bordered="false"
          scroll-x="1100"
        />

        <div v-if="total > 0" class="pagination-wrapper">
          <n-pagination
            v-model:page="page"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[20, 50, 100]"
            show-size-picker
            show-quick-jumper
            @update:page="handlePageChange"
          />
        </div>
      </n-space>
    </n-card>

    <n-modal v-model:show="showDetail" preset="card" title="审计日志详情" style="width: 700px">
      <n-descriptions v-if="detailData" :column="1" bordered>
        <n-descriptions-item label="操作人">
          {{ detailData.operator || '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="操作类型">
          <n-tag :type="actionTypeMap[detailData.action]?.type || 'default'">
            {{ actionTypeMap[detailData.action]?.text || detailData.action }}
          </n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="资源类型">
          {{ detailData.model_name || '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="资源ID">
          {{ detailData.record_id || '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="IP地址">
          {{ detailData.operator_ip || '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="操作时间">
          {{ detailData.created_at ? new Date(detailData.created_at).toLocaleString() : '-' }}
        </n-descriptions-item>
        <n-descriptions-item label="操作前数据">
          <pre class="json-pre">{{ formatJson(detailData.before_data) }}</pre>
        </n-descriptions-item>
        <n-descriptions-item label="操作后数据">
          <pre class="json-pre">{{ formatJson(detailData.after_data) }}</pre>
        </n-descriptions-item>
      </n-descriptions>
      <template #footer>
        <n-button @click="showDetail = false">关闭</n-button>
      </template>
    </n-modal>
  </div>
</template>

<style scoped>
.audit-log-list {
  padding: 0;
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
  color: var(--gray-900);
  margin: 0 0 4px 0;
}

.page-desc {
  font-size: 13px;
  color: var(--gray-500);
  margin: 0;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}

.json-pre {
  max-height: 200px;
  overflow: auto;
  background: var(--gray-50);
  padding: 12px;
  border-radius: 4px;
  font-size: 12px;
  margin: 0;
}
</style>
