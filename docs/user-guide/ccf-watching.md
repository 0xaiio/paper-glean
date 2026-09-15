# CCF-A 会议 / 期刊监控与推送

> 盯住 CCF-A 类会议与期刊的主页，一旦发布**新的征稿（CFP）、新的 Program、新的接收论文列表**
> 就落盘 digest 并推送给你。名单以**勾选框**形式管理，勾选即订阅、取消即暂停。

## 它解决什么问题

[学者监控](watching.md) 是**按人**抓的：某人挂出了新论文。但「会议节奏」是另一类信息，
它不属于任何一个人：

- SIGMOD 2027 的 CFP 什么时候放出、截稿是哪天；
- ICSE 2026 的 Program 排出来了没有；
- TODS 又出了一期（新一卷新一期的论文列表）。

这些信息**只在会议/期刊自己的主页上**，arXiv 日报和学者监控都看不见。
本功能是第三条互补的监控线：

| | arXiv 日报（`daily`） | 学者监控（`watch`） | **会议/期刊监控（`ccf`）** |
|---|----------------------|-------------------|--------------------------|
| 组织维度 | 按 arXiv 类别 | 按人 | **按会议 / 期刊** |
| 覆盖 | 仅论文（arXiv 收录） | 论文 + 视频 + TR + talk | **CFP + Program + 接收论文列表** |
| 来源 | arXiv API | 个人主页 → DBLP → S2 | **ccfddl.com 截稿 RSS → 会议主页**（期刊走 Crossref） |
| 名单 | 类别固定 | `watchlist.md` | **`ccf.md`（勾选框）** |
| 产物 | `arXiv-schedule.md` | `WATCH-digest.md` | **`CCF-digest.md`** |

