import request from './request'

export function getCategoryList() {
  return request({
    url: '/categories',
    method: 'get'
  })
}

export function getCategoryDetail(slug) {
  return request({
    url: `/categories/slug/${slug}`,
    method: 'get'
  })
}

// 别名：NewsList/ToolList 等页面使用的命名风格
export function getCategories(params) {
  return request({
    url: '/categories/all',
    method: 'get',
    params
  })
}

// 兼容：部分页面从 category.js 导入 getTags，提供别名以减少改动
export { getAllTags as getTags } from './tag'
