import request from './request'

/**
 * 运营监控 API
 */

// Celery 状态（Worker + Beat 调度配置）
export function getCeleryStatus() {
  return request.get('/operations/celery-status')
}

// APScheduler 状态（Pipeline 调度器）
export function getSchedulerStatus() {
  return request.get('/operations/scheduler')
}

export function startScheduler() {
  return request.post('/operations/scheduler/start')
}

export function stopScheduler() {
  return request.post('/operations/scheduler/stop')
}

// 数据源健康
export function getSourceHealth() {
  return request.get('/operations/sources/health')
}

// Pipeline 状态
export function getPipelineStatus() {
  return request.get('/operations/pipeline/status')
}

// 综合运营指标
export function getOperationalMetrics() {
  return request.get('/operations/metrics')
}
