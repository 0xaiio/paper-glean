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
pytest tests/test_cli.py -v

# 带覆盖率
pytest tests/ --cov=glean --cov-report=html
```

## 项目结构

```
paper-glean/
├── glean/              # 主包
│   ├── __init__.py
│   ├── core.py         # 业务逻辑（共享）
│   ├── cli.py          # CLI 入口
│   ├── config.py       # 常量配置
│   └── web/            # Web 应用
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py
│       ├── routes.py
│       ├── models.py
│       ├── templates_config.py
│       └── templates/
├── tests/              # 测试
│   ├── test_core.py
│   ├── test_web.py
│   └── test_cli.py
├── data/               # 论文数据
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

## 文档更新

任何代码变更都必须同步更新相关文档：

- CLI 变更 → 更新 `docs/user-guide/cli.md`
- API 变更 → 更新 `docs/developer-guide/api-reference.md`
- 数据格式变更 → 更新 `docs/developer-guide/data-schema.md`
- 架构变更 → 更新 `docs/developer-guide/index.md`

## 发布流程

1. 更新 `pyproject.toml` 中的版本号
2. 更新 `docs/` 中的相关文档
3. 确保所有测试通过
4. 提交并推送
5. 打标签：`git tag v0.x.x`
