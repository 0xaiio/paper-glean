# 系统设计

> 本文档是 Paper-Glean 的**贯穿性系统设计说明**：从分层架构、模块职责、核心接口、
> 数据流、关键机制到扩展点，一次讲清「系统是怎么搭起来的、为什么这么搭、往哪里扩」。
>
> 相关文档：[架构概览](index.md)（速览）· [数据规范](data-schema.md)（schema）
> · [Web 层详解](web-layer.md)（FastAPI 细节）· [API 参考](api-reference.md)（自动生成）

---

## 1. 定位与边界

**一句话**：研究者个人的、画像可审计的、多源论文推荐与归档工作台
（a personal, auditable-profile, multi-source paper recommendation & archiving workbench）。

**系统边界（不做的事）**：

- 不引入数据库、账号体系、云端托管（违反本地优先，见 [ADR-003](../product/decisions/adr-003-no-database.md)）
- 不自建爬虫绕过官方 API；只用 arXiv 官方 API 并遵守配额礼仪
- 不改变本仓库既有的 PDF 命名规则与 venue 目录结构（这是不可替代的既有资产）

---

## 2. 分层架构

```
┌──────────────────────────── 表现层（Presentation） ────────────────────────────┐
│  CLI: glean/cli.py  ·  arxiv_daily.py（薄包装）  ·  scripts/*.ps1（定时）        │
│  Web: glean/web/ + 模板 + 静态资源   ·   保活: glean/serve.py                    │
└───────────────────────────────────┬───────────────────────────────────────────┘
                                    │  统一调用（逻辑不分叉）
┌───────────────────────────────────▼───────────────────────────────────────────┐
│                          核心库（Core，纯业务逻辑）                              │
│   glean/core.py  ——  抓取 · 命中标注 · digest 生成 · 反馈 · 下载 · 持久化        │
│   glean/config.py ——  路径常量 · 类别 · UA · digest 头                          │
└───────────────────────────────────┬───────────────────────────────────────────┘
                                    │  读写
┌───────────────────────────────────▼───────────────────────────────────────────┐
│                          数据层（唯一事实源，零数据库）                          │
│  interests.md  ·  data/YYYYMMDD.json  ·  feedback.jsonl  ·  arXiv-schedule.md   │
│  PDF: $ARXIV_DIR（默认 ~/papers）                                                │
└───────────────────────────────────────────────────────────────────────────────┘

              ┌───────────────────────────────────────────────┐
   Agent 层 → │ 语义理解：填推荐小节 · 解析新材料扩画像 · 下载归档 │  （非确定性，人工/定时触发）
              └───────────────────────────────────────────────┘
```

**设计意图**：表现层是「壳」，核心库是「唯一实现」，数据层是「唯一事实源」。
Agent 层不属于代码，而是**围绕同一批文件的语义工作流**——这是本系统与
「LLM 黑盒推荐产品」的根本差异：脚本保证确定性，Agent 提供语义增量，两者可独立开关。

---

## 3. 模块与职责

