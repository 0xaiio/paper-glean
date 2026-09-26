# 定时运行

> 让「三条链路抓取 → 生成 digest 与快照 → 确保本地 Web 服务在线 → 呈递」无人值守地跑起来

Paper-Glean 的定时能力**就在仓库内**，不依赖任何外部脚本：

| 层次 | 载体 | 适用场景 |
|------|------|---------|
| ① 一键命令（日频） | `arxiv_daily.py daily` | 手动跑一次 arXiv 线流水线 |
| ① 一键命令（周频） | `arxiv_daily.py weekly` | 手动跑一次完整周任务（三条链路） |
| ② 平台定时任务 | WorkBuddy 自动化（推荐） | 每周由 agent 抓取、写推荐、呈递页面 |
| ③ Windows 计划任务 | `scripts/register_task.ps1` | 不想开 agent，只要确定性地抓取落盘 |

三层共用同一段实现：`daily` → `glean.cli.cmd_daily`；`weekly` → `glean.cli.cmd_weekly`
（其 arXiv 段复用同一个 `_run_fetch`，因此两个入口永不漂移）；服务保证统一走
`glean.serve.ensure`。无论走哪条路，产出的文件、日志与失败降级行为完全一致。

> **周频请用 `weekly`**：它是三条链路（CCF 监控 / 学者监控 / arXiv 日报）的聚合入口，
> 且 `--hours` 默认 **168**（覆盖整周，不必在 prompt 里重复交代）。
> 细节见 [CLI 参考](cli.md) 的 `weekly` 一节。

---

## 一、`daily` 命令

`daily` = `fetch` + 确保 Web 服务在线。它把原本要分两步做的事合并成一条命令：

```powershell
python -X utf8 arxiv_daily.py daily [--hours N] [--cap N] [--date YYYYMMDD] [--serve] [--host H] [--port P]
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--hours` | int | 24 | 抓取回溯窗口（小时） |
| `--cap` | int | 100 | digest 中每类别最多列出的论文数 |
| `--date` | str | 今天 | 覆盖 digest 章节日期（YYYYMMDD） |
| `--serve` | flag | 关 | 结束后确保本地 Web 服务在线（不在线则后台拉起） |
| `--host` | str | `127.0.0.1` | Web 服务地址 |
| `--port` | int | `8000` | Web 服务端口 |
| `--reload` | flag | 关 | 仅 `serve`：开发模式，代码变更自动重载 |

### 行为

1. **抓取并落盘** — 与 `fetch` 完全共用 `_run_fetch()`，因此两个入口永远不会漂移：
   写 `data/YYYYMMDD.json`、更新 `arXiv-schedule.md` 的当日章节。
2. **提示 agent 补推荐** — 打印 `[NEXT] agent 填写 ★/🧐 推荐小节`。
   ★/🧐 属于语义判断，脚本层不做，留给 agent（即平台定时任务环节）。
3. **确保服务在线**（仅 `--serve`）— 见下节。

### 输出示例

```text
[INFO] interests.md keywords: 12/128 papers hit
[OK] 128 papers -> arXiv-schedule.md section 20260913; data -> ...\data\20260913.json
[NEXT] agent 填写 ★/🧐 推荐小节（见 docs/user-guide/scheduling.md）
[OK] web app already online -> http://127.0.0.1:8000
```

### 失败降级（重要）

`daily` 是**故意 fail-soft** 的：

- digest 与 `data/*.json` 在拉起服务**之前**就已经写好了；
- 若服务拉不起来，只打印 `[WARN]`，**退出码仍为 0**。

这样定时任务不会因为「Web 因端口占用/依赖缺失没起来」而整条报失败——
最坏情况下你仍然有 `arXiv-schedule.md` 可读。

---

## 二、`serve` 命令

`serve` 在前台启动本地 Web 应用，用于手动/开发场景：

```powershell
python -X utf8 arxiv_daily.py serve [--host H] [--port P] [--reload]
```

它与 `python -m glean.web` 等价。区别在于：

| | `daily --serve` | `serve` |
|---|---|---|
| 运行位置 | 后台独立进程（脱离父进程存活） | 前台，Ctrl+C 结束 |
| 是否复用已在线的实例 | 是（先探测 `/api/ping`，在线则不重复启动） | 否，直接占用端口 |
| 日志 | 追加到 `logs/serve-<host>-<port>.log` | 打印到当前终端 |

