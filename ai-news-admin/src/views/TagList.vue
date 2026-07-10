<script setup>
import { ref, onMounted, h } from 'vue'
import {
  NCard, NDataTable, NButton, NSpace, NInput, NPagination,
  useMessage, useDialog, NModal, NForm, NFormItem
} from 'naive-ui'
import { PlusOutlined, DeleteOutlined, SearchOutlined } from '@vicons/antd'
import {
  getTags, createTag, updateTag, deleteTag
} from '@/api/tag'

const message = useMessage()
const dialog = useDialog()

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')

const showModal = ref(false)
const modalTitle = ref('')
const editingId = ref(null)
const formRef = ref(null)
const formData = ref({
  name: '',
  slug: ''
})

const rules = {
  name: [
    { required: true, message: '请输入标签名称', trigger: 'blur' }
  ]
}

const columns = [
  { title: '标签名称', key: 'name', width: 200 },
  { title: 'Slug', key: 'slug', width: 200 },
  {
    title: '创建时间',
    key: 'created_at',
    width: 180,
    render: (row) => new Date(row.created_at).toLocaleString()
  },
  {
    title: '操作',
    key: 'actions',
    width: 160,
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
    const res = await getTags(params)
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

function handleCreate() {
  editingId.value = null
  modalTitle.value = '新建标签'
  formData.value = { name: '', slug: '' }
  showModal.value = true
}

function handleEdit(row) {
  editingId.value = row.id
  modalTitle.value = '编辑标签'
  formData.value = {
    name: row.name,
    slug: row.slug || ''
  }
  showModal.value = true
}

function handleDelete(row) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除标签「${row.name}」吗？`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await deleteTag(row.id)
        message.success('删除成功')
        loadData()
      } catch (e) {
        message.error(e.message || '删除失败')
      }
    }
  })
}

async function handleSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }
  
  try {
    if (editingId.value) {
      await updateTag(editingId.value, formData.value)
      message.success('更新成功')
    } else {
      await createTag(formData.value)
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
  loadData()
})
</script>

<template>
  <div class="tag-list">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">标签管理</h2>
        <p class="page-desc">管理文章标签，支持创建、编辑和搜索</p>
      </div>
      <n-button type="primary" @click="handleCreate">
        <template #icon><plus-outlined /></template>
        新建标签
      </n-button>
    </div>
    <n-card>
      <n-space vertical :size="16">
        <n-space :size="12" align="center">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索标签名称..."
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
          scroll-x="800"
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

    <n-modal v-model:show="showModal" preset="dialog" :title="modalTitle" :show-icon="false" style="width: 600px">
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-placement="left"
        label-width="100px"
      >
        <n-form-item label="标签名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入标签名称" />
        </n-form-item>
        <n-form-item label="Slug">
          <n-input v-model:value="formData.slug" placeholder="可选，留空自动生成" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button @click="showModal = false">取消</n-button>
        <n-button type="primary" @click="handleSubmit">确定</n-button>
      </template>
    </n-modal>
  </div>
</template>

<style scoped>
.tag-list {
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
