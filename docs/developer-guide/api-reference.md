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

## 数据模型

::: glean.web.models
    options:
      members: true
