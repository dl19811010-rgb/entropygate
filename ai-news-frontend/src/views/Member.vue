<template>
  <div class="member-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">个人中心</h1>
        <p class="page-desc">管理你的账号资料与偏好设置</p>
      </div>

      <div class="member-grid">
        <aside class="member-sidebar">
          <div class="profile-card">
            <div class="profile-avatar">{{ avatarText }}</div>
            <div class="profile-name">{{ userStore.userInfo?.username }}</div>
            <div class="profile-email">{{ userStore.userInfo?.email }}</div>
          </div>

          <div class="menu-card">
            <button
              v-for="item in menuItems"
              :key="item.key"
              class="menu-item"
              :class="{ active: activeTab === item.key }"
              @click="activeTab = item.key"
            >
              <component :is="item.icon" class="menu-icon" />
              <span>{{ item.label }}</span>
            </button>
          </div>
        </aside>

        <main class="member-main">
          <!-- 个人资料 -->
          <div v-if="activeTab === 'profile'" class="panel-card">
            <div class="panel-header">
              <h2 class="panel-title">
                <person-outline />
                个人资料
              </h2>
            </div>

            <n-form class="member-form">
              <n-form-item label="用户名" :validation-status="usernameStatus" :feedback="usernameFeedback">
                <n-input
                  v-model:value="profileForm.username"
                  placeholder="请输入用户名"
                  size="large"
                  @input="validateUsername"
                  @blur="validateUsername"
                >
                  <template #suffix>
                    <checkmark-circle-outline v-if="usernameStatus === 'success'" class="status-icon success" />
                    <close-circle-outline v-else-if="usernameStatus === 'error'" class="status-icon error" />
                  </template>
                </n-input>
              </n-form-item>

              <n-form-item label="邮箱" :validation-status="emailStatus" :feedback="emailFeedback">
                <n-input
                  v-model:value="profileForm.email"
                  placeholder="请输入邮箱"
                  size="large"
                  @input="validateEmail"
                  @blur="validateEmail"
                >
                  <template #suffix>
                    <checkmark-circle-outline v-if="emailStatus === 'success'" class="status-icon success" />
                    <close-circle-outline v-else-if="emailStatus === 'error'" class="status-icon error" />
                  </template>
                </n-input>
              </n-form-item>

              <div v-if="profileMsg" class="form-feedback" :class="profileMsg.type">
                <checkmark-circle-outline v-if="profileMsg.type === 'success'" />
                <close-circle-outline v-else />
                <span>{{ profileMsg.text }}</span>
              </div>

              <n-button type="primary" size="large" :loading="profileLoading" @click="saveProfile">
                保存资料
              </n-button>
            </n-form>
          </div>

          <!-- 修改密码 -->
          <div v-else-if="activeTab === 'password'" class="panel-card">
            <div class="panel-header">
              <h2 class="panel-title">
                <lock-closed-outline />
                修改密码
              </h2>
            </div>

            <n-form class="member-form">
              <n-form-item label="当前密码" :validation-status="oldPasswordStatus" :feedback="oldPasswordFeedback">
                <n-input
                  v-model:value="pwdForm.oldPassword"
                  type="password"
                  placeholder="请输入当前密码"
                  size="large"
                  show-password-on="click"
                  @input="validateOldPassword"
                  @blur="validateOldPassword"
                >
                  <template #suffix>
                    <checkmark-circle-outline v-if="oldPasswordStatus === 'success'" class="status-icon success" />
                    <close-circle-outline v-else-if="oldPasswordStatus === 'error'" class="status-icon error" />
                  </template>
                </n-input>
              </n-form-item>

              <n-form-item label="新密码" :validation-status="newPasswordStatus" :feedback="newPasswordFeedback">
                <n-input
                  v-model:value="pwdForm.newPassword"
                  type="password"
                  placeholder="请输入新密码"
                  size="large"
                  show-password-on="click"
                  @input="validateNewPassword"
                  @blur="validateNewPassword"
                >
                  <template #suffix>
                    <checkmark-circle-outline v-if="newPasswordStatus === 'success'" class="status-icon success" />
                    <close-circle-outline v-else-if="newPasswordStatus === 'error'" class="status-icon error" />
                  </template>
                </n-input>
              </n-form-item>

              <n-form-item label="确认新密码" :validation-status="confirmStatus" :feedback="confirmFeedback">
                <n-input
                  v-model:value="pwdForm.confirmPassword"
                  type="password"
                  placeholder="请再次输入新密码"
                  size="large"
                  show-password-on="click"
                  @input="validateConfirm"
                  @blur="validateConfirm"
                >
                  <template #suffix>
                    <checkmark-circle-outline v-if="confirmStatus === 'success'" class="status-icon success" />
                    <close-circle-outline v-else-if="confirmStatus === 'error'" class="status-icon error" />
                  </template>
                </n-input>
              </n-form-item>

              <div v-if="pwdMsg" class="form-feedback" :class="pwdMsg.type">
                <checkmark-circle-outline v-if="pwdMsg.type === 'success'" />
                <close-circle-outline v-else />
                <span>{{ pwdMsg.text }}</span>
              </div>

              <n-button type="primary" size="large" :loading="pwdLoading" @click="savePassword">
                修改密码
              </n-button>
            </n-form>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  PersonOutline, LockClosedOutline,
  CheckmarkCircleOutline, CloseCircleOutline
} from '@vicons/ionicons5'