> **端口说明**：Paper-Glean 默认 `8000`。若与其他项目（例如 arXiv-daily 空间的 `8765`）区分，
> 用 `--port` 指定即可，`serve.ensure()` 的探测与启动会自动跟随该端口。

---

## 三、服务保活机制（`glean/serve.py`）

`daily --serve` 背后是这样一套逻辑：

```text
ensure(host, port)
  ├─ probe()  对 http://<host>:<port>/api/ping 发 GET，200 即视为在线
  │            ├─ 在线  → 复用，返回 (True, started=False)
  │            └─ 不在线 → start_background()
  └─ 轮询 probe()，最多等 15s
```

三个关键设计：

1. **`/api/ping` 是唯一探活口径**。它由 `glean/web/routes.py` 提供，无依赖、无副作用：

   ```json
   {"status": "ok", "service": "paper-glean", "version": "0.1.0", "time": "..."}
   ```

   因此校验服务是否在线，人肉也只是一条 curl（见下）。

2. **探测必须绕过环境代理**。本机注入的 `HTTP_PROXY` 会把回环请求拦成
   `502 CONNECT tunnel failed`。`probe()` 内部用了一个空 `ProxyHandler` 的
   opener，保证 `127.0.0.1` 直连。手动核对时请带 `--noproxy`：

   ```bash
   curl --noproxy '*' http://127.0.0.1:8000/api/ping
   ```

3. **后台进程要活过父进程**。Windows 上用
   `CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS` 启动，
   否则计划任务退出时会连带杀死服务。

---

## 四、方式 A：WorkBuddy 平台定时任务（推荐）

这是能力最完整的方式：agent 除了跑 `daily`，还能**读 `data/*.json` 写 ★/🧐 推荐**，
并在最后用 `present_files` 把页面直接呈递给你。

### 注册

在 Paper-Glean 工作区创建一个**周期性**自动化：

| 字段 | 值 |
|------|-----|
| 工作目录 | `D:\code-repo\paper-glean` |
| 周期 | 每周 · 周五 · 10:00 |
| 名称 | 例：`paper-glean 周报（每周五 10:00 · 日报 + 学者监控 + CCF-A 监控）` |

**一个任务、一条命令。** 三条链路此前是三个独立自动化（各自 `daily` / `watch run` /
`ccf run`，时间错峰），现已在**代码层**收口为 `weekly`，因此调度层只需要一个周任务。

> **端口**：下面示例用 `8011`（`8000` 常被其他常驻程序占用；`ensure()` 会先探测复用）。
> 换端口只影响 `--port` 与 `/api/ping` 的探测地址，其余步骤不变。

### 推荐的任务提示词

> 在 `D:\code-repo\paper-glean` 跑**每周一次**的三链路流水线：
>
> 1. 执行 `python -X utf8 arxiv_daily.py weekly --host 127.0.0.1 --port 8011`
>    —— 一条命令跑完 CCF 监控 → 学者监控 → arXiv 日报 → 确保 Web 服务在线
>    （`--hours 168` / `--cap 300` 已是默认值，**不必**在命令里再交代）。
>    三段各自独立容错，一段失败不影响其余；末段失败不要紧，前三段产物已落盘。
> 2. 阅读 `data/<YYYYMMDD>.json` 与 `interests.md`，在 `arXiv-schedule.md` 的当日章节填写
>    **★ 重点关注** / **🧐 视野扩展** 推荐小节（附理由：命中了哪个条目、权重多少），
>    随后跑一次 `python -X utf8 arxiv_daily.py reanchor` 补锚点与跳转链接。
> 3. 确认服务在线：`curl --noproxy '*' http://127.0.0.1:8011/api/ping` 返回 200。
>    不在线则重跑 `weekly`（它默认就会确保服务在线）；仍失败则提示查看
>    `logs/serve-127.0.0.1-8011.log`。
> 4. **补一次 HTML 快照**：填完推荐后再跑 `python -X utf8 arxiv_daily.py html`
>    （第 1 步的快照是填推荐**之前**的，这一步才把人工判断写进页面）。
> 5. 用 `present_files` 呈递（顺序即优先级）：
>    - `exports/arxiv-digest-<YYYYMMDD>.html`
>    - `exports/watch-digest-<YYYY-MM-DD>.html`
>    - `exports/ccf-digest-<YYYY-MM-DD>.html`
>    - `http://127.0.0.1:8011/`（主界面，同源 `/api/*`，打分/下载/收藏均可用）、
>      `http://127.0.0.1:8011/watch`、`http://127.0.0.1:8011/ccf`
>    - `arXiv-schedule.md`（离线可读备份）、`interests.md`（本次推荐所依据的画像）
> 6. 推飞书（发给用户本人的机器人单聊）：**一条汇总文字 + 每个 HTML 附件各一条**。
>    发送前 `cd` 到仓库根，附件用相对路径（`./exports/...`）。
> 7. 若 arXiv API 被限流（429/503），改跑
>    `python -X utf8 scripts/backfill_rss.py --date <YYYYMMDD> --cap 1000000`。
>    **RSS 一轮只覆盖一个公告批次**，报告里必须写明「本轮仅 RSS 补到最近 1 天」，
>    不要含糊成「本周已全覆盖」。论文不会永久丢：下一轮 168h 窗口的起点正好接上
>    本轮窗口的终点。

