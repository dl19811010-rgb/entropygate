import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'HomePage',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'news',
        name: 'NewsList',
        component: () => import('@/views/NewsList.vue'),
        meta: { title: 'AI资讯' }
      },
      {
        path: 'news/:slug',
        redirect: to => `/article/${to.params.slug}`,
      },
      {
        path: 'tools',
        name: 'ToolList',
        component: () => import('@/views/ToolList.vue'),
        meta: { title: 'AI工具库' }
      },
      {
        path: 'tools/:slug',
        name: 'ToolDetail',
        component: () => import('@/views/ToolDetail.vue'),
        meta: { title: '工具详情' }
      },

      {
        path: 'article/:id',
        name: 'ArticleDetail',
        component: () => import('@/views/ArticleDetail.vue'),
        meta: { title: '文章详情' }
      },
      {
        path: 'category/:slug',
        name: 'CategoryList',
        component: () => import('@/views/CategoryList.vue'),
        meta: { title: '分类' }
      },
      {
        path: 'tag/:slug',
        name: 'TagList',
        component: () => import('@/views/TagList.vue'),
        meta: { title: '标签' }
      },
      {
        path: 'search',
        name: 'Search',
        component: () => import('@/views/Search.vue'),
        meta: { title: '搜索' }
      },
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/views/Login.vue'),
        meta: { title: '登录' }
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/views/Register.vue'),
        meta: { title: '注册' }
      },
      {
        path: 'member',
        name: 'Member',
        component: () => import('@/views/Member.vue'),
        meta: { title: '个人中心', requiresAuth: true }
      },
      {
        path: 'entity/:type/:slug',
        name: 'EntityDetail',
        component: () => import('@/views/EntityDetail.vue'),
        meta: { title: '实体详情' }
      },
      {
        path: 'timeline',
        name: 'Timeline',
        component: () => import('@/views/Timeline.vue'),
        meta: { title: '时间线' }
      },
      {
        path: 'timeline/:type/:slug',
        name: 'EntityTimeline',
        component: () => import('@/views/Timeline.vue'),
        meta: { title: '实体时间线' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('@/views/NotFound.vue'),
        meta: { title: '页面不存在' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta?.requiresAuth && !userStore.isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
    return
  }

  const title = to.meta?.title
  if (title) {
    document.title = `${title} - EntropyGate AI`
  } else {
    document.title = 'EntropyGate AI - AI新闻资讯平台'
  }
  next()
})

export default router
