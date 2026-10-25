# 前端开发规范

> 适用范围：`frontend/src`
> 配套文档：仓库根目录 `API.md`（接口契约）、`frontend/README.md`（启动方式）
> 冲突处理：本规范与 `API.md` 冲突时，接口字段以 `API.md` 为准，代码组织以本文为准。

---

## 1. 目录结构

```
src/
├─ api/
│  └─ request.ts          # 【唯一】网络出口：axios 实例 + 拦截器
├─ types/
│  ├─ api.ts              # 通用类型：ApiResponse<T>
│  └─ router.d.ts         # RouteMeta 类型增强
├─ components/            # 共享组件（2 个以上模块使用）
├─ layouts/               # 布局组件（DefaultLayout、AppHeader）
│  └─ components/
├─ modules/               # 业务模块，按领域划分
│  └─ auth/
│     ├─ index.ts         # 【模块出口】外部只能从这里 import
│     ├─ api.ts           # 本模块的后端接口
│     ├─ types.ts         # 本模块的类型
│     ├─ routes.ts        # 本模块的路由表（导出 RouteRecordRaw[]）
│     ├─ stores/          # 本模块的 pinia store
│     ├─ components/      # 本模块专用组件
│     └─ views/           # 本模块的页面
├─ router/
│  └─ index.ts            # 创建 router + 聚合各模块 routes + 全局守卫
├─ stores/                # 跨模块共享 store（主题、字典）
├─ utils/                 # 纯函数工具
├─ App.vue
└─ main.ts
```

**模块内固定件**：`index.ts` / `api.ts` / `types.ts` / `routes.ts` / `stores/` / `views/` / `components/`。新模块照此建，不要自创文件名。

---

## 2. 共享 vs 专用（唯一判定规则）

> 该文件 **import 了某个 module 里的东西** 吗？
> - **是** → 留在那个 module，哪怕被 100 个地方引用
> - **否** → 被 **2 个以上** module 用到吗？是 → 上移 `src/`；否 → 留在 module

典型结论：

| 内容 | 位置 | 理由 |
|---|---|---|
| `useUserStore`（当前登录用户） | `modules/auth/stores/` | 由 auth 的接口产生，概念归属 auth |
| 主题、侧边栏折叠状态 | `src/stores/` | 不依赖任何业务模块 |
| `ApiResponse<T>` | `src/types/` | 纯类型，无业务 |
| 带用户名的导航栏 | `src/layouts/` | 属于应用外壳，不是通用组件 |
| `BaseTable`、`EmptyState` | `src/components/` | 与业务无关 |

---

## 3. 依赖方向（单向，不可逆）

```
src/api、src/utils、src/types        基础设施
        ▲
        │ 可以被依赖
src/modules/*                        业务模块
        ▲
        │ 可以被依赖
src/components、src/layouts、src/views、router    组合层
```

**禁止：**

- 基础设施层 import `modules/` 或 `stores/`（会造成依赖倒置与循环依赖）
- 模块 A 的 `api.ts` / `stores` 直接 import 模块 B 的 `api.ts` / `stores`
- 模块之间互相 import `views/`、`components/`（页面和组件不跨模块复用，需要复用就上移）

**允许：** 组合层（组件、布局、页面）import 任意模块的出口。

---

## 4. import 规范

| 场景 | 写法 | 示例 |
|---|---|---|
| 模块内部 | **相对路径** | `from './api'`、`from '../types'` |
| 跨模块 | **`@/` + 模块出口** | `from '@/modules/auth'` |
| 基础设施 | `@/` 别名 | `from '@/api/request'` |
| 纯类型 | `import type` / 行内 `type` | `import type { UserInfo } from './types'` |

**禁止跨模块深路径：**

```ts
import { useUserStore } from '@/modules/auth/stores/user' // ❌
import { useUserStore } from '@/modules/auth'            // ✅
```

判断信号：**跨模块 import 的路径里出现了 `stores/`、`views/`、`api.ts` 等具体文件，就是越界。**&#8203;

`import type` 必须显式标注（项目开启 `verbatimModuleSyntax`，漏标会在运行时找不到导出）。

---

## 5. 接口调用规范

### 5.1 三层职责

```
页面/组件  →  modules/*/api.ts  →  src/api/request.ts  →  后端
  调用函数        定义接口           加 token / 解包 / 报错
```

