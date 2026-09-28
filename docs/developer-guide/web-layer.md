# Web 层详解

> FastAPI + HTMX + Alpine.js 实现

## 架构图

![Web 组件图](../assets/images/web-components.png)

> 图源文件：[web-components.puml](../assets/diagrams/web-components.puml)

## 目录结构

```
glean/web/
├── __init__.py
├── __main__.py       # 入口：python -m glean.web
├── main.py           # FastAPI 应用工厂
├── routes.py         # 只做聚合：把下面三个子路由 include 进一个 router
├── routes_papers.py  # 论文流：/digest /profile /archive + /api/* + /htmx/*
├── routes_watch.py   # 学者监控：/watch + /api/watch/*
├── routes_ccf.py     # 会议期刊监控：/ccf + /api/ccf/*
├── common.py         # 三个路由模块共用的助手（取日 / 404 / 过滤 / 运行摘要）
├── models.py         # 线上模型（Pydantic）+ PaperFilters（查询参数组）
├── templates_config.py  # 共享 Jinja2 环境 + 自定义过滤器
└── (模板在 glean/templates/)
```

> 模板目录是 `glean/templates/`（与 `glean/web/` 平级），不是 `glean/web/templates/`。

**一屏一组路由。** `routes.py` 不再承载任何端点，只把三个子路由挂到一起
（`include_router` 不加前缀，因此路径与拆分前逐字相同）；加一个新界面 =
新写一个路由模块 + 在 `routes.py` 加一行。每个模块自带 OpenAPI `tags`
（`papers` / `watch` / `ccf`），`/docs` 因此按界面分组而不是糊成一片。

**共用的东西只有一份。** 三个界面都要「决定看哪一天、过滤、论文不存在就 404」，
这些放在 `common.py`：

| 助手 | 作用 |
|------|------|
| `Filters` | `Annotated[PaperFilters, Depends()]` 类型别名，见下节 |
| `current_papers(filters)` | 「没指定日期就看最新一天」的**唯一**实现（此前在页面 / API / 片段里各写一遍） |
| `require_paper(id)` / `require_entry(rows, key, what)` | 取不到就 404，避免每个端点各写一次查找 |
| `filter_papers` / `hit_visible` | 分类 → 搜索 → 命中类型 → 按分数排序 |
| `run_summary(result)` | 把监控运行结果裁成计数（`RunSummary`），watch / ccf 共用 |

## 路由分类

### HTML 页面路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 重定向到 /digest |
| `/digest` | GET | Digest 流主页面 |
| `/profile` | GET | 兴趣画像页面 |
| `/archive` | GET | 归档库页面 |
| `/watch` | GET | 学者监控面板 |
| `/ccf` | GET | 会议期刊监控面板 |

### API 路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/ping` | GET | 存活探测（无副作用，供 `glean.serve` 与定时任务使用） |
| `/api/days` | GET | 获取所有可用日期（只含真正的日文件） |
| `/api/papers` | GET | 获取论文列表（筛选 + 分页） |
| `/api/papers/{paper_id}` | GET | 获取单篇论文详情 |
| `/api/interests` | GET | 获取兴趣画像条目 |
| `/api/feedback` | POST | 提交反馈打分 |
| `/api/download/{paper_id}` | POST | 下载 PDF |
| `/api/watch/resolve` | POST | **身份解析**：由姓名 / 主页 / DBLP / S2 任一线索反查其余字段，返回提案（不写盘，见 [`glean.resolve`](api-reference.md)） |
| `/api/watch/*` | GET/POST/DELETE | 学者名单增删启停、`new` / `ack`、`events`、`run` |
| `/api/ccf/*` | GET/POST/DELETE | venue 增删启停、`toggle-area`、`refresh`、`new` / `ack`、`events`、`run` |

### HTMX 片段路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/htmx/paper-list` | GET | 论文列表片段（用于筛选后更新） |
| `/htmx/paper-card/{paper_id}` | GET | 单张卡片片段 |
| `/htmx/paper-detail/{paper_id}` | GET | 详情面板片段 |

## 共享筛选参数组

`/digest`、`/api/papers`、`/htmx/paper-list` 接受**完全相同的六个查询参数**，
并共用同一个过滤函数。为避免三处参数表漂移，参数组只在 `models.py` 声明一次，
由 FastAPI 按查询串注入：

