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
| `test_watch_page` | GET /watch 页面渲染 | ✅ |
| `test_api_watch_researchers` | GET /api/watch/researchers 返回名单 | ✅ |
| `test_api_watch_new` | GET /api/watch/new 返回未读新作 | ✅ |
| `test_api_watch_events` | GET /api/watch/events 返回推送历史 | ✅ |
| `test_api_watch_add_then_toggle_then_remove` | POST / DELETE / toggle 写操作往返（隔离到 tmp） | ✅ |
| `test_api_watch_add_duplicate_is_conflict` | 重名添加返回 409 | ✅ |
| `test_api_watch_remove_unknown_is_404` | 删除不存在条目返回 404 | ✅ |
| `test_api_watch_ack_clears_badge` | ack 清空 NEW 徽标 | ✅ |

> 注：`/api/watch/*` 的写操作（add / toggle / delete / ack）通过
> `isolated_watch` fixture 把 `watchlist.md` 与 `data/watch_new.json`
> 重定向到 `tmp_path`，**不会改动仓库内的真实文件**。

### `tests/test_watch.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_slugify` / `test_fingerprint_stable_and_distinct` | key 与指纹生成 | ✅ |
| `test_load_watchlist_parses_sections` | 名单两节（监控中/已暂停）解析 | ✅ |
| `test_add_then_remove_roundtrip` | 增删往返 + 重名拒绝 | ✅ |
| `test_set_enabled_moves_between_sections` | 启停会同步移动条目所在小节 | ✅ |
| `test_remove_forgets_seen_state` | 移除同时清除已见指纹 | ✅ |
| `test_collect_prefers_homepage_and_merges_configured_fallbacks` | 主页优先 + 兜底合并 | ✅ |
| `test_collect_falls_back_when_homepage_yields_nothing` | 主页无结果才回落 DBLP | ✅ |
| `test_collect_dedups_by_title_across_sources` | 跨源按标题去重 | ✅ |
| `test_run_seeds_baseline_without_pushing` | 首次建基线不推送 | ✅ |
| `test_paused_researchers_are_never_scanned` | 暂停对象不扫描 | ✅ |
| `test_run_detects_only_unseen_items` | 只推未见过条目 + digest 落盘 | ✅ |
| `test_run_force_pushes_on_first_sighting` | `--force` 覆盖基线行为 | ✅ |
| `test_run_only_filters_to_one` / `test_run_only_unknown_name_scans_nothing` | `--only` 过滤 | ✅ |
| `test_run_survives_one_broken_researcher` | 单人失败不影响整体 | ✅ |
| `test_events_are_logged_once_per_item` | 事件审计 | ✅ |
| `test_digest_upsert_is_idempotent` / `test_render_section_flags_low_confidence` | digest 幂等与低置信标记 | ✅ |

### `tests/test_notify.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_file_channel_writes_and_dedups` | 文件通道写入与按指纹去重 | ✅ |
| `test_load_new_tolerates_missing_and_corrupt` | 缺失/损坏 JSON 容错 | ✅ |
| `test_ack_all_clears` | 标记已读 | ✅ |
| `test_summary_groups_by_researcher` | 推送文案按人聚合 | ✅ |
| `test_desktop_disabled_by_env` / `test_desktop_skipped_off_windows` | 桌面通道开关 | ✅ |
| `test_desktop_shells_out_on_windows` | Windows 下确实调用 PowerShell | ✅ |
| `test_webhook_off_without_url` | 未配置则关闭 | ✅ |
| `test_webhook_payload_shapes` | generic / feishu / wecom 三种载荷 | ✅ |
| `test_webhook_posts_when_configured` | 配置后确实 POST | ✅ |
| `test_webhook_failure_is_swallowed` | 网络失败降级不抛异常 | ✅ |
| `test_push_runs_enabled_channels_only` | 编排只跑已启用通道 | ✅ |

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
| `test_cli_help` | 列出全部七个子命令（含 `watch`） | ✅ |
| `test_cli_daily_help` | `daily` 暴露 `--serve/--host/--port` | ✅ |
| `test_cli_serve_help` | `serve` 暴露 `--reload` | ✅ |
| `test_cli_watch_help` | `watch` 暴露 add/remove/enable/disable/list/run/ack/push-test | ✅ |
| `test_cli_watch_list_is_read_only` | `watch list --all` 只读输出名单 | ✅ |
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
