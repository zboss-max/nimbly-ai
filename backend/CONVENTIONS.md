# 后端开发规范

> 适用范围：`backend/`
> 配套文档：仓库根目录 `API.md`（接口契约，**改接口必须同步更新**）
> 技术栈：Flask + flask-restful + SQLAlchemy + flask-jwt-extended + MySQL

---

## 1. 目录结构

```
backend/
├─ run.py
├─ config.py
├─ utils/                     # 建库脚本等一次性工具
└─ app/
   ├─ __init__.py             # 应用工厂 create_app
   ├─ extensions.py           # db / jwt 实例（避免循环导入）
   ├─ api/
   │  ├─ __init__.py          # 版本注册表 get_registry()
   │  └─ v1.py                # v1 蓝图聚合，注册各模块蓝图
   ├─ common/                 # 横切关注点
   │  ├─ responses.py         # ok() / fail() / parse_json()
   │  ├─ errors.py            # 全局 404 / 500 处理
   │  └─ jwt_callbacks.py     # JWT 错误统一响应
   ├─ models/                 # 跨模块共享模型
   │  ├─ base_model.py        # create_time / update_time
   │  └─ user.py
   └─ modules/                # 业务模块
      └─ auth/
         ├─ __init__.py
         ├─ routes.py        # 蓝图 + Api 注册
         ├─ resources.py     # HTTP 适配层
         ├─ schemas.py       # 入参校验
         └─ services.py      # 业务逻辑 + 事务
```

**模块内固定五件套**：`routes.py` / `resources.py` / `schemas.py` / `services.py` / `__init__.py`。新模块照此建。

---

## 2. 分层职责（每层只做一件事）

| 层 | 职责 | 禁止 |
|---|---|---|
| `routes.py` | 创建 Blueprint、挂 `url_prefix`、`api.add_resource()` | 写任何业务逻辑 |
| `resources.py` | 解析请求 → 调 schema 校验 → 调 service → 用 `ok/fail` 返回 | 直接查库、写业务规则、拼 SQL |
| `schemas.py` | 请求体格式校验（必填、长度、正则） | 查数据库（唯一性检查属于 service） |
| `services.py` | 业务规则、数据库读写、**事务提交** | 触碰 `request` / `jsonify` / HTTP 状态码 |
| `models/` | 表结构、字段方法、`to_dict()` | 业务编排 |

依赖方向单向：`resources → services → models`，`resources → schemas`。**反向一律禁止**（models 不 import services）。

---

## 3. 接口规范

### 3.1 URL

- 统一前缀 `/api/v1/<模块名>`
- **资源型**接口用名词复数：`/api/v1/orders`、`/api/v1/orders/<int:id>`
- **动作型**接口（认证、导出、审批）允许动词：`/api/v1/auth/signin`
- 路径全小写，多单词用连字符：`/api/v1/user-profiles`
- 版本号只出现在前缀，不出现在模块名里；新增不兼容版本时新建 `api/v2.py`，旧版保留

### 3.2 HTTP 方法

| 方法 | 用途 | 成功状态码 |
|---|---|---|
| GET | 查询 | 200 |
| POST | 创建 / 动作 | 201（创建）、200（动作） |
| PUT / PATCH | 全量 / 部分更新 | 200 |
| DELETE | 删除 | 200 或 204 |

### 3.3 响应格式

**所有**接口（含错误、含 404/500）必须返回统一结构，禁止直接 `return {...}`：

```python
return ok(data, '登录成功')          # 200
return ok(data, '注册成功', 201)     # 201
return fail('账号或密码错误', 401)    # 401
```

```json
{ "code": 0, "msg": "登录成功", "data": { } }
```

- `code = 0` 表示成功，失败时等于 HTTP 状态码
- `msg` 是**面向用户的中文提示**，前端直接展示，不要写英文或堆栈
- 失败时 `data` 必须为 `null`

### 3.4 状态码约定

| 场景 | 状态码 |
|---|---|
| 参数缺失 / 格式错误 | 400 |
| 未登录、凭证无效、凭证过期 | 401 |
| 无权限（已登录但角色不够） | 403 |
| 资源不存在 | 404 |
| 唯一约束冲突 / 状态冲突 | 409 |
| 服务端异常 | 500 |

**安全约定**：登录失败统一返回「账号或密码错误」，不区分「用户不存在」与「密码错误」，防止账号枚举。

### 3.5 认证

- 需要登录的接口加 `@jwt_required()`，用 `get_jwt_identity()` 取用户 id（**字符串**，需转 `int`）
- 认证失败响应由 `common/jwt_callbacks.py` 统一处理，**不要在 resource 里自己判 token**
- 新增 JWT 相关错误类型时，在 `jwt_callbacks.py` 补对应 loader

---

## 4. 校验规范

- 请求体一律通过 `parse_json(Schema)` 解析，**不要直接 `request.get_json()`**
- 必填校验、长度、正则放 `schemas.py`
- **需要查库的校验**（唯一性、存在性）放 `services.py`
- 校验失败必须 `raise ValueError('中文提示')`，由 `parse_json` 转成 400
- 正则常量统一定义在 model 层，schema 与 model 共用一份，不重复写

---

## 5. 事务规范

- **`commit()` 只在 service 层调用**，resource 层禁止提交
- 任何 `commit()` 必须包在 `try/except IntegrityError` 中，异常时 `rollback()`，否则 session 会停留在脏状态导致后续请求连环报错
- 一次请求内的多次写操作，应在同一个 service 方法内完成，保证原子性

---

## 6. 新增模块 Checklist

