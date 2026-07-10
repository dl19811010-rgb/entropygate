<template>
  <div class="main-layout">
    <header class="site-header">
      <div class="container header-inner">
        <div class="logo-area" @click="goHome">
          <div class="logo-icon">
            <svg viewBox="0 0 32 32" width="32" height="32">
              <defs>
                <linearGradient id="headerLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#6366f1"/>
                  <stop offset="100%" stop-color="#8b5cf6"/>
                </linearGradient>
              </defs>
              <path d="M16 2L26 8V24L16 30L6 24V8L16 2Z" fill="url(#headerLogoGrad)"/>
              <circle cx="16" cy="16" r="4" fill="white" opacity="0.9"/>
            </svg>
          </div>
          <span class="logo-text">EntropyGate <span class="logo-accent">AI</span></span>
        </div>

        <nav class="main-nav">
          <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">
            <home-outline class="nav-icon" />
            <span>首页</span>
          </router-link>
          <router-link to="/news" class="nav-link" :class="{ active: route.path === '/news' }">
            <flash-outline class="nav-icon" />
            <span>AI新动态</span>
          </router-link>
          <router-link to="/tools" class="nav-link" :class="{ active: route.path.startsWith('/tools') }">
            <construct-outline class="nav-icon" />
            <span>工具库</span>
          </router-link>
        </nav>

        <div class="header-right">
          <div class="search-box" :class="{ focused: searchFocused }">
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索文章..."
              :bordered="false"
              clearable
              @focus="searchFocused = true"
              @blur="searchFocused = false"
              @keydown.enter="handleSearch"
            >
              <template #prefix>
                <search-outline class="search-icon" />
              </template>
            </n-input>
          </div>

          <template v-if="userStore.isLoggedIn">
            <n-dropdown :options="userMenuOptions" placement="bottom-end" trigger="click" @select="handleUserMenuSelect">
              <div class="user-trigger">
                <div class="user-avatar">{{ avatarText }}</div>
                <span class="user-name">{{ userStore.userInfo?.username }}</span>
                <chevron-down-outline class="user-arrow" />
              </div>
            </n-dropdown>
          </template>
          <template v-else>
            <div class="auth-buttons">
              <n-button quaternary size="small" @click="router.push('/login')">
                登录
              </n-button>
              <n-button type="primary" size="small" @click="router.push('/register')">
                注册
              </n-button>
            </div>
          </template>

          <a v-if="userStore.isLoggedIn" href="/admin" target="_blank" class="admin-link">
            <settings-outline class="admin-icon" />
          </a>
        </div>

        <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
          <menu-outline v-if="!mobileMenuOpen" />
          <close-outline v-else />
        </button>
      </div>

      <div v-if="mobileMenuOpen" class="mobile-menu">
        <div class="container">
          <router-link to="/" class="mobile-nav-link" @click="mobileMenuOpen = false">首页</router-link>
          <router-link to="/news" class="mobile-nav-link" @click="mobileMenuOpen = false">AI新动态</router-link>
          <router-link to="/tools" class="mobile-nav-link" @click="mobileMenuOpen = false">工具库</router-link>
          <router-link to="/search" class="mobile-nav-link" @click="mobileMenuOpen = false">搜索</router-link>
          <div class="mobile-nav-divider"></div>
          <template v-if="userStore.isLoggedIn">
            <router-link to="/member" class="mobile-nav-link" @click="mobileMenuOpen = false">
              <person-outline class="mobile-nav-icon" />
              个人中心
            </router-link>
            <a href="#" class="mobile-nav-link" @click.prevent="handleLogout">
              <log-out-outline class="mobile-nav-icon" />
              退出登录
            </a>
          </template>
          <template v-else>
            <router-link to="/login" class="mobile-nav-link" @click="mobileMenuOpen = false">登录</router-link>
            <router-link to="/register" class="mobile-nav-link" @click="mobileMenuOpen = false">注册</router-link>
          </template>
        </div>
      </div>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="site-footer">
      <div class="container footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">
            <svg viewBox="0 0 32 32" width="28" height="28">
              <defs>
                <linearGradient id="footerLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#6366f1"/>
                  <stop offset="100%" stop-color="#8b5cf6"/>
                </linearGradient>
              </defs>
              <path d="M16 2L26 8V24L16 30L6 24V8L16 2Z" fill="url(#footerLogoGrad)"/>
              <circle cx="16" cy="16" r="4" fill="white" opacity="0.9"/>
            </svg>
            <span>EntropyGate AI</span>
          </div>
          <p class="footer-desc">探索 AI 领域的无限可能，汇聚全球前沿人工智能资讯</p>
        </div>

        <div class="footer-links">
          <div class="footer-col">
            <h4>内容分类</h4>
            <router-link to="/news">AI新动态</router-link>
            <router-link to="/tools">工具库</router-link>
          </div>
          <div class="footer-col">
            <h4>关于我们</h4>
            <a href="#">关于 EntropyGate</a>
            <a href="#">联系方式</a>
            <a href="#">隐私政策</a>
            <a href="#">使用条款</a>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="container">
          <p>© 2026 EntropyGate AI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  HomeOutline, SearchOutline, FlashOutline, ConstructOutline,
  SettingsOutline, MenuOutline, CloseOutline, ChevronDownOutline,
  PersonOutline, LogOutOutline
} from '@vicons/ionicons5'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const searchKeyword = ref('')
const searchFocused = ref(false)
const mobileMenuOpen = ref(false)

