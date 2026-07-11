import request from './request'

export function login(data) {
  return request.post('/admin/auth/login', data)
}

export function getCurrentAdmin() {
  return request.get('/admin/auth/me')
}

export function changePassword(data) {
  return request.post('/admin/auth/change-password', data)
}

export function logout() {
  return request.post('/admin/auth/logout')
}
