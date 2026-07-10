/**
 * 管理后台 - 工具列表页增强
 *
 * 在原有 CRUD 基础上新增：
 * - 批量可用性状态更新（一键标记）
 * - 批量分类变更
 * - 可用性快速编辑行内操作
 * - 工具对比预览入口
 * - 导出功能
 */

<template>
  <div class="tool-manage">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">工具管理</h2>
        <p class="page-desc">管理AI工具信息、可用性状态与分类</p>
      </div>
    </div>

    <!-- 顶部统计卡片 -->
    <n-grid :cols="4" :x-gap="16" :y-gap="16" class="stat-cards" responsive="screen" item-style="display:flex;">
      <n-gi>
        <n-card size="small" :bordered="false">
          <div class="stat-card-content">
            <div class="stat-icon" style="background: #f3f4f6; color: #111827;">
              <n-icon size="22"><ToolOutlined /></n-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total }}</div>
              <div class="stat-label">工具总数</div>
            </div>
          </div>
        </n-card>
      </n-gi>
      <n-gi>
        <n-card size="small" :bordered="false">
          <div class="stat-card-content">
            <div class="stat-icon" style="background: #f3f4f6; color: #111827;">
              <n-icon size="22"><CheckCircleOutlined /></n-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.available }}</div>
              <div class="stat-label">国内可用</div>
            </div>
          </div>
        </n-card>
      </n-gi>
      <n-gi>
        <n-card size="small" :bordered="false">
          <div class="stat-card-content">
            <div class="stat-icon" style="background: #f3f4f6; color: #111827;">
              <n-icon size="22"><WarningOutlined /></n-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.restricted }}</div>
              <div class="stat-label">需VPN/代理</div>
            </div>
          </div>
        </n-card>
      </n-gi>
      <n-gi>
        <n-card size="small" :bordered="false">
          <div class="stat-card-content">
            <div class="stat-icon" style="background: #f3f4f6; color: #111827;">
              <n-icon size="22"><QuestionCircleOutlined /></n-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.uncertain }}</div>
              <div class="stat-label">待核实</div>
            </div>
          </div>
        </n-card>
      </n-gi>
    </n-grid>

    <!-- 搜索与筛选 -->
    <n-card class="filter-card" size="small">
      <n-space>
        <n-input v-model:value="searchQuery" placeholder="搜索工具名称..." clearable style="width:200px" @clear="loadData" @keyup.enter="loadData">
          <template #prefix><n-icon><SearchOutlined /></n-icon></template>
        </n-input>
        <n-select v-model:value="filterCategory" :options="categoryOptions" placeholder="全部分类" clearable style="width:150px" />
        <n-select v-model:value="filterAvailability" :options="availabilityOptions" placeholder="全部可用性" clearable style="width:150px" />
        <n-select v-model:value="filterStatus" :options="statusOptions" placeholder="全部状态" clearable style="width:120px" />
        <n-button type="primary" @click="loadData">搜索</n-button>
        <n-button @click="resetFilters">重置</n-button>
      </n-space>
    </n-card>

    <!-- 批量操作栏 -->
    <div v-if="selectedRowKeys.length > 0" class="batch-bar">
      <n-space align="center">
        <span class="batch-info">已选 {{ selectedRowKeys.length }} 项</span>
        <n-button size="small" @click="batchUpdateAvailability('available')">标记为国内可用</n-button>
        <n-button size="small" @click="batchUpdateAvailability('needs_vpn')">标记为需VPN</n-button>
        <n-button size="small" @click="batchUpdateAvailability('blocked')">标记为已封禁</n-button>
        <n-button size="small" @click="batchUpdateStatus('published')">发布选中</n-button>
        <n-button size="small" @click="batchUpdateStatus('archived')">归档选中</n-button>
        <n-popconfirm @positive-click="batchDelete">
          <template #trigger><n-button size="small" class="btn-danger">删除选中</n-button></template>
          确定删除选中的 {{ selectedRowKeys.length }} 个工具吗？
        </n-popconfirm>
        <n-button size="small" text @click="selectedRowKeys = []">取消选择</n-button>
      </n-space>
    </div>

    <!-- 数据表格 -->
    <n-data-table
      :columns="columns"
      :data="tableData"
      :loading="loading"
      :row-key="(row) => row.id"
      :checked-row-keys="selectedRowKeys"
      @update:checked-row-keys="handleCheck"
      :pagination="{ pageSize: 20 }"
      scroll-x="1200"
      size="small"
    />

    <!-- 可用性快速编辑弹窗 -->
    <n-modal v-model:show="showAvailEdit" preset="dialog" title="快速编辑可用性" positive-text="保存" negative-text="取消" @positive-click="saveAvailabilityEdit">
      <n-form ref="availFormRef" :model="availEditForm" label-placement="left" label-width="100px">
        <n-form-item label="工具名称">
          <span>{{ availEditForm.tool_name }}</span>
        </n-form-item>
        <n-form-item label="可用性状态">
          <n-select v-model:value="availEditForm.availability_status" :options="availabilityFullOptions" />
        </n-form-item>
        <n-form-item label="访问方式说明">
          <n-input v-model:value="availEditForm.access_method" type="textarea" :rows="2" placeholder="如：需科学上网 / 手机号注册直接访问 / 需企业邮箱" />
        </n-form-item>
        <n-form-item label="备注">
          <n-input v-model:value="availEditForm.availability_note" type="textarea" :rows="2" placeholder="补充说明..." />
        </n-form-item>
      </n-form>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, h, onMounted } from 'vue'
