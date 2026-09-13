# 反馈与权重演化

> 人工调整 → 画像演化 → 更精准的推荐

## 反馈机制概述

Paper-Glean 的核心特色之一是**反馈闭环**：用户对推荐结果打分后，系统自动调整兴趣画像权重，从而影响后续推荐。

```
用户打分 → 更新权重 → 次日 fetch 生效 → 更精准的排序与推荐
```

## 如何反馈

### CLI 方式

```powershell
# 调整 ★ 推荐指数（0-5）
python -X utf8 arxiv_daily.py feedback 2607.25916 --stars 3

# 调整 🧐 好奇指数（0-5）
python -X utf8 arxiv_daily.py feedback 2607.25992 --curiosity 5
```

### Web 方式

在 Web 界面的 Digest 流页面：
1. 选中论文卡片（鼠标点击或 `j`/`k` 导航）
2. 按 `1-5` 打 ★ 分，或 `Shift+1-5` 打 🧐 分
3. 打分即时生效，无确认弹窗

### Agent 方式

直接对 Quest 说：

> "把 Hermes 那篇调成三星"
> "MemLens 升为五个 🧐"

## 反馈的副作用

每次反馈会依次完成三件事：

### 1. 更新 Digest 表格

将 `arXiv-schedule.md` 中对应论文的 ★/🧐 改为新指数。

### 2. 更新兴趣画像权重

论文命中的 `interests.md` 条目按新指数调整权重：

| 新评分 | 权重变化 | 说明 |
|--------|----------|------|
| 5 星 | +1 | 强烈推荐该方向 |
| 4 星 | +1 | 推荐该方向 |
| 3 星 | 0 | 中性，不变 |
| 2 星 | -1 | 不太感兴趣 |
| 1 星 | -1 | 明确不感兴趣 |
| 0 星 | -1 | 完全无关 |

权重范围 1-10，超出时截断。

### 3. 追加 Feedback 日志

在 `feedback.jsonl` 中追加一条审计记录：

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

> 字段口径：`kind` 为 `star` / `expand`；`weight_updates` 为 `{条目标题: 新权重(int)}`。
> 完整 schema 见 [数据规范](../developer-guide/data-schema.md)。

## 权重演化时间线

`feedback.jsonl` 是 append-only 的日志文件，完整记录了画像的演化历史：

- 可回放：查看某个条目权重随时间的变化
- 可审计：每次调整都有时间戳和上下文
- 可恢复：基于日志可重建任意时刻的画像状态

## 高分未命中提示

如果某篇论文被打高分（≥4 星）但未命中任何兴趣条目，系统会提示：

```
HINT: 该论文未命中任何兴趣条目，建议从该论文提炼新条目
```

此时可：
1. 让 agent 阅读该论文，提炼关键词
2. 手动在 `interests.md` 中添加新条目
3. 忽略提示（如果是一次性兴趣）

## 反馈的最佳实践

1. **及时打分**：读完摘要后立即打分，记忆最准确
2. **敢于打低分**：1-2 星同样重要，帮助系统排除不相关方向
3. **关注权重演化**：定期查看 `interests.md`，了解哪些方向在升温/降温
4. **利用 Web 界面**：键盘流打分比 CLI 更高效
