import request from './request'

export function getTools(params) {
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
