<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  NCard, NForm, NFormItem, NInput, NSelect, NSwitch, NButton, NSpace,
  NInputNumber, useMessage
} from 'naive-ui'
import { getTool, createTool, updateTool } from '@/api/tool'
import { getAllCategories } from '@/api/category'
import { getAllTags } from '@/api/tag'
import { logError } from '@/utils/log'

const router = useRouter()
const route = useRoute()
const message = useMessage()

const isEdit = computed(() => !!route.params.id)
const pageTitle = computed(() => isEdit.value ? '编辑工具' : '新建工具')
const loading = ref(false)
const saving = ref(false)

const formRef = ref(null)
const formData = ref({
  name: '',
  slug: '',
  description: '',
  full_description: '',
  website_url: '',
  logo_url: '',
  category_id: null,
  pricing_type: 'free',
  pricing_url: '',
  availability_status: 'pending',
  availability_note: '',
  status: 'active',
  sort_order: 0,
  tag_ids: []
})

const rules = {
  name: [
    { required: true, message: '请输入工具名称', trigger: 'blur' }
  ],
  slug: [
    { required: true, message: '请输入Slug', trigger: 'blur' }
  ]
}

const statusOptions = [
  { label: '启用', value: 'active' },
  { label: '禁用', value: 'inactive' }
]

const pricingOptions = [
  { label: '免费', value: 'free' },
  { label: '付费', value: 'paid' },
  { label: '免费+付费', value: 'freemium' },
  { label: '开源', value: 'opensource' }
]

const availabilityOptions = [
  { label: '国内可用', value: 'available' },
  { label: '部分受限', value: 'partial' },
  { label: '已被封禁', value: 'blocked' },
  { label: '仅企业版', value: 'enterprise' },
  { label: '待核实', value: 'pending' }
]

const categoryOptions = ref([])
const tagOptions = ref([])

async function loadCategories() {
  try {
    const res = await getAllCategories()
    categoryOptions.value = res.data.map(item => ({
      label: item.name,
      value: item.id
    }))
  } catch (e) {
    logError('加载分类失败', e)
  }
}

async function loadTags() {
  try {
    const res = await getAllTags()
    tagOptions.value = res.data.map(item => ({
      label: item.name,
      value: item.id
    }))
  } catch (e) {
    logError('加载标签失败', e)
  }
}

async function loadTool() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const res = await getTool(route.params.id)
    const data = res.data
    formData.value = {
      name: data.name || '',
      slug: data.slug || '',
      description: data.description || '',
      full_description: data.full_description || '',
      website_url: data.website_url || '',
      logo_url: data.logo_url || '',
      category_id: data.category_id || null,
      pricing_type: data.pricing_type || 'free',
      pricing_url: data.pricing_url || '',
      availability_status: data.availability_status || 'pending',
      availability_note: data.availability_note || '',
      status: data.status || 'active',
      sort_order: data.sort_order || 0,
      tag_ids: data.tags?.map(t => t.id) || []
    }
  } catch (e) {
    message.error(e.message || '加载失败')
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }

  saving.value = true
  try {
    if (isEdit.value) {
      await updateTool(route.params.id, formData.value)
      message.success('更新成功')
    } else {
      await createTool(formData.value)
      message.success('创建成功')
    }
    router.push('/tools')
  } catch (e) {
    message.error(e.message || '保存失败')
  } finally {
    saving.value = false
  }
}

function handleCancel() {
  router.push('/tools')
}

onMounted(() => {
  loadCategories()
  loadTags()
  loadTool()
})
</script>

<template>
  <div class="tool-edit">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">{{ pageTitle }}</h2>
      </div>
    </div>
    <n-card>
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-placement="left"
        label-width="110px"
        :disabled="loading"
      >
        <n-form-item label="工具名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入工具名称" />
        </n-form-item>
        <n-form-item label="Slug" path="slug">
          <n-input v-model:value="formData.slug" placeholder="url-friendly slug" />
        </n-form-item>
        <n-form-item label="分类">
          <n-select
            v-model:value="formData.category_id"
            :options="categoryOptions"
            placeholder="请选择分类"
            clearable
          />
        </n-form-item>
        <n-form-item label="标签">
          <n-select
            v-model:value="formData.tag_ids"
            :options="tagOptions"
            multiple
            placeholder="请选择标签"
            clearable
          />
        </n-form-item>
        <n-form-item label="简短描述">
          <n-input
            v-model:value="formData.description"
            type="textarea"
            :rows="2"
            placeholder="一句话描述"
          />
        </n-form-item>
        <n-form-item label="详细描述">
          <n-input
            v-model:value="formData.full_description"
            type="textarea"
            :rows="8"
            placeholder="详细介绍"
          />
        </n-form-item>
        <n-form-item label="官网地址">
          <n-input v-model:value="formData.website_url" placeholder="https://..." />
        </n-form-item>
        <n-form-item label="Logo地址">
          <n-input v-model:value="formData.logo_url" placeholder="图片URL" />
        </n-form-item>
        <n-form-item label="定价模式">
          <n-select
            v-model:value="formData.pricing_type"
            :options="pricingOptions"
          />
        </n-form-item>
        <n-form-item label="定价页面">
          <n-input v-model:value="formData.pricing_url" placeholder="定价页面链接" />
        </n-form-item>
        <n-form-item label="可用性状态">
          <n-select
            v-model:value="formData.availability_status"
            :options="availabilityOptions"
          />
        </n-form-item>
        <n-form-item label="可用性说明">
          <n-input
            v-model:value="formData.availability_note"
            type="textarea"
            :rows="2"
            placeholder="可用性补充说明"
          />
        </n-form-item>
        <n-form-item label="状态">
          <n-select
            v-model:value="formData.status"
            :options="statusOptions"
          />
        </n-form-item>
        <n-form-item label="排序权重">
          <n-input-number v-model:value="formData.sort_order" :min="0" />
        </n-form-item>
        <n-form-item label="">
          <n-space>
            <n-button type="primary" :loading="saving" @click="handleSave">
              保存
            </n-button>
            <n-button @click="handleCancel">取消</n-button>
          </n-space>
        </n-form-item>
      </n-form>
    </n-card>
  </div>
</template>

<style scoped>
.tool-edit {
  max-width: 900px;
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
</style>
