import request from './request'

export function getDashboardStats() {
  return request.get('/dashboard/stats')
}

export function getAvailabilityDashboard() {
  return request.get('/dashboard/availability')
}
