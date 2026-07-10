import { defineStore } from 'pinia'
import { getCategoryList } from '@/api/category'
import { logError } from '@/utils/log'

const DEFAULT_CATEGORIES = [
  { id: 1, name: 'AI新动态', slug: 'ai-news', description: '针对国内用户有实际价值的新工具、新技术与行业动态' },
  { id: 2, name: 'AI工具指南', slug: 'ai-tools', description: '解决 AI 难使用的问题，提供实用工具教程与使用技巧' }
]

function isAllowedCategory(name) {
  if (!name) return false
  return DEFAULT_CATEGORIES.some(cat => cat.name === name)
}

export const useAppStore = defineStore('app', {
  state: () => ({
    categories: DEFAULT_CATEGORIES,
    loading: false
  }),
  
  actions: {
    async loadCategories() {
      if (this.categories.length > 0 && this.categories !== DEFAULT_CATEGORIES) return
      this.loading = true
      try {
        const res = await getCategoryList()
        const list = res.items || res.list || res || []
        const filtered = list.filter(cat => isAllowedCategory(cat.name))
        this.categories = filtered.length > 0 ? filtered : DEFAULT_CATEGORIES
      } catch (e) {
        logError('加载分类失败:', e)
        this.categories = DEFAULT_CATEGORIES
      } finally {
        this.loading = false
      }
    }
  }
})
