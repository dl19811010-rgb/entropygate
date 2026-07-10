<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo" @click="goHome">
        <svg viewBox="0 0 32 32" width="40" height="40">
          <defs>
            <linearGradient id="authLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#6366f1"/>
              <stop offset="100%" stop-color="#8b5cf6"/>
            </linearGradient>
          </defs>
          <path d="M16 2L26 8V24L16 30L6 24V8L16 2Z" fill="url(#authLogoGrad)"/>
          <circle cx="16" cy="16" r="4" fill="white" opacity="0.9"/>
        </svg>
        <span>EntropyGate AI</span>
      </div>

      <h1 class="auth-title">欢迎回来</h1>
      <p class="auth-subtitle">登录后继续浏览 AI 资讯</p>

      <n-form class="auth-form">
        <n-form-item label="邮箱" :validation-status="emailStatus" :feedback="emailFeedback">
          <n-input
            v-model:value="form.email"
            placeholder="请输入邮箱"
            size="large"
            @input="validateEmail"
            @blur="validateEmail"
          >
            <template #prefix>
              <mail-outline />
            </template>
            <template #suffix>
              <checkmark-circle-outline v-if="emailStatus === 'success'" class="status-icon success" />
              <close-circle-outline v-else-if="emailStatus === 'error'" class="status-icon error" />
            </template>
          </n-input>
        </n-form-item>

        <n-form-item label="密码" :validation-status="passwordStatus" :feedback="passwordFeedback">
          <n-input
            v-model:value="form.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password-on="click"
            @input="validatePassword"
            @blur="validatePassword"
          >
            <template #prefix>
              <lock-closed-outline />
            </template>
            <template #suffix>
              <checkmark-circle-outline v-if="passwordStatus === 'success'" class="status-icon success" />
              <close-circle-outline v-else-if="passwordStatus === 'error'" class="status-icon error" />
            </template>
          </n-input>
        </n-form-item>

        <div class="auth-options">
          <n-checkbox v-model:checked="rememberMe">记住我</n-checkbox>
          <a href="#" class="forgot-link">忘记密码？</a>
        </div>

        <div v-if="errorMsg" class="form-error">
          <close-circle-outline />
          <span>{{ errorMsg }}</span>
        </div>

        <n-button type="primary" size="large" :loading="loading" block @click="handleLogin">
          登录
        </n-button>
      </n-form>

      <div class="auth-footer">
        还没有账号？
        <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  MailOutline, LockClosedOutline,
  CheckmarkCircleOutline, CloseCircleOutline
} from '@vicons/ionicons5'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const loading = ref(false)
const rememberMe = ref(false)

const form = reactive({
  email: '',
  password: ''
})

const emailStatus = ref('')
const emailFeedback = ref('')
const passwordStatus = ref('')
const passwordFeedback = ref('')
const errorMsg = ref('')

function validateEmail() {
  if (!form.email) {
    emailStatus.value = 'error'
    emailFeedback.value = '请输入邮箱'
    return false
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    emailStatus.value = 'error'
    emailFeedback.value = '邮箱格式不正确'
    return false
  }
  emailStatus.value = 'success'
  emailFeedback.value = ''
  return true
}

function validatePassword() {
  if (!form.password) {
    passwordStatus.value = 'error'
    passwordFeedback.value = '请输入密码'
    return false
  }
  if (form.password.length < 6) {
    passwordStatus.value = 'error'
    passwordFeedback.value = '密码长度不能少于 6 位'
    return false
  }
  passwordStatus.value = 'success'
  passwordFeedback.value = ''
  return true
}

function goHome() {
  router.push('/')
}

async function handleLogin() {
  errorMsg.value = ''
  const ok = validateEmail() && validatePassword()
  if (!ok) return

  loading.value = true
  const res = await simulateLogin()
  loading.value = false

  if (res.success) {
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } else {
    errorMsg.value = res.message
  }
}

function simulateLogin() {
  return new Promise((resolve) => {
    setTimeout(() => {
      const result = userStore.login({ email: form.email, password: form.password, remember: rememberMe.value })
      resolve(result)
    }, 600)
  })
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-xl);
}

.auth-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
  cursor: pointer;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.auth-logo svg {
  flex-shrink: 0;
}

.auth-title {
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
}

.auth-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.auth-form :deep(.n-form-item) {
  margin-bottom: var(--spacing-md);
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

.form-error {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px;
  margin-bottom: var(--spacing-md);
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: var(--border-radius-md);
  font-size: 13px;
  color: #dc2626;
}

.form-error svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.auth-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-lg);
  font-size: 13px;
}

.forgot-link {
  color: var(--brand-primary);
  transition: color var(--transition-fast);
}

.forgot-link:hover {
  color: var(--brand-secondary);
}

.auth-footer {
  text-align: center;
  margin-top: var(--spacing-xl);
  font-size: 14px;
  color: var(--text-secondary);
}

.auth-footer a {
  color: var(--brand-primary);
  font-weight: 500;
  margin-left: 4px;
}

.auth-footer a:hover {
  color: var(--brand-secondary);
}

@media (max-width: 480px) {
  .auth-card {
    padding: var(--spacing-xl);
  }
}
</style>