```python
# glean/web/models.py
@dataclass
class PaperFilters:
    day: str | None = None
    category: str | None = None
    search: str | None = None
    show_star: bool = True
    show_expand: bool = True
    show_other: bool = False

# glean/web/common.py
Filters = Annotated[PaperFilters, Depends()]

@router.get("/api/papers")
async def api_papers(filters: Filters, limit: int = Query(50, ge=1, le=200), ...):
    ...
```

> 用 `@dataclass` 而非 Pydantic 模型是**有意为之**：FastAPI 对 `BaseModel` 类型的参数
> 按**请求体**解析，只有普通类/数据类才会逐字段从查询串读取。
> 过滤优先级：`category` → `search` → 命中类型（★ 优先于 🧐，两者皆无则归入 Other），
> 最后按 `score_star + score_expand` 降序。

## 模板系统

### 模板环境

`templates_config.py` 只是对 Starlette `Jinja2Templates` 的一层薄封装，
提供目录常量、模板实例与 `format_timestamp` 过滤器：

```python
templates_dir = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

templates.env.filters["format_timestamp"] = format_timestamp
```

> **历史包袱已清除**：早期版本有 `NoCacheJinja2Templates` 子类，用来规避 Starlette
> 把渲染上下文塞进模板缓存 key 的缺陷（`TypeError: unhashable type: 'dict'`），
> 并因此依赖私有符号 `starlette.templating._TemplateResponse`。当前 Starlette
> 只按名字取模板、由 `TemplateResponse` 自行把 `request` 注入上下文，该子类已无必要，
> 连同私有依赖一并删除。
>
> 相应地，所有调用点使用现代签名 `TemplateResponse(request, name, context)`，
> 上下文里**不再需要**手写 `"request": request`。

### 模板契约（partials）

`partials/paper_card.html` 要求调用方提供两样东西：

| 变量 | 内容 |
|------|------|
| `paper` | 一条论文记录；`hits_star` / `hits_expand` 是**命中的关键词**（不是条目标题） |
| `interests` | `load_interest_entries()` 的结果（`title` / `keywords` / `weight`） |

