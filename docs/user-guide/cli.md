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
| `download` | 按 ID 下载 PDF |
| `feedback` | 人工调整推荐指数 |
| `reanchor` | 补齐 digest 锚点与跳转链接 |

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
| `--cap` | int | 30 | 每类别列表上限 |

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
- **fail-soft**：单个对象抓取失败只记录 `[WARN]`，不影响其余；推送通道失败同理。

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
