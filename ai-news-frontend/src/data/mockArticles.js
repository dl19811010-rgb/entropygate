import mockData from './mockArticles.json'

export const mockArticles = mockData.articles || []

export const mockCategories = [
  { id: 1, name: 'AI新动态', slug: 'ai-news', description: '针对国内用户有实际价值的新工具、新技术与行业动态' },
  { id: 2, name: 'AI工具指南', slug: 'ai-tools', description: '解决 AI 难使用的问题，提供实用工具教程与使用技巧' }
]

export function getMockArticleList({ category_slug, keyword, page = 1, page_size = 12 } = {}) {
  let list = [...mockArticles]
  if (category_slug) {
    list = list.filter(a => a.category_slug === category_slug)
  }
  if (keyword) {
    const lower = keyword.toLowerCase()
    list = list.filter(a =>
      a.title.toLowerCase().includes(lower) ||
      (a.summary && a.summary.toLowerCase().includes(lower))
    )
  }
  const total = list.length
  const start = (page - 1) * page_size
  const end = start + page_size
  return {
    items: list.slice(start, end),
    total
  }
}

export function getMockArticleById(id) {
  return mockArticles.find(a => String(a.id) === String(id))
}

export function getMockHotArticles(count = 5) {
  return mockArticles.slice(0, count).map(a => ({
    id: a.id,
    title: a.title,
    view_count: a.view_count
  }))
}
