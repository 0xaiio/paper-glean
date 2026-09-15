# CLI 参考

> 命令行接口完整手册

## 命令概览

```powershell
arxiv-daily <command> [options]
```

| 命令 | 说明 |
|------|------|
| `fetch` | 抓取 arXiv 论文并生成 digest |
| `daily` | 每日流水线：fetch → digest →（可选）确保本地 Web 服务在线 |
| `serve` | 启动本地 Web 应用（前台） |
| `watch` | 学者监控与推送（子命令见下，详见 [学者监控与推送](watching.md)） |
| `ccf` | CCF-A 会议/期刊监控与推送（子命令见下，详见 [CCF 会议期刊监控](ccf-watching.md)） |
| `download` | 按 ID 下载 PDF |
| `feedback` | 人工调整推荐指数 |
| `reanchor` | 补齐 digest 锚点与跳转链接 |
| `html` | 把某天 digest 渲染成可直接在浏览器打开的独立 HTML |

---

## fetch — 抓取论文

抓取指定时间窗口内的新增论文，生成/更新 digest。

```powershell
python -X utf8 arxiv_daily.py fetch [options]
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--hours` | int | 24 | 回溯时间窗口（小时） |
| `--date` | str | 今天 | 指定 digest 章节日期（YYYYMMDD） |
| `--cap` | int | 100 | 每类别列表上限 |

### 示例

```powershell
# 抓取过去 24 小时（默认）
python -X utf8 arxiv_daily.py fetch

# 回补 48 小时
python -X utf8 arxiv_daily.py fetch --hours 48

# 指定日期章节
python -X utf8 arxiv_daily.py fetch --date 20260728

# 提高每类别上限
python -X utf8 arxiv_daily.py fetch --cap 50
```

### 行为说明

- **幂等**：同一天重复 `fetch` 会整体替换该章节，不会重复追加
- **保留推荐**：agent 已填写的 ★/🧐 推荐小节会被保留，不会被占位符覆盖
- **跨类别去重**：同一论文 cross-list 到多个类别时只计一次
- **API 礼仪**：每类别请求间隔 3 秒

### 输出文件

| 文件 | 说明 |
|------|------|
| `data/YYYYMMDD.json` | 当天全部论文原始数据 |
| `arXiv-schedule.md` | 更新 digest 章节 |
| `exports/arxiv-digest-YYYYMMDD.html` | 可在浏览器直接打开的独立快照 |

---

## daily — 每日流水线

`fetch` + 确保本地 Web 服务在线的合并入口，供定时任务使用。

```powershell
python -X utf8 arxiv_daily.py daily [options]
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--hours` | int | 24 | 回溯时间窗口（小时） |
| `--cap` | int | 100 | 每类别列表上限 |
| `--date` | str | 今天 | 指定 digest 章节日期（YYYYMMDD） |
| `--serve` | flag | 关 | 结束后确保 Web 服务在线（不在线则后台拉起） |
| `--host` | str | `127.0.0.1` | Web 服务地址 |
| `--port` | int | `8000` | Web 服务端口 |

### 示例

```powershell
# 抓取并在需要时拉起 Web 服务
python -X utf8 arxiv_daily.py daily --serve

# 仅抓取（等价于 fetch）
python -X utf8 arxiv_daily.py daily

# 指定端口，避免与其他本地服务冲突
python -X utf8 arxiv_daily.py daily --serve --port 8100
```

### 行为说明

- 抓取部分与 `fetch` 完全一致（共用同一实现，产物相同）。
- **fail-soft**：digest 先落盘，服务拉不起来只警告、不报错退出，
  最坏情况下你仍有 `arXiv-schedule.md` 可读。
- 服务在线判定口径是 `GET /api/ping` 返回 200；已在线则复用，不重复启动。

详见 [定时运行](scheduling.md)。

---

## serve — 启动 Web 应用

前台启动本地 Web 应用，用于手动 / 开发场景。

```powershell
python -X utf8 arxiv_daily.py serve [--host H] [--port P] [--reload]
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--host` | str | `127.0.0.1` | 绑定地址 |
| `--port` | int | `8000` | 绑定端口 |
| `--reload` | flag | 关 | 开发模式：代码变更自动重载 |

