/**
 * auth 模块的类型定义
 * 原则：字段名照抄后端 JSON，不做任何改名，改名就等于给自己挖坑
 */

/** 用户信息，对应 backend/app/models/user.py 的 to_dict() */
export interface UserInfo {
  id: number
  username: string | null // 后端可能存 null，所以不能写 string
  phone: string | null
  email: string | null
  create_time: string | null // 'YYYY-MM-DD HH:mm:ss'
}

/** 登录入参，对应 backend/app/modules/auth/schemas.py 的 SignInSchema */
export interface SignInPayload {
  identifier: string // 用户名 / 手机号 / 邮箱，三选一
  password: string
}

/** 登录返回，对应 auth/resources.py 的 SignIn.post */
export interface SignInResult {
  access_token: string
  user: UserInfo
}

/** 注册入参，对应 SignUpSchema：三个标识至少填一个，密码至少 6 位 */
export interface SignUpPayload {
  username?: string // ? = 可以不传（前端没填就不发这个字段）
  phone?: string
  email?: string
  password: string
}
