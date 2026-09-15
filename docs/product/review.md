# 需求与现状审阅报告

> 审阅对象：paper-glean v0.1.0（M0 + M1）
> 审阅日期：2026-09-13
> 审阅范围：需求文档（`plan.md` / `survey.md` / `interests.md`）与仓库内全部代码、文档资产
> 阅读方式：**结论先行**；正文严格区分「事实（可核实）」与「判断（有推理）」两类陈述。

> **2026-09-13 跟进（调度集成）**：`plan.md §4.9` / `docs/product/features.md §9`
> 原描述「定时任务已有 Quest/schtasks 通道」属未落地的占位。本轮新增：
> `glean/serve.py`（保活 + 代理绕过）+ `arxiv_daily.py daily/serve` 子命令 +
> `/api/ping` 存活探测 + `scripts/run_daily.ps1` 与 `scripts/register_task.ps1`
> （Windows 计划任务）+ 上述文档一致化。详见 [定时运行](../user-guide/scheduling.md)。

> **2026-09-14 跟进（监控与推送）**：新增「按人监控」能力（`plan.md §4.11` /
> `features.md §11`）。`glean/watch.py` + `glean/homeparse.py`（主页启发式解析）
> + `glean/notify.py`（四通道推送）+ `watchlist.md` / `WATCH-digest.md`
> + Web `/watch` 页面与 `/api/watch/*`；关键取舍：**不做 Google Scholar**
> （无官方 API、违反 ToS、易封禁），改以 DBLP + Semantic Scholar 公开 API 覆盖，
> 个人主页作为唯一能覆盖「视频 / 技术报告 / talk」的首选源。
> 详见 [学者监控与推送](../user-guide/watching.md)。
>
> **2026-09-14 跟进（CCF 会议期刊监控）**：新增第三个监控维度「按会议/期刊」
> （`plan.md §4.12` / `features.md §12`）。`glean/ccf.py` + `glean/venueparse.py`
> + `glean/ccf_catalog.py`（CCF-A 目录快照：71 会议 + 22 期刊）+ `ccf.md`（**勾选框**名单）
> / `CCF-digest.md` + Web `/ccf` 页面与 `/api/ccf/*`。关键取舍：
> ① **CFP 走结构化来源**（ccfddl.com 公开 RSS，带等级/领域/官网），不去猜 HTML；
> ② **期刊走 Crossref 开放 API**（按 ISSN 取卷期），因为 ACM DL / IEEE Xplore 是 JS 渲染空壳；
> ③ **DBLP 已不可抓取**（2026-09 起全部端点返回 Anubis 反爬拦截页），`dblp` 字段降级为人工参考链接；
> ④ 推送复用同一套四通道但走**独立命名空间**，与学者监控的未读互不清除。
> 详见 [CCF 会议期刊监控](../user-guide/ccf-watching.md)。

---

## 1. 结论摘要

1. **方向无问题**。系统定位（本地优先的个人论文推荐与归档工作台）清晰，四条设计原则
   在文档与代码中一致落地，M0/M1 均已实现且可运行（CLI 与 Web 双界面 + 自动化测试）。
2. **问题集中在「文档与实现的一致性」**，而非产品方向。共发现 **6 处**文档表述与代码实际
   行为不符（§4），其中 2 处会误导使用者（反馈日志 schema、digest 格式）。
3. **M1 实现是 `plan.md` §5 目标设计的子集**。已实现「能用的视图层」，但尚未实现
   plan.md 中承诺的关键交互（卡内打分、⌘K 命令面板、权重演化、归档库检索等），见 §5。
4. **建议**：先按 §4 清单修复文档一致性（低风险、纯文档改动），再按 M2 路线推进；
   Web 界面的目标形态以本仓库新增的 [界面设计规范](../design/index.md) 与
   [高保真原型](../design/prototype.html) 为准。

---

## 2. 需求基线（复核）