与 `python -m glean.web` 等价。区别在于 `daily --serve` 是**后台独立进程**
（写日志到 `logs/serve-<host>-<port>.log`、可脱离父进程存活），`serve` 是前台。

---

## watch — 学者监控与推送

按**人**跟踪新作（论文 / 视频 / 技术报告 / talk）。名单是 `watchlist.md`。
完整说明见 [学者监控与推送](watching.md)。

```powershell
python -X utf8 arxiv_daily.py watch <action> [options]
```

| action | 说明 | 主要参数 |
|--------|------|---------|
| `add` | 添加监控对象 | `<姓名>` `--homepage` `--dblp` `--s2` `--tags` |
| `remove` | 移除监控对象（同时清除其已见状态） | `<姓名>` |
| `enable` / `disable` | 启用 / 暂停（保留条目与历史） | `<姓名>` |
| `list` | 列出名单 | `--all`（含已暂停） |
| `run` | 扫描并推送新作 | `--only` `--force` `--no-push` |
| `ack` | 清除 Web 端 NEW 徽标 | — |
| `push-test` | 检查推送通道 | `--send`（发自检消息） |

### 示例

```powershell
# 添加（主页为首选解析源；DBLP/S2 兜底）
python -X utf8 arxiv_daily.py watch add "魏恒峰 Hengfeng Wei" `
  --homepage https://hengxin.github.io --tags "分布式一致性;形式化方法"

# 扫描（首次建基线不推送；之后只推新作）
python -X utf8 arxiv_daily.py watch run

# 只扫一人 / 强制首次也推送 / 只落盘不推送
python -X utf8 arxiv_daily.py watch run --only "Alexey Gotsman"
python -X utf8 arxiv_daily.py watch run --force
python -X utf8 arxiv_daily.py watch run --no-push
```

### 行为说明

- **解析顺序**：个人主页 → DBLP → Semantic Scholar；显式配置了 `dblp`/`s2` 时会并行合并去重。
- **首次建基线**：新加入的对象第一次运行只记录「已见」，**不推送**历史成果（除非 `--force`）。
- **落盘 HTML 快照**：每次 `run` 都会产出 `exports/watch-digest-<YYYY-MM-DD>.html`（失败只降级 `[WARN]`）。
  **零新作也会出页面** —— 页面上带「本次运行」证据表（扫描范围 / 各源取回条数 / 新建基线 / 推送通道），
  「今天没消息」与「脚本根本没跑通」是两件事，这里要把后者排除掉。
  > ⚠️ **监控快照用 `YYYY-MM-DD`**（`run_monitor` 的 `day` 就是 `strftime("%Y-%m-%d")`），
  > 与 arXiv 快照的 `arxiv-digest-<YYYYMMDD>.html` **不同**，脚本里拼文件名时别想当然。
- **盲区告警**：某位学者本轮**一条内容都没取到**（`sources=[]`、指纹 0）时打印
  `[WARN] 盲区：<姓名> …… 源可能不可达（不是「没有新作」）`，并在 HTML 里标为「盲区」。
  这一情形下 `last_checked` 仍会刷新、`sources` 仍可能残留上一次的累积并集，**两者都不能证明本次抓取成功**。
- **fail-soft**：单个对象抓取失败只记录 `[WARN]`，不影响其余；推送通道失败同理。

---

## ccf — CCF-A 会议 / 期刊监控与推送

按**会议 / 期刊**跟踪 CFP / Program / 接收论文列表。名单是 `ccf.md`（勾选框）。
完整说明见 [CCF 会议期刊监控](ccf-watching.md)。

```powershell
python -X utf8 arxiv_daily.py ccf <action> [options]
```

| action | 说明 | 主要参数 |
|--------|------|---------|
| `list` | 列出勾选状态 | `--all`（含未勾选） `--area <领域>` |
| `enable` / `disable` | 勾选 / 取消勾选 | `<名称>` 或 `--area <领域>`（批量） |
| `add` | 添加目录未覆盖的条目 | `<名称>` `--homepage` `--journal` `--full` `--area` `--dblp` `--issn` `--ccf` |
| `remove` | 移除条目（同时清除其已见状态） | `<名称>` |
| `run` | 扫描并推送新动态 | `--only` `--force` `--no-push` |
| `ack` | 清除 Web 端 CCF 的 NEW 徽标 | — |
| `refresh` | 把内置 CCF-A 目录并入 `ccf.md`（**保留你的勾选**） | `--new-disabled`（新增条目默认不勾选） |

### 示例

```powershell
# 看数据库领域的勾选状态
python -X utf8 arxiv_daily.py ccf list --area DB

