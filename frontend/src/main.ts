import {createApp} from 'vue'
import {createPinia} from 'pinia'
import ElementPlus from 'element-plus'

// Element 基础样式
import 'element-plus/dist/index.css'
//
import '@/styles/tokens.css'
//
import '@/styles/base.css'
//
import '@/styles/element-plus.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia()) // 全局状态（跨组件共享数据），要在router之前注册
app.use(router) // 路由（根据 URL 切换页面）
app.use(ElementPlus) // UI 组件库

app.mount('#app')
