import request from './request'

export function getRoles(params) {
  return request.get('/admin/roles', { params })
}

export function getAllRoles() {
  return request.get('/admin/roles/all')
}

export function getRole(id) {
  return request.get(`/admin/roles/${id}`)
}

export function createRole(data) {
  return request.post('/admin/roles', data)
}

export function updateRole(id, data) {
  return request.put(`/admin/roles/${id}`, data)
}

export function deleteRole(id) {
  return request.delete(`/admin/roles/${id}`)
}

export function getPermissions(params) {
  return request.get('/admin/permissions', { params })
}

export function getPermissionsByModule() {
  return request.get('/admin/permissions/by-module')
}

export function createPermission(data) {
  return request.post('/admin/permissions', data)
}

export function updatePermission(id, data) {
  return request.put(`/admin/permissions/${id}`, data)
}

export function deletePermission(id) {
  return request.delete(`/admin/permissions/${id}`)
}
