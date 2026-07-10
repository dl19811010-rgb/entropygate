/**
 * 工具增强 API - EntropyGate AI 前端
 *
 * 在原有 api/tool.js 基础上新增：
 * - 工具对比数据接口
 * - 使用场景筛选
 * - 可用性统计增强
 * - 推荐算法
 */

import request from './request'
import { logError } from '../utils/log'

// ============================================================
// 原有接口（保持兼容）
// ============================================================

export function getTools(params = {}) {
  return request.get('/tools', { params })
}

export function getTool(id) {
  return request.get(`/tools/${id}`)
}

export function createTool(data) {
  return request.post('/tools', data)
}

export function updateTool(id, data) {
  return request.put(`/tools/${id}`, data)
}

export function deleteTool(id) {
  return request.delete(`/tools/${id}`)
}

export function getToolAvailability(id) {
  return request.get(`/tools/${id}/availability`)
}

export function updateToolAvailability(id, data) {
  return request.put(`/tools/${id}/availability`, data)
}

export function addAlternative(toolId, data) {
  return request.post(`/tools/${toolId}/alternatives`, data)
}

export function deleteAlternative(altId) {
  return request.delete(`/tools/alternatives/${altId}`)
}

// ============================================================
// 【新增】工具指南版块专用接口
// ============================================================

/**
 * 获取工具对比数据
 * GET /api/v1/tools/compare?ids=id1,id2,id3
 */
export function getToolCompareData(ids) {
  return request.get('/tools/compare', { params: { ids: ids.join(',') } })
}

/**
 * 按使用场景筛选工具
 * GET /api/v1/tools?use_case=text-generation&availability=available&pricing=freemium
 */
export function getToolsByUseCase(params = {}) {
  return request.get('/tools/by-use-case', { params })
}

/**
 * 获取可用性统计面板数据（增强版）
 * GET /api/v1/tools/availability/stats
 *
 * 返回：各状态数量 + 最近变更 + 即将到期检测的工具
 */
export function getAvailabilityStats() {
  return request.get('/tools/availability/stats')
}

/**
 * 获取推荐工具列表
 * GET /api/v1/tools/recommended?limit=6
 *
 * 推荐逻辑：高评分 + 国内可用 + 近期更新 + 匹配用户偏好
 */
export function getRecommendedTools(limit = 6) {
  return request.get('/tools/recommended', { params: { limit } })
}

/**
 * 获取工具分类下的使用场景列表
 * GET /api/v1/tools/use-cases
 */
export function getUseCases() {
  return request.get('/tools/use-cases')
}

/**
 * 搜索工具（全文搜索 + 标签匹配）
 * GET /api/v1/tools/search?q=xxx&category=xxx
 */
export function searchTools(params = {}) {
  return request.get('/tools/search', { params })
}

/**
 * 批量获取工具简要信息（用于对比选择器的预加载）
 * GET /api/v1/tools/brief?ids=id1,id2,id3
 */
export function getToolsBrief(ids) {
  return request.get('/tools/brief', { params: { ids: ids.join(',') } })
}

/**
 * 获取可用性变更历史
 * GET /api/v1/tools/{id}/availability/history?limit=20
 */
export function getAvailabilityHistory(toolId, limit = 20) {
  return request.get(`/tools/${toolId}/availability/history`, { params: { limit } })
}

/**
 * 订阅可用性变更通知（用户关注某个工具后）
 * POST /api/v1/tools/{id}/availability/subscribe
 */
export function subscribeAvailabilityChange(toolId) {
  return request.post(`/tools/${toolId}/availability/subscribe`)
}

/**
 * 取消订阅
 * DELETE /api/v1/tools/{id}/availability/subscribe
 */
export function unsubscribeAvailabilityChange(toolId) {
  return request.delete(`/tools/${toolId}/availability/subscribe`)
}

export default {
  getTools,
  getTool,
  createTool,
  updateTool,
  deleteTool,
  getToolAvailability,
  updateToolAvailability,
  addAlternative,
  deleteAlternative,
  // 新增
  getToolCompareData,
  getToolsByUseCase,
  getAvailabilityStats,
  getRecommendedTools,
  getUseCases,
  searchTools,
  getToolsBrief,
  getAvailabilityHistory,
  subscribeAvailabilityChange,
  unsubscribeAvailabilityChange,
}