| 模块 | 职责 | 不负责 |
|------|------|--------|
| `glean/config.py` | 仓库路径、`ARXIV_DIR`（可用环境变量覆盖）、9 个 arXiv 类别、UA、digest 头部 | 任何逻辑 |
| `glean/core.py` | HTTP/XML、抓取、命中标注、digest 生成、反馈、下载、持久化 | CLI 参数、HTTP 路由 |
| `glean/cli.py` | argparse 子命令 `fetch`/`daily`/`serve`/`watch`/`ccf`/`download`/`feedback`/`reanchor`；控制台输出 | 业务逻辑（全部委托 core / serve / watch / ccf） |
| `glean/serve.py` | 本地 Web 服务保活：`/api/ping` 探测（绕过环境代理）、后台 detached 拉起、`ensure()` 复用已在线的实例；日志落 `logs/` | 业务逻辑、路由 |
| `glean/monitor.py` | **监控内核（共享）**：`MonitorSpec`/`MonitorJob` 描述子系统，`run_monitor()` 实现「名单 → 抓取 → 指纹 diff → 基线 → digest → 推送 → 审计」；另含身份基元 `slugify`/`norm_title`/`fingerprint`/`kind_of`/`year_of` | **任何网络请求**（抓取函数由调用方注入，故可离线测试） |
| `glean/watch.py` | 学者监控：`watchlist.md` 解析/增删/启停、主页→DBLP→S2 解析、digest 文案；diff/基线/推送/审计委托 `monitor` | HTTP 细节（委托 homeparse / core.http_get） |
| `glean/ccf.py` | 会议期刊监控：`ccf.md` 勾选框名单、目录同步、ccfddl/Crossref/主页三源、digest 文案；diff/基线/推送/审计委托 `monitor` | HTTP 细节（委托 venueparse） |
| `glean/ccf_catalog.py` | CCF-A 目录**快照**（生成物）：71 会议 + 22 期刊，含官网/领域/DBLP/ISSN | 网络（由 `scripts/gen_ccf_catalog.py` 生成） |
| `glean/homeparse.py` | 个人主页启发式解析（stdlib `html.parser`），输出带 `kind` 与 `confidence` 的条目 | 网络（由调用方 fetch） |
| `glean/venueparse.py` | 会议/期刊页启发式解析（`cfp`/`program`/`papers`）+ ccfddl RSS + Crossref 卷期 | 网络（由调用方 fetch） |
| `glean/notify.py` | 推送：`file` / Web NEW / `desktop` / `webhook`，全 fail-soft；**密钥只从环境变量读**；`watch`/`ccf` 双命名空间 | 决定是否推送、推送什么 |
| `glean/htmlkit.py` | **静态快照的共享构件**：内联 CSS（`STYLE`）、渐进增强脚本（`SCRIPT`，暗色为 opt-in）、`escape()`、筛选控件、页面外壳 `page()`；三条链路共用，避免样式/暗色逻辑三份漂移 | 业务逻辑、网络（纯字符串拼装） |
| `glean/report.py` | **独立 HTML 快照渲染**：`build_html()`（arXiv，理由从 `arXiv-schedule.md` 反解析而非重算）+ `MonitorView` / `build_monitor_html()` / `render_monitor_day()`（watch/ccf 共用，零新增也出页面，含「本次运行」证据表与盲区标注）；输出 `exports/<namespace>-digest-<day>.html` | 网络、画像重算 |
| `glean/web/main.py` | `create_app()` 应用工厂；挂载 `/static`；`/` 重定向 | 路由实现 |
| `glean/web/routes.py` | 页面路由、REST API（含 `/api/ping` 存活探测）、HTMX 片段；共享 `PaperFilters` 查询参数组 + `_require_paper` / `_require_entry` / `_run_summary` 助手 | 业务逻辑（全部委托 core） |
| `glean/web/models.py` | Pydantic 线上模型（`FeedbackRequest` 带 0–5 校验）+ `PaperFilters`（`Depends()` 注入的查询参数组） | 持久化 |
| `glean/web/templates_config.py` | 共享 Jinja2 环境（Starlette `Jinja2Templates`）+ `format_timestamp` 过滤器 | — |
| `arxiv_daily.py` | 向后兼容入口 → `glean.cli:main` | — |
| `scripts/run_daily.ps1` / `register_task.ps1` | Windows 计划任务入口（ASCII-only）与注册器 | 业务逻辑 |

---

## 4. 核心接口（`glean/core.py`）

> 全部为纯函数或纯 IO 函数；CLI 与 Web 共享，保证「Web 与 CLI 行为完全一致」。

### 4.1 抓取与解析

| 函数 | 签名 | 说明 |
|------|------|------|
| `http_get` | `(url, timeout=60) -> bytes` | 带 UA 的 GET（二进制；PDF、Atom XML、JSON 一律用它） |
| `http_get_text` | `(url, timeout=60) -> str` | 带 UA 的 GET，并按响应 `Content-Type` 的 charset 解码；charset 缺失或非法一律降级 UTF-8，**不抛异常**（主页 / venue 页抓取走这条） |
| `parse_xml` | `(data: bytes) -> ET.Element` | **拒绝含 `<!DOCTYPE>`/`<!ENTITY>` 的 XML**（防注入） |
| `fetch_category` | `(cat, start_utc, end_utc, max_results=500) -> list[dict]` | 单类别时间窗查询，归一化字段 |
| `fetch_all` | `(hours) -> (papers, start, end)` | 遍历类别、**按 id 跨类别去重**、逐类别间隔 3s（API 礼仪） |

### 4.2 画像与命中

| 函数 | 签名 | 说明 |
|------|------|------|
| `load_interest_entries` | `() -> list[dict]` | 解析 `interests.md`：`section`/`title`/`keywords`/`weight`（缺省 3，钳制 1–10） |
| `load_interest_keywords` | `() -> (star, expand)` | 拍平关键词 |
| `match_keywords` | `(paper, keywords) -> list[str]` | **整词匹配**（`(?<![A-Za-z0-9])…(?:e?s)?(?![A-Za-z0-9])`，大小写不敏感） |
| `annotate_hits` | `(papers) -> bool` | 写入 `hits_star`/`hits_expand`（**命中的关键词**）与 `score_star`/`score_expand`（**命中条目的权重和**） |

