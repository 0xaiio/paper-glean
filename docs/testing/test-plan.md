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
| `test_ccf_page` | GET /ccf 页面渲染 | ✅ |
| `test_api_ccf_venues` | GET /api/ccf/venues 名单 + area/enabled 过滤 | ✅ |
| `test_api_ccf_new_and_events` | GET /api/ccf/new、/api/ccf/events | ✅ |
| `test_api_ccf_add_then_toggle_then_remove` | POST / DELETE / toggle 写操作往返（隔离到 tmp） | ✅ |
| `test_api_ccf_add_duplicate_is_conflict` | 重名添加返回 409 | ✅ |
| `test_api_ccf_add_without_homepage_is_rejected` | 空 homepage 422、纯空白 homepage 409 | ✅ |
| `test_api_ccf_remove_unknown_is_404` | 删除不存在条目返回 404 | ✅ |
| `test_api_ccf_toggle_area_is_bulk` | 按 area 批量勾选/取消 | ✅ |
| `test_api_ccf_ack_clears_only_ccf_badge` | ack 只清 CCF 徽标，不影响学者徽标 | ✅ |

> 注：`/api/watch/*` 与 `/api/ccf/*` 的写操作分别通过 `isolated_watch` /
> `isolated_ccf` fixture 把 `watchlist.md`、`ccf.md` 及其状态/未读文件
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
| `test_collect_offline_returns_nothing` | 离线模式不发起网络请求 | ✅ |
| `test_run_seeds_baseline_without_pushing` | 首次建基线不推送 | ✅ |
| `test_paused_researchers_are_never_scanned` | 暂停对象不扫描 | ✅ |
| `test_run_detects_only_unseen_items` | 只推未见过条目 + digest 落盘 | ✅ |
| `test_run_force_pushes_on_first_sighting` | `--force` 覆盖基线行为 | ✅ |
| `test_run_only_filters_to_one` / `test_run_only_unknown_name_scans_nothing` | `--only` 过滤 | ✅ |
| `test_run_survives_one_broken_researcher` | 单人失败不影响整体 | ✅ |
| `test_events_are_logged_once_per_item` | 事件审计 | ✅ |
| `test_digest_upsert_is_idempotent` / `test_render_section_flags_low_confidence` | digest 幂等与低置信标记 | ✅ |

### `tests/test_ccf.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_parse_ccf_md_reads_kind_checkbox_and_fields` | 解析勾选框 + 缩进字段 + 会议/期刊分节 | ✅ |
| `test_add_then_remove_roundtrip` | 增删往返 + 重名拒绝 | ✅ |
| `test_add_requires_a_homepage` | 缺 homepage 拒绝添加 | ✅ |
| `test_set_enabled_rewrites_the_checkbox` | 勾选/取消改写 `[x]`/`[ ]` | ✅ |
| `test_set_enabled_area_is_bulk` | 按 area 批量勾选/取消 | ✅ |
| `test_sync_catalog_keeps_user_ticks` | 目录刷新保留用户勾选，仅补新条目 | ✅ |
| `test_conference_prefers_ccfddl_then_homepage` | 会议优先 ccfddl RSS，再补主页 | ✅ |
| `test_journal_uses_crossref_not_ccfddl` | 期刊走 Crossref（ISSN），不走 ccfddl | ✅ |
| `test_collect_is_offline_when_asked` | 离线模式零网络 | ✅ |
| `test_items_are_deduped_by_fingerprint` | 按指纹去重 | ✅ |
| `test_run_seeds_baseline_without_pushing` | 首扫建基线不推送 | ✅ |
| `test_unticked_venues_are_never_scanned` | 未勾选条目不扫描 | ✅ |
| `test_run_detects_only_unseen_items` | 只推未见过条目 + digest 落盘 | ✅ |
| `test_force_pushes_on_first_sighting` | `--force` 覆盖基线行为 | ✅ |
| `test_events_are_logged_once_per_item` | 事件审计每条一次 | ✅ |
| `test_run_survives_one_broken_venue` | 单站点失败不影响整体 | ✅ |
| `test_digest_upsert_is_idempotent` | digest 章节 upsert 幂等 | ✅ |
| `test_render_section_labels_kinds` | 渲染按 kind 打标（📢/📅/📄） | ✅ |

