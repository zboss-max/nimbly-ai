<script setup lang="ts">
import {reactive, ref} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import type {FormInstance, FormRules} from 'element-plus'
import {signUp} from '../api'
import type {SignUpPayload} from '../types'

// 表单里的值都由输入框提供，所以全部明确为 string
interface SignUpForm {
  username: string
  phone: string
  email: string
  password: string
  confirmPassword: string
}

const router = useRouter()
const formRef = ref<FormInstance>()
const submitting = ref(false)

const form = reactive<SignUpForm>({
  username: '',
  phone: '',
  email: '',
  password: '',
  confirmPassword: '',
})

function validateConfirmPassword(
  _rule: unknown,
  value: string,
  callback: (error?: Error) => void,
) {
  if (!value) {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 三种账号都不是单独必填，但填写后必须符合格式
const rules: FormRules<SignUpForm> = {
  username: [
    {
      pattern: /^[a-zA-Z0-9]{8,16}$/,
      message: '用户名需为 8～16 位字母或数字',
      trigger: 'blur',
    },
  ],
  phone: [
    {
      pattern: /^1\d{10}$/,
      message: '手机号格式不正确',
      trigger: 'blur',
    },
  ],
  email: [
    {
      pattern: /^[\w.+-]+@[\w-]+(\.[\w-]+)+$/,
      message: '邮箱格式不正确',
      trigger: 'blur',
    },
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
    {min: 8, message: '密码至少 8 位', trigger: 'blur'},
  ],
  confirmPassword: [
    {
      required: true,
      validator: validateConfirmPassword,
      trigger: 'blur',
    },
  ],
}

async function handleSubmit() {
  if (!formRef.value || submitting.value) return

  const valid = await formRef.value.validate().catch(() => false)

  // 检查三个账号字段是否至少填写了一个
  const hasIdentifier = [
    form.username,
    form.phone,
    form.email,
  ].some((value) => value.trim() !== '')

  if (!hasIdentifier) {
    ElMessage.error('用户名、手机号、邮箱至少填写一个')
  }

  if (!valid || !hasIdentifier) return

  submitting.value = true

  try {
    // password 必传，其余三个字段只在填写后加入请求体
    const payload: SignUpPayload = {
      password: form.password,
    }

    const username = form.username.trim()
    const phone = form.phone.trim()
    const email = form.email.trim()

    if (username) payload.username = username
    if (phone) payload.phone = phone
    if (email) payload.email = email

    await signUp(payload)

    ElMessage.success('注册成功，请登录')
    await router.replace({name: 'auth-signin'})
  } catch {
    // request.ts 已统一显示错误
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <main>
    <h1>注册</h1>
    <p>用户名、手机号、邮箱至少填写一个</p>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="form.username"
          placeholder="8～16 位字母或数字"
        />
      </el-form-item>

      <el-form-item label="手机号" prop="phone">
        <el-input
          v-model="form.phone"
          placeholder="选填，11 位手机号"
        />
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input
          v-model="form.email"
          placeholder="选填，例如 user@example.com"
        />
      </el-form-item>

      <el-form-item label="密码" prop="password">
        <el-input
          v-model="form.password"
          type="password"
          show-password
          placeholder="至少 8 位"
          autocomplete="new-password"
        />
      </el-form-item>

      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input
          v-model="form.confirmPassword"
          type="password"
          show-password
          placeholder="再次输入密码"
          autocomplete="new-password"
        />
      </el-form-item>

      <el-button
        type="primary"
        native-type="submit"
        :loading="submitting"
      >
        注册
      </el-button>
    </el-form>

    <router-link :to="{ name: 'auth-signin' }">
      已有账号？去登录
    </router-link>
  </main>
</template>

<style scoped></style>
