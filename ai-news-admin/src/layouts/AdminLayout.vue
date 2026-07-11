<script setup>
import { ref, computed, h, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAdminStore } from '@/stores/admin'
import { useMessage } from 'naive-ui'
import {
  NLayout, NLayoutSider, NLayoutHeader, NLayoutContent,
  NMenu, NDropdown, NAvatar, NIcon, NButton, NBadge, NSpace,
  NBreadcrumb, NBreadcrumbItem
} from 'naive-ui'
import {
  DashboardOutlined,
  FileTextOutlined,
  ToolOutlined,
  FolderOpenOutlined,
  TagsOutlined,
  ShareAltOutlined,
  CloudDownloadOutlined,
  UserOutlined,
  LogoutOutlined,
  TeamOutlined,
  SafetyCertificateOutlined,
  FileSearchOutlined,
  SettingOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
  FullscreenOutlined,
  FullscreenExitOutlined,
  HomeOutlined
} from '@vicons/antd'

const router = useRouter()
const route = useRoute()
const adminStore = useAdminStore()
const message = useMessage()
const collapsed = ref(false)
const isFullscreen = ref(false)
const notificationCount = ref(0)

const menuOptions = computed(() => {
  const baseMenu = [
    {
      label: '仪表盘',
      key: '/dashboard',
      icon: () => h(DashboardOutlined)
    },
    {
      label: '内容管理',
      key: '/content',
      icon: () => h(FileTextOutlined),
      children: [
        {
          label: '文章管理',
          key: '/articles',
          icon: () => h(FileTextOutlined)
        },
        {
          label: '文章审核',
          key: '/articles/review',
          icon: () => h(SafetyCertificateOutlined)
        },
        {
          label: '工具管理',
          key: '/tools',
          icon: () => h(ToolOutlined)
        }
      ]
    },
    {
      label: '分类管理',
      key: '/categories',
      icon: () => h(FolderOpenOutlined)
    },
    {
      label: '标签管理',
      key: '/tags',
      icon: () => h(TagsOutlined)
    },
    {
      label: '来源管理',
      key: '/sources',
      icon: () => h(ShareAltOutlined)
    },
    {
      label: '采集监控',
      key: '/crawler-monitor',
      icon: () => h(CloudDownloadOutlined)
    }
  ]

  // 仅超管可见：系统管理及其子菜单
  if (adminStore.isSuperAdmin) {
    baseMenu.push({
      label: '系统管理',
      key: '/system',
      icon: () => h(SettingOutlined),
      children: [
        {
          label: '管理员管理',
          key: '/system/admins',
          icon: () => h(TeamOutlined)
        },
        {
          label: '角色权限',
          key: '/system/roles',
          icon: () => h(SafetyCertificateOutlined)
        },
        {
          label: '审计日志',
          key: '/system/audit-logs',
          icon: () => h(FileSearchOutlined)
        }
      ]
    })
  }

  return baseMenu
})

const userDropdownOptions = [
  {
    label: '个人信息',
    key: 'profile',
    icon: () => h(UserOutlined)
  },
  {
    type: 'divider',
    key: 'd1'
  },
  {
    label: '退出登录',
    key: 'logout',
    icon: () => h(LogoutOutlined)
  }
]

const activeKey = computed(() => {
  if (route.meta.activeMenu) {
    return route.meta.activeMenu
  }
  return route.path
})

const expandedKeys = ref([])

function updateExpandedKeysByRoute() {
  const keys = []
  if (route.path.startsWith('/articles') || route.path.startsWith('/tools')) {
    keys.push('/content')
  }
  if (route.path.startsWith('/system/')) {
    keys.push('/system')
  }
  expandedKeys.value = keys
}

updateExpandedKeysByRoute()
watch(() => route.path, updateExpandedKeysByRoute)

function handleExpandedKeysUpdate(keys) {
  expandedKeys.value = keys
}

const breadcrumbItems = computed(() => {
  const items = []
  const matched = route.matched.filter(r => r.meta && r.meta.title && r.path !== '/')
  
  if (matched.length > 0) {
    items.push({ label: '首页', key: '/dashboard', icon: () => h(HomeOutlined), clickable: true })
  }
  
  matched.forEach((r, index) => {
    items.push({
      label: r.meta.title,
      key: r.path,
      clickable: index < matched.length - 1
    })
  })
  
  return items
})

