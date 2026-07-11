import { createRouter, createWebHistory } from 'vue-router'
import { useAdminStore } from '@/stores/admin'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true },
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘', icon: 'dashboard' }
      },
      {
        path: 'articles',
        name: 'Articles',
        component: () => import('@/views/ArticleList.vue'),
        meta: { title: '文章管理', icon: 'article' }
      },
      {
        path: 'articles/review',
        name: 'ArticleReview',
        component: () => import('@/views/ArticleReview.vue'),
        meta: { title: '文章审核', icon: 'article', activeMenu: '/articles/review' }
      },
      {
        path: 'articles/create',
        name: 'ArticleCreate',
        component: () => import('@/views/ArticleEdit.vue'),
        meta: { title: '新建文章', activeMenu: '/articles' }
      },
      {
        path: 'articles/edit/:id',
        name: 'ArticleEdit',
        component: () => import('@/views/ArticleEdit.vue'),
        meta: { title: '编辑文章', activeMenu: '/articles' }
      },
      {
        path: 'tools',
        name: 'Tools',
        component: () => import('@/views/ToolList.vue'),
        meta: { title: '工具管理', icon: 'tool' }
      },
      {
        path: 'tools/create',
        name: 'ToolCreate',
        component: () => import('@/views/ToolEdit.vue'),
        meta: { title: '新建工具', activeMenu: '/tools' }
      },
      {
        path: 'tools/edit/:id',
        name: 'ToolEdit',
        component: () => import('@/views/ToolEdit.vue'),
        meta: { title: '编辑工具', activeMenu: '/tools' }
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('@/views/CategoryList.vue'),
        meta: { title: '分类管理', icon: 'category' }
      },
      {
        path: 'tags',
        name: 'Tags',
        component: () => import('@/views/TagList.vue'),
        meta: { title: '标签管理', icon: 'tag' }
      },
      {
        path: 'sources',
        name: 'Sources',
        component: () => import('@/views/SourceList.vue'),
        meta: { title: '来源管理', icon: 'source' }
      },
      {
        path: 'crawler-monitor',
        name: 'CrawlerMonitor',
        component: () => import('@/views/CrawlerMonitor.vue'),
        meta: { title: '采集监控', icon: 'crawler' }
      },
      {
        path: 'system/admins',
        name: 'AdminList',
        component: () => import('@/views/AdminList.vue'),
        meta: { title: '管理员管理', icon: 'admin', requiresSuper: true }
      },
      {
        path: 'system/roles',
        name: 'RoleList',
        component: () => import('@/views/RoleList.vue'),
        meta: { title: '角色权限', icon: 'role', requiresSuper: true }
      },
      {
        path: 'system/audit-logs',
        name: 'AuditLogList',
        component: () => import('@/views/AuditLogList.vue'),
        meta: { title: '审计日志', icon: 'log', requiresSuper: true }
      }
    ]
  },
  {
    path: '/logout',
    name: 'Logout',
    beforeEnter: async () => {
      const adminStore = useAdminStore()
      await adminStore.logout()
      return '/login'
    }
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '无权限', requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面不存在', requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const adminStore = useAdminStore()
  
  if (to.meta.requiresAuth !== false && !adminStore.isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else if (to.path === '/login' && adminStore.isLoggedIn) {
    next({ path: '/dashboard' })
  } else if (to.meta.requiresSuper && !adminStore.isSuperAdmin) {
    // 非超管访问超管页面，跳回仪表盘
    next({ path: '/dashboard' })
  } else {
    next()
  }
})

export default router
