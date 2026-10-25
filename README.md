# Nimbly AI

全栈项目：Vue 3 前端 + Flask 后端，已实现用户注册 / 登录（JWT 认证）。

| 层 | 技术栈 |
|---|---|
| 前端 | Vue 3 + TypeScript + Vite + Vue Router + Pinia + Element Plus |
| 后端 | Flask + Flask-RESTful + Flask-SQLAlchemy + Flask-JWT-Extended + MySQL |

## 目录结构

```
nimbly-ai/
├─ API.md                 接口契约（前后端共用，改接口必须同步更新）
├─ frontend/              Vue 3 前端
│  ├─ CONVENTIONS.md      前端规范：目录约定、接口调用规范
│  └─ src/
│     ├─ api/request.ts   唯一的网络出口
│     ├─ modules/auth/    auth 业务模块
│     └─ ...
└─ backend/               Flask 后端
   ├─ CONVENTIONS.md      后端规范：分层职责、接口规范
   ├─ .env.example        环境变量模板（复制为 .env 使用）
   ├─ requirements.txt    依赖清单
   ├─ config.py           读取环境变量
   └─ app/
      ├─ api/v1.py        接口版本聚合
      ├─ common/          统一响应 / 错误 / JWT 回调
      ├─ models/          数据模型
      └─ modules/auth/    auth 业务模块
```

## 快速开始

### 1. 后端

```bash
cd backend

# ① 准备虚拟环境（已存在 .venv 可跳过）
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# ② 安装依赖
pip install -r requirements.txt

# ③ 配置环境变量（必须做，否则启动会直接报错退出）
cp .env.example .env
# 然后编辑 .env，填入真实的数据库连接串和 JWT 密钥
# JWT 密钥生成：python -c "import secrets; print(secrets.token_urlsafe(48))"

# ④ 建库建表
mysql -u root -p < utils/create_sql.sql
python utils/create_db.py

# ⑤ 启动，默认 http://127.0.0.1:5000
python run.py
```

> `config.py` 启动时会校验 `SQLALCHEMY_DATABASE_URI` 和 `JWT_SECRET_KEY`，缺失直接抛 `RuntimeError` 中断启动——这是刻意的，避免用空密钥签名却毫无察觉。

### 2. 前端

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

开发环境由 Vite 把 `/api` 代理到 `http://127.0.0.1:5000`（见 `vite.config.ts`），因此前端一律使用相对路径 `/api/v1/...`，**不需要配置 CORS**。

### 3. 验证

打开 `http://localhost:5173`，注册一个账号再登录，成功后浏览器 `localStorage` 会写入 `nimbly_token`。

## 环境变量

| 变量 | 说明 |
|---|---|
| `SQLALCHEMY_DATABASE_URI` | 数据库连接串，`mysql+pymysql://用户:密码@主机:端口/库名?charset=utf8mb4` |
| `JWT_SECRET_KEY` | JWT 签名密钥，同时用作 Flask `SECRET_KEY` |

- 真实值只放在 `backend/.env`，**该文件已被 `.gitignore` 排除，禁止提交**
- 更换 `JWT_SECRET_KEY` 后，所有已签发的 token 立即失效，需要重新登录

## 文档

| 文档 | 内容 |
|---|---|
| [API.md](./API.md) | 接口契约：路径、入参、响应、错误码 |
| [frontend/CONVENTIONS.md](./frontend/CONVENTIONS.md) | 前端目录约定、依赖方向、接口调用规范 |
| [backend/CONVENTIONS.md](./backend/CONVENTIONS.md) | 后端分层职责、接口与事务规范 |

## 常用命令

| 目录 | 命令 | 作用 |
|---|---|---|
| frontend | `npm run dev` | 开发服务器 |
| frontend | `npm run build` | 生产构建 |
| frontend | `npm run type-check` | 类型检查 |
| frontend | `npm run lint` | 代码检查并修复 |
| frontend | `npm run format` | Prettier 格式化 |
| backend | `python run.py` | 启动服务 |