> ⚠️ **呈递与附件是两份不同的 HTML，别混**：
>
> | | 来源 | 用途 | 前提 |
> |---|---|---|---|
> | `http://127.0.0.1:8000/` | 本地 Web 服务 | `present_files` 交互呈递 | 服务在线（有 `/api/*`） |
> | `exports/arxiv-digest-<day>.html` | `html` 子命令 | `file://` 打开 / 当附件发出 | 无，完全自包含 |
>
> 把静态快照当呈递主入口是错的（相对 `/api/*` 会打到错误 origin，按钮失效）；
> 反过来把 `127.0.0.1` 地址当附件发给别人也是错的（对方打不开）。
> **两条链路各发各的，不冲突。**

### 三条链路的自动化

三条链路在**代码层**已收口为一条命令（`weekly`），调度层因此只有一个周任务：

| 链路 | `weekly` 中的步骤 | HTML 快照 | 飞书 |
|------|-----------------|----------|------|
| CCF 监控 | 第 1 段 | `exports/ccf-digest-<YYYY-MM-DD>.html` | 摘要 + 附件 |
| 学者监控 | 第 2 段 | `exports/watch-digest-<YYYY-MM-DD>.html` | 摘要 + 附件 |
| arXiv 日报 | 第 3 段 | `exports/arxiv-digest-<YYYYMMDD>.html` | 摘要 + 附件 |

任一段都可用 `--skip-ccf` / `--skip-watch` / `--skip-fetch` 单独跳过，
便于只排查一条链路而不动其余两条。

> **为什么不再是三个错峰任务**：三条链路本就是同一个本地 Web 应用（一个 FastAPI app）
> 的三个页面，此前却要起两个端口（日报一个、监控一个）、写三份 prompt。
> 收口到 `weekly` 后：一个端口、一条命令、一份行为可回归的实现。顺带修掉一个真实的坑
> —— 日频改周频时若沿用 `daily` 的 `--hours 24` 默认值，会静默漏掉一周里 6/7 的论文。

> ⚠️ **日期格式不统一**：arXiv 线是 `YYYYMMDD`，两条监控线是 `YYYY-MM-DD`。
> 在自动化 prompt 里拼附件路径时按本表写，别统一成一种。

> **展示口径：定时任务只产出页面，不弹任何窗口。** 它跑完只做两件事——把结果写进
> `exports/*.html`（自包含、`file://` 双击即开），并保证本地 Web 应用在线
> （`/digest` `/watch` `/ccf`，`NEW` 徽标即未读）。`weekly` 结束时会打印一段
> `[SHOW]` 把这两条入口列出来，照着打开即可；要外部提醒只能走可选的
> `PAPER_GLEAN_WEBHOOK_URL`（早期那个 PowerShell 系统气泡通道已移除）。

> **监控两条线要盯「盲区」**：`watch run` / `ccf run` 都是 fail-soft，
> 源不可达时会静默返回 0 条，与控制台打印的「没有新作 / 没有更新」长得一模一样。
> 所以定时任务的 prompt 里必须要求 agent 转述 `[WARN] 盲区：…` 与 HTML 证据表的
> 「各源取回条数」，**不能只报一句「今天没有新内容」**。

### 手动触发验证

注册后先手动跑一次，确认：

