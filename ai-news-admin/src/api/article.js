import request from './request'

export function getArticles(params) {
  return request.get('/articles', { params })
}

export function getArticle(id) {
  return request.get(`/articles/${id}`)
}

export function createArticle(data) {
  return request.post('/articles', data)
}

export function updateArticle(id, data) {
  return request.put(`/articles/${id}`, data)
}

export function deleteArticle(id) {
  return request.delete(`/articles/${id}`)
}

export function approveArticle(id) {
  return request.post(`/articles/${id}/approve`)
}

export function publishArticle(id) {
  return request.post(`/articles/${id}/publish`)
}

export function rejectArticle(id, reason) {
  return request.post(`/articles/${id}/reject`, { reason })
}

export function batchApproveArticles(ids) {
  return request.post('/articles/batch-approve', ids)
}

export function rewriteArticle(id) {
  return request.post(`/articles/${id}/rewrite`)
}

export function batchRewriteArticles(ids) {
  return request.post('/articles/batch-rewrite', ids)
}

// ESS v2 — 分组审核
export function getGroupedReview(bucket) {
  return request.get('/articles/grouped-review', { params: bucket ? { bucket } : {} })
}
