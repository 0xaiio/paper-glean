# 学者监控与推送

> 盯住一批学者，一旦他们的个人主页 / DBLP / Semantic Scholar 出现**论文、视频、技术报告、talk**，
> 就落盘 digest 并推送给你。名单可随时增删。

## 它解决什么问题

arXiv 日报（见 [CLI 参考](cli.md) 的 `fetch`）是**按类别**抓的：只看 cs.DB / cs.LO …
这些类别里今天新增了什么。它看不见：

- 你关注的那几位学者**新挂在自己主页上的**技术报告、talk 视频、预印本；
- 类别之外的产出（数学、交叉领域）；
- 「某人终于把他三年前那篇 TR 挂出来了」这类事件。

监控功能是**按人**抓的，与 arXiv 日报互补：

| | arXiv 日报（`daily`） | 学者监控（`watch`） |
|---|----------------------|-------------------|
| 组织维度 | 按 arXiv 类别 | 按人 |
| 覆盖 | 仅论文（arXiv 收录） | 论文 + 视频 + 技术报告 + talk |
| 来源 | arXiv API | 个人主页 → DBLP → Semantic Scholar |
| 频率 | 每日本类别增量 | 每日全量比对差异 |
| 产物 | `arXiv-schedule.md` | `WATCH-digest.md` |

---

## 一、名单：`watchlist.md`

Markdown 是唯一真相源（设计原则 2），与 `interests.md` 平行：

```markdown
## 监控中

### 魏恒峰 Hengfeng Wei
- homepage: https://hengxin.github.io
- dblp: Hengfeng Wei
- tags: 分布式一致性; 形式化方法
- enabled: true
- 备注: 南京大学

## 已暂停

### Hagit Attiya
- homepage: https://hagit.net.technion.ac.il
- enabled: false
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `homepage` | 推荐 | 个人主页 URL，**首选解析源**（唯一能覆盖视频/TR 的源） |
| `dblp` | 可选 | DBLP 的 PID（`pid/00/0000`）或作者全名 —— 兜底 |
| `s2` | 可选 | Semantic Scholar author id —— 兜底，可补摘要/venue |
| `tags` | 可选 | 分号分隔，用于 Web 端过滤 |
| `enabled` | 否 | 缺省 `true`；`false` = 暂停监控但**保留条目与历史** |

### 动态增删（三种方式，任选）

**① CLI**

```powershell
python -X utf8 arxiv_daily.py watch add "魏恒峰 Hengfeng Wei" --homepage https://hengxin.github.io --tags "分布式;形式化"
python -X utf8 arxiv_daily.py watch disable "Hagit Attiya"     # 暂停（保留历史）
python -X utf8 arxiv_daily.py watch enable  "Hagit Attiya"     # 恢复
python -X utf8 arxiv_daily.py watch remove  "Hagit Attiya"     # 移除（同时清除已见状态）
python -X utf8 arxiv_daily.py watch list --all
```

**② Web** — 打开 `http://127.0.0.1:8000/watch`，表单添加，每行右侧「暂停 / 移除」按钮。

**③ 直接编辑** `watchlist.md`（agent 或手工均可，`watch` 下次运行即生效）。

---

## 二、解析顺序：主页 → DBLP → S2

```
         ┌─ 1. 个人主页（首选，覆盖论文/视频/TR/talk）
学者 ────┤
         └─ 2. DBLP → 3. Semantic Scholar（兜底）
```

- **主页优先**：只有主页里有「视频 / 技术报告 / talk」，DBLP 与 S2 **只收录论文**。
- **兜底触发**：主页抓不到任何条目（改版、JS 渲染、网络失败）时才回落到 DBLP / S2。
- **并行合并**：若你显式填了 `dblp` / `s2`，会**同时**抓取并按标题去重合并
  （主页版本优先）——既然填了 id，就认为你想用上。
- **Google Scholar 不做**：无官方 API、抓取违反其 ToS 且极易被封。
  要达到同等覆盖，用 **DBLP（CS 最全）+ Semantic Scholar（有摘要与引用）**，二者都是公开 API。

### 主页解析是启发式的（重要）

个人主页没有统一结构，解析基于「链接长得像不像一条成果」的启发式规则，并为每条给出
**置信度**：

- 站点根链接（`https://www.hnu.edu.cn/`）→ 判定为单位/机构 logo，**丢弃**；
- 命中论文特征（`.pdf` / `arxiv` / `doi` / 会议名）→ `paper`，置信度 0.8；
- 命中视频站（YouTube / Bilibili / Vimeo）→ `video`，0.9；
- 命中 `Technical Report` / `-TR.pdf` → `report`，0.8；
- 其余 → `other`，0.4；
- **置信度 < 0.5 一律丢弃**，`0.5–0.6` 保留但在 digest 与 Web 上标「⚠️ 低置信」。

