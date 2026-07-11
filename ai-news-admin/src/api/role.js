import request from './request'

export function getRoles(params) {
  return request.get('/roles', { params })
}

export function getAllRoles() {
  return request.get('/roles/all')
}

export function getRole(id) {
  return request.get(`/roles/${id}`)
}

export function createRole(data) {
  return request.post('/roles', data)
}

export function updateRole(id, data) {
  return request.put(`/roles/${id}`, data)
}

export function deleteRole(id) {
  return request.delete(`/roles/${id}`)
}

export function getPermissions(params) {
  return request.get('/roles/permissions', { params })
}

export function getPermissionsByModule() {
  return request.get('/roles/permissions/by-module')
}

export function createPermission(data) {
  return request.post('/roles/permissions', data)
}

export function updatePermission(id, data) {
  return request.put(`/roles/permissions/${id}`, data)
}

export function deletePermission(id) {
  return request.delete(`/roles/permissions/${id}`)
}
