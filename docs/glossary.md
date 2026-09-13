# 术语表

> 本文档使用的统一术语定义

## 核心术语

| 术语 | 英文 | 定义 |
|------|------|------|
| **Digest** | Digest | 每日论文摘要汇总，按类别组织，包含命中标记和推荐表格 |
| **兴趣画像** | Interest Profile | 用户研究兴趣的结构化描述，存储在 `interests.md` 中 |
| **兴趣点** | Star Interest | 与当前研究直接相关的方向，产生 ★ 推荐候选 |
| **扩展点** | Expand Interest | 值得关注的延伸领域，产生 🧐 推荐候选 |
| **命中** | Hit | 论文标题/摘要匹配到兴趣条目的关键词 |
| **反馈** | Feedback | 用户对论文的评分行为，驱动画像权重演化 |
| **权重** | Weight | 兴趣条目的重要性评分（1-10），影响排序和推荐 |

## 技术术语

| 术语 | 英文 | 定义 |
|------|------|------|
| **HTMX** | HTMX | 前端库，通过 AJAX 实现服务器渲染 HTML 的局部更新 |
| **Alpine.js** | Alpine.js | 轻量级前端框架，用于客户端交互和状态管理 |
| **Pydantic** | Pydantic | Python 数据验证库，用于 API 请求/响应模型 |
| **Jinja2** | Jinja2 | Python 模板引擎，用于服务端 HTML 渲染 |
| **JSON Lines** | JSONL | 每行一个 JSON 对象的文本格式，用于日志类数据 |

## 设计与界面术语

| 术语 | 英文 | 定义 |
|------|------|------|
| **设计令牌** | Design Token | 设计决策的可复用变量（色彩/字号/间距/圆角/动效），以 CSS 自定义属性落地 |
| **双通道** | Dual Channel | ★ 兴趣点（amber）与 🧐 扩展点（sky）两条互不混同的推荐通道 |
| **命中得分** | Hit Score | **系统算的**：命中条目权重之和（`score_star` / `score_expand`），以实心徽标呈现 |
| **我的评分** | My Rating | **我给的**：用户对论文的 ★/🧐 打分（0–5），以分段控件呈现 |
| **高保真原型** | Hi-Fi Prototype | 可交互、贴近最终视觉与交互的界面原型（本仓库见 `docs/design/prototype.html`） |
| **Anti-Slop** | Anti-Slop | 一组禁止项，用于避免「AI 生成感」廉价视觉（见设计系统 §7） |
| **密度切换** | Density Toggle | 舒适 / 紧凑两档阅读密度切换 |
| **pips** | Pips | 5 格分段评分控件，用于「我的评分」（区别于命中徽标） |

## 数据文件

| 术语 | 文件 | 说明 |
|------|------|------|
| **日数据文件** | `data/YYYYMMDD.json` | 某天抓取的全部论文原始数据 |
| **兴趣文件** | `interests.md` | 兴趣画像的 Markdown 格式存储 |
| **反馈日志** | `feedback.jsonl` | 用户反馈的 append-only 审计日志 |
| **Digest 文件** | `arXiv-schedule.md` | 人读的每日论文摘要汇总 |

## 评分符号

| 符号 | 含义 | 范围 |
|------|------|------|
| ★ | 兴趣度（重点关注的推荐强度） | 0-5 |
| 🧐 | 好奇度（视野扩展的推荐强度） | 0-5 |
| 🎯★ | 命中兴趣点关键词 | — |
| 🎯🧐 | 命中扩展点关键词 | — |

## 缩写

| 缩写 | 全称 | 说明 |
|------|------|------|
| **ADR** | Architecture Decision Record | 架构决策记录 |
| **API** | Application Programming Interface | 应用程序接口 |
| **CLI** | Command Line Interface | 命令行界面 |
| **MVP** | Minimum Viable Product | 最小可行产品 |
| **PWA** | Progressive Web App | 渐进式 Web 应用 |
| **RAG** | Retrieval-Augmented Generation | 检索增强生成 |
| **TTS** | Text-to-Speech | 文本转语音 |
