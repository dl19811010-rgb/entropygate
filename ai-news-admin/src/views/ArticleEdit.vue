<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  NCard, NForm, NFormItem, NInput, NSelect, NSwitch, NButton, NSpace, useMessage,
  NUpload, NImage, NDivider
} from 'naive-ui'
import { getArticle, createArticle, updateArticle, rewriteArticle } from '@/api/article'
import { getAllCategories } from '@/api/category'
import { getAllTags } from '@/api/tag'
import { uploadImage } from '@/api/upload'
import { logError } from '@/utils/log'

const router = useRouter()
const route = useRoute()
const message = useMessage()

const isEdit = computed(() => !!route.params.id)
const pageTitle = computed(() => isEdit.value ? '编辑文章' : '新建文章')
const loading = ref(false)
const saving = ref(false)
const rewriting = ref(false)

const formRef = ref(null)
const formData = ref({
  title: '',
  slug: '',
  summary: '',
  content: '',
  cover_image: '',
  category_id: null,
  status: 'draft',
  is_featured: false,
  is_daily: false,
  source_name: '',
  source_url: '',
  tag_ids: []
})

const originalContent = ref('')
const showOriginal = ref(false)
const hasOriginal = ref(false)

const rules = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' }
  ],
  slug: [
    { required: true, message: '请输入Slug', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入内容', trigger: 'blur' }
  ],
  cover_image: [
    { required: true, message: '请上传封面图片', trigger: 'change' }
  ]
}

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '待编辑', value: 'approved' },
  { label: '已发布', value: 'published' },
  { label: '已下架', value: 'archived' }
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

async function loadArticle() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const res = await getArticle(route.params.id)
    const data = res.data
    formData.value = {
      title: data.title || '',
      slug: data.slug || '',
      summary: data.summary || '',
      content: data.content || '',
      cover_image: data.cover_image || '',
      category_id: data.category_id || null,
      status: data.status || 'draft',
      is_featured: data.is_featured || false,
      is_daily: data.is_daily || false,
      source_name: data.source_name || '',
      source_url: data.source_url || '',
      tag_ids: data.tags?.map(t => t.id) || []
    }
    // 提取原文（AI重写后保存在 extra_data.original_text）
    const extra = data.extra_data
    if (extra && extra.original_text) {
      originalContent.value = extra.original_text
      hasOriginal.value = true
    }
  } catch (e) {
    message.error(e.message || '加载失败')
  } finally {
    loading.value = false
  }
}

async function handleSave(publish = false) {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }

  saving.value = true
  try {
    const data = { ...formData.value }
    if (publish) {
      data.status = 'published'
    }
    
    if (isEdit.value) {
      await updateArticle(route.params.id, data)
      message.success('更新成功')
    } else {
      await createArticle(data)
      message.success('创建成功')
    }
    router.push('/articles')
  } catch (e) {
    message.error(e.message || '保存失败')
  } finally {
    saving.value = false
  }
}

function handleCancel() {
  router.push('/articles')
}

async function handleRewrite() {
  if (!isEdit.value) {
    message.warning('请先保存文章后再使用 AI 重写')
    return
  }
  if (!formData.value.content?.trim()) {
    message.warning('文章内容为空，无法重写')
    return
  }

  // 保存当前内容作为原文参考
  originalContent.value = formData.value.content
  hasOriginal.value = true
  showOriginal.value = false

  rewriting.value = true
  try {
    const res = await rewriteArticle(route.params.id)
    formData.value.content = res.data.content || res.data
    message.success('AI 翻译重写完成，可切换"查看原文"对比')
  } catch (e) {
    message.error(e.message || 'AI 翻译重写失败')
  } finally {
    rewriting.value = false
  }
}

async function handleCoverUpload({ file, onFinish, onError }) {
  try {
    const res = await uploadImage(file.file)
    formData.value.cover_image = res.data.url
    message.success('封面上传成功')
    onFinish()
  } catch (e) {
    message.error(e.message || '封面上传失败')
    onError()
  }
}

function removeCover() {
  formData.value.cover_image = ''
}

const contentInputRef = ref(null)

async function handleContentImageUpload({ file, onFinish, onError }) {
  try {
    const res = await uploadImage(file.file)
    const imageUrl = res.data.url
    const markdown = `\n![图片说明](${imageUrl})\n`

    const input = contentInputRef.value?.textareaElRef
    if (input) {
      const start = input.selectionStart || 0
      const end = input.selectionEnd || 0
      const text = formData.value.content
      formData.value.content = text.substring(0, start) + markdown + text.substring(end)
      setTimeout(() => {
        input.focus()
        input.setSelectionRange(start + markdown.length, start + markdown.length)
      }, 0)
    } else {
      formData.value.content += markdown
    }
    message.success('图片已插入')
    onFinish()
  } catch (e) {
    message.error(e.message || '图片插入失败')
    onError()
  }
}