已知边界（均为**漏报**而非误报，符合「宁可漏、不可吵」）：

- 主页用 JavaScript 渲染发表列表 → 抓不到（此时会回落到 DBLP/S2）；
- 只有裸链接没有标题 → 用文件名反推标题（如 `swiftpaxos-nsdi24.pdf` → `swiftpaxos nsdi24`）；
- 主页改版 → 旧条目指纹失效，可能产生一次「全新增」的误报。

---

## 三、怎么判断「新」：基线 vs 差异

```
首次运行  → 建立基线：把当前全部条目记为「已见」，不推送（避免一次性轰炸几十条历史成果）
之后每次  → 与 data/watch_state.json 比对，只推送指纹未出现过的条目
指纹      = sha1(规范化标题 + 可选 URL 主机指纹)，改链接不改标题不会重复推送
```

- 想让首次运行也推送：`watch run --force`。
- 移除某人会**一并清除**其已见状态（下次加回来重新建基线）。
- 暂停（disable）**不清除**状态，恢复后不会重推暂停期间的内容。

---

## 四、推送通道

四个通道，全部 **fail-soft**（某个通道挂了不影响其它，也不让 `watch run` 失败）：

| 通道 | 默认 | 落点 | 开关 |
|------|------|------|------|
| `file` | ✅ 常开 | `WATCH-digest.md` + `data/watch_new.json`（Web 的 NEW 徽标数据源） | — |
| Web 高亮 | ✅ 常开 | `/watch` 页面新条目打 `NEW` 红标，导航「学者」显示未读计数（与「CCF」计数互相独立） | 页面上「全部标记已读」或 `watch ack` |
| `desktop` | ✅ Windows 开 | 系统气泡通知 | `PAPER_GLEAN_DESKTOP=0` 关闭 |
| `webhook` | ❌ 关 | POST JSON 到自定义 URL | 设 `PAPER_GLEAN_WEBHOOK_URL` |

### 配置 webhook

> ⚠️ **Webhook URL 是凭据**。它**只从环境变量读取**，不要写进任何被 Git 跟踪的文件。

```powershell
# Windows（当前会话）
$env:PAPER_GLEAN_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
$env:PAPER_GLEAN_WEBHOOK_FORMAT = "feishu"     # generic | feishu | wecom

python -X utf8 arxiv_daily.py watch push-test --send
```

| 变量 | 取值 | 说明 |
|------|------|------|
| `PAPER_GLEAN_WEBHOOK_URL` | URL | 空则关闭该通道 |
| `PAPER_GLEAN_WEBHOOK_FORMAT` | `generic`（默认）/ `feishu` / `wecom` | 载荷形状 |
| `PAPER_GLEAN_DESKTOP` | `1`（默认）/ `0` | 关闭桌面通知 |

`generic` 载荷：`{"text": "...", "day": "2026-09-14", "count": 2, "items": [...]}`
（飞书/企业微信机器人需要各自的信封格式，用 `feishu` / `wecom` 一步到位。）

### 自检

```powershell
python -X utf8 arxiv_daily.py watch push-test          # 只看哪些通道开着
python -X utf8 arxiv_daily.py watch push-test --send   # 真发一条自检消息
```

### 第五个落点：HTML 快照

上面四个通道之外，每次 `watch run` 还会**无条件**写一份独立 HTML：

```
exports/watch-digest-<YYYYMMDD>.html
```

它与 `WATCH-digest.md` 的区别不是内容而是**场景**：md 是给人翻的日志，HTML 是自包含单文件，
`file://` 双击即开、断网可读、可直接当附件发出去（微信/邮件/飞书都可以）。
它也不参与 fail-soft 通道计数 —— 导出失败只打印 `[WARN] html 导出失败`，不影响 digest 与状态的落盘。

页面顶部有一张**「本次运行」证据表**：运行日期 / 运行编号 / 扫描范围（`--only` 时写明是谁）/
新增条数 / **各源取回条数** / 新建基线 / 无变化 / 推送通道 / 抓取错误。这是刻意设计的：
`watch` 全程 fail-soft，**网络不通时三个源全 0 也会报「没有新作」**，光看 `[NEW]` 计数无法区分
「今天真的没有」和「整轮假阴性」。逐源的取回条数就是那条判据。

### 飞书投递（Feishu）：不在进程内，由定时任务承担