- [ ] 建 `app/modules/<name>/` 及四件套
- [ ] `routes.py` 提供 `create_<name>_bp() -> Blueprint`，`url_prefix` 为模块名
- [ ] 在 `app/api/v1.py` 中 `register_blueprint`
- [ ] 模型放 `app/models/`，继承 `BaseModel` 与 `db.Model`
- [ ] 需要独立配置时改 `config.py`，不要硬编码在模块里

## 7. 新增接口 Checklist

- [ ] 先在 `API.md` 补接口说明（**同一提交内**）
- [ ] `schemas.py` 写入参校验，中文错误提示
- [ ] `services.py` 写业务逻辑，事务在这里提交并处理 `IntegrityError`
- [ ] `resources.py` 只做翻译：校验 → 调 service → `ok/fail`
- [ ] `routes.py` 注册资源
- [ ] 状态码符合 3.4 约定，`msg` 面向用户
- [ ] 需要登录则加 `@jwt_required()`
- [ ] 用 Postman / curl 跑通成功 + 至少两种失败路径

---

## 8. 命名规范

| 对象 | 规则 | 示例 |
|---|---|---|
| 模块目录 | 小写、单数 | `auth`、`order` |
| Blueprint 名 | 与模块同名 | `Blueprint('auth', ...)` |
| Resource 类 | PascalCase | `SignIn`、`OrderList` |
| Service 类 | PascalCase + Service | `AuthService` |
| 方法 | snake_case | `sign_in`、`get_by_identifier` |
| JSON 字段 | snake_case | `access_token`、`create_time` |
| 常量 | UPPER_SNAKE | `USERNAME_PATTERN` |

**JSON 字段统一 snake_case，前端照抄不转换**；如确需驼峰，必须在 `API.md` 中明确说明，并由前端在 api 层做映射。

---

## 9. 禁止事项

- 禁止在 `resources.py` 里写业务逻辑或直接 `db.session` 操作
- 禁止在 `services.py` 里 import `request` / `flask_restful` / 返回 `jsonify`
- 禁止 `models` 反向 import `services`
- 禁止裸 `return {...}`，必须走 `ok/fail`
- 禁止把密码、token 明文写进日志
- 禁止在代码里硬编码密钥与数据库连接串，一律从 `.env` 读取（配置项见仓库根 `README.md` 的「环境变量」一节）

---

## 10. 依赖与虚拟环境

### 10.1 清单来源

`backend/requirements.txt` 由 `pip freeze` 生成，**禁止手写、禁止手改版本号**。当前与实际环境零漂移。

### 10.2 依赖分类（共 18 个）

| 类别 | 包 | 说明 |
|---|---|---|
| 直接依赖（代码里有 import） | `Flask`、`Flask-RESTful`、`Flask-SQLAlchemy`、`Flask-JWT-Extended`、`SQLAlchemy`、`python-dotenv`、`Werkzeug` | 7 个，每个都有明确的 import 点 |
| 运行期动态加载（搜不到 import） | `PyMySQL`、`PyJWT` | 2 个，**绝对不能删**，见 10.3 |
| 传递依赖（别的包拉进来的） | `blinker`、`click`、`itsdangerous`、`Jinja2`、`MarkupSafe`（Flask 链）<br>`aniso8601`、`pytz`、`six`（Flask-RESTful 链）<br>`typing_extensions`（SQLAlchemy 链） | 9 个，不能单独卸载 |

### 10.3 两个「搜不到 import 但绝对不能删」的包

| 包 | 为什么必需 | 删掉的后果 |
|---|---|---|
| `PyMySQL` | `.env` 里 `mysql+pymysql://` 的 `pymysql` 部分是在告诉 SQLAlchemy 用哪个驱动，**驱动由 SQLAlchemy 在运行时按字符串动态导入**，代码中不存在 `import pymysql` | 启动或首次查库报 `ModuleNotFoundError: No module named 'pymysql'` |
| `PyJWT` | `Flask-JWT-Extended` 内部用它签发 / 校验 token，代码中不存在 `import jwt`（`extensions.py` 里的 `jwt` 是 `JWTManager()` 实例的变量名，不是这个包） | 登录签发 token 时报错，接口返回 500 |

**判断某个包能不能删的统一方法**：

```bash
.venv\Scripts\python -m pip show 包名
# Required-by 非空 → 有别的包在依赖它，不要删
# Required-by 为空 且 全项目搜不到 import → 才是真孤儿
```

### 10.4 已知的「僵尸」依赖（了解即可，不要动）

`aniso8601`、`pytz`、`six` 只服务于 `Flask-RESTful`（日期解析 / 时区 / Python 2 兼容），当前项目一个功能都没用到，合计约 2.3MB。

**但不能单独卸载**——`flask_restful` 导入时会连带导入它们，卸掉直接 `ImportError`。移除的唯一途径是整体替换 `Flask-RESTful`，省 2.3MB 远小于改造 `resources.py` / `routes.py` 的风险，**明确不做**。

### 10.5 新增依赖的流程

```bash
# 1. 激活虚拟环境
cd backend
.venv\Scripts\activate

# 2. 安装
pip install 包名

# 3. 代码里用上并跑通

# 4. 更新清单，与代码同一次提交
pip freeze > requirements.txt
```

### 10.6 从零重建环境

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate            # macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
# 再按根 README 配置 .env 才能启动
```

### 10.7 禁止事项

- 禁止把 `.venv/` 提交进仓库（根 `.gitignore` 已覆盖）
- 禁止手改 `requirements.txt` 的版本号；要升级就 `pip install --upgrade 包名` 后重新 `pip freeze`
- 禁止因为「全项目搜不到 import」就卸载某包，先 `pip show` 看 `Required-by`
