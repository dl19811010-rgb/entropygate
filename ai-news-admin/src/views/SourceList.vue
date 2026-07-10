<script setup>
import { ref, onMounted, h } from 'vue'
import {
  NCard, NDataTable, NButton, NSpace, NInput, NInputNumber, NPagination,
  useMessage, useDialog, NModal, NForm, NFormItem, NSelect, NTag, NSwitch
} from 'naive-ui'
import { PlusOutlined, SearchOutlined } from '@vicons/antd'
import {
  getSources, createSource, updateSource, deleteSource
} from '@/api/source'
import { getAllCategories } from '@/api/category'

const message = useMessage()
const dialog = useDialog()

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')
const categories = ref([])

const showModal = ref(false)
const modalTitle = ref('')
const editingId = ref(null)
const formRef = ref(null)
const formData = ref({
  name: '',
  url: '',
  type: 'website',
  category_id: null,
  parser_type: 'rss',
  fetch_interval: 60,
  is_active: true,
  auto_publish: false,
  ai_preprocess: true,
  dedup_strategy: 'url',
  config: '{}',
  description: ''
})

const parserTypeOptions = [
  { label: 'RSS 订阅', value: 'rss' },
  { label: 'API - JSON', value: 'api_json' },
  { label: 'API - XML', value: 'api_xml' },
  { label: '静态网页', value: 'static_html' },
  { label: '动态网页', value: 'dynamic_html' },
  { label: 'Webhook', value: 'webhook' }
]

const dedupStrategyOptions = [
  { label: 'URL 精确匹配', value: 'url' },
  { label: '标题相似度', value: 'title' },
  { label: '内容摘要哈希', value: 'content_hash' }
]

const typeOptions = [
  { label: '网站', value: 'website' },
  { label: '微信公众号', value: 'wechat' },
  { label: '微博', value: 'weibo' },
  { label: '知乎', value: 'zhihu' },
  { label: '其他', value: 'other' }
]

const categoryOptions = ref([])

const rules = {
  name: [
    { required: true, message: '请输入来源名称', trigger: 'blur' }
  ],
  url: [
    { required: true, message: '请输入来源地址', trigger: 'blur' }
  ],
  parser_type: [
    { required: true, message: '请选择解析类型', trigger: 'change' }
  ],
  fetch_interval: [
    { required: true, type: 'number', message: '请输入抓取间隔', trigger: 'blur' }
  ],
  config: [
    {
      validator(rule, value) {
        if (!value) return true
        try {
          JSON.parse(value)
          return true
        } catch (e) {
          return new Error('JSON 格式不正确')
        }
      },
      trigger: 'blur'
    }
  ]
}

const columns = [
  { title: '来源名称', key: 'name', width: 160 },
  {
    title: '分类',
    key: 'category',
    width: 120,
    render: (row) => {
      const cat = categories.value.find(c => c.id === row.category_id)
      return cat?.name || '-'
    }
  },
  {
    title: '解析器',
    key: 'parser_type',
    width: 120,
    render: (row) => {
      const map = {
        rss: 'RSS',
        api_json: 'API-JSON',
        api_xml: 'API-XML',
        static_html: '静态网页',
        dynamic_html: '动态网页',
        webhook: 'Webhook'
      }
      return map[row.parser_type] || row.parser_type
    }
  },
  { title: 'URL', key: 'url', ellipsis: { tooltip: true } },
  {
    title: '状态',
    key: 'is_active',
    width: 90,
    render: (row) => {
      return h(NTag, { type: row.is_active ? 'success' : 'default' }, {
        default: () => row.is_active ? '启用' : '禁用'
      })
    }
  },
  {
    title: '自动发布',
    key: 'auto_publish',
    width: 90,
    render: (row) => row.auto_publish ? '是' : '否'
  },
  {
    title: 'AI预处理',
    key: 'ai_preprocess',
    width: 90,
    render: (row) => row.ai_preprocess ? '是' : '否'
  },
  {
    title: '去重策略',
    key: 'dedup_strategy',
    width: 120,
    render: (row) => {
      const map = { url: 'URL', title: '标题', content_hash: '内容哈希' }
      return map[row.dedup_strategy] || row.dedup_strategy
    }
  },
  { title: '抓取间隔(分)', key: 'fetch_interval', width: 110 },
  {
    title: '最后抓取',
    key: 'last_fetch_at',
    width: 160,
    render: (row) => row.last_fetch_at ? new Date(row.last_fetch_at).toLocaleString() : '-'
  },
  {
    title: '创建时间',
    key: 'created_at',
    width: 160,
    render: (row) => new Date(row.created_at).toLocaleString()
  },
  {
    title: '操作',
    key: 'actions',
    width: 160,
    fixed: 'right',
    render: (row) => {
      return h(NSpace, { size: 'small' }, {
        default: () => [
          h(NButton, {
            size: 'small',
            type: 'primary',
            text: true,
            onClick: () => handleEdit(row)
          }, { default: () => '编辑' }),
          h(NButton, {
            size: 'small',
            type: 'error',
            text: true,
            onClick: () => handleDelete(row)
          }, { default: () => '删除' })
        ]
      })
    }
  }
]

async function loadCategories() {
  try {
    const res = await getAllCategories()
    categories.value = res.data || []
    categoryOptions.value = [
      { label: '未分类', value: null },
      ...categories.value.map(c => ({ label: c.name, value: c.id }))
    ]
  } catch (e) {
    message.warning('分类加载失败')
  }
}

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      size: pageSize.value
    }
    if (searchKeyword.value) {
      params.keyword = searchKeyword.value
    }
    const res = await getSources(params)
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

