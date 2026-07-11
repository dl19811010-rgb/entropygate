import request from './request'

export function getAdmins(params) {
  return request.get('/admin/admins', { params })
}

export function getAdmin(id) {
  return request.get(`/admin/admins/${id}`)
}

export function createAdmin(data) {
  return request.post('/admin/admins', data)
}

export function updateAdmin(id, data) {
  return request.put(`/admin/admins/${id}`, data)
}

export function deleteAdmin(id) {
  return request.delete(`/admin/admins/${id}`)
}

export function resetAdminPassword(id, newPassword) {
  return request.post(`/admin/admins/${id}/reset-password`, { new_password: newPassword })
}

export function getAdminLoginLogs(id, params) {
  return request.get(`/admin/admins/${id}/login-logs`, { params })
}
