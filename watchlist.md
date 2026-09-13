# 学者监控名单（新作推送依据）

> 本文件是**监控名单的唯一真相源**，可随时增删条目（CLI：`arxiv_daily.py watch add/remove`，
> 或 Web「监控」页）。完整说明见 [docs/user-guide/watching.md](docs/user-guide/watching.md)。
>
> **解析优先级**：**个人主页 → DBLP → Semantic Scholar**。
> 主页是首选，因为只有它才能覆盖「视频 / 技术报告 / talk」等非论文产出
> （Semantic Scholar 与 DBLP 只收录论文）；主页解析不出条目时才回落到 DBLP / S2。
>
> **格式约定**（脚本与 agent 共同遵守）：
> - 每位学者一个 `###` 小节（小节标题即显示名，建议使用「中文名 英文名」）。
> - `- homepage:` 个人主页 URL —— **首选解析源**。
> - `- dblp:` DBLP 的 PID（如 `pid/00/0000`）或用于检索的姓名全称 —— 兜底。
> - `- s2:` Semantic Scholar author id —— 兜底，可补摘要/venue/引用数。
> - `- tags:` 分号分隔的标签，用于 Web 端过滤（可选）。
> - `- enabled: true|false`（缺省 `true`）— `false` 表示**暂停监控但保留条目与历史**。
> - 小节正文其它内容视为备注，不影响解析。
> - 文件分 `## 监控中` / `## 已暂停` 两节；`enabled` 与所在小节需保持一致
>   （CLI 的 `enable/disable` 会同时改 `enabled` 并把条目移到对应小节）。

## 监控中

### 魏恒峰 Hengfeng Wei
- homepage: https://hengxin.github.io
- tags: 分布式一致性; 形式化方法; 数据库
- enabled: true
- 备注: 南京大学；分布式一致性、事务隔离与形式化验证。arXiv 画像初始来源之一。

### Alexey Gotsman
- homepage: https://software.imdea.org/~gotsman/
- tags: 分布式; 一致性; 程序验证
- enabled: true
- 备注: IMDEA Software Institute；分布式一致性与程序验证。

### Hagit Attiya
- homepage: https://hagit.net.technion.ac.il
- tags: 分布式计算; 共享内存; 下界
- enabled: true
- 备注: Technion；分布式计算理论。

## 已暂停

<!-- 暂停的条目会被移到这里；`enabled: false` 的条目不会被 `watch run` 扫描。 -->
