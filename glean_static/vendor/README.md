# 第三方前端库（仓库内自带，不走 CDN）

这里放的是 Web 界面**必需**的两个交互库。它们必须是本地的，不能挂 CDN —— 原因见下。

## 文件

| 文件 | 来源 | 版本 | 许可证 |
|---|---|---|---|
| `htmx.min.js` | `https://unpkg.com/htmx.org@1.9.12/dist/htmx.min.js` | 1.9.12 | BSD-2-Clause |
| `alpine.min.js` | `https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js` | 3.14.1 | MIT |

均未改动，原样保存。

## 为什么不能继续用 CDN

`/watch` 与 `/ccf` 上的**全部**写操作（添加 / 暂停 / 移除 / 勾选 / 标记已读）都靠 `hx-*`
属性，由 htmx 接管；Alpine 负责键盘导航等。此前这两个库走公网 CDN，一旦取不到：

- 所有 `hx-*` 按钮**静默失效** —— 没有请求、没有报错、页面看起来完全正常；
- 旧的 `onclick="setTimeout(()=>location.reload(), 300)"` 仍会整页刷新一次，
  于是症状精确表现为「点了按钮没反应」，而读代码完全正常（2026-09-28 用无头 Edge
  屏蔽 CDN 域名实测复现：`htmx 就绪: False`，点击后服务端条目仍在）。

对一个**本地优先**的工具，把「能不能改名单」押在三个公网 CDN 上是不成立的；
静态快照（`glean/report.py`）本来就坚持零 CDN、断网可读，Web 界面没有理由更弱。

Tailwind 继续走 `https://cdn.tailwindcss.com`：它只影响外观，取不到时页面依然能正常
增删改查（只是变朴素），所以不值得为它增加约 400KB 的仓库体积。

## 升级方式

换版本时替换文件并同步上表的版本号；`glean_static/vendor/` 由 `/static/vendor/`
直接提供（`glean/web/main.py` 把 `glean_static/` 挂到 `/static`），不需要改代码。

## 已知边界：只在源码树里存在

`glean_static/` **不在** `pyproject.toml` 的包数据里，所以它不会进 wheel ——
（`[tool.setuptools.packages.find]` 的名包只有 `glean*` 下带 `__init__.py` 的目录）。
而 `glean/web/main.py` 是「`glean_static/` 目录存在才挂载 `/static`」，于是：

- **editable 安装（`pip install -e .`）**：正常，CI 与文档都用这个；
- **非 editable 安装**：`/static` 不挂载 → 没样式、**没有 htmx** → 又回到「所有按钮静默失效」。

本项目不分发 wheel，所以按现状保留；若日后要出包，需把 `glean_static` 一并纳入包数据
（例如给它加 `__init__.py` 并补 `package-data`）。
