import { defineStore } from 'pinia'
import { login as apiLogin, getCurrentAdmin, logout as apiLogout } from '@/api/auth'

function safeParseJSON(str) {
  try {
    return JSON.parse(str)
  } catch (e) {
    return null
  }
}

const TOKEN_KEY = 'admin_token'
const ADMIN_INFO_KEY = 'admin_info'

// 优先读 localStorage，其次 sessionStorage，兼容历史仅用 localStorage 的状态
function readToken() {
  return localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY) || ''
}

function readAdminInfo() {
  const raw = localStorage.getItem(ADMIN_INFO_KEY) || sessionStorage.getItem(ADMIN_INFO_KEY)
  return safeParseJSON(raw || 'null')
}

function clearStored() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(ADMIN_INFO_KEY)
  sessionStorage.removeItem(TOKEN_KEY)
  sessionStorage.removeItem(ADMIN_INFO_KEY)
}

export const useAdminStore = defineStore('admin', {
  state: () => ({
    token: readToken(),
    adminInfo: readAdminInfo()
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    isSuperAdmin: (state) => state.adminInfo?.is_super || false
  },

  actions: {
    async login(username, password, remember = true) {
      const res = await apiLogin({ username, password })
      this.token = res.data.access_token
      this.adminInfo = res.data.admin
      // 先清理所有存储，再按是否记住写入对应存储
      clearStored()
      const storage = remember ? localStorage : sessionStorage
      storage.setItem(TOKEN_KEY, this.token)
      storage.setItem(ADMIN_INFO_KEY, JSON.stringify(this.adminInfo))
      return res
    },

    async fetchCurrentAdmin() {
      const res = await getCurrentAdmin()
      this.adminInfo = res.data
      // 写回当前使用的存储
      const storage = localStorage.getItem(TOKEN_KEY) ? localStorage : sessionStorage
      storage.setItem(ADMIN_INFO_KEY, JSON.stringify(this.adminInfo))
      return res
    },

    async logout() {
      try {
        await apiLogout()
      } catch (e) {
        // ignore
      }
      this.token = ''
      this.adminInfo = null
      clearStored()
    }
  }
})