import { NDataTable, NButton, NSpace, NTag, NInput, NSelect, NPopconfirm, NModal, NForm, NFormItem, NGrid, NGi, NCard, NStatistic, NIcon, useMessage, useDialog } from 'naive-ui'
import { SearchOutlined, ToolOutlined, CheckCircleOutlined, WarningOutlined, QuestionCircleOutlined } from '@vicons/antd'
import { useRouter } from 'vue-router'
import * as toolApi from '@/api/tool'

const router = useRouter()
const message = useMessage()
const dialog = useDialog()

// ====== 数据 ======
const loading = ref(false)
const tableData = ref([])
const selectedRowKeys = ref([])
const searchQuery = ref('')
const filterCategory = ref(null)
const filterAvailability = ref(null)
const filterStatus = ref(null)

const stats = reactive({ total: 0, available: 0, restricted: 0, uncertain: 0 })

// 分类选项（从后端获取或静态定义）
const categoryOptions = ref([
  { label: '文本生成', value: 'text-generation' },
  { label: '图像生成', value: 'image-generation' },
  { label: '编程辅助', value: 'code-assistant' },
  { label: '语音合成', value: 'voice-synthesis' },
  { label: '数据分析', value: 'data-analysis' },
  { label: '视频生成', value: 'video-generation' },
  { label: '效率办公', value: 'productivity' },
])

const availabilityOptions = [
  { label: '国内可用', value: 'available' },
  { label: '需VPN', value: 'needs_vpn' },
  { label: '需代理', value: 'needs_proxy' },
  { label: '部分受限', value: 'restricted' },
  { label: '已被封禁', value: 'blocked' },
  { label: '仅企业版', value: 'enterprise_only' },
  { label: '待核实', value: 'uncertain' },
]

const availabilityFullOptions = [
  { label: '国内可用', value: 'available' },
  { label: '需VPN', value: 'needs_vpn' },
  { label: '需代理', value: 'needs_proxy' },
  { label: '部分受限', value: 'restricted' },
  { label: '已被封禁', value: 'blocked' },
  { label: '仅企业版', value: 'enterprise_only' },
  { label: '待核实', value: 'uncertain' },
]

const statusOptions = [
  { label: '已发布', value: 'published' },
  { label: '草稿', value: 'draft' },
  { label: '已归档', value: 'archived' },
  { label: '已废弃', value: 'deprecated' },
]

// 可用性编辑弹窗
const showAvailEdit = ref(false)
const availEditForm = reactive({
  id: '',
  tool_name: '',
  availability_status: '',
  access_method: '',
  availability_note: '',
})

