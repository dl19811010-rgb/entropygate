import { defineStore } from 'pinia'

const STORAGE_KEY = 'eg_users'
const SESSION_KEY = 'eg_current_user'

function loadUsers() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  } catch (e) {
    return []
  }
}

function saveUsers(users) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(users))
}

// remember=true 写 localStorage（跨会话保留），remember=false 写 sessionStorage（关闭标签即失效）
function saveSession(user, remember = true) {
  clearSession()
  const storage = remember ? localStorage : sessionStorage
  storage.setItem(SESSION_KEY, JSON.stringify(user))
}

function loadSession() {
  try {
    const raw = localStorage.getItem(SESSION_KEY) || sessionStorage.getItem(SESSION_KEY)
    return raw ? JSON.parse(raw) : null
  } catch (e) {
    return null
  }
}

function clearSession() {
  localStorage.removeItem(SESSION_KEY)
  sessionStorage.removeItem(SESSION_KEY)
}

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: loadSession()
  }),

  getters: {
    isLoggedIn: (state) => !!state.currentUser?.token,
    userInfo: (state) => state.currentUser
  },

  actions: {
    register({ username, email, password, remember = true }) {
      const users = loadUsers()
      const exists = users.some(u => u.email === email)
      if (exists) {
        return { success: false, message: '该邮箱已被注册' }
      }
      const newUser = {
        id: Date.now(),
        username,
        email,
        password,
        createdAt: new Date().toISOString()
      }
      users.push(newUser)
      saveUsers(users)
      return this.login({ email, password, remember })
    },

    login({ email, password, remember = true }) {
      const users = loadUsers()
      const found = users.find(u => u.email === email)
      if (!found) {
        return { success: false, message: '账号不存在，请先注册' }
      }
      if (found.password !== password) {
        return { success: false, message: '密码错误' }
      }
      const session = {
        id: found.id,
        username: found.username,
        email: found.email,
        token: `demo-token-${found.id}-${Date.now()}`
      }
      this.currentUser = session
      saveSession(session, remember)
      return { success: true, message: '登录成功' }
    },

    logout() {
      this.currentUser = null
      clearSession()
    },

    updateProfile({ username, email }) {
      if (!this.currentUser) return { success: false, message: '未登录' }
      const users = loadUsers()
      const idx = users.findIndex(u => u.id === this.currentUser.id)
      if (idx === -1) return { success: false, message: '用户不存在' }

      // 如果修改邮箱，检查是否与他人冲突
      if (email !== this.currentUser.email && users.some(u => u.email === email)) {
        return { success: false, message: '该邮箱已被其他账号使用' }
      }

      users[idx].username = username
      users[idx].email = email
      saveUsers(users)

      this.currentUser.username = username
      this.currentUser.email = email
      // 写回当前正在使用的存储（localStorage 优先）
      const remember = !!localStorage.getItem(SESSION_KEY)
      saveSession(this.currentUser, remember)
      return { success: true, message: '资料已更新' }
    },

    changePassword({ oldPassword, newPassword }) {
      if (!this.currentUser) return { success: false, message: '未登录' }
      const users = loadUsers()
      const idx = users.findIndex(u => u.id === this.currentUser.id)
      if (idx === -1) return { success: false, message: '用户不存在' }
      if (users[idx].password !== oldPassword) {
        return { success: false, message: '原密码错误' }
      }
      users[idx].password = newPassword
      saveUsers(users)
      return { success: true, message: '密码已修改' }
    }
  }
})
