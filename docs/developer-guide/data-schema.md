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
  "version": "1",
  "title": "Hermes: BFT Consensus with Trusted Components",
  "authors": ["Alice Smith", "Bob Jones"],
  "abstract": "We present Hermes, a new BFT consensus protocol...",
  "primary": "cs.DC",
  "categories": ["cs.DC", "cs.CR"],
  "published": "2026-07-28T10:00:00Z",
  "abs_url": "https://arxiv.org/abs/2607.25979",
  "pdf_url": "https://arxiv.org/pdf/2607.25979",
  "hits_star": ["分布式计算与共识"],
  "hits_expand": [],
  "score_star": 4,
  "score_expand": 0
}
```

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
## 兴趣点 ★

### <条目标题>
- keywords: <分号分隔的关键词>
- weight: <1-10 的整数>
- 来源: <来源说明或链接>

## 扩展点 🧐

### <条目标题>
- keywords: <分号分隔的关键词>
- weight: <1-10 的整数>
- 来源: <来源说明或链接>
```

### 解析规则

- `## 兴趣点 ★` 和 `## 扩展点 🧐` 为固定小节标题
- 每个条目以 `###` 开头
- `keywords` 行以 `- keywords:` 开头，值用分号分隔
- `weight` 行以 `- weight:` 开头，值为整数，缺省为 3
- `来源` 行以 `- 来源:` 开头，可选

---

## feedback.jsonl

### 格式

每行一个 JSON 对象，append-only。

```json
{
  "time": "2026-07-29T10:30:00",
  "id": "2607.25916",
  "day": "20260729",
  "title": "Hermes: BFT Consensus with Trusted Components",
  "primary": "cs.DC",
  "abstract_head": "We present Hermes...",
  "adjustments": [
    {
      "kind": "stars",
      "rating": 3,
      "delta": -1,
      "matched_entries": ["分布式计算与共识"],
      "digest_updated": true
    }
  ],
  "weight_updates": {
    "分布式计算与共识": {"old": 4, "new": 3}
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
| `abstract_head` | str | 摘要前 100 字符 |
| `adjustments` | [Adjustment] | 调整详情 |
| `weight_updates` | dict | 权重变更记录 |

### Adjustment 对象

| 字段 | 类型 | 说明 |
|------|------|------|
| `kind` | str | `"stars"` 或 `"curiosity"` |
| `rating` | int | 新评分 0-5 |
| `delta` | int | 评分变化量 |
| `matched_entries` | [str] | 命中的兴趣条目 |
| `digest_updated` | bool | digest 是否已更新 |

---

## arXiv-schedule.md

### 格式规范

```markdown
# arXiv Daily Digest

## 20260729

### cs.AI (12 篇, 🎯★ 3 篇, 🎯🧐 1 篇)

| 标题 | 作者 | 类别 | ★ | 🧐 |
|------|------|------|---|---|
| [论文标题](abs_url) | 作者 | cs.AI | ★★★☆☆ | 🧐🧐☆☆☆ |

### 📌 重点关注

| 论文 | 推荐理由 | ★ |
|------|----------|---|
| [论文标题](abs_url) | 命中「分布式计算与共识」(w=4, score=3) + agent 理由... | ★★★★☆ |

### 🧐 视野扩展

| 论文 | 推荐理由 | 🧐 |
|------|----------|---|
| [论文标题](abs_url) | ... | 🧐🧐🧐☆☆ |

<!-- BEGIN 20260729 -->
... 论文详细列表 ...
<!-- END 20260729 -->
```

### 分节标记

- 每个日期章节用 `<!-- BEGIN YYYYMMDD -->` 和 `<!-- END YYYYMMDD -->` 包裹
- 同一天重复 `fetch` 会替换该标记间的内容
- agent 填写的推荐小节位于标记外，不会被覆盖
