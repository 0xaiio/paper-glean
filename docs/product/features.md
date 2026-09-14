# 功能域清单

> 功能域清单：MVP / 增强 / 远期

## 功能域总览

| 域 | MVP | 增强 | 远期 | 策略 |
|----|-----|------|------|------|
| 多源采集 | 插件接口 + arXiv 适配器 | S2/OpenAlex/DBLP 适配器 | 学者主页监控 | 自研 + 借 API |
| 画像与推荐 | L0 关键词命中 | L1 嵌入相似 + L2 LLM 评分 | L3 混合排序 | 自研 + 借 API |
| 反馈闭环 | 打分 + 权重更新 | 隐式信号 + 时间线 | 画像体检报告 | 自研 |
| 阅读工作流 | 三态队列 | PDF.js + Markdown 笔记 | TTS 听摘要 | 自研 + Obsidian |
| PDF 库集成 | 下载命名规则 | 全库索引 + 统计 | 库内相关提示 | 自研 |
| 引文图谱 | 外链 Connected Papers | 轻量本地关系图 | — | 外链 + 自研 |
| AI 摘要/周报 | — | 结构化摘要 + 周报 | 库内 RAG | 自研 + LLM |
| 协作与分享 | 导出 Markdown | 导出 HTML/RSS | 组内共享 | 自研 |
| 通知渠道 | — | 邮件 + Webhook | RSS 输出 | 自研 |
| 监控与推送 | 按人监控（主页 → DBLP/S2，四通道推送）✅ | 按会议/期刊监控 CFP/Program/接收论文 ✅ | 三线合并为统一简报 | 自研 |
| 移动端/PWA | 响应式布局 | PWA 离线缓存 | 推送通知 | 自研 |

## 1. 多源采集

**MVP**：
- 定义插件式 source adapter 接口
- arXiv 适配器（现有逻辑重构）

**增强**：
- DBLP 适配器（CS venue 权威）
- Semantic Scholar / OpenAlex 适配器
- Crossref DOI 解析

**远期**：
- 学者主页监控（关注作者新作）
- ACL Anthology、HAL 等区域源

## 2. 画像与推荐算法

分四级渐进，任何一级都可解释、可关停回退：

- **L0 关键词命中（MVP）**：`interests.md` keywords 整词匹配 + 条目权重求和
- **L1 嵌入相似（增强）**：条目标题+keywords 向量化，论文 SPECTER2 嵌入，余弦相似
- **L2 LLM 语义评分（增强）**：对 top-N 调用 LLM 打分并生成中文推荐理由
- **L3 混合排序（远期）**：`最终分 = w1·L0 + w2·L1 + w3·L2 + 反馈时间衰减项`

## 3. 反馈闭环

**MVP**：
- 卡片上一键 0-5 ★/🧐 打分
- 直接调用现有 `feedback` 逻辑

**增强**：
- 隐式信号：skip / save / read / download
- 权重演化时间线
- 高分未命中 → 「建议新增条目」收件箱

**远期**：
- 周期性「画像体检」报告

## 4. 阅读工作流

**MVP**：
- 阅读队列三态：inbox → reading → done/archived

**增强**：
- 内嵌 PDF 阅读器（PDF.js）
- 每篇论文一页 Markdown 笔记（Obsidian 兼容）

**远期**：
- TTS 听摘要/速读模式

## 5. PDF 库集成

**MVP**：
- 下载沿用现有命名规则
- 落 `$ARXIV_DIR`（默认 `~/papers`）目录

**增强**：
- 全库扫描建索引
- Venue/年份统计面板
- 重复文件检测

**远期**：
- 「库内已有相关论文」提示
- 全文检索

## 6. 引文图谱

**MVP**：外链 Connected Papers / Litmaps / Semantic Scholar

**增强**：轻量本地关系图（「本次推荐论文 ↔ 库内已有论文」引用连边）

**远期**：不做通用引文图谱探索（明确非目标）

## 7. AI 摘要 / 问答 / 周报

**MVP**：不做（现有 digest 已够用）

**增强**：
- 单篇结构化摘要卡片（问题/方法/结果/相关性）
- 每周趋势周报（Markdown 落盘）

**远期**：
- 库内 RAG 问答
- 跨篇对比表格

## 8. 协作与分享

**MVP**：导出精选清单为 Markdown

