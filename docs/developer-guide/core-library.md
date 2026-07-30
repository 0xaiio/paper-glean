# 核心库详解

> `glean/core.py` — 共享业务逻辑模块

## 模块职责

`glean/core.py` 包含所有纯业务逻辑函数，被 CLI (`glean/cli.py`) 和 Web (`glean/web/routes.py`) 共同调用。

## 主要函数

### 数据抓取

#### `fetch_category(category, start, end, cap=30)`

抓取指定 arXiv 类别在时间段内的论文。

**参数**：
- `category` (str): arXiv 类别代码（如 `cs.AI`）
- `start` (datetime): 开始时间
- `end` (datetime): 结束时间
- `cap` (int): 每类别上限，默认 30

**返回**：论文列表，每篇为 dict 包含 `id`, `title`, `authors`, `abstract`, `primary`, `categories`, `published`, `abs_url`, `pdf_url`

**副作用**：无（纯函数）

---

#### `fetch_all(hours=24, cap=30)`

抓取所有配置的类别，自动去重。

**参数**：
- `hours` (int): 回溯时间窗口，默认 24
- `cap` (int): 每类别上限，默认 30

**返回**：`(day_str, papers)` 元组
- `day_str`: YYYYMMDD 格式日期
- `papers`: 去重后的论文列表

**副作用**：
- 写入 `data/YYYYMMDD.json`
- 更新 `arXiv-schedule.md`

---

### 兴趣画像

#### `load_interest_entries()`

解析 `interests.md`，返回兴趣条目列表。

**返回**：`[{"title": str, "keywords": [str], "weight": int, "source": str, "kind": "star"|"expand"}, ...]`

---

#### `match_keywords(text, entries)`

对文本做关键词匹配。

**参数**：
- `text` (str): 待匹配的文本（标题+摘要）
- `entries`: 兴趣条目列表

**返回**：`{"star": [(entry_title, keyword)], "expand": [(entry_title, keyword)]}`

**匹配规则**：
- 大小写不敏感
- 容忍复数形式
- 整词匹配（避免子串误匹配）

---

### 反馈处理

#### `apply_feedback(paper, day, stars=None, curiosity=None)`

应用用户反馈，更新画像权重和 digest。

**参数**：
- `paper` (dict): 论文信息
- `day` (str): YYYYMMDD 日期
- `stars` (int|None): ★ 评分 0-5
- `curiosity` (int|None): 🧐 评分 0-5

**返回**：反馈记录 dict

**副作用**：
1. 更新 `interests.md` 权重
2. 追加 `feedback.jsonl`
3. 更新 `arXiv-schedule.md` 表格

---

### 数据持久化

#### `save_day_data(day, papers)`

保存当天论文数据到 JSON。

**副作用**：原子写入 `data/YYYYMMDD.json`

---

#### `upsert_digest(day, papers, anchor=True)`

更新 digest Markdown 文件。

**副作用**：
- 创建/更新 `arXiv-schedule.md` 中对应日期章节
- 使用 `<!-- BEGIN YYYYMMDD --> ... <!-- END YYYYMMDD -->` 标记分节

---

### PDF 下载

#### `download_pdf(paper_id, dest_dir=None)`

下载指定论文的 PDF。

**参数**：
- `paper_id` (str): arXiv ID（如 `2607.25916`）
- `dest_dir` (str|None): 目标目录，默认 `arXiv/`

**返回**：下载的文件路径

**命名规则**：
```
arXiv<年份> <id><版本> <去标点标题>.pdf
```

**安全措施**：
- 下载前校验 `%PDF` 魔数
- 下载间隔 3 秒（API 礼仪）

---

## 数据流详情

![反馈闭环图](../assets/images/feedback-loop.png)

> 图源文件：[feedback-loop.puml](../assets/diagrams/feedback-loop.puml)
