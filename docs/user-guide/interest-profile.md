# 兴趣画像管理

> 研究兴趣的集中维护与演化

## 什么是兴趣画像

兴趣画像是 Paper-Glean 的推荐依据，集中维护在 `interests.md` 文件中。分为两个小节：

- **兴趣点 ★**：与当前研究直接相关的方向（产生 ★ 推荐候选）
- **扩展点 🧐**：值得关注的延伸领域（产生 🧐 推荐候选）

## 文件格式

```markdown
## 兴趣点 ★

### 分布式计算与共识
- keywords: consensus; BFT; Paxos; Raft; distributed systems
- weight: 4
- 来源: hengxin.github.io

### 形式化验证
- keywords: TLA+; model checking; verification; Coq
- weight: 3
- 来源: Lamport 主页

## 扩展点 🧐

### 机器学习系统
- keywords: ML systems; training infrastructure; distributed ML
- weight: 2
- 来源: arxiv.org/abs/2607.25916
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `###` 标题 | 是 | 条目主题名称 |
| `keywords` | 是 | 分号分隔的关键词列表 |
| `weight` | 否 | 权重 1-10，默认 3 |
| `来源` | 否 | 该兴趣点的来源链接/说明 |

## 如何添加兴趣点

### 方式一：直接编辑文件

直接编辑 `interests.md`，按上述格式添加新条目。

### 方式二：通过 Agent

对 Qoder Quest 说：

> "把 https://example.edu/~alice 加入兴趣点"

Agent 会：
1. 抓取主页内容
2. 提炼研究方向与关键词
3. 生成新条目追加到 `interests.md`

### 支持的材料形式

| 材料 | 示例说法 | 处理方式 |
|------|----------|----------|
| 研究人员主页 | "把 https://example.edu/~alice 加入兴趣点" | 抓取主页，提炼研究方向 |
| 论文（PDF） | 上传文件 + "据此增加一个扩展点" | 阅读论文，提取关键词 |
| 论文链接 | "关注 arxiv.org/abs/2607.25916" | 抓取摘要页 |
| GitHub 仓库 | "把 github.com/tlaplus/tlaplus 加入兴趣点" | 读 README/topics |

## 权重机制

### 初始权重

- 手动添加的条目默认权重为 3
- 可在 `interests.md` 中直接修改 `weight` 值（1-10）

### 权重演化

权重通过 `feedback` 命令自动调整：

| 评分 | 权重变化 | 说明 |
|------|----------|------|
| ≥ 4 星 | +1 | 高兴趣，提升该方向权重 |
| ≤ 2 星 | -1 | 低兴趣，降低该方向权重 |
| 3 星 | 0 | 中性，权重不变 |

权重范围：1-10。超出范围时截断。

### 权重如何影响推荐

1. **排序**：`fetch` 时分类清单内按命中条目权重和降序排列
2. **候选**：高权重主题的论文更易入选 ★/🧐 推荐表
3. **星级**：agent 推荐时以权重为优先级先验

## 关键词建议

- **宜精准**：如 `BFT consensus` 而非 `distributed systems`
- **避免过泛**：如 `learning` 会导致 🎯 标记刷屏
- **使用分号分隔**：`keywords: consensus; BFT; Paxos`
- **容忍复数**：系统会自动处理单复数匹配