`watch run` **自己不发飞书** —— 四个通道里没有飞书，它只把 HTML 快照写到 `exports/`。
投递是**自动化那一层**的事：定时任务在 `run` 之后调用 `lark-cli`，把摘要文字 + HTML 附件
发给机器人单聊（即发给你自己）。

这样分工的三个好处：

1. **凭据不落进仓库** —— 发信身份由 `lark-cli` 的登录态提供，本仓库里没有任何 token；
2. **网络失败不影响监控** —— 飞书发不出去，`WATCH-digest.md` 与状态照常落盘；
3. **换投递目标不用改代码** —— 想改成群、改成邮件，只动自动化 prompt。

> ⚠️ `lark-cli im +messages-send` 的 `--dry-run` **不能阻止发送**（实测仍会发出并返回真实 `message_id`）。
> 自检请用 `watch push-test`（它什么都不发），或用 `--no-push` 跑监控。

---

## 五、定时运行

监控与 arXiv 日报**解耦**（监控每天一次足够，且互不阻塞）。已注册独立自动化；
手动等价命令：

```powershell
python -X utf8 arxiv_daily.py watch run
```

常用变体：

```powershell
python -X utf8 arxiv_daily.py watch run --only "Alexey Gotsman"  # 只扫一人
python -X utf8 arxiv_daily.py watch run --force                  # 首次也推送
python -X utf8 arxiv_daily.py watch run --no-push                # 只落盘 digest
```

> 完整定时机制（平台任务 / Windows 计划任务）见 [定时运行](scheduling.md)。

---

## 六、文件与产物

| 文件 | 是否入 Git | 说明 |
|------|-----------|------|
| `watchlist.md` | ✅ | **名单真相源** |
| `WATCH-digest.md` | ✅ | 人读 digest，按日期分节（`<!-- BEGIN WATCH YYYY-MM-DD -->` 幂等） |
| `data/watch_state.json` | ✅ | 每人已见指纹 + 上次检查时间（**决定「新」的定义**，建议跟踪） |
| `data/watch_new.json` | ✅ | 未读新作（Web 的 NEW 徽标数据源） |
| `exports/watch-digest-<day>.html` | ❌ 派生产物 | 自包含静态快照（含「本次运行」证据表），可当附件发出去 |
| `watch_events.jsonl` | ❌ gitignore | 推送审计日志，append-only |

---

## 七、故障排查

| 症状 | 原因 | 处理 |
|------|------|------|
| `0 条基线` | 主页是 JS 渲染 / 被墙 / 返回非 HTML | 补 `dblp:` 或 `s2:` 走兜底 |
| `[WARN] 盲区：某人` | 该人本轮**一条内容都没取到**（源不可达），不是「没有新作」 | 看 HTML 证据表的「各源取回」；补 `dblp:`/`s2:` 兜底；或换可解析的 `homepage` |
| 加人后一次性推几十条 | 用了 `--force` | 去掉 `--force`，让首次运行建基线 |
| 主页改版后误报一堆「新作」 | 标题变了 → 指纹变了 | 删掉 `data/watch_state.json` 里该人的记录重建基线 |
| 桌面通知没弹 | 非 Windows / `PAPER_GLEAN_DESKTOP=0` / 无托盘环境 | 用 `watch push-test` 确认通道状态 |
| webhook 不通 | URL 未设、被代理拦、格式不符 | `push-test --send`；回环探测记得 `--noproxy '*'` |
| 想要被墙站点的主页 | 网络限制 | 走 DBLP / S2 兜底，或配代理后重试 |
| 报告「没有新作」但心里没底 | 整轮 fail-soft 假阴性：网络不通时三个源都是 0 | **别信 `sources` 与 `last_checked`** —— `sources` 是累积并集（粘性）、`last_checked` 无论成败都刷新。判据是 HTML 证据表的逐源取回条数 |
| 跑了 `--dry-run` 还是发出去了 | `lark-cli` 的 `--dry-run` 不拦发送 | 自检改用 `watch push-test`；只落盘用 `watch run --no-push` |

> **兜底是硬要求**：只写 `- homepage:` 的条目，主页一挂就完全失聪。
> 至少给一位学者配一个 `dblp:` 或 `s2:`，否则他的沉默永远无法与「真的没新作」区分开。

---

## 下一步

- [CLI 参考](cli.md) — 全部命令
- [定时运行](scheduling.md) — 平台任务与 Windows 计划任务
- [兴趣画像](interest-profile.md) — 监控结果与 arXiv 日报共用同一套画像
- [开发者指南 · 监控模块](../developer-guide/index.md) — 模块职责与扩展点
