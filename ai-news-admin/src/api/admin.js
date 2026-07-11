import request from './request'

export function getAdmins(params) {
  return request.get('/admins', { params })
}

export function getAdmin(id) {
  return request.get(`/admins/${id}`)
}

export function createAdmin(data) {
  return request.post('/admins', data)
}

export function updateAdmin(id, data) {
  return request.put(`/admins/${id}`, data)
}

export function deleteAdmin(id) {
  return request.delete(`/admins/${id}`)
}

export function resetAdminPassword(id, newPassword) {
  return request.post(`/admins/${id}/reset-password`, { new_password: newPassword })
}

export function getAdminLoginLogs(id, params) {
  return request.get(`/admins/${id}/login-logs`, { params })
}