参考实现：[ccfddl.com](https://ccfddl.com/)（CCF Conference Deadlines）。

---

## 一、名单：`ccf.md`（勾选框）

Markdown 是唯一真相源（设计原则 2），结构是**一个勾选框列表** —— 勾选即订阅：

```markdown
## 会议

- [x] **SIGMOD** — ACM Conference on Management of Data
  - area: 数据库/数据挖掘/内容检索 (DB)
  - homepage: https://2027.sigmod.org/
  - dblp: https://dblp.org/db/conf/sigmod
  - ccf: A

- [ ] **PODS** — ACM Symposium on Principles of Database Systems
  - area: 数据库/数据挖掘/内容检索 (DB)
  - homepage: https://sigmod.org/pods/
  - ccf: A

## 期刊

- [x] **TODS** — ACM Transactions on Database Systems
  - area: 数据库/数据挖掘/内容检索 (DB)
  - homepage: https://dl.acm.org/journal/tods
  - issn: 0362-5915
```

| 字段 | 必填 | 说明 |
|------|------|------|
| 勾选框 `[x]` / `[ ]` | ✅ | `[x]` = 监控；`[ ]` = 暂停（**不会发起任何网络请求**） |
| `homepage` | ✅ | 会议/期刊主页，**监控的唯一依据** |
| `area` | 推荐 | CCF 领域（如 `数据库/数据挖掘/内容检索 (DB)`），用于批量勾选 |
| `full` | 自动 | 全称（写在标题破折号之后） |
| `dblp` | 可选 | DBLP 索引地址，**仅作人工参考链接，不做抓取** |
| `issn` | 期刊需要 | 期刊经 Crossref 监控新卷期时必需；`ccf refresh` 会自动补 |
| `ccf` | 自动 | CCF 等级（目录内置均为 A） |

### 动态勾选 / 取消（三种方式，任选）

**① CLI**

```powershell
python -X utf8 arxiv_daily.py ccf list                      # 只看已勾选
python -X utf8 arxiv_daily.py ccf list --all --area DB       # 按领域查看全部
python -X utf8 arxiv_daily.py ccf disable SIGMOD             # 取消勾选（暂停）
python -X utf8 arxiv_daily.py ccf enable  SIGMOD             # 重新勾选
python -X utf8 arxiv_daily.py ccf disable --area "数据库"    # 批量取消整个领域
python -X utf8 arxiv_daily.py ccf enable  --area "形式化"    # 批量勾选
python -X utf8 arxiv_daily.py ccf run --only SIGMOD          # 只扫一个
```

**② Web** — 打开 `http://127.0.0.1:8000/ccf`：每条左侧是可点的勾选框，右侧是「主页 / DBLP / 移除」；
面板顶部还提供**按领域「全选 / 全不选」**（名单有 90+ 条，批量操作是刚需）。

**③ 直接编辑** `ccf.md`（agent 或手工均可，下次运行即生效）。

### 添加目录未收录的会议/期刊

内置目录覆盖 ccfddl 收录的全部 CCF-A 会议 + 人工整理的 A 类期刊。缺什么自己加：

```powershell
python -X utf8 arxiv_daily.py ccf add ICDT --homepage https://icdt2027.org/ --area "数据库/数据挖掘/内容检索 (DB)"
python -X utf8 arxiv_daily.py ccf add "某期刊" --journal --homepage https://... --issn 1234-5678
python -X utf8 arxiv_daily.py ccf refresh          # 把内置目录新增的条目并入（保留你的勾选）
python -X utf8 arxiv_daily.py ccf refresh --new-disabled   # 新增条目默认不勾选
```

> `ccf refresh` **只新增与刷新元数据，绝不改动你的勾选状态** —— 勾选是你的决定。

---

## 二、目录从哪来（可审计）

**会议**：`https://ccfddl.com/conference/deadlines_en.xml`（公开 RSS）。
每条都带 **CCF 等级 / 领域 / 官网 / DBLP 索引**，同一会议取**最新一届**的官网（即当前真正在线的那个）。

**期刊**：没有任何截稿站收录期刊，因此 A 类期刊**全部来自人工整理**，并按 ISSN 到
[Crossref](https://www.crossref.org/) 校验。**这是目录里最可能出错的部分** ——
发现错误请直接在 `ccf.md` 里取消勾选或删除。

> 生成脚本：`python scripts/gen_ccf_catalog.py`（可重新抓取并覆盖 `glean/ccf_catalog.py`）。
> 生成时会对每个 URL 做真实 HTTP 校验，并把「真 4xx/5xx」与「本机网络不可达」分开报告 ——
> 后者**不是**死链证据，不要据此删条目。
>
> 本仓库快照：CCF-A 会议 71 个 + A 类期刊 22 个。

---

## 三、解析顺序：ccfddl → 会议主页

```
        ┌─ 1. ccfddl.com 截稿 RSS  →  新的 CFP（结构化，置信度 0.95）
会议 ───┤
        └─ 2. 会议主页 → CFP / Program / 接收论文列表（启发式，0.6–0.9）

        ┌─ 1. Crossref（按 ISSN 取卷期） → 新一卷 / 新一期（置信度 0.95）
期刊 ───┤
        └─ 2. 期刊主页 → 新 issue / 文章列表（启发式）
```

**为什么这样分工**：

- CFP 有**结构化来源**（ccfddl 每天更新截稿日期），就不该去猜 HTML —— 所以 CFP 由 ccfddl 驱动；
- Program 与「接收论文列表」**只存在于会议主页**，只能用启发式解析（同 `homeparse` 的纪律：
  宁可漏、不可吵）；
- **期刊主页大多抓不到**：ACM DL、IEEE Xplore 的表头是 JavaScript 渲染的，抓下来是空壳。
  所以期刊改用 **Crossref 开放 API** 按 ISSN 取 `volume / issue / published`。

### 三个信号怎么判定

| 信号 | 判定依据 | 置信度 |
|------|---------|--------|
| `cfp` 征稿 | ccfddl 条目；或链接文本/URL 含 `call for papers` / `cfp` / `submission` | 0.75–0.95 |
| `program` 日程 | 含 `program` / `schedule` / `timetable` / `agenda` | 0.70–0.85 |
| `papers` 接收论文 | 含 `accepted` / `proceedings` / `award`；期刊由 Crossref 卷期产生 | 0.60–0.95 |

站点根链接（logo）、导航词（`Home` / `Registration` / `Venue` / `Committee` …）一律丢弃；
置信度 < 0.5 丢弃，`0.5–0.6` 保留但在 digest 与 Web 上标「⚠️ 低置信」。

### ⚠️ DBLP 已不可抓取（2026-09 起）

DBLP 现在对 **所有** 端点（HTML 与 API）返回 Anubis「Making sure you're not a bot!」拦截页。
因此本功能的 `dblp` 字段**只是给你点开看的人工链接**，程序从不请求它。
同一原因，学者监控里的 DBLP 兜底源目前也会静默返回空 —— 那是 fail-soft 设计，
不会报错，但请知悉。

---

## 四、怎么判断「新」：基线 vs 差异

```
首次运行  → 建立基线：把当前全部条目记为「已见」，不推送（避免一次性轰炸几十条历史 CFP）
之后每次  → 与 data/ccf_state.json 比对，只推送指纹未出现过的条目
指纹      = sha1(规范化标题 + 可选 URL 主机指纹)
```

- 想让首次运行也推送：`ccf run --force`。
- **期刊指纹的稳定性是刻意设计的**：身份 = `(venue, volume, issue)`，标题只写
  `TODS Volume 51 Issue 4`，URL 固定用期刊主页 —— 这样「某一期持续有新文章入库」
  不会把同一期重复播报，只有**新卷新期**才算新事件。
- 移除条目会**一并清除**其已见状态；取消勾选（`[ ]`）**不清除**，重新勾选后不重推暂停期间的内容。

---

## 五、推送通道

与[学者监控](watching.md) **完全一致**的四个通道，全部 **fail-soft**：

| 通道 | 默认 | 落点 | 开关 |
|------|------|------|------|
| `file` | ✅ 常开 | `CCF-digest.md` + `data/ccf_new.json`（Web 的 NEW 徽标数据源） | — |
| Web 高亮 | ✅ 常开 | `/ccf` 页面新条目打 `NEW` 红标，导航「CCF」显示未读计数 | 页面上「全部标记已读」或 `ccf ack` |
| `desktop` | ✅ Windows 开 | 系统气泡通知（标题为「paper-glean CCF 监控提醒」） | `PAPER_GLEAN_DESKTOP=0` |
| `webhook` | ❌ 关 | POST JSON 到自定义 URL | 设 `PAPER_GLEAN_WEBHOOK_URL` |

> **两条监控线互不干扰**：`watch ack` 不会清掉 CCF 的未读，`ccf ack` 也不会清掉学者的未读
> —— 它们各自写 `data/watch_new.json` 与 `data/ccf_new.json`。

webhook 的配置与载荷格式见 [学者监控 · 配置 webhook](watching.md#webhook)。
`generic` 载荷多两个 CCF 专有字段：`namespace: "ccf"` 与每条 item 的 `venue` / `deadline`。

### 自检

```powershell
python -X utf8 arxiv_daily.py watch push-test          # 通道是共用的，自检命令也共用
python -X utf8 arxiv_daily.py watch push-test --send
```

### 第五个落点：HTML 快照

每次 `ccf run` 还会**无条件**写一份自包含单文件：

```
exports/ccf-digest-<YYYY-MM-DD>.html
```

与 `CCF-digest.md` 同源不同场景：md 是给人翻的日志，HTML 可 `file://` 双击即开、
断网可读、能直接当附件发出去。导出失败只打印 `[WARN] html 导出失败`，不影响 digest 与状态落盘。

页面顶部的**「本次运行」证据表**（运行日期 / 运行编号 / 扫描范围 / 新增 / **各源取回条数** /
新建基线 / 无变化 / 推送通道 / 抓取错误）在 CCF 这条线上尤其要紧：

- `ccf run` 全程 fail-soft，**站点不可达时会静默返回 0 条**，「没有新动态」和「根本没抓到」长得一模一样；
- `last_error` **恒为空** —— 引擎不持久化抓取错误，别指望靠它识别盲点。

所以判据只有两个：**逐源取回条数**，以及控制台/页面上的 `[WARN] 盲区：…`。

### 飞书投递（Feishu）：不在进程内

与[学者监控](watching.md#feishu)一样，`ccf run` **自己不发飞书**，只落盘 HTML 快照；
投递由定时任务调用 `lark-cli`（摘要文字 + HTML 附件发给机器人单聊）承担。
好处是凭据不进仓库、飞书发不出去也不影响监控本身。

> ⚠️ `lark-cli im +messages-send` 的 `--dry-run` **不能阻止发送**。自检请用 `watch push-test`。

---

## 六、定时运行

与 arXiv 日报、学者监控**解耦**。手动等价命令：

```powershell
python -X utf8 arxiv_daily.py ccf run
```

常用变体：

```powershell
python -X utf8 arxiv_daily.py ccf run --only SIGMOD   # 只扫一个会议
python -X utf8 arxiv_daily.py ccf run --force         # 首次也推送
python -X utf8 arxiv_daily.py ccf run --no-push       # 只落盘 digest
```

> 全量 93 个条目一次扫描约需数分钟（条目间有 1.5s 礼貌延时）。想缩短：
> `ccf disable --area <不关心的领域>` 批量取消勾选，或在自动化里按 `--only` 分组跑。

> 完整定时机制（平台任务 / Windows 计划任务）见 [定时运行](scheduling.md)。

---

## 七、文件与产物

| 文件 | 是否入 Git | 说明 |
|------|-----------|------|
| `ccf.md` | ✅ | **名单真相源**（勾选框） |
| `glean/ccf_catalog.py` | ✅ | CCF-A 目录快照（由 `scripts/gen_ccf_catalog.py` 生成） |
| `CCF-digest.md` | ✅ | 人读 digest，按日期分节（`<!-- BEGIN CCF YYYY-MM-DD -->` 幂等） |
| `data/ccf_state.json` | ✅ | 每条目已见指纹 + 上次检查时间（**决定「新」的定义**） |
| `data/ccf_new.json` | ✅ | 未读更新（Web 的 NEW 徽标数据源） |
| `exports/ccf-digest-<YYYY-MM-DD>.html` | ❌ 派生产物 | 自包含静态快照（含「本次运行」证据表），可当附件发出去 |
| `ccf_events.jsonl` | ❌ gitignore | 推送审计日志，append-only |

---

## 八、故障排查

| 症状 | 原因 | 处理 |
|------|------|------|
| 某会议 `0 条基线` | 主页是 JS 渲染 / 需登录 / 网络不可达 | 换一个可解析的页面（如 CFP 子页）作 `homepage` |
| 期刊一条都抓不到 | `issn` 缺失 | `ccf refresh` 自动补；或 `ccf add --issn` 手工补 |
| 期刊主页抓不到内容 | ACM DL / IEEE Xplore 是 JS 渲染 | 正常现象，期刊靠 Crossref，不依赖主页 |
| 一次性推了几十条 | 用了 `--force`；或刚新建基线后 `ccf refresh` 引入大量新条目 | 去掉 `--force`；重新建基线 |
| 主页改版后误报一堆 | 标题变了 → 指纹变了 | 删 `data/ccf_state.json` 中该条目的记录重建基线 |
| 全量跑太慢 | 93 个条目 × 1.5s 延时 | `ccf disable --area <领域>` 批量取消，或 `--only` 分组 |
| webhook 不通 | URL 未设、被代理拦、格式不符 | `watch push-test --send`；回环探测记得 `--noproxy '*'` |
| `[WARN] 盲区：某会议` | 该条目本轮一条都没取到（主页不可达 / 解析规则不匹配） | 看 HTML 证据表的「各源取回」；换一个可解析的 `homepage`（如 CFP 子页） |
| 想知道某会议是不是永久失聪 | 盲区会每天都报，但只看 `last_error` 看不出来（恒为空） | 连续几天在同一条目上出现 0 指纹即可判定；见下例 |

### 已知的永久失聪条目

- **TACAS**：ccfddl 只在伞形标题 `ETAPS 2027 Deadline [ESOP round 2, FoSSaCS, TACAS, iFS]`
  里收录它，而解析要求标题的年份前缀**精确等于** venue 名（`"etaps" ≠ "tacas"`）→ 跳过；
  主页 `www.etaps.org` 是 ETAPS 门户站，实测 0 条；DBLP 按设计不抓。**待修，勿擅自改动解析规则。**
- **DISC**：不在 ccfddl 名录里，只有主页能取到稀疏的 2 条指纹 —— 这是**正常稀疏，不是故障**。
  注意别按子串数它：`DISC` 会命中 "distributed"，计数虚高。

---

## 下一步

- [学者监控与推送](watching.md) — 按人监控（另一条监控线）
- [CLI 参考](cli.md) — 全部命令
- [定时运行](scheduling.md) — 平台任务与 Windows 计划任务
- [开发者指南 · 监控模块](../developer-guide/index.md) — 模块职责与扩展点
