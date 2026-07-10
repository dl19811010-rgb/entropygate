import request from './request'

/**
 * Timeline API — P3 Search & Discovery
 * Reads from feed snapshot and entity snapshots
 */

export function getTimeline(period = 'all', typeFilter = null, limit = 50) {
  const params = { period, limit }
  if (typeFilter) {
    params.type_filter = typeFilter
  }
  return request.get('/timeline', { params })
}

export function getEntityTimeline(type, slug) {
  return request.get(`/timeline/entity/${type}/${slug}`)
}
