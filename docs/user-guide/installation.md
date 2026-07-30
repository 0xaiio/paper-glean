# 安装指南

## 系统要求

| 组件 | 最低版本 | 说明 |
|------|---------|------|
| Python | 3.10 | 核心逻辑使用标准库，Web 层需 3.10+ |
| Windows / Linux / macOS | — | 跨平台支持 |

## 安装方式

### 方式一：开发安装（推荐）

```powershell
# 克隆仓库
git clone <repository-url>
cd paper-glean

# 基础安装（仅 CLI）
pip install -e .

# 完整安装（CLI + Web）
pip install -e ".[web]"

# 开发安装（含测试依赖）
pip install -e ".[dev]"
```

### 方式二：仅使用 CLI

```powershell
pip install -e .
```

安装后可用命令：
```powershell
arxiv-daily --help
```

### 方式三：文档构建

```powershell
pip install -e ".[docs]"
```

## 验证安装

```powershell
# 检查 CLI 可用
arxiv-daily --help

# 运行测试
pytest tests/ -v

# 启动 Web 应用（如安装了 web 依赖）
python -m glean.web
```

## 可选依赖说明

| 依赖组 | 包含 | 用途 |
|--------|------|------|
| `web` | FastAPI, uvicorn, jinja2 | Web 应用 |
| `dev` | pytest, httpx, pytest-asyncio | 测试与开发 |
| `docs` | mkdocs, mkdocs-material, mkdocstrings | 文档构建 |

## Windows 特别说明

Windows 控制台默认使用 GBK 编码，运行 CLI 时建议加 `-X utf8`：

```powershell
python -X utf8 arxiv_daily.py fetch
```

或在 PowerShell 中设置：
```powershell
$env:PYTHONUTF8 = "1"
```
