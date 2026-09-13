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
| `hits_star` | [str] | 否 | 命中的兴趣点条目名 |
| `hits_expand` | [str] | 否 | 命中的扩展点条目名 |
| `score_star` | int | 否 | 兴趣点权重和 |
| `score_expand` | int | 否 | 扩展点权重和 |

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
