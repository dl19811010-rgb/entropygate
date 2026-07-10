/**
 * 前端 API 请求模块（改进版）
 *
 * 改进点：
 * 1. 注入用户 Token 到请求头
 * 2. 统一错误处理 + 用户友好提示
 * 3. 401 自动跳转登录
 * 4. 取消重复 GET 请求支持
 */

import axios from 'axios'
import { logError } from '../utils/log'

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// -----------------------------------------------------------
// Token 管理 — 兼容当前 localStorage 方式，后续可平滑迁移到后端 JWT
// -----------------------------------------------------------

function getToken() {
  const sessionKey = 'eg_current_user'
  try {
    const raw = localStorage.getItem(sessionKey) || sessionStorage.getItem(sessionKey)
    if (raw) {
      const user = JSON.parse(raw)
      return user?.token || ''
    }
  } catch (e) {
    // ignore parse error
  }
  return ''
}

// -----------------------------------------------------------
// 取消重复 GET 请求 Map
// -----------------------------------------------------------

const pendingRequests = new Map()

function generateRequestKey(config) {
  const { method, url, params, data } = config
  return [method, url, JSON.stringify(params), JSON.stringify(data)].join('&')
}

// -----------------------------------------------------------
// 请求拦截器 — 注入 Token + 取消重复请求
// -----------------------------------------------------------

request.interceptors.request.use(
  config => {
    // 1. 注入 Token
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 2. 取消重复请求（仅 GET）
    if (config.method === 'get') {
      const requestKey = generateRequestKey(config)
      if (pendingRequests.has(requestKey)) {
        const cancelToken = pendingRequests.get(requestKey)
        cancelToken('取消重复请求')
      }
      config.cancelToken = new axios.CancelToken(cancel => {
        pendingRequests.set(requestKey, cancel)
      })
    }

    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// -----------------------------------------------------------
// 响应拦截器 — 统一处理 + 401跳转 + 网络错误提示
// -----------------------------------------------------------

request.interceptors.response.use(
  response => {
    // 清除已完成的请求
    const config = response.config
    if (config.method === 'get') {
      const requestKey = generateRequestKey(config)
      pendingRequests.delete(requestKey)
    }

    const data = response.data

    // 统一响应格式处理
    if (data && typeof data === 'object' && 'code' in data) {
      if (data.code === 200 || data.code === 0) {
        return data.data
      }
      return Promise.reject(new Error(data.message || '请求失败'))
    }

    return data
  },
  error => {
    // 清除失败的请求
    if (error.config) {
      const requestKey = generateRequestKey(error.config)
      pendingRequests.delete(requestKey)
    }

    // 被取消的请求不报错
    if (axios.isCancel(error)) {
      return Promise.reject(error)
    }

    // 401 未授权 → 跳转登录
    if (error.response?.status === 401) {
      localStorage.removeItem('eg_current_user')
      sessionStorage.removeItem('eg_current_user')
      window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname)
      return Promise.reject(new Error('登录已过期，请重新登录'))
    }

    // 403 无权限
    if (error.response?.status === 403) {
      return Promise.reject(new Error('没有操作权限'))
    }

    // 500 服务器错误
    if (error.response?.status >= 500) {
      logError('服务器错误:', error.message)
      return Promise.reject(new Error('服务器繁忙，请稍后重试'))
    }

    // 网络错误
    if (!error.response) {
      logError('网络错误:', error.message)
      return Promise.reject(new Error('网络连接失败，请检查网络'))
    }

    logError('API Error:', error.message)
    return Promise.reject(error)
  }
)

export default request
