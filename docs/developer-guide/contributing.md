# 贡献指南

> 开发环境搭建与代码规范

## 开发环境

### 克隆仓库

```powershell
git clone <repository-url>
cd paper-glean
```

### 安装开发依赖

```powershell
pip install -e ".[dev]"
```

这将安装：
- pytest + pytest-asyncio（测试）
- httpx（Web 测试）
- 所有 web 依赖

## 运行测试

```powershell
# 运行全部测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_core.py -v
pytest tests/test_web.py -v
pytest tests/test_watch.py -v
pytest tests/test_ccf.py -v
pytest tests/test_venueparse.py -v
pytest tests/test_cli.py -v

# 带覆盖率
pytest tests/ --cov=glean --cov-report=html
```

> 测试通过 `monkeypatch` 将路径常量重定向到 `tmp_path`，**不会改动仓库内的真实文件**。
> `test_cli.py` 只断言 `--help` 与只读子命令（子进程无法 monkeypatch）。

## 项目结构

```
paper-glean/
├── glean/              # 主包
│   ├── __init__.py
│   ├── core.py         # 业务逻辑（共享）
│   ├── cli.py          # CLI 入口
│   ├── serve.py        # 本地 Web 服务保活
│   ├── watch.py        # 学者监控编排
│   ├── homeparse.py    # 个人主页启发式解析（零依赖）
│   ├── ccf.py          # CCF 会议/期刊监控编排
│   ├── ccf_catalog.py  # CCF-A 名录（生成物）
│   ├── venueparse.py   # ccfddl RSS / 会议主页 / Crossref 解析
│   ├── notify.py       # 推送通道（watch / ccf 双命名空间）
│   ├── config.py       # 常量配置
│   └── web/            # Web 应用
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py
│       ├── routes.py
│       ├── models.py
│       ├── templates_config.py
│       └── templates/
├── scripts/            # 定时基础设施
│   ├── run_daily.ps1   # 任务体（ASCII-only）
│   ├── gen_ccf_catalog.py  # 重新生成 CCF-A 名录
│   └── register_task.ps1
├── tests/              # 测试
│   ├── test_core.py
│   ├── test_web.py
│   ├── test_serve.py
│   ├── test_watch.py
│   ├── test_ccf.py
│   ├── test_venueparse.py
│   ├── test_notify.py
│   └── test_cli.py
├── data/               # 论文数据
├── ccf.md              # CCF 会议/期刊监控勾选清单
├── CCF-digest.md       # CCF 抓取结果沉淀（按日章节）
├── docs/               # 文档
└── glean_static/       # Web 静态资源
```

> PDF 默认下载到 `$ARXIV_DIR`（`~/papers`），**不在仓库内**——可用环境变量指向任意本地论文库。

## 代码规范

### Python 风格

- 遵循 PEP 8
- 使用类型注解（Python 3.10+）
- 函数文档字符串使用 Google 风格

### 提交规范

```
<type>: <subject>

<body>

type:
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式（不影响代码运行）
- refactor: 重构
- test: 测试
- chore: 构建/工具
```

## 添加新功能

### 1. 修改核心逻辑

如果新功能涉及业务逻辑：

1. 在 `glean/core.py` 中添加纯函数
2. 在 `tests/test_core.py` 中添加单元测试
3. 确保 CLI 和 Web 都能调用

### 2. 添加 CLI 命令

1. 在 `glean/cli.py` 中添加子命令解析
2. 调用 `glean/core.py` 中的函数
3. 在 `tests/test_cli.py` 中添加测试

### 3. 添加 Web 功能

1. 在 `glean/web/routes.py` 中添加路由
2. 如需新数据模型，在 `glean/web/models.py` 中添加 Pydantic 模型
3. 如需新模板，在 `glean/web/templates/` 中添加
4. 在 `tests/test_web.py` 中添加测试

### 4. 添加新的监控线

监控线遵循统一的「编排模块 + 命名空间推送」范式（现有 `daily` / `watch` / `ccf` 三条）：

1. 新建 `glean/<line>.py`，实现 `load_*` / `run` / digest upsert 等编排函数
2. 在 `glean/config.py` 中登记该线的路径与常量
3. 在 `glean/notify.py` 的 `_NEW_PATHS` / `NS_LABEL` 中注册新命名空间（保证未读集合互相隔离）
4. 在 `glean/cli.py` 中挂子命令，在 `glean/web/routes.py` 中挂 API 与页面
5. 补测试：核心编排 `tests/test_<line>.py`，解析器单独成文件

## 文档更新

任何代码变更都必须同步更新相关文档：

- CLI 变更 → 更新 `docs/user-guide/cli.md`
- API 变更 → 更新 `docs/developer-guide/api-reference.md`
- 数据格式变更 → 更新 `docs/developer-guide/data-schema.md`
- 架构变更 → 更新 `docs/developer-guide/index.md`
- 测试变更 → 更新 `docs/testing/index.md` 与 `docs/testing/test-plan.md`
- 新功能 → 更新 `docs/product/features.md` 与 `plan.md`

## 发布流程

1. 更新 `pyproject.toml` 中的版本号
2. 更新 `docs/` 中的相关文档
3. 确保所有测试通过
4. 提交并推送
5. 打标签：`git tag v0.x.x`
