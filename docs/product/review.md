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
> （来源：[plan.md §1](../../plan.md)）

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
| `glean/web/main.py` | FastAPI 应用工厂、静态挂载；`watch_new_count` / `ccf_new_count` 模板全局（导航未读角标） | ✅ |
| `glean/web/routes.py` | 页面 / API（含 `/api/ping` 存活探测）/ HTMX 片段三类路由 | ✅ |
| `glean/web/models.py` | Pydantic 响应模型 | ✅ |
| `glean/web/templates_config.py` | `NoCacheJinja2Templates`（规避 dict 上下文不可哈希） | ✅ |
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

`tests/test_core.py`（纯函数单元测试）、`tests/test_web.py`（`TestClient` 集成测试，
覆盖 5 页面 + 6 个 API（含 `/api/ping`）+ 1 个 HTMX 片段 + 8 个 `/api/watch/*` 端点
（4 只读 + add/toggle/delete/ack 四个写操作）+ `/api/ccf/*` 端点（venues/new/events 只读，
add/toggle/toggle-area/ack/remove 五个写操作），
写操作均隔离到 `tmp_path` 不碰真实文件）、
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
`tests/test_cli.py`（子进程验证 CLI 八个子命令与包装器，含 `watch` / `ccf` 两个子命令组）。
共 **144 个测试，全部通过**（`pytest -q` → `144 passed`）。

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
| D6 | `docs/product/decisions/adr-002-file-storage.md` | 「原子写入：写临时文件 + `os.replace()`」 | **代码中不存在原子写入**；`pyproject.toml` 声明的 `filelock` 亦**从未被 import** | 中：ADR 描述的是设计意图而非现状 | 已加现状标注 |
| D7 | `.github/workflows/docs.yml` | `publish_dir: ./docs/site` | `docs/mkdocs.yml` 中 `site_dir: ../site`，构建产物实际落在**仓库根 `site/`** | 中：Pages 发布会指向空目录 | 已修正为 `./site` |
| D8 | `docs/developer-guide/core-library.md` | 记录了大量**不存在的函数与错误签名**（`download_pdf`、`fetch_all(hours, cap)` 返回 `(day_str, papers)`、`match_keywords(text, entries)` 返回 dict、`upsert_digest(day, papers, anchor=True)`、`load_interest_entries` 返回 `kind`/`source`、`save_day_data` 声称「原子写入」等） | 真实函数名/签名/返回值以 `glean/core.py` 为准 | 高：开发者照此调用必然失败 | 已按代码重写；`api-reference.md` 的 mkdocstrings 成员表同步修正（原含不存在的 `download_pdf`） |
| D9 | 多处（`user-guide/index.md`、`user-guide/cli.md`、`testing/manual-tests.md`、`product/features.md`、`developer-guide/contributing.md`、`developer-guide/index.md`） | 「PDF 落盘到 `arXiv/` 目录」（暗示在仓库内） | `config.ARXIV_DIR` 默认 `~/papers`，**位于仓库之外**，可用环境变量覆盖 | 高：用户按文档找不到下载的 PDF | 已全部改为 `$ARXIV_DIR`（默认 `~/papers`） |

**另发现**（判断，非文档错误）：`glean/templates/partials/paper_card.html` 的
「Why recommended」区块用 `interest.title in paper.hits_star` 判断——但 `hits_star`
存的是**命中关键词**而非条目标题，该区块因而**永不渲染**。属实现缺陷，
已在 §6 风险中记录，建议 M1.x 修复。

---

## 5. M1 实现 vs 设计目标差距

对比基准：`plan.md` §5（现代界面设计）。**这是"完善原型系统设计"的直接输入。**

| 能力 | plan.md §5 目标 | M1 现状 | 缺口 |
|------|----------------|---------|------|
| 三栏布局 | 日期/过滤器 + 卡片流 + 详情面板 | ✅ 已实现（lg 断点以下折叠） | — |
| 卡内「为什么推荐」 | 卡片自带命中条目 + 权重 + agent 理由 | ⚠ 因 §4 注记的缺陷未渲染 | 需修 |
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
| 文档与实现漂移 | 中 | §4 六处，其中 3 处为高影响 | 修复后，在 CI 中加入「文档-代码一致性」检查项（可选） |
| 卡内推荐理由失效 | 中 | 违反第 4 条原则「可解释」 | M1.x 修：让 `hits_*` 同时携带条目标题，或模板改为关键词匹配 |
| 并发写入 | 低 | 声明了 `filelock` 但未使用；Web 与 CLI 可同时写 `interests.md` | 落实 ADR-002 的原子写入，或删除未用依赖 |
| 未用依赖 | 低 | `pyproject.toml` 的 `filelock` 未被引用 | 二选一：实现文件锁 or 移除依赖 |

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

*本报告为审阅产物，不替代 [plan.md](../../plan.md)（需求规格）与 [survey.md](../../survey.md)（选型决策）。*
