<script setup lang="ts">
import {reactive, ref} from 'vue'

import type {FormInstance, FormRules} from 'element-plus'
import type {SignInPayload} from '../types'

import {useRouter} from 'vue-router'
import {useUserStore} from '../stores/user'

import AuthLayout from "../layouts/AuthLayout.vue";


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
  <AuthLayout mode="signin">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="80px"
      label-position="left"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="账 号" prop="identifier">
        <el-input
          v-model="form.identifier"
          placeholder="用户名 / 手机号 / 邮箱"
        />
      </el-form-item>

      <el-form-item label="密 码" prop="password">
        <el-input
          v-model="form.password"
          type="password"
          show-password
        />
      </el-form-item>

      <el-button
        class="auth-submit"
        type="primary"
        native-type="submit"
        :loading="submitting"
      >
        登录
      </el-button>
    </el-form>

    <router-link
      class="auth-switch"
      :to="{ name: 'auth-signup' }"
    >
      没有账号？去注册
    </router-link>
  </AuthLayout>
</template>

<style scoped>
.auth-submit {
  width: 100%;
  min-height: 46px;
  margin-top: 8px;
  font-size: 16px;
  letter-spacing: 0.08em;
}

.auth-switch {
  display: block;
  width: fit-content;
  margin: 20px 0 0 auto;
  color: var(--color-text-secondary);
  font-size: 14px;
  transition: color var(--transition-fast);
}

.auth-switch:hover {
  color: var(--color-primary-hover);
}
</style>
