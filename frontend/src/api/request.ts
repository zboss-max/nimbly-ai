import axios, { type AxiosError, type AxiosInstance, type AxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import type { ApiResponse } from '@/types/api'

const TOKEN_KEY = 'nimbly_token'

/** localStorage 里 token 的读写，集中在一处，方便以后换成 cookie */
export function getToken(): string {
  return localStorage.getItem(TOKEN_KEY) ?? '' // ?? 是“左边为 null/undefined 才用右边”
}
export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}
export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

/** 请求地址 配合vite proxy **/
const http: AxiosInstance = axios.create({
  baseURL: '/api/v1', // 配合 vite proxy，浏览器请求 /api/v1/auth/signin
  timeout: 10000,
})

// 请求拦截器：每个请求出去前自动挂上 Authorization
http.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：只处理“失败的 HTTP 状态”（axios 对 4xx/5xx 会走这里）
http.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiResponse<unknown>>) => {
    const status = error.response?.status
    const message = error.response?.data?.msg ?? '网络异常，请稍后重试'
    // 关键：登录接口密码错也返回 401，此时不能当“登录过期”处理，否则会把用户刷回登录页
    const isSignIn = error.config?.url?.includes('/auth/signin') ?? false

    if (status === 401 && !isSignIn) {
      clearToken()
      ElMessage.error('登录已过期，请重新登录')
      void router.replace({ name: 'signin' }) // void 表示“故意不处理这个 Promise”
    } else {
      ElMessage.error(message)
    }
    return Promise.reject(error) // 继续抛给页面，让页面能 catch
  },
)

/**
 * 唯一出口：解包 {code,msg,data}，直接返回 data
 * 泛型 <T> 让调用方写 post<SignInResult>() 就能拿到带类型的返回值
 */
async function request<T>(config: AxiosRequestConfig): Promise<T> {
  const response = await http.request<ApiResponse<T>>(config)
  const body = response.data
  if (body.code !== 0) {
    // 兜底：万一后端用 200 返回了业务错误
    ElMessage.error(body.msg)
    throw new Error(body.msg)
  }
  return body.data
}

export function get<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  return request<T>({ url, method: 'get', params })
}

export function post<T>(url: string, data?: unknown): Promise<T> {
  return request<T>({ url, method: 'post', data })
}
