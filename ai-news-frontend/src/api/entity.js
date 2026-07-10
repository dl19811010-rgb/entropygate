import request from './request'

/**
 * Entity API — P2 Entity Experience
 * Reads pre-computed entity snapshots
 */

export function getEntity(type, slug) {
  return request.get(`/entity/${type}/${slug}`)
}

export function listEntities(type) {
  return request.get(`/entity/${type}/list`)
}

export function refreshEntity(type, slug) {
  return request.post(`/entity/${type}/${slug}/refresh`)
}
