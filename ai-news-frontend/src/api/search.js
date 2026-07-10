import request from './request'

/**
 * Search API — P3 Search & Discovery
 * Reads search_index.json, no DB LIKE queries
 */

export function search(q, limit = 20) {
  return request.get('/search', { params: { q, limit } })
}

export function searchSuggest(q, limit = 10) {
  return request.get('/search/suggest', { params: { q, limit } })
}

export function searchEntity(slug) {
  return request.get(`/search/entity/${slug}`)
}
