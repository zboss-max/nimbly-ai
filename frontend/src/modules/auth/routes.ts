import type {RouteRecordRaw} from 'vue-router'

/** auth 模块自带的路由，由 router/index.ts 统一聚合 */
const authRoutes: RouteRecordRaw[] = [
  {
    path: '/signin',
    name: 'auth-signin',
    component: () => import('./views/SignInView.vue'),
    meta: {title: '登录', requiresAuth: false},
  },
  {
    path: '/signup',
    name: 'auth-signup',
    component: () => import('./views/SignUpView.vue'),
    meta: {title: '注册', requiresAuth: false},
  },
]

export default authRoutes
