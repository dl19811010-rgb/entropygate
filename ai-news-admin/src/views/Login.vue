<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAdminStore } from '@/stores/admin'
import { NForm, NFormItem, NInput, NButton, useMessage } from 'naive-ui'
import { UserOutlined, LockOutlined } from '@vicons/antd'

const router = useRouter()
const route = useRoute()
const adminStore = useAdminStore()
const message = useMessage()

const formRef = ref(null)
const loading = ref(false)
const formData = ref({
  username: '',
  password: '',
  remember: false
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

async function handleLogin() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    await adminStore.login(formData.value.username, formData.value.password, formData.value.remember)
    message.success('登录成功，欢迎回来！')

    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } catch (e) {
    if (e.message) {
      message.error(e.message)
    }
  } finally {
    loading.value = false
  }
}

const particles = ref([])

function initParticles() {
  const count = 20
  for (let i = 0; i < count; i++) {
    particles.value.push({
      id: i,
      size: Math.random() * 60 + 20,
      left: Math.random() * 100,
      top: Math.random() * 100,
      duration: Math.random() * 20 + 15,
      delay: Math.random() * -20
    })
  }
}

onMounted(() => {
  initParticles()
})
</script>

<template>
  <div class="login-page">
    <div class="bg-decoration">
      <div class="gradient-bg"></div>
      <div class="grid-overlay"></div>
      <div class="particles">
        <div
          v-for="p in particles"
          :key="p.id"
          class="particle"
          :style="{
            width: p.size + 'px',
            height: p.size + 'px',
            left: p.left + '%',
            top: p.top + '%',
            animationDuration: p.duration + 's',
            animationDelay: p.delay + 's'
          }"
        ></div>
      </div>
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
      <div class="glow glow-3"></div>
    </div>

    <div class="login-container">
      <div class="login-wrapper">
        <div class="brand-section">
          <div class="brand-logo">
            <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M32 4L52 16V48L32 60L12 48V16L32 4Z" stroke="#111827" stroke-width="2" fill="rgba(17,24,39,0.04)"/>
              <path d="M32 20L42 26V38L32 44L22 38V26L32 20Z" fill="#111827" opacity="0.15"/>
              <circle cx="32" cy="32" r="4" fill="#111827"/>
            </svg>
          </div>
          <h1 class="brand-title">EntropyGate AI</h1>
          <p class="brand-subtitle">AI 新闻资讯管理平台</p>
          <div class="brand-tags">
            <span class="brand-tag">智能采集</span>
            <span class="brand-tag">分类管理</span>
            <span class="brand-tag">数据洞察</span>
          </div>
        </div>

        <div class="login-card-wrapper">
          <div class="login-card">
            <div class="card-header">
              <h2 class="card-title">欢迎登录</h2>
              <p class="card-desc">请输入您的账号信息以继续</p>
            </div>

            <n-form
              ref="formRef"
              :model="formData"
              :rules="rules"
              label-placement="top"
              @submit.prevent="handleLogin"
            >
              <n-form-item label="用户名" path="username">
                <n-input
                  v-model:value="formData.username"
                  placeholder="请输入用户名"
                  size="large"
                  :bordered="false"
                  class="custom-input"
                >
                  <template #prefix>
                    <user-outlined class="input-icon" />
                  </template>
                </n-input>
              </n-form-item>

              <n-form-item label="密码" path="password">
                <n-input
                  v-model:value="formData.password"
                  type="password"
                  placeholder="请输入密码"
                  size="large"
                  :bordered="false"
                  show-password-on="click"
                  class="custom-input"
                  @keyup.enter="handleLogin"
                >
                  <template #prefix>
                    <lock-outlined class="input-icon" />
                  </template>
                </n-input>
              </n-form-item>

              <div class="form-actions">
                <label class="remember-me">
                  <input type="checkbox" v-model="formData.remember" />
                  <span>记住我</span>
                </label>
                <a class="forgot-link" href="javascript:;" @click="message.info('请联系超级管理员重置密码')">忘记密码？</a>
              </div>

              <n-button
                type="primary"
                size="large"
                block
                :loading="loading"
                class="login-btn"
                @click="handleLogin"
              >
                <span v-if="!loading">登 录</span>
              </n-button>
            </n-form>

            <div class="card-footer">
              <p>© 2026 EntropyGate AI · All Rights Reserved</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  overflow: hidden;
}

.gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 30%, #4c1d95 60%, #581c87 100%);
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(129, 140, 248, 0.4) 0%, transparent 70%);
  animation: float linear infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0.3;
  }
  50% {
    transform: translateY(-30px) translateX(20px) scale(1.1);
    opacity: 0.6;
  }
}

.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
}

.glow-1 {
  width: 400px;
  height: 400px;
  background: #6366f1;
  top: -100px;
  left: -100px;
  animation: glowMove1 15s ease-in-out infinite;
}

.glow-2 {
  width: 500px;
  height: 500px;
  background: #a855f7;
  bottom: -150px;
  right: -100px;
  animation: glowMove2 18s ease-in-out infinite;
}

.glow-3 {
  width: 300px;
  height: 300px;
  background: #ec4899;
  top: 40%;
  left: 60%;
  opacity: 0.3;
  animation: glowMove3 20s ease-in-out infinite;
}

@keyframes glowMove1 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(50px, 50px); }
}

@keyframes glowMove2 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-50px, -30px); }
}

@keyframes glowMove3 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-40px, 40px); }
}

.login-container {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-wrapper {
  display: flex;
  align-items: center;
  gap: 80px;
  max-width: 1000px;
  width: 100%;
}

.brand-section {
  flex: 1;
  color: white;
}

.brand-logo {
  width: 72px;
  height: 72px;
  margin-bottom: 24px;
}

.brand-logo svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 8px 32px rgba(99, 102, 241, 0.4));
}

.brand-title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 12px;
  background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

.brand-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 32px;
  font-weight: 400;
}

.brand-tags {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.brand-tag {
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

.login-card-wrapper {
  width: 420px;
  flex-shrink: 0;
}

.login-card {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 40px 36px 32px;
  box-shadow: 
    0 0 0 1px rgba(255, 255, 255, 0.1),
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 80px rgba(99, 102, 241, 0.15);
}

.card-header {
  margin-bottom: 32px;
  text-align: center;
}

.card-title {
  font-size: 26px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.card-desc {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.custom-input {
  background: #f9fafb;
  border-radius: 12px !important;
  transition: all 0.2s ease;
}

.custom-input :deep(.n-input__input-el) {
  font-size: 14px;
}

.custom-input :deep(.n-input__border) {
  border-color: transparent;
  border-radius: 12px;
}

.custom-input:hover {
  background: #f3f4f6;
}

.custom-input :deep(.n-input--focus) {
  background: #fff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.input-icon {
  color: #9ca3af;
  font-size: 18px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  margin-top: -8px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #6b7280;
  cursor: pointer;
  user-select: none;
}

.remember-me input {
  cursor: pointer;
  accent-color: #6366f1;
}

.forgot-link {
  font-size: 13px;
  color: #6366f1;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #4f46e5;
}

.login-btn {
  height: 46px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
  transition: all 0.3s ease !important;
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}

.login-btn:active {
  transform: translateY(0);
}

.card-footer {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
  text-align: center;
}

.card-footer p {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

/* 登录页白色简洁风格覆盖 */
.login-page {
  background: #ffffff;
}

.bg-decoration {
  display: none;
}

.brand-section {
  color: var(--text-primary);
}

.brand-title {
  background: none;
  -webkit-text-fill-color: var(--text-primary);
  color: var(--text-primary);
}

.brand-subtitle {
  color: var(--text-secondary);
}

.brand-tag {
  background: #ffffff;
  border-color: var(--gray-200);
  color: var(--text-secondary);
}

.brand-logo svg {
  filter: none;
}

.login-card {
  background: #ffffff;
  box-shadow: none;
  border: 1px solid var(--gray-100);
}

.login-btn {
  background: #111827 !important;
  box-shadow: none !important;
  transform: none !important;
}

.login-btn:hover {
  background: #374151 !important;
  box-shadow: none !important;
  transform: none !important;
}

.forgot-link {
  color: var(--text-regular);
}

.forgot-link:hover {
  color: var(--text-primary);
}

.remember-me input {
  accent-color: #111827;
}

.custom-input :deep(.n-input--focus) {
  box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.08);
}

@media (max-width: 900px) {
  .login-wrapper {
    flex-direction: column;
    gap: 40px;
  }

  .brand-section {
    text-align: center;
  }

  .brand-logo {
    margin: 0 auto 20px;
  }

  .brand-tags {
    justify-content: center;
  }

  .brand-title {
    font-size: 32px;
  }

  .login-card-wrapper {
    width: 100%;
    max-width: 420px;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px 24px;
  }

  .brand-title {
    font-size: 28px;
  }

  .brand-subtitle {
    font-size: 15px;
  }
}
</style>