### 5.2 硬性规则

| 规则 | 说明 |
|---|---|
| 禁止在页面里 `import axios` | 会绕过 token、解包、错误处理 |
| 禁止在页面里拼 URL 调 `request` | 一个后端接口对应一个 `api.ts` 函数，URL 只出现一次 |
| `api.ts` 必须无状态 | 不能 import store、不能 import 组件 |
| 返回值直接用 | `request` 已解包，`const user = await fetchMe()`，不要再点 `.data.data` |
| 错误提示归一 | 4xx 由拦截器弹 `ElMessage`，页面 `catch` 内只复位 loading，**不重复提示** |

### 5.3 新增一个接口

```ts
// 1) types.ts —— 字段名照抄后端 JSON，不做驼峰转换
export interface FooResult {
  id: number
  created_at: string | null
}

// 2) api.ts —— 一函数一接口
import { post } from '@/api/request'
import type { FooResult } from './types'

export function createFoo(payload: { name: string }): Promise<FooResult> {
  return post<FooResult>('/foo', payload)
}

// 3) index.ts —— 对外导出
export { createFoo } from './api'
export type { FooResult } from './types'
```

### 5.4 类型与接口的边界

表单类型 ≠ 接口入参类型。多出的字段（如 `confirmPassword`）定义在页面本地，提交时手工映射，不要污染 `types.ts`。

---

## 6. 状态管理规范

- 使用 **setup 语法** 定义 store：`defineStore('id', () => { ... })`
- store id 与文件名一致，全局唯一
- **状态**用 `ref` / `computed`，**动作**是普通函数
- 只有 `return` 出去的内容对外可见，内部辅助函数不导出
- **store 不做页面跳转**，跳转由调用方（页面）决定
- **持久化统一走一处**：token 的读写只在 `api/request.ts`，业务层禁止直接调 `setToken` / `clearToken`
- 组件中解构状态必须 `storeToRefs`，解构方法可直接解构

```ts
const userStore = useUserStore()
const { token, isLoggedIn } = storeToRefs(userStore)  // 状态
const { signIn, signOut } = userStore                 // 方法
```

---

## 7. 路由规范

- 模块自带 `routes.ts`，导出 `RouteRecordRaw[]`，由 `router/index.ts` 统一展开聚合
- **所有页面组件必须懒加载**：`component: () => import('./views/XxxView.vue')`
- `name` 全局唯一，跳转优先用 `{ name: 'xxx' }`，避免路径字符串散落
- 需要登录的页面标 `meta.requiresAuth: true`；未标注视为公开页
- 兜底路由 `/:pathMatch(.*)*` 必须放在**最后**
- 守卫中调用 `useUserStore()` 必须在**函数体内**，不能在模块顶层
- 页面组件文件名：`XxxView.vue`；路由 path 用 kebab-case（`/user-profile`）

---

## 8. 命名规范

| 对象 | 规则 | 示例 |
|---|---|---|
| 组件文件 | PascalCase | `AppHeader.vue` |
| 页面文件 | PascalCase + View | `SignInView.vue` |
| 组合式函数 | camelCase + use | `useUserStore` |
| 接口函数 | 动词 + 名词 | `signIn`、`createOrder`、`fetchMe` |
| 常量 | UPPER_SNAKE | `TOKEN_KEY` |
| 类型 / 接口 | PascalCase，不加 I 前缀 | `UserInfo`（不是 `IUserInfo`） |

格式化：提交前执行 `npm run format`，不要手工调缩进（项目用无分号 + 单引号，`printWidth: 100`）。

---

## 9. 新增一个页面 Checklist

- [ ] 页面放 `modules/<模块>/views/XxxView.vue`
- [ ] 路由加进 `modules/<模块>/routes.ts`，懒加载 + `name` 唯一
- [ ] 需要登录则加 `meta.requiresAuth: true`
- [ ] 调接口先写 `types.ts` → `api.ts` → `index.ts`，页面只 import 函数
- [ ] 提交按钮必须有 `:loading`，`finally` 中复位
- [ ] 表单 `el-form-item` 的 `prop` 与 `rules` 的 key 完全一致
- [ ] 页面内不出现 `axios`、不出现 `/api/v1` 字符串
- [ ] `npm run type-check` 通过
