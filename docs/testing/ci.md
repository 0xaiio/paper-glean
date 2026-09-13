# CI/CD 流程

> 自动化测试与部署

## GitHub Actions 工作流

### 测试工作流 (`.github/workflows/test.yml`)

```yaml
name: Tests

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests
        run: pytest tests/ -v

      - name: Verify CLI works
        run: arxiv-daily --help
```

### 触发条件

| 事件 | 分支 | 动作 |
|------|------|------|
| push | main, master | 运行测试 |
| pull_request | main, master | 运行测试 |

### 测试矩阵

- Python 3.10, 3.11, 3.12
- Ubuntu Latest

### 文档工作流 (`.github/workflows/docs.yml`)

在 `docs/**`、`glean/**`、`mkdocs.yml` 变更时触发，含三个**门禁**：

1. **PlantUML 同步检查**：若某 `.puml` 比对应 `.png` 新（即改了图未重新渲染），
   直接失败，并提示运行 `python render-diagrams.py`。
2. **严格构建**：`cd docs && mkdocs build --strict`——任何警告都视为错误，
   包括**存在但未加入 `nav` 的 Markdown 文件**（因此新增文档页必须同步登记到
   `docs/mkdocs.yml` 的 `nav`，`design/prototype.html` 这类静态资源除外）。
3. **部署**：仅 `main` 分支推送时，通过 `peaceiris/actions-gh-pages` 发布到 GitHub Pages。

## 本地预提交检查

在提交前建议运行：

```powershell
# 运行测试
pytest tests/ -v

# 检查代码风格（如配置了 black/flake8）
black glean/ tests/
flake8 glean/ tests/

# 验证 CLI
arxiv-daily --help
```

## 文档构建

```powershell
# 安装文档依赖
pip install -e ".[docs]"

# 本地预览
cd docs
mkdocs serve

# 构建站点
mkdocs build
```

## 发布流程

1. 更新版本号（`pyproject.toml`）
2. 更新 `docs/` 中的变更日志
3. 确保 CI 通过
4. 合并到 `main`
5. 打标签：`git tag v0.x.x`
6. 推送标签：`git push origin v0.x.x`
