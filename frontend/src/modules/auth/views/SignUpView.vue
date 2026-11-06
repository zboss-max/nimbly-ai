<script setup lang="ts">
import {reactive, ref} from 'vue'
import {useRouter} from 'vue-router'

import type {SignUpPayload} from '../types'
import {signUp} from "../api";

const router = useRouter()

// 表单数据
const signUpForm = reactive(
  {
    username: '',
    phone: '',
    email: '',
    password: '',
    confirmPassword: ''
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
  // 账号空值拦截
  if (
    !signUpForm.username.trim() &&
    !signUpForm.phone.trim() &&
    !signUpForm.email.trim()) {
    errorMessage.value = '用户名 / 手机号 / 邮箱 至少填一个'
    return
  }
  // 账号格式核对拦截
  const formatError = validateFormat()
  if (formatError) {
    errorMessage.value = formatError
    return
  }
  // 密码长度拦截
  if (signUpForm.password.length < 6) {
    errorMessage.value = '密码至少 6 位'
    return
  }
  // 密码核对拦截
  if (signUpForm.password !== signUpForm.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }
  errorMessage.value = '' // 页面内反馈区只放前端校验错误

  loading.value = true // 进入请求前置位
  //请求体
  const payload: SignUpPayload = {
    password: signUpForm.password
  }
  if (signUpForm.username.trim()) payload.username = signUpForm.username.trim()
  if (signUpForm.phone.trim()) payload.phone = signUpForm.phone.trim()
  if (signUpForm.email.trim()) payload.email = signUpForm.email.trim()
  try {
    await signUp(payload)
    await router.replace({name: 'signin'})
  } catch {
    signUpForm.confirmPassword = '' // 清空确认框
    // 409「已被占用」/ 400 格式错误已由 request.ts 统一弹窗
  } finally {
    loading.value = false // 成功/失败都复位
  }
}

// 账号格式核对
function validateFormat(): string {
  const username = signUpForm.username.trim()
  const phone = signUpForm.phone.trim()
  const email = signUpForm.email.trim()

  if (username && !/^[a-zA-Z0-9]{8,16}$/.test(username)) {
    return '用户名需为 8-16 位字母或数字'
  }
  if (phone && !/^1\d{10}$/.test(phone)) {
    return '手机号格式不正确'
  }
  if (email && !/^[\w.+-]+@[\w-]+(\.[\w-]+)+$/.test(email)) {
    return '邮箱格式不正确'
  }
  return ''
}
</script>

<template>
  <main class="auth-card">

    <header>
      <img class="brand" src="/favicon.ico" alt=""/>
      <h1>加入 Nimbly</h1>
    </header>

    <form @submit.prevent="handleSubmit">
      <input v-model="signUpForm.username" placeholder="用户名"/>
      <input v-model="signUpForm.phone" placeholder="手机"/>
      <input v-model="signUpForm.email" placeholder="邮箱"/>
      <input v-model="signUpForm.password" type="password" placeholder="密码"/>
      <input v-model="signUpForm.confirmPassword" type="password" placeholder="确认密码"/>
      <button type="submit" :disabled="loading">
        {{ loading ? '提交中…' : '提交' }}
      </button>
    </form>

    <!-- 反馈区：role="alert" 让屏幕阅读器读出错误 -->
    <p class="feedback" role="alert">{{ errorMessage }}</p>

    <footer>
      <span>
        已有账号？<router-link :to="{ name: 'signin' }">登录</router-link>
      </span>
    </footer>

  </main>
</template>

<style scoped></style>
