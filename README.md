# Paper-Glean (摘星 StarDigest)

> Interest-driven paper digest and recommender

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

周期性地从 arXiv 抓取新增论文，根据你的研究兴趣做推荐，支持 CLI 和 Web 双界面。

---

## 文档

完整文档见 [docs/index.md](docs/index.md)

| 角色 | 文档 |
|------|------|
| 用户 | [快速开始](docs/user-guide/index.md) / [CLI 参考](docs/user-guide/cli.md) / [Web 应用](docs/user-guide/web-app.md) |
| 开发者 | [架构概览](docs/developer-guide/index.md) / [系统设计](docs/developer-guide/system-design.md) / [核心库](docs/developer-guide/core-library.md) / [API 参考](docs/developer-guide/api-reference.md) |
| 产品经理 | [产品愿景](docs/product/vision.md) / [路线图](docs/product/roadmap.md) / [设计原则](docs/product/principles.md) / [需求与现状审阅](docs/product/review.md) |
| 设计 | [界面设计规范](docs/design/index.md) / [设计系统与令牌](docs/design/design-system.md) / [需求摘要](docs/design/requirements-brief.md) / [质量审查报告](docs/design/critique.md) / [高保真原型](docs/design/prototype.html) |
| 测试人员 | [测试策略](docs/testing/index.md) / [手工测试](docs/testing/manual-tests.md) |

---

## 快速开始

```powershell
# 安装
pip install -e ".[web]"

# 抓取今日论文
python -X utf8 arxiv_daily.py fetch

# 启动 Web 应用
python -m glean.web
# 打开 http://127.0.0.1:8000

# 或一步到位：抓取 + 确保 Web 服务在线（供定时任务使用）
python -X utf8 arxiv_daily.py daily --serve
```

### 定时运行

仓库内已内置定时流水线（`daily` / `serve` 命令 + Windows 计划任务脚本），
详见 [定时运行](docs/user-guide/scheduling.md)。

---

## 核心特性

- **本地优先**：数据全部在本地仓库，可 Git 版本化、可离线
- **双界面**：CLI 脚本 + Web 应用，满足不同场景
- **定时就绪**：仓库内 `daily` 一条命令抓取并确保 Web 服务在线，可直接挂平台/系统定时任务
- **兴趣驱动**：基于 interests.md 画像做关键词命中和推荐
- **反馈闭环**：打分即调整权重，次日自动生效
- **可解释**：每条推荐说明命中了哪个条目、权重多少

---

## 架构

- **脚本层**：纯标准库 Python，负责抓取、去重、命中标记、下载
- **Agent 层**：语义理解，填写推荐小节，解析新材料
- **Web 层**：FastAPI + HTMX + Alpine.js，卡片式浏览与打分

---

## 文件清单

| 文件 | 说明 |
|------|------|
| `glean/` | **Python 包**：`core.py` 核心库 · `cli.py` CLI · `config.py` 配置 · `serve.py` 服务保活 · `web/` FastAPI 视图层 · `templates/` Jinja2 模板 |
| arxiv_daily.py | 向后兼容薄包装 → `glean.cli:main` |
| scripts/ | 定时基础设施：`run_daily.ps1` 任务体 · `register_task.ps1` 注册 Windows 计划任务 |
| interests.md | 兴趣画像：兴趣点/扩展点条目 + keywords + weight |
| feedback.jsonl | 人工调整推荐指数的反馈日志（审计轨迹） |
| arXiv-schedule.md | 每日 digest，按日期章节组织 |
| data/YYYYMMDD.json | 当天全部论文原始数据 |
| logs/ | 后台服务日志（`serve-<host>-<port>.log`，被 git 忽略） |
| glean_static/ | 前端静态资源（CSS / Alpine.js） |
| tests/ | pytest 测试（core / web / cli） |
| plan.md | Web 应用需求规格（M1 已实现，目标界面见 docs/design/） |
| survey.md | 现有系统调研与自研/采购决策 |
| docs/ | **项目文档（本文档体系）** |
| site/ | MkDocs 构建产物（`cd docs && mkdocs build`） |

---

## 设计原则

1. **本地优先**：数据全部落在本仓库内，可 Git 版本化、可离线、可随时退出
2. **Markdown/JSON 为唯一事实源**：Web 应用只是视图层，文件可随时手工编辑
3. **CLI 永远是 fallback**：Web 挂了脚本照跑
4. **可解释推荐**：每条推荐必须能回答为什么推荐给我

---

## 更多

- 完整 CLI 用法：[docs/user-guide/cli.md](docs/user-guide/cli.md)
- 定时运行（平台任务 / Windows 计划任务）：[docs/user-guide/scheduling.md](docs/user-guide/scheduling.md)
- Web 键盘快捷键：[docs/user-guide/web-app.md](docs/user-guide/web-app.md)
- 兴趣画像管理：[docs/user-guide/interest-profile.md](docs/user-guide/interest-profile.md)
- 反馈机制：[docs/user-guide/feedback.md](docs/user-guide/feedback.md)
- 开发贡献：[docs/developer-guide/contributing.md](docs/developer-guide/contributing.md)