### 4.3 digest 生成（幂等）

| 函数 | 签名 | 说明 |
|------|------|------|
| `excerpt` | `(text, limit=400) -> str` | 取前两句；超限按词截断并加 ` …` |
| `day_section` | `(day, papers, start, end, cap) -> str` | 生成单日章节：头部 + `### 📌` + `### 🧐` + `### 分类清单`（每类别 bullet 列表，类别内按 score 降序，超出 `cap` 折叠） |
| `upsert_digest` | `(day, section) -> None` | 在 `<!-- BEGIN/END YYYYMMDD -->` 间**替换**；**保留 agent 已填写的推荐小节**（若非占位符） |

### 4.4 反馈闭环

| 函数 | 签名 | 说明 |
|------|------|------|
| `apply_feedback` | `(paper, day, stars=None, curiosity=None) -> dict` | **共享核心**：算 delta（≥4 → +1；≤2 → −1）→ 更新命中条目权重 → patch digest 表格 → 追加 `feedback.jsonl` |
| `patch_rating` | `(pid, symbol, n) -> bool` | 正则替换推荐表中的 `★`/`🧐` 串 |
| `set_entry_weights` | `(new_weights) -> None` | 就地重写 `interests.md` 各条目的 `- weight:` 行 |

**权重规则（唯一权威定义）**：打分 ≥4 星 → 命中条目权重 +1；≤2 星 → −1；3 星 → 不变。
权重钳制在 [1, 10]。

### 4.5 下载与持久化

| 函数 | 签名 | 说明 |
|------|------|------|
| `sanitize_title` | `(title) -> str` | 清理 LaTeX 记号（`\mathbb{X}`→`X`、`\varepsilon`→`epsilon`）与文件系统非法字符 |
| `download_paper` | `(pid) -> Path \| None` | 落盘 `arXiv<年份> <id><版本> <去标点标题>.pdf`；**校验 `%PDF` 魔数**；返回目标路径 |
| `day_files` | `() -> list[Path]` | `data/` 中真正的日文件（stem 恰为 8 位数字），倒序；**唯一的日期枚举入口** |
| `save_day_data` / `load_day_data` / `list_available_days` | — | `data/*.json` 读写与枚举（倒序，只认 `YYYYMMDD`） |

---

## 5. 关键机制说明

### 5.1 幂等分节（`upsert_digest`）

`arXiv-schedule.md` 中每个日期章节由 HTML 注释标记包裹。重复 `fetch` 只替换标记内内容，
**agent 写在标记外的推荐表不受影响**。这是「脚本可反复重跑 + agent 增量填写」能共存的前提。

### 5.2 双通道（★ / 🧐）不混流

`interests.md` 的两个小节（兴趣点 / 扩展点）分别产出 `hits_star` / `hits_expand`，
互不干涉。这是本系统区别于所有现成产品的**核心机制**：显式分离「利用（exploit）」与
「探索（explore）」，避免相关性单维度把视野收窄。

### 5.3 反馈的可审计性

每次打分产生一条 `feedback.jsonl` 记录，含 `adjustments[]`（kind/rating/delta/命中条目/
是否更新 digest）与 `weight_updates{}`（条目 → 新权重）。**append-only**，故可随时回放、
可 `git diff`、可撤销（人工改回权重）。规则化 + 留痕是 H2 的实现方式。

### 5.4 安全与稳健

- XML 防注入：`parse_xml` 拒绝 DTD/ENTITY
- 下载校验：响应体必须以 `%PDF` 开头，否则丢弃
- 抓取容错：单类别失败不影响整体（`[WARN]` 后继续）
- 文本编码：CLI 强制 `utf-8`（`sys.stdout.reconfigure`）

### 5.5 监控内核：一份引擎，两个子系统（`glean/monitor.py`）

`watch`（按人）与 `ccf`（按会议/期刊）是同一机制的两份实例化。共性收敛在 `monitor.py`：

```
MonitorSpec  ← 静态身份：namespace / subject_field / state_key / digest_marker / item_noun / max_items
MonitorJob   ← 注入点：entries / collect / prepare / accept / render_item + 四条路径
run_monitor()← 唯一实现：基线 → diff → 分组 → digest → 推送 → 审计
```

关键约定：

