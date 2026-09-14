# API 参考

> 自动生成的 API 文档

## Python API

::: glean.core
    options:
      members:
        - http_get
        - parse_xml
        - fetch_category
        - fetch_all
        - load_interest_entries
        - load_interest_keywords
        - match_keywords
        - annotate_hits
        - excerpt
        - day_section
        - upsert_digest
        - find_paper
        - set_entry_weights
        - patch_rating
        - apply_feedback
        - reanchor_day
        - sanitize_title
        - download_paper
        - save_day_data
        - load_day_data
        - list_available_days

## Web API

::: glean.web.routes
    options:
      members: true

### 存活探测

`GET /api/ping` 是唯一的服务存活口径（无依赖、无副作用），供
`glean.serve.probe()` 与定时任务判断本地 Web 应用是否已在线：

```json
{"status": "ok", "service": "paper-glean", "version": "0.1.0", "time": "2026-09-13T03:30:00+00:00"}
```

## 服务保活

::: glean.serve
    options:
      members:
        - base_url
        - ping_url
        - probe
        - log_path
        - start_background
        - ensure

## 监控内核

> `watch` 与 `ccf` 共用的「名单 → 抓取 → diff → 落盘 → 推送」引擎。
> 本模块**不发任何网络请求**，抓取函数由调用方通过 `MonitorJob` 注入。

::: glean.monitor
    options:
      members:
        - MonitorSpec
        - MonitorJob
        - run_monitor
        - slugify
        - norm_title
        - fingerprint
        - kind_of
        - year_of
        - load_state
        - save_state
        - append_events
        - load_events
        - render_section
        - upsert_digest

## 学者监控

::: glean.watch
    options:
      members:
        - slugify
        - fingerprint
        - load_watchlist
        - add_researcher
        - remove_researcher
        - set_enabled
        - fetch_dblp
        - fetch_s2
        - collect_items
        - load_state
        - save_state
        - append_events
        - load_events
        - render_section
        - upsert_watch_digest
        - run

## 主页解析

::: glean.homeparse
    options:
      members:
        - fetch_html
        - parse_homepage

## 会议期刊监控

::: glean.ccf
    options:
      members:
        - load_venues
        - add_venue
        - remove_venue
        - set_enabled
        - set_enabled_area
        - sync_catalog
        - collect_items
        - load_state
        - save_state
        - append_events
        - load_events
        - render_section
        - upsert_ccf_digest
        - run

## 会议期刊页解析

::: glean.venueparse
    options:
      members:
        - parse_venue_page
        - fetch_rss
        - parse_ccfddl
        - fetch_crossref_issues

## CCF-A 目录

::: glean.ccf_catalog
    options:
      members:
        - catalog

## 推送

::: glean.notify
    options:
      members:
        - push
        - load_new
        - ack_all
        - enabled_channels

## 数据模型

::: glean.web.models
    options:
      members: true
