import {createRouter, createWebHistory} from 'vue-router'

import marketingRoutes from "@/modules/marketing/routes";
import authRoutes from "@/modules/auth/routes"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...marketingRoutes,
    ...authRoutes,
  ],
})

export default router
