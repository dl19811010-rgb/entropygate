import request from './request'

/**
 * Homepage Feed API — P1 Intelligence Homepage
 * Reads pre-computed snapshot (feed_daily.json)
 */

export function getHomepageFeed() {
  return request.get('/homepage/feed')
}

export function getHomepageHealth() {
  return request.get('/homepage/health')
}

export function getHomepageHeadline() {
  return request.get('/homepage/headline')
}
