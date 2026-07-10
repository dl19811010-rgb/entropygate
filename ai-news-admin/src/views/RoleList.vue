<script setup>
import { ref, onMounted, h } from 'vue'
import {
  NCard, NDataTable, NButton, NSpace, NInput, NPagination,
  useMessage, useDialog, NModal, NForm, NFormItem,
  NTree, NTag, NDescriptions, NDescriptionsItem
} from 'naive-ui'
import { PlusOutlined, SearchOutlined, SafetyOutlined } from '@vicons/antd'
import {
  getRoles, createRole, updateRole, deleteRole,
  getPermissionsByModule
} from '@/api/role'
import { logError } from '@/utils/log'

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
  code: '',
  description: '',
  permission_ids: []
})

const rules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入角色编码', trigger: 'blur' }
  ]
}

const permTreeData = ref([])
const checkedPermKeys = ref([])

const columns = [
  { title: '角色名称', key: 'name', width: 180 },
  { title: '角色编码', key: 'code', width: 180 },
  { title: '描述', key: 'description', ellipsis: { tooltip: true } },
  {
    title: '权限数量',
    key: 'permissions',
    width: 100,
    render: (row) => row.permissions?.length || 0
  },
  {
    title: '创建时间',
    key: 'created_at',
    width: 180,
    render: (row) => new Date(row.created_at).toLocaleString()
  },
  {
    title: '操作',
    key: 'actions',
    width: 180,
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

function buildPermTree(permsByModule) {
  const tree = []
  for (const [module, perms] of Object.entries(permsByModule)) {
    tree.push({
      label: module,
      key: 'module-' + module,
      children: perms.map(p => ({
        label: p.name + ' (' + p.code + ')',
        key: p.id
      }))
    })
  }
  return tree
}

async function loadPermissions() {
  try {
    const res = await getPermissionsByModule()
    permTreeData.value = buildPermTree(res.data)
  } catch (e) {
    logError('加载权限失败', e)
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
    const res = await getRoles(params)
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
  modalTitle.value = '新建角色'
  formData.value = {
    name: '',
    code: '',
    description: '',
    permission_ids: []
  }
  checkedPermKeys.value = []
  showModal.value = true
}

function handleEdit(row) {
  editingId.value = row.id
  modalTitle.value = '编辑角色'
  formData.value = {
    name: row.name,
    code: row.code,
    description: row.description || '',
    permission_ids: row.permissions?.map(p => p.id) || []
  }
  checkedPermKeys.value = row.permissions?.map(p => p.id) || []
  showModal.value = true
}

function handleDelete(row) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除角色「${row.name}」吗？`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await deleteRole(row.id)
        message.success('删除成功')
        loadData()
      } catch (e) {
        message.error(e.message || '删除失败')
      }
    }
  })
}

function handlePermCheck(keys) {
  const leafKeys = keys.filter(k => !k.startsWith('module-'))
  checkedPermKeys.value = leafKeys
  formData.value.permission_ids = leafKeys
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
      await updateRole(editingId.value, formData.value)
      message.success('更新成功')
    } else {
      await createRole(formData.value)
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
  loadPermissions()
  loadData()
})
</script>

<template>
  <div class="role-list">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">角色权限</h2>
        <p class="page-desc">管理角色和权限分配，控制后台访问权限</p>
      </div>
      <n-button type="primary" @click="handleCreate">
        <template #icon><plus-outlined /></template>
        新建角色
      </n-button>
    </div>
    <n-card>
      <n-space vertical :size="16">
        <n-space :size="12" align="center">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索角色名称..."
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
        label-width="110px"
      >
        <n-form-item label="角色名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入角色名称" />
        </n-form-item>
        <n-form-item label="角色编码" path="code">
          <n-input v-model:value="formData.code" placeholder="请输入角色编码，如: editor" />
        </n-form-item>
        <n-form-item label="描述">
          <n-input
            v-model:value="formData.description"
            type="textarea"
            :rows="2"
            placeholder="角色描述"
          />
        </n-form-item>
        <n-form-item label="权限分配">
          <div class="perm-tree-wrapper">
            <n-tree
              :data="permTreeData"
              :checked-keys="checkedPermKeys"
              selectable
              checkable
              default-expand-all
              @update:checked-keys="handlePermCheck"
            />
          </div>
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
.role-list {
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

.perm-tree-wrapper {
  width: 100%;
  max-height: 360px;
  overflow-y: auto;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  padding: 12px;
}
</style>
