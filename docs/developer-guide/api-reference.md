# API 参考

> 自动生成的 API 文档

## Python API

::: glean.core
    options:
      members:
        - http_get
        - http_get_text
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
        - day_files
        - save_day_data
        - load_day_data
        - list_available_days

## Web API

> 一屏一组路由。`glean.web.routes` 只负责把下面三个子路由聚合起来，
> 因此没有端点可列；每个路由模块自带 OpenAPI `tags`（`papers` / `watch` / `ccf`），
> 在 `/docs` 里按界面分组。

::: glean.web.routes_papers
    options:
      members: true

::: glean.web.routes_watch
    options:
      members: true

::: glean.web.routes_ccf
    options:
      members: true

### 路由共用助手

::: glean.web.common
    options:
      members:
        - current_papers
        - require_paper
        - require_entry
        - run_summary
        - hit_visible
        - filter_papers

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
>
> 除**抓取**与**文案**之外的一切都在这一层：状态、事件、digest、启停、移除后遗忘
> 指纹。两个子系统只保留各自的领域知识（抓什么、主语叫什么、写到哪）。

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
        - forget_state
        - set_enabled
        - set_enabled_where
        - append_events
        - load_events
        - render_section
        - upsert_digest

## 条目类型词表

> `kind` 的图标与文案。此前分散在 `watch` / `ccf` / `notify` 三处（`notify` 那份是
> 手工合并副本），已发生漂移；现统一到这个**不依赖任何同层模块**的叶子模块。

::: glean.kinds
    options:
      members:
        - WATCH_KIND_ICONS
        - WATCH_KIND_LABELS
        - CCF_KIND_ICONS
        - CCF_KIND_LABELS
        - KIND_ICONS
        - KIND_LABELS

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

## 身份解析

> 回答「**这是谁**」——与「他最近发表了什么」（`glean.watch`）是两件事，源优先级也不同：
> 监控要**完整覆盖**（主页 → DBLP → S2），解析只要**最先答得出来**的那个源。
> 入口可以是姓名 / 个人主页 / DBLP / Semantic Scholar 四者之一。
>
> **本模块刻意不抓 DBLP**：它已启用 Anubis 反爬，每个请求都返回人机校验页
> （浏览器 UA / 程序 UA × 代理 / 直连，四种组合实测一致）→ 拿到的永远不是数据。
> 因此遇到 DBLP 值只**记录为链接与姓名线索**，并把 `DBLP_UNFETCHABLE` 作为警告
> 显式返回，而不是让一次失败的抓取伪装成「查无此人」。
>
> 返回值是一个**提案**，不是静默写入：每个字段都带来源（`evidence`），
> 同名的多个候选走 `alternates` 交给用户挑，`needs_review` 标出「姓名是推断来的」。

::: glean.resolve
    options:
      members:
        - looks_like_person_name
        - name_from_title
        - links_from_homepage
        - name_from_homepage
        - normalize_dblp
        - normalize_s2
        - s2_author
        - s2_search
        - dblp_search_url
        - resolve
        - DBLP_AUTHOR_SEARCH
        - DBLP_UNFETCHABLE
        - S2_GRAPH
        - S2_RATE_LIMITED

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

> **展示面是 HTML，不是弹窗。** 本模块只有两个通道：`file`（把未读条目写进
> `data/<ns>_new.json`，供页面渲染 `NEW` 徽标）与可选的 `webhook`（唯一出网通道）。
> 页面的另一半见下面的「静态快照：渲染」与 Web 层的 `/watch` `/ccf`。

::: glean.notify
    options:
      members:
        - push
        - load_new
        - ack_all
        - enabled_channels

## 静态快照：共享构件

> 三条链路（arXiv 日报 / 学者监控 / CCF 监控）的独立 HTML 共用这一层：
> 内联样式、渐进增强脚本、HTML 转义、筛选控件与页面外壳。
> **stdlib only**（纯字符串拼装，不引 Jinja2 —— CLI-only 安装下 Jinja2 并不存在）。

::: glean.htmlkit
    options:
      members:
        - STYLE
        - SCRIPT
        - escape
        - controls
        - page

## 静态快照：渲染

> 把一天的数据渲染成 `exports/<namespace>-digest-<day>.html`。
> arXiv 线的推荐理由**从 `arXiv-schedule.md` 反解析**而非重算；
> 监控线零新增**也出页面**（因为「跑了且什么都没发现」本身是证据）。

::: glean.report
    options:
      members:
        - MonitorView
        - build_html
        - build_monitor_html
        - render_day
        - render_monitor_day
        - monitor_export_path
        - latest_export
        - latest_monitor_export
        - group_by_category
        - parse_recommendations

## 数据模型

::: glean.web.models
    options:
      members: true
