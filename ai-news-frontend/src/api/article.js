import request from './request'

export function getArticleList(params) {
  return request({
    url: '/articles',
    method: 'get',
    params
  })
}

export function getArticleDetail(id) {
  return request({
    url: `/articles/${id}`,
    method: 'get'
  })
}

export function getPopularArticles(limit = 10) {
  return request({
    url: '/articles',
    method: 'get',
    params: { limit, sort: 'views' }
  })
}

// 别名：NewsList 等页面使用的命名风格
export function getArticles(params) {
  return request({
    url: '/articles',
    method: 'get',
    params
  })
}

// 按 slug 获取文章详情
export function getArticleBySlug(slug) {
  return request({
    url: `/articles/${slug}`,
    method: 'get'
  })
}
