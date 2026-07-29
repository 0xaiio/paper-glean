# 研究兴趣画像（arXiv 推荐依据）

> 本文件是每日 ★（重点关注）/ 🧐（视野扩展）推荐的**依据**，可随时增删条目。
>
> **如何增加兴趣点/扩展点**：告诉 agent 并提供以下任一材料，agent 解析后追加条目到相应小节：
> - 研究人员主页（如 `https://hengxin.github.io`）
> - 相关论文（上传 PDF 或给出可访问链接，如 arXiv/DOI 链接）
> - GitHub 仓库链接
> - 其它相关链接（会议主页、课程页面、博客等）
>
> **格式约定**（agent 与脚本共同遵守）：
> - 每个条目为一个 `###` 小节，含一行 `- keywords: ...`（英文关键词，分号分隔）。
> - `keywords:` 行会被 `arxiv_daily.py fetch` 用于对新增论文做 🎯 命中标记，请保持精准、避免过泛的词（如 "learning"）。
> - `- weight: N`（1-10，缺省 3）表示该条目当前权重：影响 digest 分类清单内排序与 agent 推荐优先级；
>   由 `arxiv_daily.py feedback` 根据人工调整的推荐指数自动升降（≥4 星 +1，≤2 星 -1），也可手工修改。
> - `- 来源:` 记录材料出处与加入日期，便于追溯与清理。

## 兴趣点（★ 重点关注推荐依据）

### 事务隔离与数据库一致性检测
- keywords: transaction isolation; serializability; snapshot isolation; isolation level; consistency checking; database testing; concurrency control
- weight: 3
- 来源: https://hengxin.github.io（2026-07-29，初始画像）

### 分布式计算与共识
- keywords: consensus; BFT; Byzantine; state machine replication; Paxos; Raft; CRDT; linearizability; eventual consistency; distributed transaction; replication protocol
- weight: 3
- 来源: https://hengxin.github.io（2026-07-29，初始画像）

### 形式化方法与验证
- keywords: TLA+; model checking; model checker; theorem proving; theorem prover; formal verification; formally verified; proof assistant; invariant inference; refinement mapping; SMT solver; SAT solver; runtime verification
- weight: 3
- 来源: https://hengxin.github.io（2026-07-29，初始画像）

## 扩展点（🧐 视野扩展推荐依据）

### LLM 与形式化/系统的交叉
- keywords: neural theorem proving; LLM for verification; LLM agent memory; agent memory; LLM memory; LLM-based agent; AI for systems; learned database
- weight: 3
- 来源: 会话讨论（2026-07-29，初始画像）

### 计算机辅助证明与趣味组合
- keywords: computer-assisted proof; proof certificate; formally verified; combinatorial game
- weight: 3
- 来源: 会话讨论（2026-07-29，初始画像）
