# 定时运行

> 让「抓取 → 生成 digest → 确保本地 Web 服务在线 → 呈递」无人值守地跑起来

Paper-Glean 的定时能力**就在仓库内**，不依赖任何外部脚本：

| 层次 | 载体 | 适用场景 |
|------|------|---------|
| ① 一键命令 | `arxiv_daily.py daily` | 手动跑一次完整流水线 |
| ② 平台定时任务 | WorkBuddy 自动化（推荐） | 每天由 agent 抓取、写推荐、呈递页面 |
| ③ Windows 计划任务 | `scripts/register_task.ps1` | 不想开 agent，只要确定性地抓取落盘 |

三层共用同一段实现：命令层的 `daily` → `glean.cli.cmd_daily` → `glean.serve.ensure`。
无论走哪条路，产出的文件、日志与失败降级行为完全一致。

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
| 周期 | 每周 · 周一、二、三、四、五、六 · 11:30 |
| 名称 | 例：`paper-glean 论文日报（周一至周六 11:30）` |

### 推荐的任务提示词

> 在 `D:\code-repo\paper-glean` 跑当日流水线：
>
> 1. `cd` 到该目录，执行 `python -X utf8 arxiv_daily.py daily --serve --host 127.0.0.1 --port 8000`
>    （抓取 → 更新 `arXiv-schedule.md` → 确保本地 Web 服务在线）。
> 2. 阅读 `data/<YYYYMMDD>.json` 与 `interests.md`，在 `arXiv-schedule.md` 的当日章节填写
>    **★ 重点关注** / **🧐 视野扩展** 推荐小节（附理由：命中了哪个条目、权重多少），
>    随后跑一次 `python -X utf8 arxiv_daily.py reanchor` 补锚点与跳转链接。
> 3. 确认服务在线：`curl --noproxy '*' http://127.0.0.1:8000/api/ping` 返回 200。
>    不在线则重跑第 1 步的 `--serve`；仍失败则提示查看 `logs/serve-127.0.0.1-8000.log`。
> 4. 用 `present_files` 呈递（顺序即优先级）：
>    - `http://127.0.0.1:8000/`（主界面，同源 `/api/*`，打分/下载/收藏均可用）
>    - `arXiv-schedule.md`（离线可读备份）
>    - `interests.md`（本次推荐所依据的画像）
> 5. 若 arXiv API 拉取失败或网络不通，保留**上一期** `arXiv-schedule.md` 内容即可，
>    不要向用户报错刷屏。

> ⚠️ **不要把 HTML 当本地静态文件呈递**——相对 `/api/*` 会打到错误 origin，
> 打分/下载按钮会失效。主入口必须是 `http://127.0.0.1:8000/`。

### 手动触发验证

注册后先手动跑一次，确认：

```powershell
python -X utf8 arxiv_daily.py daily --serve
curl --noproxy '*' http://127.0.0.1:8000/api/ping
```

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
