# Paper-Glean 文档

> **摘星 StarDigest** — Interest-driven paper digest & recommender
> （兴趣驱动的论文摘要与推荐工作台）

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/user/paper-glean/blob/main/LICENSE)
[![Tests](https://github.com/user/paper-glean/actions/workflows/test.yml/badge.svg)](https://github.com/user/paper-glean/actions)

---

## 按角色导航

### 我是用户

快速上手使用 Paper-Glean：

- [快速开始](user-guide/index.md) — 5 分钟上手
- [安装指南](user-guide/installation.md) — 环境准备与安装
- [CLI 参考](user-guide/cli.md) — 命令行完整手册
- [Web 界面](user-guide/web-app.md) — 浏览器操作指南
- [兴趣画像](user-guide/interest-profile.md) — 管理研究兴趣
- [反馈机制](user-guide/feedback.md) — 打分与权重演化

### 我是开发者

了解系统架构与参与开发：

- [架构概览](developer-guide/index.md) — 系统架构与模块关系
- [核心库](developer-guide/core-library.md) — `glean/core.py` 模块详解
- [Web 层](developer-guide/web-layer.md) — FastAPI + HTMX 实现
- [数据规范](developer-guide/data-schema.md) — 文件格式精确 schema
- [API 参考](developer-guide/api-reference.md) — 自动生成的 API 文档
- [贡献指南](developer-guide/contributing.md) — 开发环境与代码规范

### 我是产品经理

了解产品愿景与发展路线：

- [产品愿景](product/vision.md) — 一句话定义与四大原则
- [路线图](product/roadmap.md) — M0-M4 分期规划
- [设计原则](product/principles.md) — 本地优先、可解释推荐
- [功能域](product/features.md) — 十大功能域（MVP/增强/远期）
- [非目标](product/non-goals.md) — 明确不做的事项
- [架构决策](product/decisions/adr-001-fastapi-htmx.md) — ADR 记录

### 我是测试人员

了解测试策略与执行测试：

- [测试策略](testing/index.md) — 单元/集成/手工测试
- [测试计划](testing/test-plan.md) — 各组件测试覆盖
- [手工测试](testing/manual-tests.md) — Web UI 与 CLI 测试用例
- [CI/CD](testing/ci.md) — 自动化流程

---

## 项目简介

Paper-Glean 是一个**个人本地优先**的论文推荐与归档工作台：

- **本地优先**：数据全部落在本仓库内，可 Git 版本化、可离线、可随时退出
- **Markdown/JSON 为唯一事实源**：Web 应用只是视图层，文件可随时手工编辑
- **CLI 永远是 fallback**：Web 挂了脚本照跑
- **可解释推荐**：每条推荐能回答「为什么推荐给我」

---

## 快速开始

```powershell
# 安装（含 Web 依赖）
pip install -e ".[web]"

# 启动 Web 应用
python -m glean.web
# → 打开 http://127.0.0.1:8000
```

更多详情见 [安装指南](user-guide/installation.md)。

---

## 文档本地预览

```powershell
# 安装文档依赖
pip install -e ".[docs]"

# 启动本地文档服务器
cd docs
mkdocs serve
# → 打开 http://127.0.0.1:8000
```
