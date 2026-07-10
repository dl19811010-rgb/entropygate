import request from './request'

export function getAuditLogs(params) {
  return request.get('/audit-logs', { params })
}

export function getAuditLog(id) {
  return request.get(`/audit-logs/${id}`)
}
