import {createRouter, createWebHistory} from 'vue-router'

import homeRoutes from "@/modules/main/routes";
import authRoutes from "@/modules/auth/routes"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...homeRoutes,
    ...authRoutes,
  ],
})

export default router
