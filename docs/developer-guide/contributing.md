# 贡献指南

> 开发环境搭建与代码规范

## 开发环境

### 克隆仓库

```powershell
git clone https://github.com/0xaiio/paper-glean.git
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
pytest tests/test_monitor.py -v
pytest tests/test_watch.py -v
pytest tests/test_ccf.py -v
pytest tests/test_venueparse.py -v
pytest tests/test_cli.py -v

# 带覆盖率
pytest tests/ --cov=glean --cov-report=html
```

> 测试通过 `monkeypatch` 将路径常量重定向到 `tmp_path`，**不会改动仓库内的真实文件**。
> `test_cli.py` 分两类：子进程只断言 `--help` 与只读子命令（子进程无法 monkeypatch），
> 命令树的不变量则在**进程内**遍历 `build_parser()` 验证。

## 项目结构

```
paper-glean/
├── glean/              # 主包
│   ├── __init__.py
│   ├── core.py         # 业务逻辑（共享）
│   ├── cli.py          # CLI 入口
│   ├── serve.py        # 本地 Web 服务保活
│   ├── monitor.py      # 监控内核（共享）：diff / 基线 / 推送 / 审计 / digest 幂等
│   ├── watch.py        # 学者监控（名单 + 三源 + digest 文案）
│   ├── homeparse.py    # 个人主页启发式解析（零依赖）
│   ├── ccf.py          # CCF 会议/期刊监控（名单 + 目录同步 + 三源）
│   ├── ccf_catalog.py  # CCF-A 名录（生成物）
│   ├── venueparse.py   # ccfddl RSS / 会议主页 / Crossref 解析
│   ├── notify.py       # 推送通道（watch / ccf 双命名空间）
│   ├── config.py       # 常量配置
│   ├── web/            # Web 应用
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   └── templates_config.py
│   └── templates/      # Jinja2 模板（与 web/ 平级）
│       ├── base.html / digest.html / profile.html / archive.html
│       ├── watch.html / ccf.html / redirect.html
│       └── partials/   # paper_list / paper_card / paper_detail
├── scripts/            # 定时基础设施
│   ├── run_daily.ps1   # 任务体（ASCII-only）
│   ├── gen_ccf_catalog.py  # 重新生成 CCF-A 名录
│   └── register_task.ps1
├── tests/              # 测试
│   ├── test_core.py
│   ├── test_web.py
│   ├── test_serve.py
│   ├── test_monitor.py
│   ├── test_watch.py
│   ├── test_ccf.py
│   ├── test_venueparse.py
│   ├── test_notify.py
│   └── test_cli.py
├── data/               # 论文数据
├── ccf.md              # CCF 会议/期刊监控勾选清单
├── CCF-digest.md       # CCF 抓取结果沉淀（按日章节）
├── docs/               # 文档（MkDocs 的 docs_dir）
├── mkdocs.yml          # MkDocs 配置（**仓库根**，勿放回 docs/ 下）
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

`cli.py` 的命令树是**构造出来的**，不是一堵 argparse 墙：

1. 命令参数属于哪个域，就写进哪个构造器（`_build_watch()` / `_build_ccf()`，
   或直接写在 `build_parser()` 里）；`main()` 只有 `build_parser().parse_args()`
   与 `args.func(args)` 两行，不要把参数定义塞回去
2. 复用的参数组用 `_add_window_args()` / `_add_run_args()` / `_add_web_args()`，
   **不要**为新命令再抄一份 `--host/--port`
3. **每个叶子子命令必须 `set_defaults(func=...)`** —— 漏了只有在真正执行时才炸；
   `test_cli.py` 会遍历命令树守住这条
4. 调用 `glean/core.py` 中的函数
5. 在 `tests/test_cli.py` 中添加测试（若命令面变化，同时更新
   `test_command_surface_is_exactly_the_documented_one` 里的 22 个叶子）

### 3. 添加 Web 功能

1. 在 `glean/web/routes.py` 中添加路由
2. 如需新数据模型，在 `glean/web/models.py` 中添加 Pydantic 模型
3. 如需新模板，在 `glean/templates/`（与 `glean/web/` 平级）中添加
4. 在 `tests/test_web.py` 中添加测试

几条「不要抄第二遍」的纪律（对应本轮重构消掉的重复）：

| 重复源 | 唯一出处 |
|--------|----------|
| 论文筛选的六个查询参数（`day` / `category` / `search` / `show_*`） | `models.PaperFilters` + `routes.Filters`（`Depends()` 注入），过滤逻辑只在 `_filter_papers` |
| 导航项（桌面/移动两份版式） | `base.html` 顶部的 `nav_items` 列表 |
| `hx-include` 的六项选择器 | `digest.html` 顶部的 `hx_include` 变量 |
| 出站 HTTP 请求（User-Agent / 超时 / charset 兜底） | `core._http_request()` → `http_get()` / `http_get_text()`；`homeparse.fetch_html` 只是委托，**别再写一份 `urlopen`** |
| 监控扫描的 `--only/--force/--no-push` | `cli._add_run_args()`（`watch run` 与 `ccf run` 共用） |

「查表或 404」「跑一次监控并汇总结果」分别走 `_require_paper` / `_require_entry`
与 `_run_summary`，不要在路由里各写一遍。

### 4. 添加新的监控线

监控线遵循统一的「`glean/monitor.py` 引擎 + 编排模块 + 命名空间推送」范式
（现有 `watch` / `ccf` 两条；`daily` 是更早的独立实现，尚未迁移）：

1. 在 `glean/config.py` 中登记该线的路径与常量
2. 在 `glean/notify.py` 的 `_NEW_PATHS` / `NS_LABEL` 中注册新命名空间（保证未读集合互相隔离）
3. 新建 `glean/<line>.py`，**只写这条线独有的部分**：
   - 名单解析 / 增删 / 启停（对标 `load_watchlist` / `load_venues`）
   - 采集函数 `collect_items()`（对标 watch / ccf）
   - 一个 `MonitorSpec`（`namespace` / `subject_field` / `state_key` / `digest_marker` /
     `item_noun` / `max_items`）
   - 一个 `_job()`：从**模块全局**读路径常量并组装 `MonitorJob`
   - digest 单行渲染 `_item_line()` 与两个薄包装 `render_section()` / `upsert_*_digest()`
   - `run()` 一行转调 `monitor.run_monitor(...)`
4. 在 `glean/cli.py` 中挂子命令，在 `glean/web/routes.py` 中挂 API 与页面
5. 补测试：新增 `tests/test_<line>.py`（隔离路径 + stub 抓取），引擎本身的语义由
   `tests/test_monitor.py` 覆盖，**不要**在新线里重复测基线/差异/幂等

> 判断标准：如果一段代码在两条监控线里长得一样，它就应该在 `monitor.py` 里，而不是被抄两遍。

## 文档更新

任何代码变更都必须同步更新相关文档：

- CLI 变更 → 更新 `docs/user-guide/cli.md`
- API 变更 → 更新 `docs/developer-guide/api-reference.md`
- 数据格式变更 → 更新 `docs/developer-guide/data-schema.md`
- 架构变更 → 更新 `docs/developer-guide/index.md`
- 测试变更 → 更新 `docs/testing/index.md` 与 `docs/testing/test-plan.md`
- 新功能 → 更新 `docs/product/features.md` 与 `plan.md`

!!! warning "新增文档页必须登记 nav"
    配置在**仓库根**的 `mkdocs.yml`（`docs_dir: docs` / `site_dir: site`）。
    新增 `docs/**/*.md` 后**必须**加进 `mkdocs.yml` 的 `nav`，否则 CI 的
    `mkdocs build --strict` 会把「未登记的文件」判为警告并直接失败。
    本地自查：在仓库根执行 `mkdocs build --strict`（不是 `cd docs`）。

## 发布流程

1. 更新 `pyproject.toml` 中的版本号
2. 更新 `docs/` 中的相关文档
3. 确保所有测试通过
4. 提交并推送
5. 打标签：`git tag v0.x.x`
