import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { signIn as signInApi } from '@/modules/auth/api' // 起别名，避免和下面的 signIn 撞名
import { clearToken, getToken, setToken } from '@/api/request'
import type { SignInPayload, UserInfo } from '../types'

const USER_KEY = 'nimbly_user'

/** 从 localStorage 读回用户信息，读失败或格式坏了就当作没登录 */
function readUser(): UserInfo | null {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as UserInfo // JSON.parse 返回 any，这里断言成我们存储时的形状
  } catch {
    localStorage.removeItem(USER_KEY) // 存储被手动改坏时自愈，不留垃圾
    return null
  }
}

export const useUserStore = defineStore('user', () => {
  // ---------- 状态：会变的数据 ----------
  const token = ref<string>(getToken()) // 初始值 = 刷新页面时从 localStorage 恢复
  const user = ref<UserInfo | null>(readUser())

  // ---------- 派生状态：由状态算出来的，不单独存 ----------
  const isLoggedIn = computed(() => Boolean(token.value))
  const displayName = computed(
    () => user.value?.username || user.value?.phone || user.value?.email || '用户',
  )

  // ---------- 动作：唯一能改状态的地方 ----------
  async function signIn(payload: SignInPayload): Promise<void> {
    const result = await signInApi(payload) // 失败会 throw，交给调用方
    token.value = result.access_token
    user.value = result.user
    setToken(result.access_token) // 落盘持久化
    localStorage.setItem(USER_KEY, JSON.stringify(result.user))
  }

  function signOut(): void {
    token.value = ''
    user.value = null
    clearToken()
    localStorage.removeItem(USER_KEY)
  }

  // 只有 return 出去的才能被组件用；readUser 是内部函数，不导出
  return { token, user, isLoggedIn, displayName, signIn, signOut }
})
