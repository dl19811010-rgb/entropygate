<script setup>
import { ref, onMounted, h } from 'vue'
import {
  NCard, NDataTable, NButton, NSpace, NInput, NSelect,
  NPagination, useMessage, useDialog, NModal, NForm, NFormItem,
  NSwitch, NTag
} from 'naive-ui'
import { PlusOutlined, SearchOutlined, KeyOutlined } from '@vicons/antd'
import {
  getAdmins, createAdmin, updateAdmin, deleteAdmin, resetAdminPassword
} from '@/api/admin'
import { getAllRoles } from '@/api/role'
import { logError } from '@/utils/log'

const message = useMessage()
const dialog = useDialog()

const loading = ref(false)
const list = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')
const statusFilter = ref(null)

const showModal = ref(false)
const modalTitle = ref('')
const editingId = ref(null)
const formRef = ref(null)
const formData = ref({
  username: '',
  password: '',
  name: '',
  email: '',
  phone: '',
  role_ids: [],
  status: 'active',
  is_super: false
})

const showPwdModal = ref(false)
const pwdFormRef = ref(null)
const resetAdminId = ref(null)
const newPassword = ref('')

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur', min: 6 }
  ]
}

const pwdRules = {
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur', min: 6 }
  ]
}

const statusOptions = [
  { label: '全部状态', value: null },
  { label: '启用', value: 'active' },
  { label: '禁用', value: 'inactive' }
]

const roleOptions = ref([])

const columns = [
  { title: '用户名', key: 'username', width: 140 },
  { title: '姓名', key: 'name', width: 140 },
  { title: '邮箱', key: 'email', width: 200 },
  { title: '手机号', key: 'phone', width: 140 },
  {
    title: '角色',
    key: 'roles',
    width: 200,
    render: (row) => {
      return h(NSpace, { size: 'small' }, {
        default: () => row.roles?.map(r => h(NTag, { size: 'small' }, { default: () => r.name }))
      })
    }
  },
  {
    title: '超级管理员',
    key: 'is_super',
    width: 110,
    render: (row) => row.is_super ? h(NTag, { type: 'warning' }, { default: () => '是' }) : '否'
  },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render: (row) => {
      return h(NTag, { type: row.status === 'active' ? 'success' : 'default' }, {
        default: () => row.status === 'active' ? '启用' : '禁用'
      })
    }
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
    width: 220,
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
            text: true,
            onClick: () => handleResetPassword(row)
          }, { default: () => '重置密码' }),
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

async function loadRoles() {
  try {
    const res = await getAllRoles()
    roleOptions.value = res.data.map(r => ({
      label: r.name,
      value: r.id
    }))
  } catch (e) {
    logError('加载角色失败', e)
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
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    const res = await getAdmins(params)
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
  statusFilter.value = null
  page.value = 1
  loadData()
}

function handleCreate() {
  editingId.value = null
  modalTitle.value = '新建管理员'
  formData.value = {
    username: '',
    password: '',
    name: '',
    email: '',
    phone: '',
    role_ids: [],
    status: 'active',
    is_super: false
  }
  showModal.value = true
}

function handleEdit(row) {
  editingId.value = row.id
  modalTitle.value = '编辑管理员'
  formData.value = {
    username: row.username,
    password: '',
    name: row.name || '',
    email: row.email || '',
    phone: row.phone || '',
    role_ids: row.roles?.map(r => r.id) || [],
    status: row.status,
    is_super: row.is_super
  }
  showModal.value = true
}

function handleDelete(row) {
  dialog.warning({
    title: '确认删除',
    content: `确定要删除管理员「${row.username}」吗？`,
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await deleteAdmin(row.id)
        message.success('删除成功')
        loadData()
      } catch (e) {
        message.error(e.message || '删除失败')
      }
    }
  })
}

function handleResetPassword(row) {
  resetAdminId.value = row.id
  newPassword.value = ''
  showPwdModal.value = true
}

async function handleSubmitPwd() {
  if (!pwdFormRef.value) return
  try {
    await pwdFormRef.value.validate()
  } catch (e) {
    return
  }
  
  try {
    await resetAdminPassword(resetAdminId.value, newPassword.value)
    message.success('密码重置成功')
    showPwdModal.value = false
  } catch (e) {
    message.error(e.message || '重置失败')
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }
  
  try {
    const data = { ...formData.value }
    if (!editingId.value && !data.password) {
      message.error('请输入密码')
      return
    }
    if (editingId.value && !data.password) {
      delete data.password
    }
    
    if (editingId.value) {
      await updateAdmin(editingId.value, data)
      message.success('更新成功')
    } else {
      await createAdmin(data)
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
  loadRoles()
  loadData()
})
</script>

<template>
  <div class="admin-list">
    <div class="page-header">
      <div class="page-header-left">
        <h2 class="page-title">管理员管理</h2>
        <p class="page-desc">管理系统管理员账号、角色分配和权限</p>
      </div>
      <n-button type="primary" @click="handleCreate">
        <template #icon><plus-outlined /></template>
        新建管理员
      </n-button>
    </div>
    <n-card>
      <n-space vertical :size="16">
        <n-space :size="12" align="center">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索用户名/昵称..."
            style="width: 240px"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <search-outlined />
            </template>
          </n-input>
          <n-select
            v-model:value="statusFilter"
            :options="statusOptions"
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
          scroll-x="1500"
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
        <n-form-item label="用户名" path="username">
          <n-input v-model:value="formData.username" placeholder="请输入用户名" />
        </n-form-item>
        <n-form-item label="密码" path="password">
          <n-input
            v-model:value="formData.password"
            type="password"
            :placeholder="editingId ? '留空则不修改' : '请输入密码'"
            show-password-on="click"
          />
        </n-form-item>
        <n-form-item label="姓名">
          <n-input v-model:value="formData.name" placeholder="请输入姓名" />
        </n-form-item>
        <n-form-item label="邮箱">
          <n-input v-model:value="formData.email" placeholder="请输入邮箱" />
        </n-form-item>
        <n-form-item label="手机号">
          <n-input v-model:value="formData.phone" placeholder="请输入手机号" />
        </n-form-item>
        <n-form-item label="角色">
          <n-select
            v-model:value="formData.role_ids"
            :options="roleOptions"
            multiple
            placeholder="请选择角色"
            clearable
          />
        </n-form-item>
        <n-form-item label="状态">
          <n-select
            v-model:value="formData.status"
            :options="[
              { label: '启用', value: 'active' },
              { label: '禁用', value: 'inactive' }
            ]"
          />
        </n-form-item>
        <n-form-item label="超级管理员">
          <n-switch v-model:value="formData.is_super" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button @click="showModal = false">取消</n-button>
        <n-button type="primary" @click="handleSubmit">确定</n-button>
      </template>
    </n-modal>

    <n-modal v-model:show="showPwdModal" preset="dialog" title="重置密码" :show-icon="false">
      <n-form
        ref="pwdFormRef"
        :model="{ newPassword }"
        :rules="pwdRules"
        label-placement="left"
        label-width="110px"
      >
        <n-form-item label="新密码" path="newPassword">
          <n-input
            v-model:value="newPassword"
            type="password"
            placeholder="请输入新密码"
            show-password-on="click"
          >
            <template #prefix>
              <key-outlined />
            </template>
          </n-input>
        </n-form-item>
      </n-form>
      <template #action>
        <n-button @click="showPwdModal = false">取消</n-button>
        <n-button type="primary" @click="handleSubmitPwd">确定</n-button>
      </template>
    </n-modal>
  </div>
</template>

<style scoped>
.admin-list {
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
