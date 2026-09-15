# 测试策略

> Paper-Glean 测试体系概述

## 测试分层

```
┌─────────────────────────────────────┐
│  手工测试（Manual）                  │
│  - Web UI 交互                       │
│  - CLI 命令执行                      │
│  - 端到端工作流                      │
├─────────────────────────────────────┤
│  集成测试（Integration）              │
│  - API 端点测试                      │
│  - 文件读写测试                      │
├─────────────────────────────────────┤
│  单元测试（Unit）                    │
│  - core.py 函数测试                  │
│  - 工具函数测试                      │
└─────────────────────────────────────┘
```

## 测试覆盖范围

| 组件 | 单元测试 | 集成测试 | 手工测试 |
|------|----------|----------|----------|
| `glean/core.py` | ✅ | — | — |
| `glean/serve.py` | ✅ | ✅ | — |
| `glean/monitor.py` | ✅ | — | — |
| `glean/watch.py` | ✅ | — | ✅ |
| `glean/homeparse.py` | — | — | ✅ |
| `glean/ccf.py` | ✅ | — | ✅ |
| `glean/ccf_catalog.py` | — | — | — |
| `glean/venueparse.py` | ✅ | — | ✅ |
| `glean/notify.py` | ✅ | — | ✅ |
| `glean/htmlkit.py` | ✅ | — | — |
| `glean/report.py` | ✅ | — | ✅ |
| `glean/cli.py` | ✅ | ✅ | ✅ |
| `glean/web/routes.py` | — | ✅ | ✅ |
| `glean/web/models.py` | ✅ | — | — |
| 数据文件格式 | — | ✅ | — |
| 端到端工作流 | — | — | ✅ |

> 全量测试数：**183 passed**（`pytest tests/ -q`）。
> `ccf_catalog.py` 是生成物（数据模块），由 `scripts/gen_ccf_catalog.py` 产出，
> 由 `test_ccf.py::test_sync_catalog_keeps_user_ticks` 间接覆盖，无独立测试。
> `monitor.py` 是 `watch` / `ccf` 的共享内核，由 `tests/test_monitor.py` 独立覆盖
> （含基线/差异/`--force`/逐条失败隔离/推送降级/审计字段等），因此两条线自己的测试
> 不必重复这些语义。
> `glean/web/templates_config.py`（模板环境与 `format_timestamp` 过滤器）由
> `test_web.py` 的页面渲染路径间接覆盖，无独立测试。
> `report.py` + `htmlkit.py`（三条链路的独立 HTML 快照）由 `tests/test_report.py`
> 与 `tests/test_monitor_report.py` 覆盖：自包含（零 CDN / 零 `127.0.0.1` 外链）、
> 默认亮色（暗色 opt-in）、转义、**零新增仍出页面**、以及「盲区 vs 真的没有」的区分。

## 测试原则

1. **核心逻辑优先**：`glean/core.py` 是纯函数，最易测试，覆盖度最高
2. **IO 边界测试**：文件读写、HTTP 请求使用 mock
3. **幂等性验证**：`fetch` / `run` 重复执行应产生相同结果
4. **兼容性验证**：早期数据文件格式应能正确解析
5. **路径隔离**：涉及写盘的测试用 `monkeypatch` 把配置常量重定向到 `tmp_path`，绝不触碰仓库真实文件
6. **零网络**：解析类测试一律喂内联样本字符串（RSS / HTML / JSON），不发真实请求

## 已知限制

- 未覆盖 arXiv API 实际调用（依赖外部服务）
- 未覆盖 PDF 下载（依赖外部服务 + 文件系统）
- 未覆盖 ccfddl / Crossref 真实网络请求（解析逻辑用内联样本覆盖；端到端靠手工 `ccf run`）
- 未覆盖 agent 层（非确定性，需人工验证）
- DBLP 自 2026-09 起对爬虫返回 Anubis 人机验证页，`dblp` 字段降级为人工参考链接，不再抓取
