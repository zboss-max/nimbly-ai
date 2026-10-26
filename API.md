# Nimbly AI 接口文档

> 版本：**v1** ｜ 最后更新：2026-10-25
> 维护约定：**任何接口改动，必须同一次提交内更新本文档**。文档与代码不一致时，以代码为准，并在 PR 里指出。

---

## 1. 通用约定

### 1.1 地址与环境

| 环境 | 前端请求地址 | 实际后端 | 说明 |
|---|---|---|---|
| 开发 | `/api/v1/...`（相对路径） | `http://127.0.0.1:5000` | 由 Vite 代理转发，见 `frontend/vite.config.ts` |
| 生产 | `/api/v1/...` | 由 Nginx / 网关反向代理 | **必须同源**，否则需要额外配置 CORS |

- 所有接口统一前缀：`/api/v1`
- 开发环境**不要**在前端写 `http://127.0.0.1:5000`，一律用相对路径，否则会触发跨域
- 生产环境如需前后端分离域名，由后端开启 CORS 或在网关层处理，前端代码不改

### 1.2 认证方式

采用 **JWT Bearer Token**（无状态，服务端不存 session）。

| 项 | 值 |
|---|---|
| 请求头 | `Authorization: Bearer <access_token>` |
| 有效期 | 1 小时（`backend/config.py` → `JWT_ACCESS_TOKEN_EXPIRES`） |
| 获取方式 | 仅 `POST /auth/signin` 返回 |
| 刷新机制 | **暂无**，过期需重新登录 |
| 存储位置 | 前端 `localStorage`，键名 `nimbly_token` |

> ⚠️ `Bearer` 后面必须有一个空格，缺失会被服务端判定为凭证格式错误。

### 1.3 统一响应格式

所有接口（含错误）均返回如下结构：