const router = useRouter()
const userStore = useUserStore()
const activeTab = ref('profile')

const menuItems = [
  { key: 'profile', label: '个人资料', icon: PersonOutline },
  { key: 'password', label: '修改密码', icon: LockClosedOutline }
]

const avatarText = computed(() => {
  return userStore.userInfo?.username?.charAt(0).toUpperCase() || 'U'
})

onMounted(() => {
  if (!userStore.isLoggedIn) {
    router.push({ path: '/login', query: { redirect: '/member' } })
  }
})

// 个人资料
const profileForm = reactive({
  username: userStore.userInfo?.username || '',
  email: userStore.userInfo?.email || ''
})

const usernameStatus = ref('')
const usernameFeedback = ref('')
const emailStatus = ref('')
const emailFeedback = ref('')
const profileLoading = ref(false)
const profileMsg = ref(null)

function validateUsername() {
  if (!profileForm.username) {
    usernameStatus.value = 'error'
    usernameFeedback.value = '请输入用户名'
    return false
  }
  if (profileForm.username.length < 3) {
    usernameStatus.value = 'error'
    usernameFeedback.value = '用户名至少 3 个字符'
    return false
  }
  usernameStatus.value = 'success'
  usernameFeedback.value = ''
  return true
}

function validateEmail() {
  if (!profileForm.email) {
    emailStatus.value = 'error'
    emailFeedback.value = '请输入邮箱'
    return false
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profileForm.email)) {
    emailStatus.value = 'error'
    emailFeedback.value = '邮箱格式不正确'
    return false
  }
  emailStatus.value = 'success'
  emailFeedback.value = ''
  return true
}

async function saveProfile() {
  profileMsg.value = null
  const ok = validateUsername() && validateEmail()
  if (!ok) return

  profileLoading.value = true
  await new Promise(resolve => setTimeout(resolve, 600))
  const res = userStore.updateProfile({
    username: profileForm.username,
    email: profileForm.email
  })
  profileLoading.value = false

  profileMsg.value = {
    type: res.success ? 'success' : 'error',
    text: res.message
  }
}

// 修改密码
const pwdForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const oldPasswordStatus = ref('')
const oldPasswordFeedback = ref('')
const newPasswordStatus = ref('')
const newPasswordFeedback = ref('')
const confirmStatus = ref('')
const confirmFeedback = ref('')
const pwdLoading = ref(false)
const pwdMsg = ref(null)

