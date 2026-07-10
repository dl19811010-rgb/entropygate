import api from './request'

export function getDashboardStats() {
  return api.get('/dashboard/stats')
}

export function getDashboardAvailability() {
  return api.get('/dashboard/availability')
}
