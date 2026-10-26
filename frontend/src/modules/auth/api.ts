import { post } from '@/api/request'
import type { SignInPayload, SignInResult, SignUpPayload, UserInfo } from './types'

// auth 模块的接口路径前缀
const AUTH_PREFIX = '/auth'
/**
 * 登录
 * 成功返回 { access_token, user }；失败（401）由 request.ts 拦截器统一提示并 reject
 */
export function signIn(payload: SignInPayload): Promise<SignInResult> {
  return post<SignInResult>(`${AUTH_PREFIX}/signin`, payload)
}

/**
 * 注册
 * 注意：后端注册成功只返回 user，没有 token，所以注册完要跳登录页，不能直接进首页
 */
export function signUp(payload: SignUpPayload): Promise<UserInfo> {
  return post<UserInfo>(`${AUTH_PREFIX}/signup`, payload)
}
