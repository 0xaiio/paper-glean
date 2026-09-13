# 测试计划

> 各组件测试覆盖详情

## 单元测试

### `tests/test_core.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_load_interest_entries` | 解析 interests.md | ✅ |
| `test_match_keywords` | 关键词匹配逻辑 | ✅ |
| `test_annotate_hits` | 命中标记生成 | ✅ |
| `test_apply_feedback` | 反馈应用与权重更新 | ✅ |
| `test_save_day_data` | JSON 文件原子写入 | ✅ |
| `test_upsert_digest` | Markdown 章节更新 | ✅ |

### `tests/test_web.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_digest_page` | GET /digest 返回 HTML | ✅ |
| `test_api_papers` | GET /api/papers 返回 JSON | ✅ |
| `test_api_ping` | GET /api/ping 存活探测返回 service/version/time | ✅ |
| `test_api_interests` | GET /api/interests 返回画像 | ✅ |
| `test_htmx_paper_list` | GET /htmx/paper-list 返回片段 | ✅ |

### `tests/test_serve.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_base_url_and_ping_url` | URL 拼接 | ✅ |
| `test_no_proxy_opener_carries_no_active_proxy` | 回环探测不受 `*_PROXY` 劫持 | ✅ |
| `test_probe_reaches_loopback_despite_bogus_env_proxy` | 端到端：环境代理为坏地址时仍能探到本地服务 | ✅ |
| `test_probe_hits_ping_path` | 探测打的是 `/api/ping` | ✅ |
| `test_probe_false_on_error` | 连接失败返回 False（不抛异常） | ✅ |
| `test_log_path_lives_under_logs` | 日志落 `logs/` | ✅ |
| `test_ensure_reuses_online_instance` | 已在线的实例被复用而非重复拉起 | ✅ |
| `test_ensure_reports_failure_when_spawn_fails` | 拉起失败时 fail-soft 返回 `(False, False)` | ✅ |

### `tests/test_cli.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_cli_help` | 列出全部六个子命令 | ✅ |
| `test_cli_daily_help` | `daily` 暴露 `--serve/--host/--port` | ✅ |
| `test_cli_serve_help` | `serve` 暴露 `--reload` | ✅ |
| `test_arxiv_daily_wrapper` | 薄包装器仍可调用 | ✅ |

## 集成测试场景

### 场景 1：完整 Fetch 工作流

```gherkin
Given  interests.md 已配置
When   运行 arxiv_daily.py fetch
Then   data/YYYYMMDD.json 被创建
And    arXiv-schedule.md 包含当日章节
And    章节内论文按权重排序
```

### 场景 2：Feedback 闭环

```gherkin
Given  某篇论文已存在 digest 中
When   运行 feedback --stars 5
Then   interests.md 中对应条目权重 +1
And    feedback.jsonl 追加新记录
And    arXiv-schedule.md 表格更新
```

### 场景 3：Web 打分

```gherkin
Given  Web 应用已启动
When   在 /digest 页面给论文打 4 星
Then   API 返回成功
And    文件系统同步更新
```

## 回归测试清单

每次发布前必须验证：

- [ ] `pytest tests/ -v` 全部通过
- [ ] CLI 六个子命令均可正常执行
- [ ] Web 应用可启动，三个页面可访问
- [ ] `arxiv_daily.py daily --serve` 后 `curl --noproxy '*' http://127.0.0.1:8000/api/ping` 返回 200
- [ ] 键盘快捷键工作正常
- [ ] 反馈打分后文件正确更新
- [ ] 幂等：重复 fetch 不产生重复数据