function resetForm() {
  formData.value = {
    name: '',
    url: '',
    type: 'website',
    category_id: null,
    parser_type: 'rss',
    fetch_interval: 60,
    is_active: true,
    auto_publish: false,
    ai_preprocess: true,
    dedup_strategy: 'url',
    config: '{}',
    description: ''
  }
}

function handleCreate() {
  editingId.value = null
  modalTitle.value = '新建来源'
  resetForm()
  showModal.value = true
}

function formatConfig(config) {
  if (!config) return '{}'
  if (typeof config === 'string') {
    try {
      return JSON.stringify(JSON.parse(config), null, 2)
    } catch (e) {
      return config
    }
  }
  return JSON.stringify(config, null, 2)
}

function handleEdit(row) {
  editingId.value = row.id
  modalTitle.value = '编辑来源'
  formData.value = {
    name: row.name,
    url: row.url || '',
    type: row.type || 'website',
    category_id: row.category_id || null,
    parser_type: row.parser_type || 'rss',
    fetch_interval: row.fetch_interval ?? 60,
    is_active: row.is_active ?? true,
    auto_publish: row.auto_publish ?? false,
    ai_preprocess: row.ai_preprocess ?? true,
    dedup_strategy: row.dedup_strategy || 'url',
    config: formatConfig(row.config),
    description: row.description || ''
  }
  showModal.value = true
}

function handleDelete(row) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除来源「${row.name}」吗？`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await deleteSource(row.id)
        message.success('删除成功')
        loadData()
      } catch (e) {
        message.error(e.message || '删除失败')
      }
    }
  })
}

function buildSubmitData() {
  const data = { ...formData.value }
  try {
    data.config = data.config ? JSON.parse(data.config) : {}
  } catch (e) {
    data.config = {}
  }
  if (!data.category_id) {
    data.category_id = null
  }
  return data
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }

  try {
    const submitData = buildSubmitData()
    if (editingId.value) {
      await updateSource(editingId.value, submitData)
      message.success('更新成功')
    } else {
      await createSource(submitData)
      message.success('创建成功')
    }
    showModal.value = false
    loadData()
  } catch (e) {
    message.error(e.message || '保存失败')
  }
}

function handlePageChange(p) {
  page.value = p
  loadData()
}

onMounted(() => {
  loadCategories()
  loadData()
})
</script>

<template>
  <div class="source-list">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">来源管理</h2>
        <p class="page-desc">管理内容采集来源，配置解析规则和抓取策略</p>
      </div>
      <n-button type="primary" @click="handleCreate">
        <template #icon><plus-outlined /></template>
        新建来源
      </n-button>
    </div>
    <n-card>
      <n-space vertical :size="16">
        <n-space :size="12" align="center">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索来源名称..."
            style="width: 240px"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <search-outlined />
            </template>
          </n-input>
          <n-button type="primary" @click="handleSearch">搜索</n-button>
        </n-space>

        <n-data-table
          :columns="columns"
          :data="list"
          :loading="loading"
          :bordered="false"
          scroll-x="1400"
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
          />
        </div>
      </n-space>
    </n-card>

    <n-modal
      v-model:show="showModal"
      preset="dialog"
      :title="modalTitle"
      :show-icon="false"
      style="width: 600px"
    >
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-placement="left"
        label-width="110px"
      >
        <n-form-item label="来源名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入来源名称" />
        </n-form-item>

        <n-form-item label="来源类型" path="type">
          <n-select v-model:value="formData.type" :options="typeOptions" />
        </n-form-item>

        <n-form-item label="来源URL" path="url">
          <n-input v-model:value="formData.url" placeholder="https://..." />
        </n-form-item>

        <n-form-item label="所属分类" path="category_id">
          <n-select v-model:value="formData.category_id" :options="categoryOptions" clearable />
        </n-form-item>

        <n-form-item label="解析类型" path="parser_type">
          <n-select v-model:value="formData.parser_type" :options="parserTypeOptions" />
        </n-form-item>

        <n-form-item label="抓取间隔(分钟)" path="fetch_interval">
          <n-input-number
            v-model:value="formData.fetch_interval"
            :min="5"
            :max="1440"
            placeholder="分钟"
            style="width: 100%"
          />
        </n-form-item>

        <n-form-item label="启用状态" path="is_active">
          <n-switch v-model:value="formData.is_active">
            <template #checked>启用</template>
            <template #unchecked>禁用</template>
          </n-switch>
        </n-form-item>

        <n-form-item label="自动发布" path="auto_publish">
          <n-switch v-model:value="formData.auto_publish">
            <template #checked>开启</template>
            <template #unchecked>关闭</template>
          </n-switch>
        </n-form-item>

        <n-form-item label="AI预处理" path="ai_preprocess">
          <n-switch v-model:value="formData.ai_preprocess">
            <template #checked>开启</template>
            <template #unchecked>关闭</template>
          </n-switch>
        </n-form-item>

        <n-form-item label="去重策略" path="dedup_strategy">
          <n-select v-model:value="formData.dedup_strategy" :options="dedupStrategyOptions" />
        </n-form-item>

        <n-form-item label="扩展配置(JSON)" path="config">
          <n-input
            v-model:value="formData.config"
            type="textarea"
            :rows="4"
            placeholder='{"rss_url": "...", "selector": "..."}'
          />
        </n-form-item>

        <n-form-item label="描述" path="description">
          <n-input
            v-model:value="formData.description"
            type="textarea"
            :rows="2"
            placeholder="来源描述"
          />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space>
          <n-button @click="showModal = false">取消</n-button>
          <n-button type="primary" @click="handleSubmit">确定</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<style scoped>
.source-list {
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
</style>
