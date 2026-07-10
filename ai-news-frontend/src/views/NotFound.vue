<script setup>
import { useRouter } from 'vue-router'
import { NButton } from 'naive-ui'

const router = useRouter()
</script>

<template>
  <div class="not-found-page">
    <div class="content">
      <div class="code">404</div>
      <h1 class="title">页面不存在</h1>
      <p class="desc">你访问的页面可能已被移除或链接错误</p>
      <n-button type="primary" size="large" @click="router.push('/')">
        返回首页
      </n-button>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
}

.content {
  text-align: center;
}

.code {
  font-size: 120px;
  font-weight: 800;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 20px;
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.desc {
  font-size: 15px;
  color: var(--text-tertiary);
  margin-bottom: 32px;
}
</style>
