/**
 * 后端统一响应体，对应 backend/app/common/responses.py 的 ok() / fail()
 * 泛型 T 代表 data 的真实类型，调用时由使用方指定
 */
export interface ApiResponse<T> {
  code: number // 0 = 成功；失败时等于 HTTP 状态码
  msg: string // 给用户看的提示语
  data: T // 成功时的业务数据
}
