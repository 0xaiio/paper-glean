# 发展路线图

> M0-M4 分期规划

## 分期概览

| 期 | 内容 | 交付判据 | 状态 |
|----|------|---------|------|
| M0 | CLI + agent + Markdown | 可独立运行 fetch/download/feedback | ✅ 已完成 |
| M1 | 只读 Web 视图 + 打分/下载按钮 | 晨间浏览不再打开编辑器/敲命令 | ✅ 已完成 |
| M2 | 多源接入 + 嵌入推荐 | DBLP 源上线；L1 相似分数上卡片 | 📝 规划中 |
| M3 | 阅读流 + 库集成 | 阅读队列可用；归档库统计面板 | 📝 规划中 |
| M4 | 图谱连边 / 周报 / 通知 | 库内关系图；每周 Markdown 周报 | 📝 规划中 |

## M0：CLI 基础（已完成）

- `arxiv_daily.py` 抓取脚本
- `interests.md` 兴趣画像
- `feedback.jsonl` 反馈日志
- `arXiv-schedule.md` 每日 digest

## M1：Web 应用（已完成）

- FastAPI + HTMX + Alpine.js 本地 Web 应用
- Digest 流：卡片式浏览、筛选、搜索、键盘导航
- 兴趣画像：可视化展示条目与权重
- 归档库：查看已下载 PDF
- 反馈打分：Web 端直接打分，同步到文件

## M2：多源与嵌入（规划中）

### 多源采集
- 定义插件式 source adapter 接口
- 实现 DBLP 适配器（CS venue 权威）
- Semantic Scholar / OpenAlex 适配器

### 嵌入推荐（L1）
- interests.md 每条目向量化
- 论文用 SPECTER2 嵌入
- 余弦相似 × 条目权重

## M3：阅读流与库集成（规划中）

### 阅读工作流
- 阅读队列三态：inbox → reading → done
- 内嵌 PDF 阅读器（PDF.js）
- 每篇论文 Markdown 笔记

### PDF 库集成
- 全库扫描建索引
- Venue/年份统计面板
- 重复文件检测

## M4：高级功能（规划中）

### 引文图谱
- 轻量本地关系图
- 「本次推荐论文 ↔ 库内已有论文」引用连边

### AI 摘要与周报
- 单篇结构化摘要（问题/方法/结果/相关性）
- 每周趋势周报（Markdown 落盘）

### 通知渠道
- 每日 digest 邮件
- Telegram / 企业微信 webhook