# 批量订阅 / 退订整个领域（名单有 90+ 条，批量是刚需）
python -X utf8 arxiv_daily.py ccf disable --area "形式化方法"

# 添加目录未收录的会议（必须给主页 —— 监控的唯一依据）
python -X utf8 arxiv_daily.py ccf add ICDT --homepage https://icdt2027.org/ --area "数据库"

# 扫描（首次建基线不推送；之后只推新 CFP / Program / 接收论文列表）
python -X utf8 arxiv_daily.py ccf run
python -X utf8 arxiv_daily.py ccf run --only SIGMOD
```

### 行为说明

- **解析顺序**：会议 = ccfddl 截稿 RSS → 会议主页；期刊 = Crossref（按 ISSN 取卷期）→ 期刊主页。
- **DBLP 不做抓取**：2026-09 起 DBLP 全部端点都有反爬拦截页，`dblp` 字段仅作人工参考链接。
- **首次建基线**：新条目第一次运行只记录「已见」，**不推送**历史 CFP（除非 `--force`）。
- **勾选即订阅**：`[ ]` 的条目**不会发起任何网络请求**；`refresh` 不会改动你的勾选状态。
- **落盘 HTML 快照**：每次 `run` 都会产出 `exports/ccf-digest-<YYYY-MM-DD>.html`（失败只降级 `[WARN]`）。
  与学者监控同一套页面骨架与「本次运行」证据表，零更新同样出页面。
- **盲区告警**：某会议/期刊本轮**一条内容都没取到**时打印 `[WARN] 盲区：…`，
  HTML 中同样标为「盲区」而非「无更新」。注意 `last_error` 恒为空 —— 引擎不持久化抓取错误，
  **判抓取成败只能看指纹数是否为 0**，不能看这个字段。
- **fail-soft**：单个站点抓取失败只记录 `[WARN]`，不影响其余。

---

## download — 下载 PDF

按 arXiv ID 下载论文 PDF。

```powershell
python -X utf8 arxiv_daily.py download <id> [id ...]
```

### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | str | arXiv ID（如 `2607.25916`），可多个 |

### 示例

```powershell
# 下载单篇
python -X utf8 arxiv_daily.py download 2607.25916

# 下载多篇
python -X utf8 arxiv_daily.py download 2607.25916 2607.25793 2607.25979
```

### 命名规则

PDF 保存到 `$ARXIV_DIR`（默认 `~/papers`，可设同名环境变量覆盖），文件名格式：

```
arXiv<年份> <id><版本> <去标点标题>.pdf
```

示例：`arXiv2026 2607.25916v1 Hermes BFT Consensus with Trusted Components.pdf`

---

## feedback — 反馈打分

人工调整某篇论文的推荐指数，触发画像权重演化。

```powershell
python -X utf8 arxiv_daily.py feedback <id> [--stars N] [--curiosity N]
```

### 参数

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `id` | str | — | arXiv ID |
| `--stars` | int | 0-5 | ★ 推荐指数 |
| `--curiosity` | int | 0-5 | 🧐 好奇指数 |

### 示例

```powershell
# 调整 ★ 推荐指数
python -X utf8 arxiv_daily.py feedback 2607.25916 --stars 3

# 调整 🧐 好奇指数
python -X utf8 arxiv_daily.py feedback 2607.25992 --curiosity 5

