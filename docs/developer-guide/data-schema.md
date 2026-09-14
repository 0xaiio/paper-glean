# 数据文件格式规范

> 所有数据文件的精确 schema

## 数据文件概览

| 文件 | 格式 | 用途 | 读写方式 |
|------|------|------|----------|
| `data/YYYYMMDD.json` | JSON | 每日论文原始数据 | 读写 |
| `interests.md` | Markdown | 兴趣画像 | 读写 |
| `feedback.jsonl` | JSON Lines | 反馈审计日志 | 追加 |
| `arXiv-schedule.md` | Markdown | 人读 digest | 读写 |

---

## data/YYYYMMDD.json

> **文件命名即契约**：只有文件名 stem 恰为 8 位数字（`YYYYMMDD`）的 JSON 才算「一天」。
> `data/` 同时存放监控状态文件（`watch_state.json` / `ccf_state.json` / `watch_new.json`），
> 因此**枚举日期必须按此规则过滤**——`core.day_files()` 是唯一入口，
> `list_available_days()` 与 `find_paper()` 都走它。
> 早期实现用 `data/*.json` 通配，会把状态文件当成日期，导致 Web 首页默认落在「0 篇」的假日期上。

### 顶层结构

```json
{
  "day": "20260729",
  "window_utc": ["2026-07-28T00:00:00Z", "2026-07-29T00:00:00Z"],
  "papers": [...]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `day` | str | 日期，YYYYMMDD 格式 |
| `window_utc` | [str, str] | 抓取时间窗口 [开始, 结束]，ISO 8601 UTC |
| `papers` | [Paper] | 论文列表 |

### Paper 对象

```json
{
  "id": "2607.25979",
  "version": "v1",
  "title": "Hermes: BFT Consensus with Trusted Components",
  "authors": ["Alice Smith", "Bob Jones"],
  "abstract": "We present Hermes, a new BFT consensus protocol...",
  "primary": "cs.DC",
  "categories": ["cs.DC", "cs.CR"],
  "published": "2026-07-28T10:00:00Z",
  "abs_url": "https://arxiv.org/abs/2607.25979",
  "pdf_url": "https://arxiv.org/pdf/2607.25979",
  "hits_star": ["consensus", "BFT"],
  "hits_expand": [],
  "score_star": 4,
  "score_expand": 0
}
```

> **口径说明**：`hits_*` 存的是**命中的关键词**（来自 `interests.md` 条目的 `keywords:` 行），
> 不是条目标题；`score_*` 才是**命中条目权重之和**（同一关键词命中多条时按条目各计一次权重）。
> `version` 形如 `v1`（含 `v` 前缀）。

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | str | 是 | arXiv ID |
| `version` | str | 是 | 版本号 |
| `title` | str | 是 | 论文标题 |
| `authors` | [str] | 是 | 作者列表 |
| `abstract` | str | 是 | 摘要 |
| `primary` | str | 是 | 主类别 |
| `categories` | [str] | 是 | 所有类别 |
| `published` | str | 是 | 发布时间，ISO 8601 |
| `abs_url` | str | 是 | 摘要页 URL |
| `pdf_url` | str | 是 | PDF URL |
| `hits_star` | [str] | 否 | 命中的**关键词**（`interests.md` 条目的 `keywords:` 值），不是条目标题 |
| `hits_expand` | [str] | 否 | 同上，扩展点一侧 |
| `score_star` | int | 否 | 命中的兴趣点条目权重之和 |
| `score_expand` | int | 否 | 命中的扩展点条目权重之和 |

> 消费者若要显示「命中了哪**个条目**」，必须用 `interest.keywords` 与 `hits_*` 求交集，
> 而不是拿 `interest.title` 去 `in hits_*`（`partials/paper_card.html` 曾因此永不渲染）。

!!! note "兼容性说明"
    早期数据文件（如 `20260729.json`）可能不含 `hits_*` 和 `score_*` 字段，解析时必须容错。

---

## interests.md

### 格式规范

```markdown
## 兴趣点（★ 重点关注推荐依据）

