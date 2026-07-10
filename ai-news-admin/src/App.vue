<template>
  <n-config-provider :theme="theme" :theme-overrides="themeOverrides" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-loading-bar-provider>
            <router-view v-slot="{ Component, route }">
              <component :is="Component" :key="route.fullPath" />
            </router-view>
          </n-loading-bar-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import { onMounted } from 'vue'
import { NConfigProvider, NMessageProvider, NDialogProvider, NNotificationProvider, NLoadingBarProvider } from 'naive-ui'
import { themeOverrides, zhCN, dateZhCN } from '@/styles/theme'
import { useAdminStore } from '@/stores/admin'

const theme = null
const adminStore = useAdminStore()

onMounted(() => {
  if (adminStore.isLoggedIn) {
    adminStore.fetchCurrentAdmin().catch(() => {})
  }
})
</script>

<style>
@import '@/styles/global.css';
</style>