# 同时调整两者
python -X utf8 arxiv_daily.py feedback 2607.25916 --stars 4 --curiosity 2
```

### 副作用

执行 `feedback` 会依次完成：

1. **更新 digest 表格**：对应行的 ★/🧐 改为新指数
2. **更新兴趣画像权重**：命中条目按新指数升降权重（≥4 星 +1，≤2 星 -1，范围 1-10）
3. **追加 feedback.jsonl**：记录时间/论文/新指数/命中条目/权重变更

---

## reanchor — 补齐锚点

为指定日期章节补齐摘要锚点与推荐表跳转链接。

```powershell
python -X utf8 arxiv_daily.py reanchor [--date YYYYMMDD]
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--date` | str | 今天 | 指定章节日期 |

### 示例

```powershell
# 补齐今天章节的锚点
python -X utf8 arxiv_daily.py reanchor

# 补齐指定日期
python -X utf8 arxiv_daily.py reanchor --date 20260729
```

### 使用场景

通常在 agent 填写完推荐表格后运行，用于：
- 生成论文摘要锚点 `<a id="YYYYMMDD-<arxiv id>">`
- 在推荐表中添加 `📄` 跳转链接
- 幂等操作，可重复执行

---

## html — 导出独立 HTML 快照

把某天的 digest 渲染成**一个文件**，`file://` 双击即可在浏览器打开，
不需要本地 Web 服务、不需要联网、不依赖任何 CDN。

```powershell
python -X utf8 arxiv_daily.py html [--date YYYYMMDD] [--out 路径]
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--date` | str | 今天 | 要渲染的日期 |
| `--out` | str | `exports/arxiv-digest-<day>.html` | 输出文件路径 |

### 示例

```powershell
# 渲染今天
python -X utf8 arxiv_daily.py html

# 渲染指定日期
python -X utf8 arxiv_daily.py html --date 20260914

# 指定输出位置（比如直接交给别人 / 放进网盘）
python -X utf8 arxiv_daily.py html --date 20260914 --out D:/tmp/digest.html
```

### 行为说明

- **推荐理由来自 digest**：`★ / 🧐` 两节按 `arXiv-schedule.md` 里 agent 写的内容原样呈现；
  只有该节仍是占位符时，才退回「按命中关键词的权重和」自动排序，并在页面上明确标注。
  所以正确顺序是：**先填 md → 再跑 `html`**。
- **自包含**：样式与交互全部内联，无 CDN、无外链脚本；断网与 `file://` 场景下同样可读。
- **无 JS 也能读**：搜索 / 类别筛选 / 只看出命中 / 暗色是渐进增强，全部用原生 JS 实现；
  关掉 JS 后正文、摘要与链接照常显示。
- **不回写画像**：静态快照背后没有服务端，页面上的「复制打分命令」按钮只把等价的
  `feedback` 命令放进剪贴板，真正打分仍走本地 Web 服务或 CLI。
- **派生产物**：`exports/` 不入库，`data/*.json` + `arXiv-schedule.md` 才是事实源。

`fetch` / `daily` 每次运行都会顺带产出这份快照（失败只降级为 `[WARN]`），
填完推荐后再手动跑一次 `html` 即可把人工判断同步进去。

### 三条链路各自的快照

| 链路 | 触发时机 | 产物 | 手动重跑 |
|------|---------|------|---------|
| arXiv 日报 | `fetch` / `daily` | `exports/arxiv-digest-<YYYYMMDD>.html` | `html` |
| 学者监控 | `watch run` | `exports/watch-digest-<YYYY-MM-DD>.html` | `watch run` |
| CCF 监控 | `ccf run` | `exports/ccf-digest-<YYYY-MM-DD>.html` | `ccf run` |

> ⚠️ **日期格式不统一**：arXiv 线用 `YYYYMMDD`（digest 章节的既成格式），
> 两条监控线用 `YYYY-MM-DD`（`run_monitor` 的 `day`）。这是历史原因，拼文件名时以本表为准。

三份快照共用同一套内联样式、暗色开关与前端筛选脚本，都是**自包含单文件**：
无 CDN、无外链脚本，`file://` 双击即开、断网可读、关掉 JS 正文照常显示。
`exports/` 全部不入库。

命令执行时的 `--only` 会写进快照的「扫描范围」，便于事后判断这一页是几点的哪一轮跑出来的。