- **`subject_field` 统一「主语」概念**：新条目挂在 `researcher` 还是 `venue` 名下，由
  `spec` 决定，推送摘要分组、事件日志、digest 小标题都读同一个字段。
- **首次静默建基线**：`subjects.get(key) is None` 时只写指纹不推送，避免上线即刷屏；
  `force=True` 才把首扫结果当作新条目。
- **逐条失败隔离**：单个条目抛异常只进 `errors`，同轮其余条目照跑。
- **审计在推送之后写**：事件行里的 `pushed_to` 才能如实记录每条最终落到了哪些通道。
- **引擎不发网络请求**：抓取函数由调用方注入，因此 `tests/test_monitor.py` 可以完全离线
  地验证基线/差异/幂等/降级等全部语义。
- **路径在调用时解析**：`watch._job()` / `ccf._job()` 每次从模块全局读路径常量，这样
  测试才能用 `monkeypatch.setattr` 把全部文件重定向到 `tmp_path`。

**历史遗留与已修缺陷**：`watch._split_sections` 原本在「名单里没有 `## ` 小节标题」时返回
空前言，导致下一次 `watch add` 会把手写的标题与说明整段抹掉；现已改为「前言截止到第一个
`## `/`### ` 标题之前，找不到则整份文件都是前言」，并加了回归测试
（`tests/test_watch.py::test_preamble_survives_a_list_without_section_headings`）。

---

## 6. 并发与一致性（**现状标注**）

| 项 | 设计意图（ADR-002） | 代码现状 |
|----|-------------------|---------|
| 原子写入 | 写临时文件 + `os.replace()` | ❌ **未实现**，直接 `Path.write_text` |
| 并发写保护 | 文件锁 | ❌ **未实现**；原先声明却从未 import 的 `filelock` 依赖已**于 2026-09-14 从 `pyproject.toml` 移除** |

**判断**：单用户本地场景下风险低（Web 与 CLI 同时写 `interests.md` 才会冲突），
但**文档不应描述未实现的机制**——本表已如实标注。若日后要落实，路径是在 `core.py` 的
`set_entry_weights` / `upsert_digest` / `apply_feedback` 处引入 `FileLock` 并重新声明依赖。

---

## 7. 扩展点

### 7.1 多源采集（M2）

引入插件式 source adapter，arXiv 适配器即现有 `fetch_*` 逻辑的重构：

```python
class SourceAdapter(Protocol):
    name: str
    def fetch_window(self, start: datetime, end: datetime) -> list[Paper]: ...
```

统一实体主键优先级：`DOI > arXiv id > S2 id > OpenAlex id >（标题+作者 指纹）`。
落盘形态不变（仍是每日 JSON），不因多源引入数据库。

### 7.2 推荐算法演进（L0→L3）

| 级 | 机制 | 状态 |
|----|------|------|
| L0 | 关键词整词匹配 + 条目权重求和 | ✅ 已实现 |
| L1 | 条目/论文嵌入向量 + 余弦相似 × 权重 | 📝 M2 |
| L2 | LLM 对 top-N 打分并生成中文理由 | 📝 M2（Agent 层 Web 化） |
| L3 | `w1·L0 + w2·L1 + w3·L2 + 反馈时间衰减` | 📝 远期 |

每级可解释、可关停回退到上一级。

### 7.3 阅读流与库集成（M3）

阅读队列三态（inbox → reading → done）存本地 JSON；全库 PDF 扫描建索引（venue/年份统计）。

---

## 8. 非功能需求

| 维度 | 要求 |
|------|------|
| 离线 | 核心功能完全离线（抓取需网络，其余不需要） |
| 依赖 | CLI 纯标准库；Web 额外需 fastapi/uvicorn/jinja2/python-multipart（原先声明却从未使用的 `filelock` 已于 2026-09-14 移除） |
| 性能 | 单日 ≤500 篇内存过滤足够快；数百篇卡片流需虚拟滚动（M1 未实现） |
| 安全 | XML 防注入、%PDF 校验、无外传用户数据 |
| 可移植 | Python ≥3.10；Windows/macOS/Linux 均可（路径经 `pathlib`） |

---

## 9. 运行与部署

```powershell
pip install -e ".[web]"     # 安装（含 Web 依赖）
python -X utf8 arxiv_daily.py fetch   # 或：arxiv-daily fetch
python -m glean.web          # 启动 Web，默认 127.0.0.1:8000
pytest                        # 运行测试
```

单进程、零运维；数据在仓库内，Git 即同步/备份机制。

---

*本文档与代码同步审阅于 2026-09-14（见 [需求与现状审阅报告](../product/review.md)）。*
