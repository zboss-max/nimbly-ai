<script setup lang="ts">
import {reactive, ref} from 'vue'

import type {FormInstance, FormRules} from 'element-plus'
import type {SignInPayload} from '../types'

import {useRouter} from 'vue-router'
import {useUserStore} from '../stores/user'


const form = reactive<SignInPayload>({
  identifier: '',
  password: '',
})

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const submitting = ref(false)

const rules: FormRules<SignInPayload> = {
  identifier: [
    {required: true, message: '请输入账号', trigger: 'blur'},
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
  ],
}


async function handleSubmit() {
  // 校验
  if (!formRef.value || submitting.value) return

  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true

  // 请求
  try {
    await userStore.signIn(form)
    await router.replace({name: 'marketing-home'})
  } catch {
    // request.ts 已经统一显示错误，这里只需阻止继续跳转
  } finally {
    submitting.value = false
  }

}

</script>

<template>
  <main>
    <h1>登录</h1>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="账号" prop="identifier">
        <el-input
          v-model="form.identifier"
          placeholder="用户名 / 手机号 / 邮箱"
        />
      </el-form-item>

      <el-form-item label="密码" prop="password">
        <el-input
          v-model="form.password"
          type="password"
          show-password
        />
      </el-form-item>

      <el-button type="primary" native-type="submit" :loading="submitting">
        登录
      </el-button>
    </el-form>

    <router-link :to="{ name: 'auth-signup' }">
      没有账号？去注册
    </router-link>
  </main>
</template>

<style scoped></style>