```powershell
python -X utf8 arxiv_daily.py weekly --port 8011
curl --noproxy '*' http://127.0.0.1:8011/api/ping
```

`weekly` 末尾会打印一份汇总：每段的新增条数、源级告警数、完成段数；紧接着是 `[SHOW]`
段（在线页面地址 + 离线快照目录）。
**退出码只在三段全部失败时非 0** —— 所以「退出码 0」不等于「三段都拿到了新内容」，
要读汇总里的 `[WARN] … 处源级告警` 与各段打印的 `[WARN] 盲区：…`。

---

## 五、方式 B：Windows 计划任务（schtasks）

不想依赖 agent、只要确定性抓取时使用。仓库已备好两个 ASCII-only 脚本
（**故意不写中文**，避免 PowerShell 代码页把路径/参数写坏）。

### 注册

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\register_task.ps1
```

默认行为：创建计划任务 `PaperGleanDaily`，**周一至周六 11:30**，
执行 `scripts\run_daily.ps1`。

> 这条路径走的是 `daily`（**日频、只含 arXiv 线**），与 `weekly` 的三链路周任务定位不同。
> 需要周频三链路时请用方式 A，或手动跑 `weekly`；只想改本节的频率与时刻，
> 用 `-Time` / `-Days` 即可。

| 参数 | 默认 | 说明 |
|------|------|------|
| `-TaskName` | `PaperGleanDaily` | 计划任务名 |
| `-Time` | `11:30` | 触发时间 |
| `-Days` | `MON,TUE,WED,THU,FRI,SAT` | 触发日 |
| `-RunNow` | — | 注册后立即运行一次 |
| `-Remove` | — | 删除该计划任务 |

```powershell
# 改时间
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\register_task.ps1 -Time 09:00
# 立即验证一次
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\register_task.ps1 -RunNow
# 卸载
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\register_task.ps1 -Remove
```

### `scripts/run_daily.ps1`

任务体。它 `cd` 到仓库根目录后调用 `daily`：

```powershell
param([int]$Hours=24, [int]$Cap=100, [string]$Date="",
      [string]$BindHost="127.0.0.1", [int]$Port=8000, [switch]$NoServe)
```

- 默认带 `--serve`（拉起/复用本地服务）；加 `-NoServe` 只抓取。
- 用环境变量 `PAPER_GLEAN_PYTHON` 可指定解释器（默认 `python`）。
- 以流水线退出码退出，便于在「任务计划程序」里判定成败。

### 查询与排错

```powershell
schtasks /Query /TN PaperGleanDaily /V /FO LIST
schtasks /Run   /TN PaperGleanDaily
```

> 计划任务方式**不会**替你写 ★/🧐 推荐（那是 agent 的语义工作）。
> digest 章节里会是占位符，你仍可手动或用 agent 后续补齐。

---

## 六、环境变量

| 变量 | 默认 | 作用 |
|------|------|------|
| `HOST` | `127.0.0.1` | Web 绑定地址 |
| `PORT` | `8000` | Web 绑定端口 |
| `ARXIV_DIR` | `~/papers` | PDF 下载目录 |
| `PAPER_GLEAN_PYTHON` | `python` | 仅 `run_daily.ps1`：指定解释器路径 |

---

## 七、故障排查

| 症状 | 原因 | 处理 |
|------|------|------|
| `probe` 永远 False，但浏览器能打开 | 环境 `HTTP_PROXY` 把回环请求拦成 502 | 探测一律带 `--noproxy '*'`；`serve.probe()` 已内置绕过 |
| 服务起来了，任务一结束就没了 | 父进程退出连带杀死子进程 | 已用 `DETACHED_PROCESS` 规避；自定义启动请自行 detach |
| 端口被占用，服务反复起不来 | 已有实例占着 8000 | `ensure()` 会先探测复用；确认是否另有进程 |
| `[WARN] web app 未在 ... 上线` | 依赖缺失或启动报错 | 看 `logs/serve-127.0.0.1-8000.log`；确认 `pip install -e ".[web]"` |
| 计划任务中文路径乱码 | PowerShell 代码页 | 仓库脚本已 ASCII-only；不要往其中写中文 |

---

## 下一步

- CLI 全量命令：[CLI 参考](cli.md)
- Web 界面操作：[Web 应用](web-app.md)
- 服务端接口细节：[API 参考](../developer-guide/api-reference.md)