**增强**：
- 导出 HTML/RSS feed
- 外部热度信号参考

**远期**：组内共享画像/清单（多人场景，优先级最低）

## 9. 通知渠道

**MVP**：无独立推送渠道。**调度已实现**：仓库内 `arxiv_daily.py daily`
（fetch → 确保本地 Web 服务在线）+ `scripts/register_task.ps1`（Windows 计划任务），
或 WorkBuddy 平台定时任务（agent 抓取 + 填推荐 + `present_files` 呈递）。
见 [定时运行](../user-guide/scheduling.md)。

**增强**：
- 每日 digest 邮件
- Telegram / 企业微信 webhook

**远期**：RSS 输出端点

## 11. 监控与推送（M1.x 已实现）

**MVP（已实现）**：
- 名单 `watchlist.md`（Markdown 真相源），CLI / Web / 直接编辑三种增删
- 解析顺序 **个人主页 → DBLP → Semantic Scholar**；主页唯一覆盖视频/TR/talk
- 不做 Google Scholar（无官方 API、违反 ToS、易封）；以 DBLP + S2 公开 API 覆盖
- 差异判定：指纹去重；**首次建基线不推送**，`--force` 可强制
- 推送四通道：`file`（digest + Web NEW 徽标）、Web 高亮、`desktop`、`webhook`
  （`generic`/`feishu`/`wecom`）；全部 fail-soft
- Web `/watch` 页面：名单增删 + NEW 徽标 + 推送历史

**增强**：
- 主页解析 JS 渲染兜底
- 按 tags 订阅推送
- S2 补全摘要/venue/引用数

**远期**：
- 从高分论文作者自动发现监控对象
- 与 arXiv 日报合并为统一简报

**已知边界**：主页解析为启发式，置信度 < 0.5 丢弃；偏漏报而非误报。

## 12. CCF-A 会议 / 期刊监控与推送（M1.x 已实现）

**MVP（已实现）**：
- 名单 `ccf.md`（Markdown 真相源，**勾选框**）：勾选即订阅、取消即暂停；
  CLI（含 `--area` 批量）/ Web（可点勾选框 + 按领域全选/全不选）/ 直接编辑三种方式
- 目录 `glean/ccf_catalog.py`（快照，`scripts/gen_ccf_catalog.py` 可重新生成）：
  会议取 [ccfddl.com](https://ccfddl.com/) 公开 RSS（带 CCF 等级 / 领域 / 官网 / DBLP），
  期刊为人工整理的 A 类期刊并按 ISSN 到 Crossref 校验；当前 **71 会议 + 22 期刊**
- 解析顺序：会议 = **ccfddl 截稿 RSS → 会议主页**；期刊 = **Crossref（按 ISSN 取卷期）→ 期刊主页**
- 三类信号：`cfp` 征稿 / `program` 日程 / `papers` 接收论文列表，每条带置信度
- 差异判定：指纹去重；**首次建基线不推送**，`--force` 可强制
- 复用同一套推送四通道，但走**独立命名空间**（`data/ccf_new.json` + `CCF-digest.md`），
  与学者监控的未读互不清除
- Web `/ccf` 页面：勾选框名单 + 批量勾选 + NEW 徽标 + 推送历史

**增强**：
- 会议主页 JS 渲染兜底
- 按 `area` 分别配置推送渠道
- 与 arXiv 日报交叉匹配（提前发现接收论文）
- 截稿日临近提醒（ccfddl 已提供 deadline）

**远期**：
- 目录自动跟随 ccfddl 更新（当前为快照 + `ccf refresh` 手动同步）
- 三条监控线合并为统一简报

**已知边界**：
- **DBLP 已不可抓取**（2026-09 起全部端点返回 Anubis 反爬拦截页），`dblp` 字段仅为人工参考链接；
  这也意味着 §11 的 DBLP 兜底源目前静默返回空
- 期刊目录为人工整理，是目录里最可能出错的部分（出错的条目取消勾选即可）
- 期刊主页（ACM DL / IEEE Xplore）是 JS 渲染的空壳，期刊靠 Crossref 而非主页

## 10. 移动端 / PWA

**MVP**：响应式布局（手机浏览器可用）

**增强**：
- PWA 离线缓存
- 通勤时刷卡片打分，回网后同步

**远期**：推送通知
