# Web 层详解

> FastAPI + HTMX + Alpine.js 实现

## 架构图

![Web 组件图](../assets/images/web-components.png)

> 图源文件：[web-components.puml](../assets/diagrams/web-components.puml)

## 目录结构

```
glean/web/
├── __init__.py
├── __main__.py      # 入口：python -m glean.web
├── main.py          # FastAPI 应用工厂
├── routes.py        # 路由定义
├── models.py        # Pydantic 模型
├── templates_config.py  # 自定义 Jinja2 模板（解决缓存问题）
└── templates/       # Jinja2 模板
    ├── base.html
    ├── digest.html
    ├── profile.html
    ├── archive.html
    └── partials/    # HTMX 片段模板
        ├── paper_list.html
        ├── paper_card.html
        └── paper_detail.html
```

## 路由分类

### HTML 页面路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 重定向到 /digest |
| `/digest` | GET | Digest 流主页面 |
| `/profile` | GET | 兴趣画像页面 |
| `/archive` | GET | 归档库页面 |

### API 路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/days` | GET | 获取所有可用日期 |
| `/api/papers` | GET | 获取论文列表（支持筛选） |
| `/api/papers/{paper_id}` | GET | 获取单篇论文详情 |
| `/api/interests` | GET | 获取兴趣画像条目 |
| `/api/feedback` | POST | 提交反馈打分 |
| `/api/download/{paper_id}` | POST | 下载 PDF |

### HTMX 片段路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/htmx/paper-list` | GET | 论文列表片段（用于筛选后更新） |
| `/htmx/paper-card/{paper_id}` | GET | 单张卡片片段 |
| `/htmx/paper-detail/{paper_id}` | GET | 详情面板片段 |

## 模板系统

### 自定义模板类

由于 Starlette 的 `Jinja2Templates` 在传递 dict 上下文时会触发缓存 key 的 hash 计算（dict 不可 hash），我们创建了自定义的 `NoCacheJinja2Templates`：

```python
class NoCacheJinja2Templates:
    def __init__(self, directory: str) -> None:
        self.env = Environment(
            loader=FileSystemLoader(directory),
            autoescape=True,
        )

    def TemplateResponse(self, name: str, context: dict, ...):
        template = self.env.get_template(name)  # 不传递 globals
        return _TemplateResponse(template, context, ...)
```

### 模板继承链

```
base.html
├── digest.html
│   └── partials/paper_list.html
│   └── partials/paper_card.html
│   └── partials/paper_detail.html
├── profile.html
└── archive.html
```

## HTMX 模式

### 局部更新

筛选器变更时，HTMX 请求 `/htmx/paper-list` 并替换中间栏内容：

```html
<div hx-get="/htmx/paper-list"
     hx-trigger="change from:.filter"
     hx-target="#paper-list">
```

### 卡片选择

点击卡片时，HTMX 加载详情到右侧面板：

```html
<div hx-get="/htmx/paper-detail/{{ paper.id }}"
     hx-target="#detail-panel">
```

## Alpine.js 状态管理

### 全局 Store

```javascript
function appStore() {
    return {
        selectedPaperIndex: -1,
        papers: [],
        
        handleKeydown(event) {
            // j/k 导航, 1-5 打分, o 打开, d 下载
        },
        
        navigatePaper(direction) {
            // 更新选中状态
        },
        
        rateSelectedPaper(kind, rating) {
            // 发送评分请求
        }
    }
}
```

## 静态文件

```
glean_static/
├── css/
│   └── tailwind.css    # Tailwind 编译后的样式
└── js/
    └── app.js          # Alpine.js 应用逻辑
```

静态文件通过 FastAPI 的 `StaticFiles` 挂载：

```python
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
```