「Why recommended」须用 `interest.keywords` 与 `hits_*` **求交集**来反查条目；
直接用 `interest.title in paper.hits_star` 会永远匹配不上。
论文记录的完整字段见[数据文件格式规范](data-schema.md#paper)。

### 模板继承链

```
base.html（导航项由单一列表生成，桌面/移动两种版式共用）
├── digest.html
│   └── partials/paper_list.html
│       └── partials/paper_card.html
├── partials/paper_detail.html
├── profile.html
├── archive.html
├── watch.html
└── ccf.html
```

## HTMX 模式

### 局部更新

筛选器变更时，HTMX 请求 `/htmx/paper-list` 并替换中间栏内容。六个筛选项必须**一起**提交，
因此每个控件都带同一个 `hx-include` 选择器（在 `digest.html` 里 `{% set %}` 一次、复用六处）：

```html
<select name="category"
        hx-get="/htmx/paper-list"
        hx-target="#paper-list"
        hx-include="[name='day'], [name='category'], [name='search'],
                    [name='show_star'], [name='show_expand'], [name='show_other']">
```

日期下拉走的是整页 `/digest`（`hx-push-url="true"`），搜索框额外带
`hx-trigger="keyup changed delay:300ms"`。

### 卡片选择

点击卡片时，HTMX 加载详情到右侧面板（目标是 `#paper-detail`）：

```html
<div data-paper-id="{{ paper.id }}"
     hx-get="/htmx/paper-detail/{{ paper.id }}"
     hx-target="#paper-detail">
```

## Alpine.js 状态管理

`glean_static/js/app.js` 注册两个 Store（`alpine:init` 时挂载）：

| Store | 挂载点 | 职责 |
|-------|--------|------|
| `appStore()` | `<body>` | 键盘流：`j/k`（或 ↑/↓）移动选中、`1-5` 打分、`Shift+1-5` 打好奇分、`o` 打开、`d` 下载、`/` 聚焦搜索；监听 `htmx:afterSwap` 刷新 `[data-paper-id]` 列表 |
| `digestStore()` | `#paper-list` 所在容器 | 记录当前选中论文并切换卡片高亮 |

```javascript
Alpine.data('appStore', () => ({
    selectedPaperIndex: -1,
    papers: [],          // 由 updatePapers() 从 DOM 的 [data-paper-id] 收集

    init() { /* 收集 + 监听 htmx:afterSwap */ },
    updatePapers() { /* querySelectorAll('[data-paper-id]') */ },
    handleKeydown(event) { /* j/k · 1-5 · Shift+1-5 · o · d · / */ },
    navigatePaper(direction) { /* 移动高亮 + scrollIntoView + 触发卡片 hx-get */ },
    openSelectedPaper() { /* 打开 arXiv 链接 */ },
    downloadSelectedPaper() { /* htmx.ajax POST /api/download/{id} */ },
    rateSelectedPaper(kind, rating) { /* htmx.ajax POST /api/feedback */ },
}));
```

> 导航未读角标（`watch_new_count()` / `ccf_new_count()`）不是 Alpine 状态，
> 而是 `main.py` 注册的 Jinja 全局函数——每次页面渲染现算。

## 静态文件

```
glean_static/
├── css/
│   └── app.css         # 样式（Tailwind CDN + 自定义变量）
├── js/
│   └── app.js          # Alpine.js 应用逻辑 + 统一失败提示
└── vendor/             # htmx / Alpine 的仓库内副本（不再走公网 CDN）
    ├── htmx.min.js
    ├── alpine.min.js
    └── README.md       # 来源、版本、许可证，以及「为什么不再挂 CDN」
```

静态文件通过 FastAPI 的 `StaticFiles` 挂载（目录存在才挂，便于纯 API 场景）：

```python
static_dir = Path(__file__).resolve().parent.parent.parent / "glean_static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
```

## 交互脚本与「不许静默失败」

两条规则，都是踩过坑之后定下来的。

### 一、交互层不从公网 CDN 加载

`base.html` 里 htmx 与 Alpine 指向 `/static/vendor/*`（**仓库自带**），
只有 Tailwind 还留在 CDN。

原因是一次真实的误诊：`/watch` 页「移除」按钮被报「点了没反应」。
服务端查下来完全正常（`DELETE` 返回 200、条目真的没了），最后定位到
**htmx 从 `unpkg.com` 加载失败** —— htmx 没起来，页面上**所有** `hx-*` 按钮就全部失效，
连点击都不会发出请求。而 `hx-confirm` 是 htmx 自己的确认框实现，
**不是** 原生 `window.confirm`，所以连对话框都不弹。

关键区分：

| 依赖 | 取不到时的后果 | 策略 |
|------|----------------|------|
| Tailwind | 页面变朴素，**功能完好** | 继续走 CDN |
| htmx / Alpine | **所有交互静默失效** | 仓库自带静态文件 |

兜底还要**自己报告**：`base.html` 里一段内联脚本在 `DOMContentLoaded` 检查
`window.htmx` / `window.Alpine`，缺失就显示橙色降级横幅（`#ui-degraded`）点名是哪个脚本。

> 附带修掉一个同源问题：`tailwind.config = {…}` 在 CDN 取不到时，
> `tailwind` 是未声明的全局 → 抛未捕获 `ReferenceError`。现改为先 `window.tailwind ||= {}`。

### 二、请求失败必须可见

所有列表操作（`/watch` 与 `/ccf` 的 添加 / 暂停 / 移除 / 全选 / 全不选 / ack / refresh）
统一挂 `hx-on::after-request="pgAfterRequest(event)"`，由 `app.js` 决定下一步：

```javascript
window.pgAfterRequest = function (event) {
    const detail = event.detail || {};
    if (detail.successful) { window.location.reload(); return; }   // 成功才刷新
    // 失败：把原因显示出来，而不是刷新页面把它盖过去
    let reason = /* detail.xhr.responseText 里的 detail 字段 */ '';
    if (!reason) reason = detail.xhr.status ? ('HTTP ' + detail.xhr.status) : '网络请求未送达';
    window.pgToast('操作失败：' + reason);
};
```

约定：**成功才整页刷新；失败一律走右下角 `#action-toast` 提示条**（8 秒自动消失、点击关闭）。

> 以前每个按钮上还带一个 `onclick="setTimeout(()=>location.reload(), 300)"`，
> 本意是「刷新看到结果」，实际效果是**把失败也刷新掉** —— 请求没发出去时页面照样重载一次，
> 用户看到的现象就是「点了没反应」。那个内联 `onclick` 已全部删除，刷新改由
> `htmx:afterRequest` 的成功分支负责。
