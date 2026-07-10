<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NMenu, NButton, NInput } from 'naive-ui'
import { SearchOutlined } from '@vicons/antd'

const router = useRouter()
const route = useRoute()
const searchKeyword = ref('')
const menuOptions = [
  { label: '首页', key: '/' },
  { label: 'AI新动态', key: '/news' },
  { label: 'AI工具库', key: '/tools' }
]

function handleMenuSelect(key) {
  router.push(key)
}

function handleSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/news', query: { q: searchKeyword.value } })
  }
}
</script>

<template>
  <header class="app-header">
    <div class="header-inner">
      <div class="logo" @click="router.push('/')">
        <span class="logo-text">EntropyGate AI</span>
      </div>
      <nav class="nav-menu">
        <n-menu
          mode="horizontal"
          :value="route.path"
          :options="menuOptions"
          @update:value="handleMenuSelect"
        />
      </nav>
      <div class="header-right">
        <n-input
          v-model:value="searchKeyword"
          placeholder="搜索文章、工具..."
          style="width: 220px"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <component :is="SearchOutlined" />
          </template>
        </n-input>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  z-index: 1000;
  box-shadow: var(--shadow-sm);
}

.header-inner {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.logo {
  cursor: pointer;
  flex-shrink: 0;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  flex: 1;
}

.nav-menu :deep(.n-menu) {
  border-bottom: none;
  background: transparent;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style>
