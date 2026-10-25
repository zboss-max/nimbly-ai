import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from '../App.vue'

describe('App', () => {
  it('挂载后能渲染路由页面', async () => {
    // 测试环境用 memory history，不依赖真实 URL
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/', component: { template: '<div>home-page</div>' } }],
    })
    await router.push('/')
    await router.isReady() // 必须等路由初始化完成，否则 router-view 还是空的

    const wrapper = mount(App, {
      global: { plugins: [router, createPinia()] }, // 模拟 main.ts 的装配
    })

    expect(wrapper.html()).toContain('home-page')
  })
})
