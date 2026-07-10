import request from './request'

/**
 * Product Dashboard API
 * Product Health + Runtime Health
 */

export function getProductHealth() {
  return request.get('/product-dashboard/product')
}

export function getRuntimeHealth() {
  return request.get('/product-dashboard/runtime')
}

export function getAllHealth() {
  return request.get('/product-dashboard/all')
}