function handleMenuSelect(key) {
  router.push(key)
}

function handleUserSelect(key) {
  if (key === 'profile') {
    message.info('个人信息功能即将上线，当前可在「系统管理-管理员管理」查看账号信息')
  } else if (key === 'logout') {
    handleLogout()
  }
}

async function handleLogout() {
  await adminStore.logout()
  router.push('/login')
}

function handleNotificationClick() {
  if (notificationCount.value === 0) {
    message.info('暂无新通知')
  } else {
    message.info(`您有 ${notificationCount.value} 条未读通知`)
  }
}

function toggleCollapse() {
  collapsed.value = !collapsed.value
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    document.exitFullscreen()
    isFullscreen.value = false
  }
}
</script>

<template>
  <n-layout has-sider class="admin-layout">
    <n-layout-sider
      :collapsed="collapsed"
      :collapsed-width="64"
      :width="240"
      :native-scrollbar="false"
      show-trigger="bar"
      class="layout-sider"
      @collapse="collapsed = true"
      @expand="collapsed = false"
    >
      <div class="logo-area">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 2L26 8V24L16 30L6 24V8L16 2Z" fill="#111827"/>
            <circle cx="16" cy="16" r="4" fill="white" opacity="0.9"/>
          </svg>
        </div>
        <div class="logo-text" v-show="!collapsed">EntropyGate AI</div>
      </div>

      <div class="menu-wrapper">
        <n-menu
          :value="activeKey"
          :expanded-keys="expandedKeys"
          :options="menuOptions"
          :collapsed="collapsed"
          :collapsed-width="64"
          :indent="20"
          @update:value="handleMenuSelect"
          @update:expanded-keys="handleExpandedKeysUpdate"
        />
      </div>

      <div class="sider-footer" v-show="!collapsed">
        <div class="version-info">
          <span class="version-label">版本</span>
          <span class="version-num">v1.0.0</span>
        </div>
      </div>
    </n-layout-sider>

    <n-layout class="main-layout">
      <n-layout-header class="layout-header" :bordered="false">
        <div class="header-left">
          <n-button
            text
            size="medium"
            class="collapse-btn"
            @click="toggleCollapse"
          >
            <template #icon>
              <n-icon size="18">
                <menu-unfold-outlined v-if="collapsed" />
                <menu-fold-outlined v-else />
              </n-icon>
            </template>
          </n-button>

          <div class="breadcrumb-area" v-if="breadcrumbItems.length > 1">
            <n-breadcrumb>
              <n-breadcrumb-item
                v-for="(item, index) in breadcrumbItems"
                :key="item.key"
                :class="{ 'clickable': item.clickable }"
                @click="item.clickable && handleMenuSelect(item.key)"
              >
                <n-icon v-if="item.icon" class="breadcrumb-icon">
                  <component :is="item.icon" />
                </n-icon>
                <span>{{ item.label }}</span>
              </n-breadcrumb-item>
            </n-breadcrumb>
          </div>
        </div>

        <div class="header-right">
          <n-space :size="8">
            <n-button text size="medium" class="header-btn" @click="handleNotificationClick">
              <template #icon>
                <n-badge :value="notificationCount" :max="99" :show-zero="false">
                  <n-icon size="18">
                    <bell-outlined />
                  </n-icon>
                </n-badge>
              </template>
            </n-button>

            <n-button
              text
              size="medium"
              class="header-btn"
              @click="toggleFullscreen"
            >
              <template #icon>
                <n-icon size="18">
                  <fullscreen-exit-outlined v-if="isFullscreen" />
                  <fullscreen-outlined v-else />
                </n-icon>
              </template>
            </n-button>

            <n-button
              text
              size="medium"
              class="header-btn"
              title="退出登录"
              @click="handleLogout"
            >
              <template #icon>
                <n-icon size="18">
                  <logout-outlined />
                </n-icon>
              </template>
            </n-button>
          </n-space>

          <div class="divider"></div>

          <n-dropdown
            :options="userDropdownOptions"
            trigger="click"
            placement="bottom-end"
            @select="handleUserSelect"
          >
            <div class="user-info">
              <n-avatar size="small" class="user-avatar">
                <template #icon>
                  <user-outlined />
                </template>
              </n-avatar>
              <div class="user-detail" v-show="!collapsed">
                <div class="user-name">{{ adminStore.adminInfo?.name || adminStore.adminInfo?.username || '管理员' }}</div>
                <div class="user-role">{{ adminStore.adminInfo?.is_super ? '超级管理员' : '管理员' }}</div>
              </div>
            </div>
          </n-dropdown>
        </div>
      </n-layout-header>

      <n-layout-content class="layout-content">
        <div class="page-container">
          <router-view />
        </div>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<style scoped>