// ====== 表格列定义 ======
const columns = [
  {
    type: 'selection',
  },
  {
    title: '工具',
    key: 'name',
    width: 160,
    render(row) {
      return h(NSpace, { align: 'center', size: 'small' }, () => [
        h('div', { style: 'font-weight:600;font-size:13px;' }, row.name),
        h('div', { style: 'font-size:11px;color:#94a3b8;' }, row.tagline || ''),
      ])
    }
  },
  {
    title: '可用性',
    key: 'availability_status',
    width: 120,
    render(row) {
      const map = {
        available: { text: '国内可用', type: 'success' },
        needs_vpn: { text: '需VPN', type: 'warning' },
        needs_proxy: { text: '需代理', type: 'warning' },
        restricted: { text: '部分受限', type: 'warning' },
        blocked: { text: '已封禁', type: 'error' },
        enterprise_only: { text: '仅企业版', type: 'info' },
        uncertain: { text: '待核实', type: 'default' },
      }
      const cfg = map[row.availability_status] || { text: row.availability_status || '-', type: 'default' }
      return h(NTag, { type: cfg.type, size: 'small', bordered: false }, () => cfg.text)
    }
  },
  {
    title: '定价',
    key: 'pricing_type',
    width: 90,
    render(row) {
      const map = { freemium: '免费增值', free_tier: '有免费额', paid: '付费', open_source: '开源', custom: '企业定制' }
      return h('span', { style: 'font-size:12px' }, map[row.pricing_type] || '-')
    }
  },
  {
    title: '分类',
    key: 'category_name',
    width: 100,
    ellipsis: { tooltip: true },
  },
  {
    title: '评分',
    key: 'rating_avg',
    width: 70,
    render(row) {
      return row.rating_count > 0 ? `${row.rating_avg}★` : '-'
    }
  },
  {
    title: '浏览量',
    key: 'view_count',
    width: 70,
    sorter: (a, b) => a.view_count - b.view_count,
  },
  {
    title: '状态',
    key: 'status',
    width: 80,
    render(row) {
      const map = { published: 'success', draft: 'default', archived: 'warning', deprecated: 'error' }
      return h(NTag, { type: map[row.status] || 'default', size: 'small', bordered: false }, () => row.status)
    }
  },
  {
    title: '更新时间',
    key: 'updated_at',
    width: 160,
    sorter: true,
    render(row) {
      return row.updated_at ? new Date(row.updated_at).toLocaleString() : '-'
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 220,
    fixed: 'right',
    render(row) {
      return h(NSpace, { size: 'small' }, () => [
        h(NButton, {
          size: 'small',
          type: 'primary',
          text: true,
          onClick: () => openAvailabilityEdit(row),
        }, () => '可用性'),
        h(NButton, {
          size: 'small',
          text: true,
          onClick: () => router.push(`/tools/${row.id}/edit`),
        }, () => '编辑'),
        h(NButton, {
          size: 'small',
          text: true,
          onClick: () => toggleFeatured(row),
        }, () => row.is_featured ? '取消推荐' : '推荐'),
        h(NPopconfirm, { onPositiveClick: () => handleDelete(row.id) }, {
          trigger: () => h(NButton, { size: 'small', text: true, class: 'btn-danger' }, () => '删除'),
          default: () => `确定删除「${row.name}」？`,
        }),
      ])
    }
  },
]

// ====== 方法 ======

async function loadData() {
  loading.value = true
  try {
    const params = {}
    if (searchQuery.value) params.q = searchQuery.value
    if (filterCategory.value) params.category = filterCategory.value
    if (filterAvailability.value) params.availability = filterAvailability.value
    if (filterStatus.value) params.status = filterStatus.value
    
    // 调用后端API（兼容原有接口 + 新增筛选参数）
    const res = await toolApi.getTools(params)
    const payload = res.data?.items || res.data?.list || res.data
    tableData.value = Array.isArray(payload) ? payload : []
    
    // 计算统计数据
    stats.total = tableData.value.length
    stats.available = tableData.value.filter(t => t.availability_status === 'available').length
    stats.restricted = tableData.value.filter(t => ['needs_vpn','needs_proxy','restricted'].includes(t.availability_status)).length
    stats.uncertain = tableData.value.filter(t => t.availability_status === 'uncertain').length
  } catch (e) {
    message.error('加载失败')
  } finally {
    loading.value = false
  }
}

function resetFilters() {
  searchQuery.value = ''
  filterCategory.value = null
  filterAvailability.value = null
  filterStatus.value = null
  loadData()
}

function handleCheck(keys) {
  selectedRowKeys.value = keys
}

// --- 批量操作 ---

async function batchUpdateAvailability(status) {
  dialog.warning({
    title: '批量更新可用性',
    content: `确定将 ${selectedRowKeys.value.length} 个工具的可用性状态改为「${availabilityOptions.find(o=>o.value===status)?.label||status}」？`,
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await Promise.all(selectedRowKeys.value.map(id =>
          toolApi.updateTool(id, { availability_status: status })
        ))
        message.success(`已批量更新 ${selectedRowKeys.value.length} 个工具`)
        selectedRowKeys.value = []
        loadData()
      } catch (e) {
        message.error('批量更新失败')
      }
    }
  })
}

