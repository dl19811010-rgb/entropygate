import request from './request'

export function getSources(params) {
  return request.get('/sources', { params })
}

export function getCrawlerStats() {
  return request.get('/crawler/stats')
}

export function getCrawlerSourceStats() {
  return request.get('/crawler/source-stats')
}

export function triggerSource(id) {
  return request.post(`/crawler/trigger/${id}`)
}

export function triggerAllSources() {
  return request.post('/crawler/trigger-all')
}

export function getRecentLogs(limit = 20) {
  return request.get('/crawler/recent-logs', { params: { limit } })
}

export function getSource(id) {
  return request.get(`/sources/${id}`)
}

export function createSource(data) {
  return request.post('/sources', data)
}

export function updateSource(id, data) {
  return request.put(`/sources/${id}`, data)
}

export function deleteSource(id) {
  return request.delete(`/sources/${id}`)
}
