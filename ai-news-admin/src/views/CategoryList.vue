<script setup>
import { ref, onMounted, h } from 'vue'
import {
  NCard, NDataTable, NButton, NSpace, NInput, NPagination,
  useMessage, useDialog, NModal, NForm, NFormItem, NInputNumber
} from 'naive-ui'
import { PlusOutlined, SearchOutlined } from '@vicons/antd'
import {
  getCategories, createCategory, updateCategory, deleteCategory
} from '@/api/category'

const message = useMessage()
const dialog = useDialog()

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')

const showModal = ref(false)
const modalTitle = ref('')
const editingId = ref(null)
const formRef = ref(null)
const formData = ref({
  name: '',
  slug: '',
  description: '',
  sort_order: 0
})

const rules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' }
  ],
  slug: [
    { required: true, message: '请输入Slug', trigger: 'blur' }
  ]
}

const columns = [
  { title: '名称', key: 'name', width: 200 },
  { title: 'Slug', key: 'slug', width: 180 },
  { title: '描述', key: 'description', ellipsis: { tooltip: true } },
  { title: '排序', key: 'sort_order', width: 80 },
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
    const res = await getCategories(params)
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
  modalTitle.value = '新建分类'
  formData.value = { name: '', slug: '', description: '', sort_order: 0 }
  showModal.value = true
}

function handleEdit(row) {
  editingId.value = row.id
  modalTitle.value = '编辑分类'
  formData.value = {
    name: row.name,
    slug: row.slug,
    description: row.description || '',
    sort_order: row.sort_order || 0
  }
  showModal.value = true
}

function handleDelete(row) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除分类「${row.name}」吗？`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await deleteCategory(row.id)
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
      await updateCategory(editingId.value, formData.value)
      message.success('更新成功')
    } else {
      await createCategory(formData.value)
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
  <div class="category-list">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">分类管理</h2>
        <p class="page-desc">管理文章分类，支持创建、编辑和排序</p>
      </div>
      <n-button type="primary" @click="handleCreate">
        <template #icon><plus-outlined /></template>
        新建分类
      </n-button>
    </div>
    <n-card>
      <n-space vertical :size="16">
        <n-space :size="12" align="center">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索分类名称..."
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
          scroll-x="900"
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

    <n-modal v-model:show="showModal" preset="dialog" :title="modalTitle" :show-icon="false" style="width: 600px">
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-placement="left"
        label-width="100px"
      >
        <n-form-item label="分类名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入分类名称" />
        </n-form-item>
        <n-form-item label="Slug" path="slug">
          <n-input v-model:value="formData.slug" placeholder="url-friendly slug" />
        </n-form-item>
        <n-form-item label="描述">
          <n-input
            v-model:value="formData.description"
            type="textarea"
            :rows="3"
            placeholder="分类描述"
          />
        </n-form-item>
        <n-form-item label="排序权重">
          <n-input-number v-model:value="formData.sort_order" :min="0" />
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
.category-list {
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