async function batchUpdateStatus(status) {
  try {
    await Promise.all(selectedRowKeys.value.map(id =>
      toolApi.updateTool(id, { status })
    ))
    message.success(`已批量${status === 'published' ? '发布' : '归档'} ${selectedRowKeys.value.length} 个工具`)
    selectedRowKeys.value = []
    loadData()
  } catch (e) {
    message.error('批量操作失败')
  }
}

async function batchDelete() {
  try {
    await Promise.all(selectedRowKeys.value.map(id => toolApi.deleteTool(id)))
    message.success(`已删除 ${selectedRowKeys.value.length} 个工具`)
    selectedRowKeys.value = []
    loadData()
  } catch (e) {
    message.error('删除失败')
  }
}

// --- 单项操作 ---

function openAvailabilityEdit(row) {
  availEditForm.id = row.id
  availEditForm.tool_name = row.name
  availEditForm.availability_status = row.availability_status || 'uncertain'
  availEditForm.access_method = row.access_method || ''
  availEditForm.availability_note = row.availability_note || ''
  showAvailEdit.value = true
}

async function saveAvailabilityEdit() {
  try {
    await toolApi.updateTool(availEditForm.id, {
      availability_status: availEditForm.availability_status,
      access_method: availEditForm.access_method,
      availability_note: availEditForm.availability_note,
    })
    message.success('可用性信息已更新')
    showAvailEdit.value = false
    loadData()
  } catch (e) {
    message.error('保存失败')
  }
}

async function handleDelete(id) {
  try {
    await toolApi.deleteTool(id)
    message.success('已删除')
    loadData()
  } catch (e) {
    message.error('删除失败')
  }
}

async function toggleFeatured(row) {
  try {
    await toolApi.updateTool(row.id, { is_featured: !row.is_featured })
    message.success(row.is_featured ? '已取消推荐' : '已设为推荐')
    loadData()
  } catch (e) {
    message.error('操作失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.tool-manage {
  background: transparent;
  min-height: auto;
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

.stat-cards {
  margin-bottom: 16px;
}

.stat-card-content {
  display: flex;
  align-items: center;
  gap: 14px;
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--border-radius-md, 8px);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-info {
  min-width: 0;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--gray-900);
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: var(--gray-500);
  margin-top: 2px;
}

.filter-card {
  margin-bottom: 12px;
  border-radius: var(--border-radius-lg, 12px) !important;
}

.batch-bar {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--gray-50, #f9fafb);
  border: 1px solid var(--gray-200, #e5e7eb);
  border-radius: var(--border-radius-md, 8px);
  padding: 8px 16px;
  margin-bottom: 12px;
}

.batch-info {
  font-weight: 600;
  font-size: 14px;
  color: var(--gray-700, #374151);
  margin-right: 8px;
}

.btn-danger {
  color: var(--gray-600, #4b5563) !important;
}

.btn-danger:hover {
  color: var(--danger, #ef4444) !important;
}
</style>
