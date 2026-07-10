import axios from 'axios'

const TOKEN_KEY = 'admin_token'
const ADMIN_INFO_KEY = 'admin_info'

function getToken() {
  return localStorage.getItem(TOKEN_KEY) || sessionStorage.getItem(TOKEN_KEY) || ''
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(ADMIN_INFO_KEY)
  sessionStorage.removeItem(TOKEN_KEY)
  sessionStorage.removeItem(ADMIN_INFO_KEY)
}

// 生产环境: HuggingFace Space → 最终 Cloudflare DNS 代理到 api.entropygate.cc.cd
const baseURL = import.meta.env.PROD
  ? 'https://dl1010-entropygate.hf.space/api/v1'
  : '/api/v1'

const request = axios.create({
  baseURL,
  timeout: 15000
})

request.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code && res.code !== 200) {
      if (res.code === 401) {
        clearAuth()
        window.location.href = '/login'
      }
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    return res
  },
  (error) => {
    if (error.response?.status === 401) {
      clearAuth()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default request
