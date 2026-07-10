import request from './request'

export function getTags(params) {
  return request.get('/tags', { params })
}

export function getAllTags() {
  return request.get('/tags/all')
}

export function getTag(id) {
  return request.get(`/tags/${id}`)
}

export function createTag(data) {
  return request.post('/tags', data)
}

export function updateTag(id, data) {
  return request.put(`/tags/${id}`, data)
}

export function deleteTag(id) {
  return request.delete(`/tags/${id}`)
}