### <条目标题>
- keywords: <分号分隔的关键词>
- weight: <1-10 的整数>
- 来源: <来源说明或链接>

## 扩展点（🧐 视野扩展推荐依据）

### <条目标题>
- keywords: <分号分隔的关键词>
- weight: <1-10 的整数>
- 来源: <来源说明或链接>
```

### 解析规则

- 小节归属由 `##` 行**按子串判定**：含「兴趣点」→ `star`，含「扩展点」→ `expand`；
  故 `## 兴趣点（★ 重点关注推荐依据）`、`## 兴趣点 ★` 等写法均被识别。
- 每个条目以 `###` 开头
- `keywords` 行以 `- keywords:` 开头，值用**英文分号 `;`** 分隔
- `weight` 行以 `- weight:` 开头，值为整数，缺省为 3，解析时钳制在 [1, 10]
- `来源` 行以 `- 来源:` 开头，可选（`load_interest_entries` 不解析该行）

---

## feedback.jsonl

### 格式

每行一个 JSON 对象，append-only。

```json
{
  "time": "2026-07-29T10:30:00+00:00",
  "id": "2607.25916",
  "day": "20260729",
  "title": "Hermes: BFT Consensus with Trusted Components",
  "primary": "cs.DC",
  "abstract_head": "We present Hermes...",
  "adjustments": [
    {
      "kind": "star",
      "rating": 3,
      "delta": -1,
      "matched_entries": ["分布式计算与共识"],
      "digest_updated": true
    }
  ],
  "weight_updates": {
    "分布式计算与共识": 3
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `time` | str | 反馈时间，ISO 8601 |
| `id` | str | arXiv ID |
| `day` | str | 所属 digest 日期 |
| `title` | str | 论文标题 |
| `primary` | str | 主类别 |
| `abstract_head` | str | 摘要前两句（`excerpt(abstract, 200)`，约 200 字符） |
| `adjustments` | [Adjustment] | 调整详情 |
| `weight_updates` | dict | 权重变更记录：`{条目标题: 新权重(int)}`（**不是** `{old, new}` 结构） |

### Adjustment 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| `kind` | str | `"star"`（兴趣点）或 `"expand"`（扩展点） |
| `rating` | int | 新评分 0-5 |
| `delta` | int | 权重增减量：≥4 星 → `+1`，≤2 星 → `-1`，否则 `0` |
| `matched_entries` | [str] | 命中的兴趣条目**标题** |
| `digest_updated` | bool | digest 推荐表是否已更新 |

---

## arXiv-schedule.md

### 格式规范

每个日期一个章节，由 `<!-- BEGIN YYYYMMDD -->` / `<!-- END YYYYMMDD -->` 包裹，
结构固定为「头部 → 两个推荐表 → 分类清单」：

```markdown
<!-- BEGIN 20260729 -->
## 20260729

时间窗口(UTC): 2026-07-28 10:31 → 2026-07-29 10:31 | 去重后共 **128** 篇 | 🎯 关键词命中(interests.md): ★ 5 篇 / 🧐 5 篇

### 📌 重点关注(基于研究兴趣, agent 填写)