```json
{
  "code": 0,
  "msg": "ok",
  "data": null
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `code` | number | `0` 表示成功；失败时等于 HTTP 状态码 |
| `msg` | string | 面向用户的提示语，前端可直接展示 |
| `data` | object \| array \| null | 业务数据，失败时恒为 `null` |

对应实现：`backend/app/common/responses.py` 的 `ok()` / `fail()`

### 1.4 错误码

| HTTP | `code` | 场景 | `msg` 示例 |
|---|---|---|---|
| 400 | 400 | 请求体不是 JSON 对象 | 请求体必须是 JSON 对象 |
| 400 | 400 | 必填项缺失 | 账号不能为空 / 密码不能为空 |
| 400 | 400 | 格式校验失败 | 密码至少 6 位 / 手机号格式不正确 |
| 401 | 401 | 登录凭证错误 | 账号或密码错误 |
| 401 | 401 | 未携带 token | 请先登录 |
| 401 | 401 | token 格式错误或签名被篡改 | 登录凭证无效 |
| 401 | 401 | token 过期 | 登录已过期，请重新登录 |
| 409 | 409 | 唯一字段冲突 | 用户名已被占用 / 用户名/手机号/邮箱已被占用 |
| 500 | 500 | 服务端未捕获异常 | 见 `backend/app/common/errors.py` |

**前端处理约定：**

- `4xx` 统一由 `src/api/request.ts` 的响应拦截器弹出 `ElMessage.error(msg)`，页面 **catch 内不再重复提示**
- `401` 且**不是登录接口**时，拦截器会清除 token 并跳转登录页
- 登录接口的 `401`（密码错误）**不会触发跳转**，只提示

---

## 2. 认证模块 Auth

### 2.1 登录

```
POST /api/v1/auth/signin
```

**鉴权**：不需要

**请求体**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `identifier` | string | 是 | 用户名 / 手机号 / 邮箱，三者任一，服务端自动识别类型 |
| `password` | string | 是 | 明文密码，长度 ≥ 6 |

> 兼容说明：服务端同时接受 `username` 字段作为 `identifier` 的别名（`schemas.py`），但**新代码统一使用 `identifier`**。

**请求示例**

```json
{
  "identifier": "zhangsan01",
  "password": "123456"
}
```

**成功响应 `200`**

```json
{
  "code": 0,
  "msg": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "zhangsan01",
      "phone": null,
      "email": null,
      "create_time": "2026-10-25 16:20:31"
    }
  }
}
```

**失败响应**

| 场景 | HTTP | msg |
|---|---|---|
| 账号为空 | 400 | 账号不能为空 |
| 密码为空 | 400 | 密码不能为空 |
| 账号不存在 / 密码错误 | 401 | 账号或密码错误 |

> 安全设计：账号不存在与密码错误返回**同一条提示**，防止被用来枚举已注册账号。

---

### 2.2 注册

```
POST /api/v1/auth/signup
```

**鉴权**：不需要

**请求体**

| 字段 | 类型 | 必填 | 约束 |
|---|---|---|---|
| `username` | string | 否 | 8-16 位字母或数字，`^[a-zA-Z0-9]{8,16}$` |
| `phone` | string | 否 | 11 位手机号，`^1\d{10}$` |
| `email` | string | 否 | 标准邮箱格式 |
| `password` | string | 是 | 长度 ≥ 6 |

**业务规则**

1. `username` / `phone` / `email` **至少填写一个**，否则返回 400
2. 填了的字段**必须通过格式校验**，未填的字段传 `null` 或不传
3. 三个字段均唯一，任一冲突返回 409

**请求示例**

```json
{
  "username": "zhangsan01",
  "email": "zhangsan@example.com",
  "password": "123456"
}
```

**成功响应 `201`**

```json
{
  "code": 0,
  "msg": "注册成功",
  "data": {
    "id": 1,
    "username": "zhangsan01",
    "phone": null,
    "email": "zhangsan@example.com",
    "create_time": "2026-10-25 16:20:31"
  }
}
```

> ⚠️ **注册成功不返回 token**。前端注册完成后必须跳转登录页，不能直接进入首页。

**失败响应**

| 场景      | HTTP | msg                        |
|---------|------|----------------------------|
| 三个标识全空  | 400  | 用户名、手机号、邮箱至少填一个            |
| 用户名格式错  | 400  | 用户名需为 8-16 位字母或数字          |
| 手机号格式错  | 400  | 手机号格式不正确                   |
| 邮箱格式错   | 400  | 邮箱格式不正确                    |
| 密码过短    | 400  | 密码至少 6 位                   |
| 用户名密码错误 | 401  |                            |
| 登录失效    | 401  |                            |
| 字段已被占用  | 409  | 用户名已被占用 / 手机号已被占用 / 邮箱已被占用 |
| 并发写入冲突  | 409  | 用户名/手机号/邮箱已被占用             |

---

## 3. 数据模型

### UserInfo

| 字段 | 类型 | 可为 null | 说明 |
|---|---|---|---|
| `id` | number | 否 | 主键 |
| `username` | string | 是 | 用户名 |
| `phone` | string | 是 | 手机号 |
| `email` | string | 是 | 邮箱 |
| `create_time` | string | 是 | 格式 `YYYY-MM-DD HH:mm:ss` |

> 前端类型定义：`frontend/src/modules/auth/types.ts`
> 注意：`create_time` 用空格分隔，`new Date('2026-10-25 16:20:31')` 在 Safari 下会得到 `Invalid Date`，需替换为 `2026-10-25T16:20:31` 再解析。

---

## 4. 前端接入说明

### 4.1 请求封装（禁止绕过）

```ts
// 唯一出口：src/api/request.ts
get<T>(url: string, params?: Record<string, unknown>): Promise<T>
post<T>(url: string, data?: unknown): Promise<T>
```

- 自动附加 `Authorization`
- 自动解包 `{code,msg,data}`，**返回值直接是 `data`**
- 自动处理 4xx 提示与 401 跳转
- **禁止在页面中直接 `import axios`**

### 4.2 业务接口层

```ts
// src/modules/auth/api.ts
signIn(payload: SignInPayload): Promise<SignInResult>
signUp(payload: SignUpPayload): Promise<UserInfo>
```

新增接口时：**一个后端接口对应一个函数**，路径字符串只出现在该文件中。

### 4.3 登录态

```ts
const userStore = useUserStore()

userStore.token        // string，空串 = 未登录
userStore.user         // UserInfo | null
userStore.isLoggedIn   // boolean
userStore.displayName  // 用户名 / 手机号 / 邮箱，取首个非空

await userStore.signIn({ identifier, password })
userStore.signOut()
```

- 页面中**不要直接调用** `setToken` / `clearToken`，一律走 store
- 组件中解构状态必须用 `storeToRefs`，否则丢失响应性

---

## 5. 已知限制 / 待实现

| 项 | 状态 | 说明 |
|---|---|---|
| 登出 | 前端实现 | JWT 无状态，服务端无需接口，前端清 token 即可 |
| Refresh Token | 未规划 | 当前 1 小时过期需重新登录 |
| 修改密码 / 找回密码 | 未规划 | — |
| 接口限流 | 未实现 | 登录接口建议加频率限制，防暴力破解 |

---

## 6. 变更记录

| 日期 | 版本 | 内容 | 变更人 |
|---|---|---|---|
| 2026-10-25 | v1 | 初始版本：登录、注册 | — |