onMounted(() => {
  loadCategories()
  loadTags()
  loadArticle()
})
</script>

<template>
  <div class="article-edit">
    <n-card :title="pageTitle">
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-placement="left"
        label-width="110px"
        :disabled="loading"
      >
        <n-form-item label="标题" path="title">
          <n-input v-model:value="formData.title" placeholder="请输入标题" />
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
        <n-form-item label="封面图片" path="cover_image">
          <div class="cover-uploader">
            <n-image
              v-if="formData.cover_image"
              :src="formData.cover_image"
              class="cover-preview"
              object-fit="cover"
            />
            <n-upload
              v-if="!formData.cover_image"
              :custom-request="handleCoverUpload"
              :show-file-list="false"
              accept="image/*"
            >
              <n-button>上传封面</n-button>
            </n-upload>
            <n-button
              v-else
              size="small"
              class="btn-danger"
              @click="removeCover"
            >
              删除封面
            </n-button>
            <p class="upload-tip">建议尺寸 800×450，支持 jpg/png/webp/gif，最大 10MB</p>
          </div>
        </n-form-item>
        <n-form-item label="摘要">
          <n-input
            v-model:value="formData.summary"
            type="textarea"
            :rows="3"
            placeholder="文章摘要"
          />
        </n-form-item>
        <n-form-item label="内容" path="content">
          <div class="content-editor">
            <div class="editor-toolbar">
              <n-upload
                :custom-request="handleContentImageUpload"
                :show-file-list="false"
                accept="image/*"
              >
                <n-button size="small">插入图片</n-button>
              </n-upload>
              <n-button
                size="small"
                :loading="rewriting"
                :disabled="!isEdit"
                @click="handleRewrite"
              >
                AI 翻译重写
              </n-button>
            </div>
            <n-input
              ref="contentInputRef"
              v-model:value="formData.content"
              type="textarea"
              :rows="15"
              placeholder="文章内容（支持 Markdown）"
            />
          </div>
        </n-form-item>
        <n-form-item label="来源名称">
          <n-input v-model:value="formData.source_name" placeholder="来源网站名称" />
        </n-form-item>
        <n-form-item label="来源链接">
          <div class="source-url-row">
            <n-input v-model:value="formData.source_url" placeholder="原文链接" />
            <n-button
              v-if="formData.source_url"
              size="small"
              text
              type="primary"
              tag="a"
              :href="formData.source_url"
              target="_blank"
            >
              打开原文
            </n-button>
          </div>
        </n-form-item>

        <!-- 原文对照区 -->
        <n-form-item v-if="hasOriginal" label="原文对照">
          <div class="original-section">
            <n-button size="small" text @click="showOriginal = !showOriginal">
              {{ showOriginal ? '收起原文' : '查看原文' }}
            </n-button>
            <div v-if="showOriginal" class="original-content">
              {{ originalContent.slice(0, 2000) }}{{ originalContent.length > 2000 ? '...' : '' }}
            </div>
          </div>
        </n-form-item>
        <n-form-item label="状态">
          <n-select
            v-model:value="formData.status"
            :options="statusOptions"
          />
        </n-form-item>
        <n-form-item label="精选文章">
          <n-switch v-model:value="formData.is_featured" />
        </n-form-item>
        <n-form-item label="每日推荐">
          <n-switch v-model:value="formData.is_daily" />
        </n-form-item>
        <n-form-item label="">
          <n-space>
            <n-button type="primary" :loading="saving" @click="handleSave(false)">
              保存草稿
            </n-button>
            <n-button type="primary" :loading="saving" @click="handleSave(true)">
              {{ isEdit ? '保存并发布' : '立即发布' }}
            </n-button>
            <n-button @click="handleCancel">取消</n-button>
          </n-space>
        </n-form-item>
      </n-form>
    </n-card>
  </div>
</template>

<style scoped>
.article-edit {
  max-width: 900px;
}

.cover-uploader {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cover-preview {
  width: 320px;
  height: 180px;
  border-radius: var(--border-radius-md);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.upload-tip {
  margin: 0;
  font-size: 12px;
  color: var(--text-placeholder);
}

.content-editor {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  overflow: hidden;
}

.editor-toolbar {
  display: flex;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-hover);
  border-bottom: 1px solid var(--border-color);
}

.content-editor :deep(.n-input) {
  border: none;
  border-radius: 0;
}

.content-editor :deep(.n-input__textarea-el) {
  padding: 12px;
  font-family: 'SF Mono', Monaco, monospace;
  font-size: 14px;
  line-height: 1.6;
}

.btn-danger {
  color: var(--gray-600, #4b5563) !important;
}

.btn-danger:hover {
  color: var(--danger, #ef4444) !important;
}

.source-url-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.original-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.original-content {
  padding: 12px;
  background: var(--bg-tertiary, #f9fafb);
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: 8px;
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary, #6b7280);
  max-height: 300px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
