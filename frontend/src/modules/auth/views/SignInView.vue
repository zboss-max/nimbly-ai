<script setup lang="ts">
import {reactive, ref} from 'vue'
import {useRouter} from 'vue-router'

import type {SignInPayload} from "../types";
import {useUserStore} from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

// 表单数据
const signInForm = reactive<SignInPayload>(
  {
    identifier: '',
    password: ''
  }
)

// 页面内错误提示
const errorMessage = ref('')

// 提交中：防连点，也驱动按钮文案
const loading = ref(false)

// 提交处理
async function handleSubmit(): Promise<void> {
  // 重复点击拦截
  if (loading.value) return
  // 空值拦截
  if (!signInForm.identifier.trim() || !signInForm.password) {
    errorMessage.value = '请填写账号和密码'
    return
  }
  errorMessage.value = '' // 页面内反馈区只放前端校验错误

  loading.value = true // 进入请求前置位
  try {
    // 发请求
    await userStore.signIn(signInForm)
    // 用 replace：登录成功后按「后退」不回到登录页
    await router.replace({name: 'home'})
  } catch {
    signInForm.password = '' // 失败后清空密码，账号保留，方便重新输入
    // 后端错误已由 request.ts 统一弹窗；catch 留着是防止未处理的 Promise 报错
  } finally {
    loading.value = false // 成功/失败都要复位
  }
}
</script>

<template>
  <main class="auth-card">

    <header>
      <img class="brand" src="/favicon.ico" alt=""/>
      <h1>登录 Nimbly</h1>
    </header>

    <!-- .prevent 阻止浏览器默认提交，否则点登录会整页刷新 -->
    <form @submit.prevent="handleSubmit">
      <input v-model="signInForm.identifier" placeholder="用户名 / 手机 / 邮箱"/>
      <input v-model="signInForm.password" type="password" placeholder="密码"/>
      <button type="submit" :disabled="loading">
        {{ loading ? '登录中…' : '登录' }}
      </button>
    </form>

    <!-- 反馈区：role="alert" 让屏幕阅读器读出错误 -->
    <p class="feedback" role="alert">{{ errorMessage }}</p>

    <footer>
      <span>忘记密码？</span>
      <span>
        第一次访问？<router-link :to="{ name: 'signup' }">创建账户</router-link>
      </span>
    </footer>

  </main>
</template>

<style scoped></style>
