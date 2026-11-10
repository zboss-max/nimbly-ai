import type {RouteRecordRaw} from 'vue-router'

/** 官网 模块自带的路由，由 router/index.ts 统一聚合 */
const marketingRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'marketing-home',
    component: () => import('./views/HomeView.vue'),
    meta: {title: '迅捷智能 Nimbly AI', requiresAuth: false},
  },
]

export default marketingRoutes
