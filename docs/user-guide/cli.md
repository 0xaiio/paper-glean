# CLI 参考

> 命令行接口完整手册

## 命令概览

```powershell
arxiv-daily <command> [options]
```

| 命令 | 说明 |
|------|------|
| `fetch` | 抓取 arXiv 论文并生成 digest |
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