### 2.1 一句话产品定义

> 研究者个人的、画像可审计的、多源论文推荐与归档工作台。
> （来源：[plan.md §1](https://github.com/0xaiio/paper-glean/blob/main/plan.md)）

### 2.2 四条设计原则（功能取舍的唯一仲裁标准）

| # | 原则 | 在代码中的落点 |
|---|------|---------------|
| 1 | 本地优先 | 全部数据落在仓库内；`glean/web/` 无数据库、无账号 |
| 2 | Markdown/JSON 为唯一事实源 | `core.py` 直接读写 `interests.md` / `data/*.json` / `feedback.jsonl` / `arXiv-schedule.md` |
| 3 | CLI 永远是 fallback | `glean/core.py` 为共享纯函数；`arxiv_daily.py` 保留为薄包装 |
| 4 | 可解释推荐 | 每篇论文携带 `hits_*`（命中关键词）与 `score_*`（命中条目权重和） |

### 2.3 硬性标准 H1–H4（来源：survey.md §2）

H1 画像可人工审计编辑 · H2 反馈→推荐演化透明可追溯 · H3 PDF 按本仓库规则落盘 ·
H4 数据本地主权。**H1+H3 的组合是本系统相对 20+ 现成系统不可替代之处**（survey.md §6）。

---

## 3. 现状盘点（事实）

### 3.1 代码资产

| 模块 | 职责 | 状态 |
|------|------|------|
| `glean/config.py` | 路径常量、arXiv 类别、UA、digest 头 | ✅ |
| `glean/core.py` | 纯业务逻辑：抓取/命中/生成 digest/反馈/下载/持久化 | ✅ 共享核心 |
| `glean/cli.py` | argparse 壳：`fetch`/`daily`/`serve`/`download`/`feedback`/`reanchor` | ✅ |
| `glean/serve.py` | 本地 Web 服务保活：`/api/ping` 探测（绕过环境代理）+ 后台 detached 拉起 + `ensure()` 复用 | ✅ |
| `glean/monitor.py` | **监控内核（watch/ccf 共享）**：`run_monitor()` 统一实现基线 → 指纹 diff → digest → 推送 → 审计；含身份基元 `slugify`/`norm_title`/`fingerprint`/`kind_of`/`year_of`。**不发网络请求**（抓取由调用方注入） | ✅ |
| `glean/watch.py` | 学者监控：名单解析/增删/启停、主页→DBLP→S2 解析、digest 文案；diff/基线/推送/审计委托 `monitor` | ✅ |
| `glean/ccf.py` | 会议期刊监控：`ccf.md` 勾选框名单、目录同步、ccfddl/Crossref/主页三源、digest 文案；diff/基线/推送/审计委托 `monitor` | ✅ |
| `glean/ccf_catalog.py` | CCF-A 目录**快照**（71 会议 + 22 期刊，含官网/领域/DBLP/ISSN），由 `scripts/gen_ccf_catalog.py` 生成 | ✅ |
| `glean/homeparse.py` | 主页启发式解析（stdlib `html.parser` 零依赖）：论文/视频/TR/talk + 置信度 | ✅ |
| `glean/venueparse.py` | 会议/期刊页启发式解析（cfp/program/papers）+ ccfddl RSS + Crossref 卷期 | ✅ |
| `glean/notify.py` | 推送四通道 `file`/Web NEW/`desktop`/`webhook`（generic·feishu·wecom），全 fail-soft；支持 `watch`/`ccf` 双命名空间 | ✅ |
| `glean/htmlkit.py` | 静态快照共享构件：内联 CSS/JS（暗色 opt-in）、`escape()`、筛选控件、页面外壳 `page()`；三条链路共用 | ✅ |
| `glean/report.py` | 独立 HTML 快照渲染：arXiv 的 `build_html()`（理由从 digest 反解析）+ watch/ccf 的 `MonitorView`/`build_monitor_html()`（零新增也出页面，含运行证据表与盲区标注） | ✅ |
| `glean/web/main.py` | FastAPI 应用工厂、静态挂载；`watch_new_count` / `ccf_new_count` 模板全局（导航未读角标） | ✅ |
| `glean/web/routes.py` | 页面 / API（含 `/api/ping` 存活探测）/ HTMX 片段三类路由；`PaperFilters` 查询参数组与 `_require_paper` / `_require_entry` / `_run_summary` 三个共用助手 | ✅ |
| `glean/web/models.py` | Pydantic 线上模型 + `PaperFilters`（`Depends()` 注入的查询参数组） | ✅ |
| `glean/web/templates_config.py` | Starlette `Jinja2Templates`（模板环境 + `format_timestamp` 过滤器）；已去掉过时的私有 API 兼容子类 | ✅ |
| `glean/templates/**` | Jinja2 模板（base / digest / profile / archive / **watch** / **ccf** + 3 个 partial） | ✅ |
| `glean_static/**` | `css/app.css`、`js/app.js`（Alpine 键盘流） | ✅ |
| `watchlist.md` | **学者监控名单真相源**：姓名/主页/DBLP/S2/tags/enabled，两节（监控中/已暂停） | ✅ |
| `ccf.md` | **会议期刊监控名单真相源**：勾选框 + 主页/领域/DBLP/ISSN，两节（会议/期刊） | ✅ |
| `WATCH-digest.md` | 监控 digest（按人），按日期分节幂等 upsert | ✅ |
| `CCF-digest.md` | 会议期刊 digest，按日期分节幂等 upsert | ✅ |
| `data/watch_state.json` | 监控「已见指纹」——决定什么算新作 | ✅ |
| `data/ccf_state.json` | 会议期刊监控「已见指纹」——决定什么算新动态 | ✅ |
| `arxiv_daily.py` | 向后兼容薄包装 → `glean.cli:main` | ✅ |
| `scripts/run_daily.ps1` / `scripts/register_task.ps1` | Windows 计划任务入口与注册器（ASCII-only） | ✅ |
| `scripts/gen_ccf_catalog.py` | 重新生成 `glean/ccf_catalog.py`（ccfddl RSS + 人工补充 + Crossref ISSN + 链接校验） | ✅ |

### 3.2 数据资产

| 文件 | 形态 | 说明 |
|------|------|------|
| `interests.md` | Markdown | 画像真相源：2 小节（兴趣点 ★ / 扩展点 🧐）、5 个条目、每条目 keywords + weight |
| `data/20260729.json` | JSON | 当日 128 篇论文原始数据（含 `hits_*` / `score_*`） |
| `feedback.jsonl` | JSONL | 反馈审计日志，append-only，懒创建 |
| `arXiv-schedule.md` | Markdown | 人读 digest，幂等分节（`<!-- BEGIN/END YYYYMMDD -->`） |
| `watchlist.md` / `WATCH-digest.md` | Markdown | 学者监控名单与 digest（按人） |
| `ccf.md` / `CCF-digest.md` | Markdown | 会议期刊监控名单（勾选框）与 digest（按会议） |

### 3.3 文档资产

`docs/` 已构成 MkDocs 体系：4 个角色分区（用户 / 开发者 / 产品 / 测试）+ 设计分区 + 术语表 +
4 篇 ADR + 4 张 PlantUML 图（含 PNG 与 `render-diagrams.py`）；`site/` 为已构建产物。

### 3.4 测试资产

`tests/test_core.py`（纯函数单元测试，含 `list_available_days` 只认 `YYYYMMDD`
日文件、不把 `data/` 里的监控状态文件当日期；以及 `http_get` 与 `http_get_text`
共用一个请求构造与 User-Agent、charset 取自 `Content-Type` 且坏 charset 降级为 UTF-8、
`homeparse.fetch_html` 确实委托 core 而不自带第二份 `urlopen`）、`tests/test_web.py`（`TestClient` 集成测试，
覆盖 5 页面 + 6 个 API（含 `/api/ping`）+ 1 个 HTMX 片段 + 8 个 `/api/watch/*` 端点
（4 只读 + add/toggle/delete/ack 四个写操作）+ `/api/ccf/*` 端点（venues/new/events 只读，
add/toggle/toggle-area/ack/remove 五个写操作）+ 共享筛选项在页面/API/HTMX 三处行为一致 +
`paper_card` 推荐理由契约，
写操作与筛选断言均隔离到 `tmp_path` 不碰真实文件）、
`tests/test_serve.py`（`probe` / `ensure` 单元 + 端到端环回服务存活测试，含环境代理绕过回归）、
`tests/test_monitor.py`（**监控内核**：身份基元、状态容错、审计字段、digest 幂等与新日期插入、
首轮静默建基线 → 增量、`--force`、逐条失败隔离、`prepare` 错误与 context 透传、`accept`
钩子、推送降级、`use_network` 透传）、
`tests/test_watch.py`（名单增删启停、解析优先级、指纹、基线/差异、事件、digest 幂等、
无 `## ` 小节时前言不被抹掉的回归）、
`tests/test_ccf.py`（勾选框名单、目录同步保留勾选、三源分工、跨源去重、基线/差异、事件、digest 幂等）、
`tests/test_venueparse.py`（venue 页 cfp/program/papers 分类、nav/logo 剔除、ccfddl 匹配与实体反转义、
Crossref 卷期分组与指纹稳定性）、
`tests/test_notify.py`（文件通道去重/ack、**双命名空间隔离**、桌面通道开关、webhook 三种载荷与失败降级）、
`tests/test_cli.py`（子进程验证 CLI 八个子命令与包装器，含 `watch` / `ccf` 两个子命令组；
并在进程内遍历 `build_parser()` 的命令树，断言**每个叶子子命令都挂了 `func`**、
命令面恰好是文档所载的 22 个叶子、`watch run` 与 `ccf run` 共用同一组标志）。
共 **183 个测试，全部通过**（`pytest -q` → `183 passed`）。

---

## 4. 文档 ↔ 实现不一致清单（必须修）

> 判定方式：逐条比对文档表述与 `glean/core.py` / 实际生成物。**均为已核实事实。**

| # | 位置 | 文档表述 | 代码实际行为 | 影响 | 处置 |
|---|------|---------|-------------|------|------|
| D1 | `docs/developer-guide/data-schema.md` | `adjustments[].kind` 为 `"stars"` / `"curiosity"` | `apply_feedback` 写入 `"star"` / `"expand"` | 高：按文档解析日志会失败 | 已修正 |
| D2 | `docs/developer-guide/data-schema.md` | `weight_updates` 为 `{条目: {old, new}}` | 实际为 `{条目标题: 新权重(int)}` | 高：字段语义错误 | 已修正 |
| D3 | `docs/developer-guide/data-schema.md` | `abstract_head` 取摘要前 100 字符 | `excerpt(abstract, 200)`，且是**前两句**截断 | 中 | 已修正 |
| D4 | `docs/developer-guide/data-schema.md` | `interests.md` 小节标题为 `## 兴趣点 ★` | 实际为 `## 兴趣点（★ 重点关注推荐依据）`（`core.py` 按「兴趣点」子串匹配，恰好兼容） | 低 | 已修正 |
| D5 | `docs/developer-guide/data-schema.md` | `arXiv-schedule.md` 为「每类别一张表格」 | 实际为「分节 + bullet 列表」（见 `core.day_section`） | 高：与真实产物不符 | 已修正 |
| D6 | `docs/product/decisions/adr-002-file-storage.md` | 「原子写入：写临时文件 + `os.replace()`」 | **代码中不存在原子写入**；`pyproject.toml` 声明的 `filelock` 亦**从未被 import** | 中：ADR 描述的是设计意图而非现状 | 已加现状标注；`filelock` 依赖已于 2026-09-14 **从 `pyproject.toml` 移除**（见 F3） |
| D7 | `.github/workflows/docs.yml` | `publish_dir: ./docs/site` | 构建产物实际落在**仓库根 `site/`** | 中：Pages 发布会指向空目录 | 已修正为 `./site`；2026-09-14 进一步把配置迁到仓库根 `mkdocs.yml`（见 F4） |
| D8 | `docs/developer-guide/core-library.md` | 记录了大量**不存在的函数与错误签名**（`download_pdf`、`fetch_all(hours, cap)` 返回 `(day_str, papers)`、`match_keywords(text, entries)` 返回 dict、`upsert_digest(day, papers, anchor=True)`、`load_interest_entries` 返回 `kind`/`source`、`save_day_data` 声称「原子写入」等） | 真实函数名/签名/返回值以 `glean/core.py` 为准 | 高：开发者照此调用必然失败 | 已按代码重写；`api-reference.md` 的 mkdocstrings 成员表同步修正（原含不存在的 `download_pdf`） |
| D9 | 多处（`user-guide/index.md`、`user-guide/cli.md`、`testing/manual-tests.md`、`product/features.md`、`developer-guide/contributing.md`、`developer-guide/index.md`） | 「PDF 落盘到 `arXiv/` 目录」（暗示在仓库内） | `config.ARXIV_DIR` 默认 `~/papers`，**位于仓库之外**，可用环境变量覆盖 | 高：用户按文档找不到下载的 PDF | 已全部改为 `$ARXIV_DIR`（默认 `~/papers`） |

**另发现**（判断，非文档错误）：`glean/templates/partials/paper_card.html` 的
「Why recommended」区块曾用 `interest.title in paper.hits_star` 判断——但 `hits_star`
存的是**命中关键词**而非条目标题，该区块因而**永不渲染**。属实现缺陷，
**已于 2026-09-14 修复**（改为按 `interest.keywords` 与 `hits_*` 求交集，
`data-schema.md` 中自相矛盾的字段说明也一并订正）。

**另发现**（同上，已修）：`core.list_available_days()` 原以 `data/*.json` 通配枚举日期，
而 `data/` 同时存放 `watch_state.json` / `ccf_state.json` / `watch_new.json`
（见 `data-schema.md`），于是返回 `['watch_state', 'watch_new', 'ccf_state', '20260729']`；
`/digest` 与 `/api/papers` 的默认日期取首个元素 = `watch_state`，
**首页因此默认显示 0 篇**。**已于 2026-09-14 修复**（新增 `core.day_files()` 只认
8 位数字日文件，`list_available_days` / `find_paper` 共用）。

### 4.1 第 2–3 轮重构（2026-09-14）——可读性 / 可维护性

> 两轮都遵循同一判据：**只收敛已被写第二遍、或已经被写错的东西**，不为重构而重构；
> 每轮独立提交、独立推送，行为等价性逐项验证后才提交。

| # | 位置 | 原状 | 处置 | 影响面 |
|---|------|------|------|--------|
| F0 | `glean/web/routes.py` · `models.py` · `templates/base.html` · `templates/digest.html` | 六个筛选查询参数在 `/digest`、`/api/papers`、`/htmx/paper-list` 各写一遍；「查表或 404」4 处、「`find_paper` 或 404」2 处、「汇总 run 结果」2 处；桌面与移动导航各自手写 5 个链接；`digest.html` 的 6 项 `hx-include` 选择器重复 6 次 | 参数组只在 `models.PaperFilters` 声明一次并以 `Annotated[..., Depends()]` 注入；收敛为 `_require_entry` / `_require_paper` / `_run_summary` / `_filter_papers`；导航共用一份 `nav_items`，`hx-include` 抽成模板变量 | 等价性实测：新 `_filter_papers` 与旧实现在 51200 组用例上 0 不一致；导航 5+5 项逐项不变；`hx-include` 6/6 逐字一致（插值需 `|safe`） |
| F1 | `glean/cli.py` | `main()` 是约 130 行的 argparse 墙：命令定义与 `set_defaults(func=…)` 交错，`watch` / `ccf` 两棵子树的参数三处近乎逐字重复，`cmd_watch_run` / `cmd_ccf_run` 各自抄一遍结果汇报 | 拆出 `build_parser()` + 每域一个构造器 `_build_watch()` / `_build_ccf()`；参数组 `_add_window_args()` / `_add_run_args()` / `_add_web_args()`；汇报逻辑收敛为 `_report_monitor_run()` + 两份 kind 词表。`main()` 只剩 `build_parser().parse_args()` 与 `args.func(args)` | 纯内部；命令面与 `--help` 文本不变（新增测试锁定 22 个叶子子命令） |
| F2 | `glean/core.py` · `glean/homeparse.py` | 两套 HTTP：`core.http_get` 与 `homeparse.fetch_html` 各写一份 `urlopen`（同一 User-Agent、同一超时策略，但拷贝两份） | `core` 新增 `_http_request()`（UA 策略唯一落点）与 `http_get_text()`（charset 取自 `Content-Type`，坏 charset 降级 UTF-8）；`homeparse.fetch_html` 退化为一行委托 | 抓取行为不变，例外路径（DBLP/S2/主页/venue 页）全部共用一条通道 |
| F3 | `pyproject.toml` | 声明了 `filelock>=3.13.0`，但全仓库**从未 import**（D6 已记录） | 移除该依赖；同时把 `project.urls` 从占位符改为真实 `github.com/0xaiio/paper-glean` | 少一个装包依赖；`pip install -e .` 不变 |
| F4 | `mkdocs.yml`（新建于仓库根，删除 `docs/mkdocs.yml`）· `.github/workflows/docs.yml` | 配置位于 `docs/mkdocs.yml` 且写 `docs_dir: .` + `site_dir: ../site`（MkDocs ≥1.6 **拒绝** `docs_dir` 为配置所在目录，严格构建必失败）；CI 里又是 `cd docs && mkdocs build --strict`；另有 3 个断链（`product/review.md` 指向仓库根 `plan.md` / `survey.md`，`user-guide/ccf-watching.md` 指向 `watching.md#配置-webhook`——该标题经 MkDocs 的 ASCII 归一后 slug 为 `webhook`） | 配置迁到仓库根：`docs_dir: docs` / `site_dir: site`；CI 改为在根目录直接 `mkdocs build --strict`；3 个断链分别改为 GitHub 绝对链接与 `#webhook` | `mkdocs build --strict` **0 警告**（原 3 警告即 abort），docs 作业的严格门禁恢复有效 |
| F5 | `pyproject.toml` 的 `[tool.setuptools.package-data]` | 只声明 `templates/*.html` | 补 `templates/partials/*.html` | 修复：装 wheel 后 `paper_card` / `paper_detail` / `paper_list` 三个片段缺失，Web 界面会 500 |
| F6 | `glean/web/` | `templates_config.py` 的 `NoCacheJinja2Templates` 依赖私有符号 `starlette.templating._TemplateResponse`；`models.py` 有从未作响应模型使用的 `PaperResponse` 与死模型 `FilterState` | 删除该子类改用官方 `Jinja2Templates`；`FilterState` 转为真正生效的 `PaperFilters`（`Annotated[..., Depends()]` 注入） | 移除对 Starlette 私有 API 的耦合（见第 2 轮 commit） |

---

## 5. M1 实现 vs 设计目标差距

对比基准：`plan.md` §5（现代界面设计）。**这是"完善原型系统设计"的直接输入。**

| 能力 | plan.md §5 目标 | M1 现状 | 缺口 |
|------|----------------|---------|------|
| 三栏布局 | 日期/过滤器 + 卡片流 + 详情面板 | ✅ 已实现（lg 断点以下折叠） | — |
| 卡内「为什么推荐」 | 卡片自带命中条目 + 权重 + agent 理由 | ✅ 已实现（命中条目 + 权重；hover 显示命中关键词） | 缺 agent 理由文本 |
| 键盘流 | `j/k` `1-5` `Shift+1-5` `d` `s` `o` `/` `⌘K` | ⚠ `app.js` 实现 j/k/1-5/Shift+1-5/d/o// | 缺 `s` 收藏、`⌘K` 命令面板 |
| 打分即生效 + 角标提示 | 打分校卡角标显示权重变动 | ⚠ 仅详情面板有按钮，无角标提示、无需更新卡片 | 缺 |
| 权重演化时间线 | 回放 `feedback.jsonl` 画折线 | ❌ `profile` 仅有静态条目卡 + 权重条 | 缺 |
| 「建议新增条目」收件箱 | 高分未命中 → 采纳/忽略 | ❌ 无（CLI 有 HINT 文本） | 缺 |
| 归档库统计/检索 | venue/年份统计面板 + 全库检索 | ⚠ 仅最近 100 个 PDF 的表格 | 缺 |
| 可视化面板 | 权重雷达图、每日新增趋势、venue 分布 | ❌ 无 | 缺 |
| 亮 / 暗主题 | 默认跟随系统 | ⚠ 默认亮色（localStorage `darkMode === 'true'` 才暗色），顶栏可切换 | 与目标略异 |
| 洪峰性能 | 虚拟滚动 | ⚠ 全量渲染（128 篇可接受） | 数百篇需处理 |

---

## 6. 风险与建议

| 风险 | 级别 | 说明 | 建议 |
|------|------|------|------|
| 文档与实现漂移 | 中 | §4 九处（D1–D9），其中 5 处为高影响，**均已修正** | 修复后，在 CI 中加入「文档-代码一致性」检查项（可选） |
| 卡内推荐理由失效 | 已修 | 违反第 4 条原则「可解释」 | 2026-09-14 已改为关键词交集匹配，并补 `test_web.py` 端到端回归 |
| 默认视图在未标注数据上为空 | 中 | `data/20260729.json` 是旧版产物，不含 `hits_*`/`score_*`；默认筛选（★+🧐，不含 Other）会把 128 篇全部滤掉，首页显示「No papers found」。属**既有行为**，与本次重构无关 | 待定：① 读时用 `annotate_hits` 重算（推荐项，`interests.md` 本就是真相源）；② 默认勾上 Other；③ 重新抓取数据。需产品决策 |
| 并发写入 | 低 | Web 与 CLI 可同时写 `interests.md`（无原子写入、无文件锁） | 落实 ADR-002 的原子写入（需重新引入文件锁依赖） |
| 未用依赖 | **已消** | `pyproject.toml` 的 `filelock` 未被任何模块引用 | 2026-09-14 已移除依赖（见 F3） |

---

## 7. 后续路线映射

| 期 | 内容 | 与本次审阅的关系 |
|----|------|-----------------|
| M0 | CLI + agent + Markdown | 已完成 |
| M1 | 只读 Web 视图 + 打分/下载 | 已完成，**界面按 design/ 原型定稿后可补齐 §5 缺口** |
| M2 | 多源接入 + 嵌入推荐 | 无阻塞 |
| M3 | 阅读流 + 库集成 | 依赖归档库改造（§5 缺口） |
| M4 | 图谱连边 / 周报 / 通知 | 无阻塞 |

---

*本报告为审阅产物，不替代 [plan.md](https://github.com/0xaiio/paper-glean/blob/main/plan.md)（需求规格）与 [survey.md](https://github.com/0xaiio/paper-glean/blob/main/survey.md)（选型决策）。*