| 推荐 | 论文 | 理由 |
|------|------|------|
| ★★★★★ | **Hermes: Low Tail-Latency Via Prefix Consensus** — [2607.25916](https://arxiv.org/abs/2607.25916) · [📄](#20260729-2607.25916) (cs.DC) | 直击共识/BFT 核心兴趣… |

### 🧐 视野扩展(agent 填写)

| 推荐 | 论文 | 理由 |
|------|------|------|
| 🧐🧐🧐🧐🧐 | **MemLens: …** — [2607.25992](https://arxiv.org/abs/2607.25992) · [📄](#20260729-2607.25992) (cs.DB) | 数据库社区切入 LLM agent 的绝佳样本… |

### 分类清单

#### cs.DC (3)

- <a id="20260729-2607.25916"></a>**Hermes: Low Tail-Latency Via Prefix Consensus** — [2607.25916](https://arxiv.org/abs/2607.25916) | cross: cs.CR | 🎯★ consensus, BFT  
  Alejandro Ranchal-Pedrosa, Dakai Kang, Neil Giridharan, Dahlia Malkhi et al.  
  Leader-based BFT protocols finalize through their leaders: …
<!-- END 20260729 -->
```

### 生成规则

- 章节内容由 `core.day_section()` 生成：头部（时间窗 + 去重篇数 + 命中统计）→
  `### 📌 重点关注` → `### 🧐 视野扩展` → `### 分类清单`。
- **分类清单是 bullet 列表**（不是表格）：每个类别一个 `#### cs.XX (n)` 小节，
  条目按 `score_star + score_expand` 降序，超出 `--cap` 的部分折叠为一行
  `_…另有 N 篇, 见 data/YYYYMMDD.json_`（**不是**「每类别一张表格」）。
- 每条 bullet 形如 `- <a id="{day}-{id}"></a>**标题** — [id](abs_url) | cross: … | 🎯★ kw1, kw2`，
  其后两行缩进依次为「作者（≤4 人 + et al.）」「摘要前两句」。

### 覆盖规则（幂等 + agent 内容保留）

- `upsert_digest()` 只替换该日期 `BEGIN/END` 标记**之间**的内容。
- agent 填写的推荐表**位于标记之内**；脚本生成的推荐表是占位符
  （`_待 agent 分析填写_`）。重复 `fetch` 时，脚本检测到旧推荐块非占位符，
  会**将 agent 已填写内容原样回填**，因此不会被覆盖。
- `reanchor` 为分类清单补齐 `<a id=…>` 锚点、为推荐表补 `· [📄](#…)` 跳转链接。

---

## 监控线数据文件（watch / ccf）

`daily` 之外的监控线（学者 `watch`、会议期刊 `ccf`）共用一套同名结构，仅前缀不同。
「新」的定义 = 指纹**首次出现**：`*_state.json` 存所有已见指纹，`*_new.json` 存未读。
两条线的未读集合**互相隔离**，`ack` 一条线不会清空另一条。

### 概览

| 文件 | 格式 | 用途 | 读写方式 |
|------|------|------|----------|
| `watchlist.md` / `ccf.md` | Markdown | 监控名单（勾选/启停即订阅） | 读写 |
| `data/watch_state.json` / `data/ccf_state.json` | JSON | 已见指纹（决定「新」） | 读写 |
| `data/watch_new.json` / `data/ccf_new.json` | JSON | 未读新条目（Web NEW 徽标数据源） | 读写 |
| `data/watch_events.jsonl` / `data/ccf_events.jsonl` | JSON Lines | 推送事件审计，append-only | 追加 |
| `WATCH-digest.md` / `CCF-digest.md` | Markdown | 人读沉淀（按日章节） | 读写 |

### `ccf.md` 勾选清单格式

```markdown
# CCF-A 会议 / 期刊监控名单

## 会议

- [x] **SIGMOD** — ACM SIGMOD Conference
  - area: 数据库/数据挖掘/内容检索
  - homepage: https://sigmod.org
  - ccf: A

## 期刊

- [x] **TODS** — ACM Transactions on Database Systems
  - area: 数据库/数据挖掘/内容检索
  - homepage: https://dl.acm.org/journal/tods
  - issn: 0362-5915
  - ccf: A
```

### 解析规则（`ccf.py::_parse_ccf_md`）

- `##` 行按子串判定分节：含「期刊」→ `journal`，否则 `conference`。
- 条目行 `- [x] 名称 — 全称`：`[x]` = 勾选（监控），`[ ]` = 取消（不发起网络请求）；
  `—` 或 ` - ` 之后为全称，缺省时用名称兜底。
- **字段行必须缩进**（`raw[:1]` 为空格/制表符），形如 `  - field: value`；
  仅识别 `area` / `homepage` / `dblp` / `ccf` / `full` / `name` / `issn` 七个字段。
  写回时由 `_write_ccf_md` 统一渲染为「2 空格缩进」。
- `homepage` 是唯一硬性必填字段（无主页无从扫描）；`add_venue` 会 strip 后校验，
  纯空白等同于缺失 → 抛 `ValueError`（Web 层映射为 409）。

> `watchlist.md` 结构同构（分「监控中 / 已暂停」两节），见
> [学者监控与推送](../user-guide/watching.md)。

### `data/ccf_state.json`（学者版同构）

```json
{
  "version": 1,
  "venues": {
    "sigmod": {
      "fingerprints": ["cfp|sigmod 2027|https://...", "papers|accepted papers|https://..."],
      "sources": ["ccfddl", "homepage"],
      "last_checked": "2026-09-14T02:11:05+00:00"
    }
  }
}
```

- `venues.<key>.fingerprints`：该 venue 已见条目的指纹全集（`fingerprint(title, url)`），
  仅保留最近 `CCF_MAX_ITEMS`（200）条。
- `sources`：该 venue 曾命中的来源（`ccfddl` / `homepage` / `crossref`）。
- 首次运行某 venue 只**建基线**（写入全部指纹、不推送）；
  可用 `ccf run --force` 覆盖为「首次即推」。
- 删除该文件里的某个 key = 让该条目下次重新建基线（用于主页改版后误报清屏）。

### `data/ccf_new.json`（未读）

```json
{
  "updated": "2026-09-14T02:11:05+00:00",
  "day": "20260914",
  "items": [
    {
      "title": "SIGMOD 2027 CFP",
      "url": "https://sigmod.org/2027/",
      "kind": "cfp",
      "venue": "SIGMOD",
      "source": "ccfddl",
      "confidence": 0.95,
      "deadline": "2026-10-15",
      "fingerprint": "cfp|sigmod 2027 cfp|https://sigmod.org/2027/"
    }
  ]
}
```

- `load_new(namespace)` / `ack_all(namespace)` 读写此文件（`namespace` ∈ `watch` / `ccf`）；
  传未知命名空间会被拒绝。写文件时按 `(fingerprint, key)` 去重。
- `kind` ∈ `cfp` / `program` / `papers` / `other`（图标 📢 / 📅 / 📄 / 🔗）。
- `venue` 为 venue 名（学者线同位置字段为 `researcher`）。

### `data/ccf_events.jsonl`（事件审计）

每行一个 JSON 对象，append-only，每条未见过条目**只记一次**：

```json
{"time": "2026-09-14T02:11:05+00:00", "run_id": "20260914T021105Z", "key": "sigmod", "venue": "SIGMOD", "item": {"title": "SIGMOD 2027 CFP", "kind": "cfp", "url": "https://sigmod.org/2027/", "source": "ccfddl", "fingerprint": "cfp|..."}, "pushed_to": ["file", "desktop"]}
```

- `run_id` 形如 `YYYYMMDDTHHMMSSZ`（UTC）；`item` 为去掉 `key`/`venue` 后的原始条目；
  `pushed_to` 列出实际生效的推送通道。

> `ccf_events.jsonl` 与 `watch_events.jsonl` 均在 `.gitignore` 中（本地审计，不入库）。

### `CCF-digest.md`（人读沉淀）

每次 `ccf run` 只追加**新发现**，每个日期一个章节，由
`<!-- BEGIN CCF YYYYMMDD -->` / `<!-- END CCF YYYYMMDD -->` 包裹；
`upsert_ccf_digest` 幂等（重复运行同一日不产生差异）。学者线用
`<!-- BEGIN WATCH YYYYMMDD -->` 标记，结构同构。