const avatarText = computed(() => {
  return userStore.userInfo?.username?.charAt(0).toUpperCase() || 'U'
})

const userMenuOptions = [
  { label: '个人中心', key: 'profile' },
  { label: '退出登录', key: 'logout' }
]

function goHome() {
  router.push('/')
}

function handleSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/search', query: { q: searchKeyword.value } })
  }
}

function handleUserMenuSelect(key) {
  if (key === 'profile') {
    router.push('/member')
  } else if (key === 'logout') {
    handleLogout()
  }
}

function handleLogout() {
  userStore.logout()
  mobileMenuOpen.value = false
  router.push('/')
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--header-height);
  gap: var(--spacing-md);
  min-width: 0;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  flex-shrink: 0;
  min-width: 0;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.3px;
  white-space: nowrap;
}

.logo-accent {
  background: var(--brand-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.main-nav {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  flex: 1;
  justify-content: center;
  min-width: 0;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: var(--border-radius-md);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  position: relative;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
}

.nav-link:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.nav-link.active {
  color: var(--brand-primary);
  background: rgba(99, 102, 241, 0.1);
}

.nav-icon {
  width: var(--icon-sm);
  height: var(--icon-sm);
  flex-shrink: 0;
}

.chevron {
  width: var(--icon-xs);
  height: var(--icon-xs);
  transition: transform var(--transition-fast);
  flex-shrink: 0;
}

.category-nav:hover .chevron {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 180px;
  max-width: 260px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: 8px;
  margin-top: 8px;
  box-shadow: var(--shadow-lg);
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-item {
  display: block;
  padding: 10px 14px;
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-shrink: 0;
  min-width: 0;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.user-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 4px;
  border-radius: 100px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.user-trigger:hover {
  background: var(--bg-secondary);
  border-color: var(--border-light);
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--brand-gradient);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-arrow {
  width: 14px;
  height: 14px;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.search-box {
  width: 220px;
  transition: all var(--transition-normal);
  flex-shrink: 0;
}

.search-box.focused {
  width: 280px;
}

.search-box :deep(.n-input) {
  background: var(--bg-secondary);
  border-radius: var(--border-radius-full) !important;
  padding: 0 8px;
}

.search-box :deep(.n-input__input) {
  font-size: 13px;
}

.search-icon {
  color: var(--text-tertiary);
  width: var(--icon-sm);
  height: var(--icon-sm);
}

.admin-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: var(--border-radius-md);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.admin-link:hover {
  background: var(--bg-hover);
  color: var(--brand-primary);
}

.admin-icon {
  width: var(--icon-md);
  height: var(--icon-md);
}

.mobile-menu-btn {
  display: none;
  width: 38px;
  height: 38px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-size: 20px;
}

.mobile-menu {
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
  padding: var(--spacing-md) 0;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
}

.mobile-nav-icon {
  width: 18px;
  height: 18px;
  color: var(--text-tertiary);
}

.mobile-nav-divider {
  height: 1px;
  background: var(--border-color);
  margin: 8px 0;
}

.mobile-nav-label {
  padding: 12px 0 8px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-tertiary);
  letter-spacing: 0.5px;
}

.mobile-cat-link {
  display: inline-block;
  padding: 6px 12px;
  margin: 4px 6px 4px 0;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-full);
  font-size: 13px;
  color: var(--text-secondary);
}

.main-content {
  flex: 1;
}

.site-footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  margin-top: var(--spacing-2xl);
}

.footer-inner {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 120px;
  padding: var(--spacing-2xl) 0;
}

.footer-brand {
  flex: 0 0 320px;
  max-width: 360px;
  min-width: 0;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  white-space: nowrap;
}

.footer-logo svg {
  flex-shrink: 0;
}

.footer-desc {
  color: var(--text-tertiary);
  font-size: 14px;
  line-height: 1.7;
  word-break: keep-all;
  overflow-wrap: break-word;
  text-wrap: pretty;
}

.footer-links {
  display: flex;
  gap: var(--spacing-2xl);
  flex-wrap: wrap;
}

.footer-col {
  min-width: 0;
  width: 140px;
}

.footer-col h4 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  white-space: nowrap;
}

.footer-col a {
  display: block;
  padding: 6px 0;
  font-size: 14px;
  color: var(--text-tertiary);
  transition: color var(--transition-fast);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.footer-col a:hover {
  color: var(--brand-primary);
}

.footer-bottom {
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-md) 0;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 13px;
}

@media (max-width: 1024px) {
  .main-nav {
    display: none;
  }
  
  .search-box {
    display: none;
  }
  
  .mobile-menu-btn {
    display: flex;
  }
  
  .footer-inner {
    flex-direction: column;
    gap: var(--spacing-xl);
    text-align: center;
  }

  .footer-brand {
    flex: 0 0 auto;
    max-width: 100%;
  }

  .footer-logo {
    justify-content: center;
  }

  .footer-links {
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .header-inner {
    gap: var(--spacing-sm);
  }
  
  .logo-text {
    font-size: 16px;
  }
  
  .header-right {
    gap: var(--spacing-sm);
  }
  
  .admin-link {
    width: 34px;
    height: 34px;
  }
  
  .footer-inner {
    flex-direction: column;
    gap: var(--spacing-xl);
  }
  
  .footer-links {
    gap: var(--spacing-xl);
  }
}
</style>
