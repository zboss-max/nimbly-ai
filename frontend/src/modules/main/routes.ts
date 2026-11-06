import type {RouteRecordRaw} from 'vue-router'

/** home 模块自带的路由，由 router/index.ts 统一聚合 */
const homeRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('./views/HomeView.vue'),
    meta: {title: '主页', requiresAuth: false},
  },
]

export default homeRoutes
