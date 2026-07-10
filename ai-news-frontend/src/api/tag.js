import request from './request'

export function getTagList(params) {
  return request({
    url: '/tags',
    method: 'get',
    params
  })
}

export function getTagDetail(slug) {
  return request({
    url: `/tags/slug/${slug}`,
    method: 'get'
  })
}

// 获取全量标签（不分页），用于筛选下拉等场景
export function getAllTags(params) {
  return request({
    url: '/tags/all',
    method: 'get',
    params
  })
}