.admin-layout {
  height: 100vh;
}

.layout-sider {
  background: var(--bg-container) !important;
  border-right: 1px solid var(--border-color-light);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 10;
}

.logo-area {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-bottom: 1px solid var(--border-color-light);
  flex-shrink: 0;
}

.logo-icon {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.logo-text {
  font-size: 17px;
  font-weight: 700;
  color: #111827;
  white-space: nowrap;
}

.menu-wrapper {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 12px 8px;
}

.menu-wrapper :deep(.n-menu) {
  background: transparent;
  border-right: none;
}

.menu-wrapper :deep(.n-menu-item) {
  height: 40px;
  border-radius: 8px;
  margin: 2px 0;
}

.menu-wrapper :deep(.n-menu-item--selected) {
  background: var(--gray-100, #f3f4f6) !important;
  color: var(--gray-900, #111827) !important;
  font-weight: 500;
}

.menu-wrapper :deep(.n-menu-item--selected .n-menu-item-content__icon) {
  color: var(--gray-900, #111827) !important;
}

.menu-wrapper :deep(.n-menu-item-content__icon) {
  font-size: 18px;
}

.menu-wrapper :deep(.n-submenu) {
  border-radius: 8px;
  margin: 2px 0;
}

.menu-wrapper :deep(.n-submenu-children) {
  padding: 4px 0;
}

.menu-wrapper :deep(.n-submenu-children .n-menu-item) {
  height: 36px;
  padding-left: 16px !important;
}

.sider-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-color-light);
  flex-shrink: 0;
}

.version-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-placeholder);
}

.main-layout {
  flex: 1;
  min-width: 0;
  background: var(--bg-body);
}

.layout-header {
  height: 60px;
  background: var(--bg-container) !important;
  border-bottom: 1px solid var(--border-color-light) !important;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
  box-shadow: none;
  position: relative;
  z-index: 5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
  min-width: 0;
}

.collapse-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px !important;
  color: var(--text-secondary);
}

.collapse-btn:hover {
  background: var(--border-color-light) !important;
}

.breadcrumb-area {
  min-width: 0;
}

.breadcrumb-area :deep(.n-breadcrumb) {
  font-size: 14px;
}

.breadcrumb-icon {
  margin-right: 4px;
  font-size: 14px;
}

.breadcrumb-item.clickable {
  cursor: pointer;
  transition: color 0.2s;
}

.breadcrumb-item.clickable:hover {
  color: var(--gray-900, #111827);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.header-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px !important;
  color: var(--text-secondary);
}

.header-btn:hover {
  background: var(--border-color-light) !important;
}

.divider {
  width: 1px;
  height: 20px;
  background: var(--border-color);
  margin: 0 4px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 4px 8px 4px 4px;
  border-radius: var(--border-radius-md);
  transition: background 0.2s;
}

.user-info:hover {
  background: var(--bg-hover);
}

.user-avatar {
  background: var(--gray-100);
  color: var(--text-secondary);
  border: none;
}

.user-detail {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.user-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.user-role {
  font-size: 11px;
  color: var(--text-placeholder);
  margin-top: 2px;
}

.layout-content {
  overflow: hidden;
  background: var(--bg-body);
}

.page-container {
  padding: 24px;
  height: calc(100vh - 60px);
  min-width: fit-content;
  overflow: auto;
}

@media (max-width: 768px) {
  .page-container {
    padding: 16px;
  }

  .breadcrumb-area {
    display: none;
  }

  .user-detail {
    display: none;
  }
}
</style>
