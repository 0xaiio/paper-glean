# 架构概览

> Paper-Glean 系统架构与模块关系

## 架构图

![系统架构图](../assets/images/architecture.png)

> 图源文件：[architecture.puml](../assets/diagrams/architecture.puml)

## 核心架构：脚本 + Agent 混合

```
┌─────────────────────────┐     ┌──────────────────────────────┐
│ arxiv_daily.py fetch    │ ──▶ │ arXiv-schedule.md (## YYYYMMDD) │
│ (确定性, 可独立定时运行) │     │ data/YYYYMMDD.json (原始数据)   │
└─────────────────────────┘     └──────────────┬───────────────┘
                                               │ agent (Qoder Quest) 阅读
                                               ▼
                                ┌──────────────────────────────┐
                                │ 填写 ★ 重点关注 / 🧐 视野扩展   │
                                │ arxiv_daily.py download <id>… │
                                │ → PDF 落盘到 $ARXIV_DIR (按命名规则)│
                                └──────────────────────────────┘
```

### 脚本层

- **确定性**：纯标准库 Python，无需 agent 即可独立运行
- **职责**：抓取、去重、生成 digest、关键词命中标记、下载 PDF
- **入口**：`arxiv_daily.py` / `glean/cli.py`

### Agent 层

- **语义理解**：读取 `data/*.json`、digest 与 `interests.md`
- **职责**：填写推荐小节、调用 download、解析新材料为兴趣条目
- **触发**：用户主动请求或定时任务

## 模块关系

```
glean/
├── core.py          # 纯业务逻辑（共享）
├── cli.py           # CLI 包装器（fetch/daily/serve/watch/download/feedback/reanchor）
├── serve.py         # 本地 Web 服务保活（探测 / 后台拉起 / ensure）
├── watch.py         # 学者监控（名单 / 解析编排 / 指纹 diff / 事件）
├── homeparse.py     # 个人主页启发式解析（stdlib html.parser，零依赖）
├── notify.py        # 推送四通道（file / desktop / webhook / Web NEW）
├── config.py        # 常量与配置
└── web/
    ├── main.py      # FastAPI 应用工厂（含 watch_new_count 模板全局）
    ├── routes.py    # 路由定义（含 /api/ping 与 /api/watch/*）
    ├── models.py    # Pydantic 模型
    └── templates/   # Jinja2 模板
```

> 仓库根另含 `scripts/`（`run_daily.ps1` / `register_task.ps1`），
> 提供 Windows 计划任务形式的定时入口；详见 [定时运行](../user-guide/scheduling.md)。

### 监控层

- **按人而非按类别**：arXiv 日报抓「今天这些类别新增了什么」，监控抓「这几个人
  最近挂出了什么」——后者才能覆盖视频 / 技术报告 / talk。
- **解析顺序**：`homeparse`（主页，首选，唯一覆盖非论文）→ `fetch_dblp` → `fetch_s2`
  （兜底，且显式配置时并行合并去重）。
- **「新」的定义**：`fingerprint = sha1(规范化标题 + 可选 URL 主机指纹)`，
  与 `data/watch_state.json` 比对；首次运行建基线不推送。
- **推送**：`notify.push()` 串行调用各通道，任一通道失败均不影响其余。

### 数据流

![数据流图](../assets/images/data-flow.png)

> 图源文件：[data-flow.puml](../assets/diagrams/data-flow.puml)

## 设计原则

1. **本地优先**：数据全部落在本仓库内，可 Git 版本化、可离线、可随时退出
2. **Markdown/JSON 为唯一事实源**：Web 应用只是视图层
3. **CLI 永远是 fallback**：Web 挂了脚本照跑
4. **可解释推荐**：每条推荐能回答「为什么推荐给我」

## 技术栈

| 层次 | 技术 | 说明 |
|------|------|------|
| CLI | Python 标准库 | 零外部依赖 |
| Web 后端 | FastAPI | 异步 HTTP 框架 |
| Web 前端 | HTMX + Alpine.js | 服务器渲染 + 轻量交互 |
| 模板 | Jinja2 | 服务端 HTML 渲染 |
| 样式 | Tailwind CSS | 实用优先 CSS |
| 数据 | Markdown + JSON | 本地文件存储 |

## 延伸阅读

- [系统设计](system-design.md) — 分层架构、核心接口、数据流、关键机制、扩展点与并发现状
- [Web 层详解](web-layer.md) — FastAPI + HTMX 路由与模板细节
- [数据规范](data-schema.md) — 四个数据文件的精确 schema
- [界面设计规范](../design/index.md) — Web 界面的目标形态与交互契约