### `tests/test_venueparse.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_parse_venue_page_classifies_the_three_signals` | 主页解析识别 cfp/program/papers 三类 | ✅ |
| `test_parse_venue_page_drops_nav_and_root_links` | 过滤导航与首页根链接 | ✅ |
| `test_parse_venue_page_makes_urls_absolute` | 相对链接转绝对 | ✅ |
| `test_parse_venue_page_never_raises_on_garbage` | 垃圾输入不抛异常 | ✅ |
| `test_parse_ccfddl_matches_venue_and_reads_deadline` | ccfddl RSS 匹配场次 + 读 deadline | ✅ |
| `test_parse_ccfddl_honours_min_year` | 过滤低于 min_year 的旧场次 | ✅ |
| `test_parse_ccfddl_unescapes_html_entities` | 反转义（如 `S&amp;P`） | ✅ |
| `test_parse_ccfddl_ignores_other_venues_and_empty_names` | 忽略其它会议与空名 | ✅ |
| `test_fetch_crossref_issues_groups_by_volume_and_issue` | Crossref 按卷/期聚合 | ✅ |
| `test_crossref_url_is_the_homepage_so_fingerprints_stay_stable` | URL 固定为主页，指纹稳定 | ✅ |
| `test_fetch_crossref_issues_without_issn_is_a_noop` | 无 ISSN 时为空操作（参数化空串/None） | ✅ |
| `test_fetch_crossref_issues_swallows_network_failure` | 网络失败降级不抛异常 | ✅ |

> 解析类测试全部喂**内联样本字符串**，零真实网络请求。

### `tests/test_notify.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_file_channel_writes_and_dedups` | 文件通道写入与按指纹去重 | ✅ |
| `test_load_new_tolerates_missing_and_corrupt` | 缺失/损坏 JSON 容错 | ✅ |
| `test_ack_all_clears` | 标记已读 | ✅ |
| `test_summary_groups_by_researcher` | 推送文案按人聚合 | ✅ |
| `test_summary_falls_back_to_venue_and_labels_namespace` | 无学者字段时回落 venue，并按命名空间打标 | ✅ |
| `test_namespaces_keep_separate_unread_sets` | watch / ccf 未读集合互相隔离 | ✅ |
| `test_unknown_namespace_is_rejected` | 未知命名空间被拒绝 | ✅ |
| `test_desktop_disabled_by_env` / `test_desktop_skipped_off_windows` | 桌面通道开关 | ✅ |
| `test_desktop_shells_out_on_windows` | Windows 下确实调用 PowerShell | ✅ |
| `test_webhook_off_without_url` | 未配置则关闭 | ✅ |
| `test_webhook_payload_shapes` | generic / feishu / wecom 三种载荷 | ✅ |
| `test_webhook_posts_when_configured` | 配置后确实 POST | ✅ |
| `test_webhook_failure_is_swallowed` | 网络失败降级不抛异常 | ✅ |
| `test_push_runs_enabled_channels_only` | 编排只跑已启用通道 | ✅ |
| `test_push_no_items_is_noop` | 空 items 直接返回不推送 | ✅ |
| `test_enabled_channels_report` | 报告各通道启用状态 | ✅ |

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
| `test_cli_help` | 列出全部八个子命令（含 `watch` / `ccf`） | ✅ |
| `test_cli_daily_help` | `daily` 暴露 `--serve/--host/--port` | ✅ |
| `test_cli_serve_help` | `serve` 暴露 `--reload` | ✅ |
| `test_cli_watch_help` | `watch` 暴露 add/remove/enable/disable/list/run/ack/push-test | ✅ |
| `test_cli_watch_list_is_read_only` | `watch list --all` 只读输出名单 | ✅ |
| `test_cli_ccf_help` | `ccf` 暴露 add/remove/enable/disable/list/run/ack/refresh | ✅ |
| `test_cli_ccf_list_is_read_only` | `ccf list` 只读输出勾选清单 | ✅ |
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

### 场景 4：CCF 监控首扫建基线

```gherkin
Given  ccf.md 已勾选若干 CCF-A 会议/期刊
When   首次运行 arxiv_daily.py ccf run
Then   data/ccf_state.json 写入全部已见指纹
And    不推送任何历史条目（基线静默）
And    CCF-digest.md 不新增章节

When   再次运行且站点出现一条新 CFP
Then   仅该新条目进入 data/ccf_new.json
And    CCF-digest.md 追加当日章节
And    CCF 页面 NEW 徽标 +1（学者页面徽标不受影响）
```

## 回归测试清单

每次发布前必须验证：

- [ ] `pytest tests/ -v` 全部通过（当前 118 项）
- [ ] CLI 八个子命令均可正常执行（fetch / download / feedback / reanchor / daily / serve / watch / ccf）
- [ ] Web 应用可启动，五个页面可访问（/digest /profile /archive /watch /ccf）
- [ ] `arxiv_daily.py daily --serve` 后 `curl --noproxy '*' http://127.0.0.1:8000/api/ping` 返回 200
- [ ] 键盘快捷键工作正常
- [ ] 反馈打分后文件正确更新
- [ ] 幂等：重复 fetch / watch run / ccf run 不产生重复数据
- [ ] `ccf list` 与 `watch list` 只读、不改动仓库文件
