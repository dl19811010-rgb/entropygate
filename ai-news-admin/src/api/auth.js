import request from './request'

export function login(data) {
  return request.post('/admin/login', data)
}

export function getCurrentAdmin() {
  return request.get('/admins/me')
}

export function changePassword(data) {
  return request.post('/admins/change-password', data)
}

export function logout() {
  return request.post('/admin/logout')
}