function validateOldPassword() {
  if (!pwdForm.oldPassword) {
    oldPasswordStatus.value = 'error'
    oldPasswordFeedback.value = '请输入当前密码'
    return false
  }
  oldPasswordStatus.value = 'success'
  oldPasswordFeedback.value = ''
  return true
}

function validateNewPassword() {
  if (!pwdForm.newPassword) {
    newPasswordStatus.value = 'error'
    newPasswordFeedback.value = '请输入新密码'
    return false
  }
  if (pwdForm.newPassword.length < 6) {
    newPasswordStatus.value = 'error'
    newPasswordFeedback.value = '密码长度不能少于 6 位'
    return false
  }
  newPasswordStatus.value = 'success'
  newPasswordFeedback.value = ''
  return true
}

function validateConfirm() {
  if (!pwdForm.confirmPassword) {
    confirmStatus.value = 'error'
    confirmFeedback.value = '请再次输入新密码'
    return false
  }
  if (pwdForm.confirmPassword !== pwdForm.newPassword) {
    confirmStatus.value = 'error'
    confirmFeedback.value = '两次输入的密码不一致'
    return false
  }
  confirmStatus.value = 'success'
  confirmFeedback.value = ''
  return true
}

async function savePassword() {
  pwdMsg.value = null
  const ok = validateOldPassword() && validateNewPassword() && validateConfirm()
  if (!ok) return

  pwdLoading.value = true
  await new Promise(resolve => setTimeout(resolve, 600))
  const res = userStore.changePassword({
    oldPassword: pwdForm.oldPassword,
    newPassword: pwdForm.newPassword
  })
  pwdLoading.value = false

  pwdMsg.value = {
    type: res.success ? 'success' : 'error',
    text: res.message
  }

  if (res.success) {
    pwdForm.oldPassword = ''
    pwdForm.newPassword = ''
    pwdForm.confirmPassword = ''
    oldPasswordStatus.value = ''
    newPasswordStatus.value = ''
    confirmStatus.value = ''
  }
}
</script>

<style scoped>
.member-page {
  padding: var(--spacing-xl) 0 var(--spacing-2xl);
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
}

.page-desc {
  font-size: 15px;
  color: var(--text-secondary);
}

.member-grid {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: var(--spacing-xl);
  align-items: start;
}

.member-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.profile-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  text-align: center;
}

.profile-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--brand-gradient);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  margin: 0 auto var(--spacing-md);
}

.profile-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  word-break: break-word;
}

.profile-email {
  font-size: 13px;
  color: var(--text-secondary);
  word-break: break-word;
}

.menu-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 14px 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:hover,
.menu-item.active {
  color: var(--brand-primary);
  background: rgba(99, 102, 241, 0.06);
}

.menu-icon {
  width: 18px;
  height: 18px;
}

.member-main {
  min-width: 0;
}

.panel-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
}

.panel-header {
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.panel-title svg {
  color: var(--brand-primary);
}

.member-form :deep(.n-form-item) {
  margin-bottom: var(--spacing-md);
}

.member-form {
  max-width: 420px;
}

.status-icon {
  width: 18px;
  height: 18px;
}

.status-icon.success {
  color: #22c55e;
}

.status-icon.error {
  color: #ef4444;
}

.form-feedback {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px;
  margin-bottom: var(--spacing-md);
  border-radius: var(--border-radius-md);
  font-size: 13px;
}

.form-feedback.success {
  background: rgba(34, 197, 94, 0.08);
  border: 1px solid rgba(34, 197, 94, 0.2);
  color: #16a34a;
}

.form-feedback.error {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #dc2626;
}

.form-feedback svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .member-grid {
    grid-template-columns: 1fr;
  }

  .member-sidebar {
    flex-direction: row;
    overflow-x: auto;
  }

  .profile-card {
    flex: 0 0 200px;
  }

  .menu-card {
    flex: 1;
    display: flex;
  }

  .menu-item {
    flex: 1;
    justify-content: center;
    border-bottom: none;
    border-right: 1px solid var(--border-color);
  }

  .menu-item:last-child {
    border-right: none;
  }
}
</style>
