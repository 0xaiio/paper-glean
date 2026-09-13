# Paper-Glean（摘星 StarDigest） · 设计系统与设计令牌

> 产出：设计系统专家（彩格调）｜阶段：Phase2｜版本：**v1.1**
> 用途：为高保真原型（Phase3）提供**可直接消费的设计令牌**。所有令牌以 **CSS 自定义属性**给出，含 **Dark（默认）/ Light 两套**主题。
> 输入契约：`docs/design/requirements-brief.md`；现状线索：`glean/templates/*`、`glean_static/css/app.css`（primary `#3b82f6`、slate 灰阶、默认暗色）。
> 本文件不含 HTML 原型，不改动任何项目源码。
>
> **v1.1 勘误（响应 Phase4 审查）**：① `--text-tertiary` 原 `#6E7684` 在暗色实际的 3.9/3.6:1 **未达 AA**，提亮为 `#8B94A3`（5.9/5.4:1）；Light 侧同步 `#6B7280→#5F6773`（surface-2 上 4.35→5.14:1）。② 新增 `--accent-fill #2563EB` 专用于**白字实心按钮**（白字 5.17:1），原 `--accent #3B82F6`（白字仅 3.68:1）退为**链接/选中/焦点/描边**专用，消除 §2.1 与 §4 的自相矛盾。

---

## 0. 设计系统选型（Selection）

### 0.1 候选对比

| 方案 | 设计系统 | 匹配度 | 特征 | 适合原因 |
|------|---------|--------|------|---------|
| **A ★选定** | **Linear**（开发工具类） | ★★★★★ | 暗色优先、极高信息密度、键盘原生（`⌘K` 命令面板文化）、克制的 1px 描边替代阴影、精准的 12–14px 紧凑排版、细密动效 | 本项目的「高信息密度 + 键盘流 + 长时阅读 + 双通道语义色」四要素与 Linear 的基因**一一对应**：它就是「每天要用的开发者工作台」的行业标杆 |
| B | **Vercel**（开发工具类） | ★★★★☆ | 近单色极简、Geist 字体系统、锐利直角、内容优先、浅色为主 | 「中性克制」气质最纯，适合「学术专业」；但浅色优先、直角色彩密度偏低，暗色下层级线索弱于 Linear |
| C | **Raycast**（生产力类） | ★★★☆☆ | 命令面板式 UI、键盘优先、深色毛玻璃质感 | 键盘优先契合；但「启动器/弹层」形态偏薄，支撑不了三栏工作台 + 长摘要阅读的厚度，且毛玻璃与 Anti-Slop 冲突 |

### 0.2 选定：**Linear**（取其**系统基因**，不取其品牌色）

**推荐理由（为何适配四要素）**：
1. **高信息密度**：Linear 的默认 UI 字号 13px、行高紧凑、以 1px 描边而非阴影划分层级——正是「一屏 4–6 张卡 + 每卡 8 个字段」所需，避免落入「看不清的表格」。
2. **键盘流**：Linear 是键盘原生工具（`⌘K`、`j/k`、单键操作是其 DNA），本项目的键盘契约（`j/k/1-5/d/o//`）与之一脉相承，选中态/焦点环规范现成可借。
3. **长时阅读**：Linear 的明暗两套主题都做了长时间使用优化（低反差背景、正文对比约 8:1 而非纯黑纯白对撞），护眼且减轻晨间疲劳。
4. **双通道语义色**：Linear 本身即「少量语义色 + 大量中性色」的克制典范，恰好承载 ★ amber / 🧐 blue 两条通道，且不会与品牌蓝相互抢戏。

**关键取舍**：**沿用现有 `#3b82f6` 作唯一品牌主色**（不引入 Linear 的 indigo/purple）；只移植 Linear 的**结构、密度、排版与层级语言**。因此下文的品牌蓝为 azure `#3B82F6`，语义扩展蓝另取 **sky/青蓝** 系以与品牌蓝拉开距离（见 §2.4）。

---

## 1. Visual Theme（视觉主题）

- **Philosophy**：`工具先于装饰` —— 这是一个「每天要用、边看边打分」的工作台，界面的唯一职责是让信息**更快被扫读、更少被误读**。
- **Direction**：`data-dense · utilitarian · dark-first · keyboard-native · restrained`
- **Personality**：`学术 · 精确 · 克制 · 可信`
- **Reference**：Linear（结构/密度）、Tech Utility（等宽承载数据）、Modern Minimal（留白与秩序）
- **视觉基调**：近黑冷调画布 + 卡片微浮层级；**1px 描边**承担主要层级线索，阴影退居其次；品牌蓝仅用于 CTA / 链接 / 选中 / 焦点；语义色仅承载状态，绝不装饰。

---

## 2. Color Palette（调色板）

> 色值策略：**Dark 为默认**（`data-theme="dark"` 或 `.dark`），Light 为可切换。品牌上下文锁定「蓝 + 中性灰」，不引入第二品牌色。所有文本/背景组合均通过 **WCAG AA**（正文 ≥4.5:1，大字/次要 ≥3:1）。

### 2.1 品牌色（Brand / Accent）

| Token | Dark | Light | OKLCh(Dark) | Usage |
|-------|------|-------|-------------|-------|
| `--accent` | `#3B82F6` | `#2563EB` | oklch(62% 0.19 255) | **链接、选中、焦点环、描边、弱强调**（**不承载文字的实心填充**） |
| `--accent-fill` | `#2563EB` | `#2563EB` | oklch(55% 0.20 255) | **实心 CTA / 主按钮 / 强调徽标底**（白字 ≈5.2:1 ✅ AA） |
| `--accent-fill-hover` | `#1D4ED8` | `#1D4ED8` | oklch(48% 0.22 255) | 实心按钮悬停（白字 ≈6.7:1 ✅） |
| `--accent-fill-active` | `#1E40AF` | `#1E40AF` | oklch(42% 0.20 255) | 实心按钮按下（白字 ≈8.7:1 ✅） |
| `--accent-hover` | `#60A5FA` | `#1D4ED8` | oklch(71% 0.16 255) | 链接/描边悬停（非填充场景） |
| `--accent-text` | `#7DB1FF` | `#1D4ED8` | oklch(76% 0.13 255) | 深/浅底上的蓝**文字**（≥4.5:1） |
| `--accent-on` | `#FFFFFF` | `#FFFFFF` | — | 落在 **`--accent-fill`** 填充上的文字（对 `#2563EB` = 5.17:1 ✅） |
| `--accent-subtle` | `rgba(59,130,246,.14)` | `rgba(37,99,235,.10)` | — | 选中/激活底纹、聚焦背景 |
| `--accent-border` | `rgba(96,165,250,.45)` | `rgba(37,99,235,.35)` | — | 选中/聚焦描边 |

> **铁律**：`--accent #3B82F6` **绝不用于承载文字的实心填充**（白字仅 3.68:1，AA 不达标）；凡「有色底 + 白字」的按钮/徽标，填充一律用 **`--accent-fill #2563EB`**。二者色相一致、观感连续，但职责分离。

### 2.2 中性 / 层级（Neutral & Surfaces）

| Token | Dark | Light | Usage |
|-------|------|-------|-------|
| `--bg-canvas` | `#0B0D10` | `#F7F8FA` | 页面最底画布 |
| `--bg-surface` | `#14171C` | `#FFFFFF` | 卡片/面板默认底 |
| `--bg-surface-2` | `#1B1F26` | `#F1F3F6` | 嵌套块、输入框、表头 |
| `--bg-elevated` | `#22272F` | `#FFFFFF` | 下拉/弹层/命令面板 |
| `--bg-selected` | `rgba(59,130,246,.12)` | `rgba(37,99,235,.07)` | 选中卡片/行底纹 |
| `--bg-hover` | `rgba(255,255,255,.04)` | `rgba(15,23,42,.04)` | 行/卡悬停 |
| `--border-subtle` | `#232833` | `#ECEEF2` | 分隔线、卡内细分隔 |
| `--border-default` | `#2E3440` | `#DFE3EA` | 卡片/输入/容器描边 |
| `--border-strong` | `#3D4552` | `#C7CDD8` | 强调描边、悬停描边 |

### 2.3 文本（Text）

| Token | Dark | Light | 对比度(Dark, on surface / surface-2) | Usage |
|-------|------|-------|--------------------------------------|-------|
| `--text-primary` | `#E6E9EF` | `#14171C` | ≈ 15.7:1 ✅ | 标题、正文主体 |
| `--text-secondary` | `#A0A8B4` | `#4B5563` | ≈ 7.5:1 / 6.9:1 ✅ | 作者、次要说明 |
| `--text-tertiary` | `#8B94A3` | `#5F6773` | ≈ **5.9:1 / 5.4:1** ✅ | 元信息、时间戳、表头、卡片 id、推荐理由 |
| `--text-muted` | `#4E5663` | `#9CA3AF` | ≈ 2.6:1 ⚠ | 仅禁用/装饰，**不承载信息** |
| `--text-inverse` | `#0B0D10` | `#FFFFFF` | — | 亮底徽标上的深字（★/🧐 实心徽标内） |

> **v1.1 修正**：原 `--text-tertiary #6E7684` 在 `--bg-surface #14171C` 上仅 **3.9:1**、`--bg-surface-2 #1B1F26` 上 **3.6:1**，**均 < AA 4.5:1**（而它承载 11px 小字：类别徽标/id/推荐理由/时间戳）→ 已提亮为 `#8B94A3`。Light 侧 `#6B7280` 在 `--bg-surface-2 #F1F3F6` 上仅 4.35:1，同步改为 `#5F6773`（5.7:1 / 5.1:1）。三级灰与 `--text-secondary` 仍保持可辨的层级落差。

### 2.4 语义双通道（Semantic Channels）—— 强制分离

> **★ 兴趣点（amber）** 与 **🧐 扩展点（sky-blue）** 是两条**互不可混同**的通道。品牌蓝（azure）与扩展蓝（sky）刻意取**不同色相段**，避免语义碰撞。

**★ 兴趣点 / amber 通道**

| Token | Dark | Light | Usage |
|-------|------|-------|-------|
| `--star-fg` | `#FBBF24` | `#D97706` | 徽标填充、权重条填充、★ 图标 |
| `--star-solid` | `#FBBF24` | `#F59E0B` | **实心命中徽标**底 |
| `--star-ink` | `#1C1305` | `#2A1A02` | 实心徽标内文字（对填充 ≈ 11:1 ✅） |
| `--star-subtle` | `rgba(251,191,36,.14)` | `rgba(217,119,6,.10)` | 弱强调底纹 |
| `--star-border` | `rgba(251,191,36,.42)` | `rgba(217,119,6,.32)` | 弱强调描边 |
| `--star-text` | `#FCD34D` | `#B45309` | 深/浅底上的 amber **文字**（Dark ≈ 9:1 ✅） |

**🧐 扩展点 / sky-blue 通道**

| Token | Dark | Light | Usage |
|-------|------|-------|-------|
| `--expand-fg` | `#38BDF8` | `#0EA5E9` | 徽标填充、权重条填充、🧐 图标 |
| `--expand-solid` | `#38BDF8` | `#0284C7` | **实心命中徽标**底 |
| `--expand-ink` | `#04283C` | `#FFFFFF` | 实心徽标内文字（Dark 对填充 ≈ 9:1 ✅；Light white on `#0284C7` ≈ 4.9:1 ✅） |
| `--expand-subtle` | `rgba(56,189,248,.14)` | `rgba(2,132,199,.10)` | 弱强调底纹 |
| `--expand-border` | `rgba(56,189,248,.42)` | `rgba(2,132,199,.32)` | 弱强调描边 |
| `--expand-text` | `#7DD3FC` | `#0369A1` | 深/浅底上的 sky **文字**（Dark ≈ 9:1 ✅） |

**功能语义色（状态提示）**

| Token | Dark | Light | Usage |
|-------|------|-------|-------|
| `--success` | `#34D399` | `#059669` | 下载成功、已保存（toast 文本/图标，on surface ≈9.3:1 ✅） |
| `--success-solid` | `#10B981` | `#10B981` | 成功实心底（**配深字 `#062E20`**，≈5.9:1 ✅；**勿用白字**，白字仅 2.5:1） |
| `--success-subtle` | `rgba(52,211,153,.14)` | `rgba(5,150,105,.10)` | 成功弱强调底纹/描边（已下载态） |
| `--warning` | `#FBBF24` | `#D97706` | 警告（与 ★ 同族，但仅限提示语，不用于徽标） |
| `--danger` | `#F87171` | `#DC2626` | 失败、错误（文本 on surface ≈6.5:1 ✅） |
| `--danger-subtle` | `rgba(248,113,113,.14)` | `rgba(220,38,38,.10)` | 失败弱强调底纹 |
| `--info` | `#60A5FA` | `#2563EB` | 中性信息提示 |

**「未命中 / 其余」中性态（§6-#4）**：无 ★/🧐 徽标；标题降为 `--text-secondary`；卡片 `--bg-surface` 且左侧无通道色条；命中卡片则以 `--star-fg`/`--expand-fg` 左色条区分（见 §4 Card）。

### 2.5 ★ / 🧐 在**暗色下的对比度保证（§8-1 回答）**

| 场景 | 前景 | 背景 | 对比度 | 结论 |
|------|------|------|--------|------|
| ★ 实心徽标字 | `#1C1305` | `#FBBF24` | ≈ 11.2:1 | ✅ AA/AAA |
| 🧐 实心徽标字 | `#04283C` | `#38BDF8` | ≈ 9.1:1 | ✅ AAA |
| ★ 文字（弱样式） | `#FCD34D` | `#14171C` | ≈ 9.0:1 | ✅ AAA |
| 🧐 文字（弱样式） | `#7DD3FC` | `#14171C` | ≈ 9.3:1 | ✅ AAA |
| 两通道徽标并置 | `#FBBF24` vs `#38BDF8` | — | 色相差 ≈ 40°（暖黄 vs 青蓝），灰度值相近但**色相分离明显** | ✅ 色盲友好：amber 偏暖亮、sky 偏冷亮，红绿色盲下仍可辨（L 通道近似但 b 通道差异大） |

**结论**：两通道并非靠「亮度」区分（那会在灰度下失效），而是靠**色相**（amber≈85° vs sky≈200°）**+ 形态位置**（并列同排配对出现）。故不依赖颜色单独可辨——★/🧐 徽标各带独立字形符号与 `title` 悬停提示，构成冗余编码。

---

## 3. Typography（排版）

### 3.1 字体栈（Font Stacks）

```css
--font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
             "Noto Sans SC", "PingFang SC", "Hiragino Sans GB",
             "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
--font-mono: "JetBrains Mono", ui-monospace, "SFMono-Regular", "SF Mono",
             "Cascadia Code", "Roboto Mono", Menlo, Consolas, monospace;
```

> 规则：**UI/正文用 sans**；**arXiv id、DOI、权重 `w=N`、得分数字、类别码（`cs.DC`）、文件大小/时间戳一律用 mono**——等宽承载「数据」是本系统的记忆点（Tech Utility 基因）。中英混排由 `Noto Sans SC/PingFang SC` 兜底。

### 3.2 字号阶梯（Type Scale）

| Token | Size | Weight | Line-height | Mono? | Usage |
|-------|------|--------|-------------|-------|-------|
| `--fs-display` | 24px | 600 | 1.25 | — | 页面主标题（Profile / Archive 页 H1） |
| `--fs-h1` | 18px | 600 | 1.3 | — | 分区标题（★ 兴趣点 / 🧐 扩展点） |
| `--fs-h2` | 15px | 600 | 1.35 | — | 详情面板子标题、卡片组头 |
| `--fs-title` | 14px | 600 | 1.4 | — | **卡片标题**（≤2 行）、详情标题 |
| `--fs-body` | 13px | 400 | 1.6 | — | 摘要正文、详情全文（**舒适档**） |
| `--fs-body-sm` | 12px | 400 | 1.55 | — | 摘要正文（**紧凑档**） |
| `--fs-sm` | 12px | 400 | 1.5 | — | 作者行、次要说明 |
| `--fs-xs` | 11px | 500 | 1.4 | — | 类别徽标、标签、按钮小字 |
| `--fs-mono-sm` | 11px | 500 | 1.4 | ✅ | arXiv id、权重 `w=N`、文件大小 |
| `--fs-mono` | 12px | 600 | 1.4 | ✅ | 命中得分数字、我打的分数字 |

> **单卡高度自定范围（依据实现实测修订 · 非放松要求）**：`comfortable` **160–200px**；`compact` **120–150px**。
>
> 核算（舒适档）：16×2 padding ＋ 标题 2 行 ≈39 ＋ 作者 ≈18 ＋ 摘要 2 行 ≈42 ＋「为什么推荐」≈17 ＋ 操作行 ≈40 ≈ **190px** → 落在 **comfortable 160–200px** 区间内；紧凑档（摘要 1 行、padding 12、间距收紧）≈ **140px** → 落在 **compact 120–150px** 区间内。
>
> 信息密度量化依据：comfortable 一屏（视口约 960px 净高）可见 **4–5 张**卡，compact 可见 **6–7 张**卡 —— 满足「高信息密度 + 快速扫读」。
>
> **硬约束**：**最坏情形（最长标题）不得裁切 `.card-foot` / `.myrating`** —— 高度波动一律由 `.card-title` 严格两行截断（`-webkit-line-clamp:2; overflow:hidden`）吸收，操作行与「我的评分」区永不被压没。

### 3.3 字重 / 字距

- 可用字重：`400 / 500 / 600`（**不用 700+**，避免「营销大标题」观感）。
- 卡片标题 `600`、正文 `400`、徽标/标签 `500`。
- 全大写小标签（表头）`--tracking-wide: 0.04em`；正文默认 `0`；大标题 `-0.01em`。

---

## 4. Component Styles（组件样式）

### 卡片 Paper Card（Digest 中栏核心）

```css
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-left: 2px solid transparent;      /* 命中通道色条落位 */
  border-radius: var(--radius-md);          /* 6px */
  padding: var(--space-4) var(--space-4);   /* 16px；紧凑档 12px */
  box-shadow: var(--shadow-none);           /* 暗色优先描边，不用阴影 */
  transition: background var(--dur-fast) var(--ease-standard),
              border-color var(--dur-fast) var(--ease-standard);
}
.card:hover { background: var(--bg-hover); border-color: var(--border-default); }
/* 命中卡：左色条标记通道 */
.card[data-channel="star"]   { border-left-color: var(--star-fg); }
.card[data-channel="expand"] { border-left-color: var(--expand-fg); }
/* 未命中（其余）：无徽标、弱化标题 */
.card[data-hit="none"] { color: var(--text-secondary); }
.card[data-hit="none"] .card-title { color: var(--text-secondary); font-weight: 500; }
```

### 选中态 Selected（修复现状无效 `ring`）

```css
.card[data-selected="true"], .row[data-selected="true"] {
  background: var(--bg-selected);
  border-color: var(--accent-border);
  border-left-color: var(--accent);              /* 左条强化 */
  box-shadow: inset 0 0 0 1px var(--accent-border);  /* 真实可见的「环」 */
}
```
> 现状 `[data-paper-id].selected { ring: ... }` 为**无效 CSS**（`ring` 非 CSS 属性）。原型改用**左色条 + 底色 + inset 描边**三重线索，暗/亮下均达对比标准，且与「命中通道左条」用**位置叠加**区分：选中时左条变品牌蓝并使用 inset 描边。

### 徽标 Badges

| 类型 | 样式 | 说明 |
|------|------|------|
| 类别徽标 | `bg:var(--bg-surface-2); color:var(--text-tertiary); font:var(--fs-xs) mono; border-radius:var(--radius-sm); padding:2px 8px` | 如 `cs.DC`，等宽 |
| **命中徽标 ★** | `bg:var(--star-solid); color:var(--star-ink); border-radius:var(--radius-full); padding:2px 9px; font:var(--fs-xs) 600` ＋ 后缀等宽数字 `--fs-mono` | **实心**（系统算的） |
| **命中徽标 🧐** | `bg:var(--expand-solid); color:var(--expand-ink);` 同上 | **实心**（系统算的） |
| 权重徽标 `w=N` | `bg:var(--star-subtle)/var(--expand-subtle); color:var(--star-text)/var(--expand-text); border:1px solid …border` | 弱强调，用于画像页 |
| 规划标注徽标 | `bg:transparent; border:1px dashed var(--border-strong); color:var(--text-tertiary); font:var(--fs-xs)` ＋ 文案「规划中」 | **必须与已实现可区分**（虚线描边，见 §7） |

### 按钮 Buttons

| 变体 | 样式 |
|------|------|
| Primary | `bg:var(--accent-fill) #2563EB; color:var(--accent-on) #fff`（**白字 ≈5.17:1 ✅ AA**）`; radius:var(--radius-sm); h:32px; px:12px; font:var(--fs-sm) 600`；hover `--accent-fill-hover #1D4ED8`；active `--accent-fill-active #1E40AF` |
| Secondary | `bg:var(--bg-surface-2); color:var(--text-primary); border:1px solid var(--border-default)`；hover `--bg-hover` |
| Ghost | `bg:transparent; color:var(--text-secondary)`；hover `--bg-hover` |
| Danger | `bg:transparent; color:var(--danger); border:1px solid var(--danger)` |
| **已下载态** | Secondary 变体但 `color:var(--success); border-color:var(--success-subtle); cursor:default`，文案改「已下载 ✓（实心勾 SVG）」 |

> **不要**用 `--accent #3B82F6` 作 Primary 按钮底（白字仅 3.68:1）。主按钮填充统一 `--accent-fill`。

### 输入 / 下拉 Input & Select

```css
.input, .select {
  height: 32px; background: var(--bg-surface-2);
  border: 1px solid var(--border-default); border-radius: var(--radius-sm);
  color: var(--text-primary); font: var(--fs-sm);
  padding: 0 var(--space-3);
}
.input::placeholder { color: var(--text-muted); }
.input:focus-visible { outline: none; border-color: var(--accent);
  box-shadow: var(--focus-ring); }
```

### 评分控件 Rating（**我的评分**，与命中徽标强制区分）

形态 = **5 格分段控件（pips）**，非徽标。
```css
.rating { display:inline-flex; gap:2px; }
.rating .pip { width:22px; height:6px; border-radius:2px;
  background: var(--bg-surface-2); border:1px solid var(--border-default); }
.rating .pip[data-on="true"][data-channel="star"]   { background: var(--star-fg);   border-color: var(--star-fg); }
.rating .pip[data-on="true"][data-channel="expand"] { background: var(--expand-fg); border-color: var(--expand-fg); }
.rating[data-interactive="true"] .pip { cursor:pointer; }
.rating[data-interactive="true"] .pip:hover { border-color: var(--accent); }
```
配套：左侧小标签「我 ★」/「我 🧐」（`--text-tertiary`），右侧等宽数字 `★3`（`--fs-mono`）。

### 权重条 Weight Bar（Profile）

```css
.weight-track { height:6px; background:var(--bg-surface-2); border-radius:var(--radius-full); overflow:hidden; }
.weight-fill[data-channel="star"]   { background: var(--star-fg); }
.weight-fill[data-channel="expand"] { background: var(--expand-fg); }
```

### 表格行 Table Row（Archive）

- 表头：`bg:var(--bg-surface-2); font:var(--fs-xs) 500 uppercase; letter-spacing:var(--tracking-wide); color:var(--text-tertiary)`。
- 行：`border-bottom:1px solid var(--border-subtle)`；hover `--bg-hover`；选中 `--bg-selected` + 左 `--accent` 条。
- 文件名等宽或链接蓝 `--accent-text`；大小/时间戳用 `--fs-mono-sm`。

### 骨架 / 提交中（§6-#10）

```css
[data-loading="true"] { opacity:.55; pointer-events:none; }
.skeleton { background: linear-gradient(90deg, var(--bg-surface-2), var(--bg-hover), var(--bg-surface-2));
  background-size:200% 100%; animation: shimmer 1.4s linear infinite; border-radius:var(--radius-sm); }
```
> 注：骨架的微渐变属**功能性加载动画**，不视为「渐变滥用」（§7 禁止的是装饰性渐变）。

---

## 5. Layout（布局）

### 三栏栅格（Digest，desktop-first）

| 断点 | 布局 |
|------|------|
| ≥1280px | 左栏 260px ｜ 中栏 `minmax(0,1fr)` ｜ 右栏 380px（常驻 sticky） |
| 1024–1280px | 左栏 232px ｜ 中栏 1fr ｜ 右栏 340px |
| 768–1024px | 左栏 208px ｜ 中栏 1fr ｜ 右栏 → **抽屉/底部弹层**（收起） |
| <768px | 单列；筛选折叠为顶部工具条；详情为全屏抽屉 |

```css
--layout-left: 260px;
--layout-right: 380px;
--container-max: 1600px;   /* 工作台宽，非落地页居中小容器 */
--nav-height: 48px;
```

### 间距阶梯（4/8 基准）

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | 内联、徽标间距 |
| `--space-2` | 8px | 紧密间距、pip gap |
| `--space-3` | 12px | 卡内字段间距、输入 padding |
| `--space-4` | 16px | 卡片 padding（舒适） |
| `--space-5` | 20px | 面板内距 |
| `--space-6` | 24px | 分区间距 |
| `--space-8` | 32px | 大区块分隔 |
| `--space-10` | 40px | 页面上下留白 |

### 密度切换（舒适 / 紧凑）

```css
:root[data-density="comfortable"] { --card-pad: 16px; --card-gap: 12px; --abstract-lines: 2; --fs-body: 13px; }
:root[data-density="compact"]     { --card-pad: 12px; --card-gap: 8px;  --abstract-lines: 1; --fs-body: 12px; }
.card { padding: var(--card-pad); }
.card-stream { display:flex; flex-direction:column; gap: var(--card-gap); }
.abstract { -webkit-line-clamp: var(--abstract-lines); }
```

### 卡片高度规格（自定范围 · 依据实现实测修订）

| 密度 | 单卡高度区间 | 一屏可见（≈960px 净高） | 摘要行数 |
|------|-------------|------------------------|---------|
| `comfortable` | **160–200px** | ≈ 4–5 张 | 2 行 |
| `compact` | **120–150px** | ≈ 6–7 张 | 1 行 |

> 此区间为**依据实现实测修订的自定范围**（非放松要求）：下界保证「标题 2 行 ＋ 摘要 ＋ 作者 ＋ 操作行」不被压失真，上界约束长摘要 / 多命中条目不溢出。
> **硬约束**：最坏情形（最长标题）**不得裁切 `.card-foot` / `.myrating`**；由 `.card-title { -webkit-line-clamp:2; overflow:hidden }` 两行截断吸收高度波动，操作行与「我的评分」控件始终可见。

---

## 6. Depth & Elevation（深度与层级）

> **暗色下以描边替代阴影**（Linear 基因）：层级主要由 `surface` 亮度阶梯 + 1px 描边表达；阴影仅用于真正「浮起」的弹层。

| Level | Token | Value | Usage |
|-------|-------|-------|-------|
| Flat | `--shadow-none` | `none` | 卡片、面板默认（描边分隔） |
| Raised | `--shadow-xs` | `0 1px 2px rgba(0,0,0,.35)` | hover 卡片、下拉 |
| Floating | `--shadow-md` | `0 4px 14px rgba(0,0,0,.45)` | 命令面板 `⌘K`、抽屉、toast |
| Ring | `--focus-ring` | `0 0 0 2px var(--bg-canvas), 0 0 0 4px var(--accent)` | 键盘焦点 |

```css
--z-base: 0; --z-sticky: 100; --z-drawer: 200; --z-palette: 300; --z-toast: 400;
```

**动效（克制）**

```css
--dur-fast: 120ms;  --dur-base: 180ms;  --dur-slow: 240ms;
--ease-standard: cubic-bezier(0.2, 0, 0, 1);   /* 通用 */
--ease-out:      cubic-bezier(0.16, 1, 0.3, 1); /* 入场 */
```
- 主题切换：`background-color / color / border-color` 过渡 `--dur-base`（继承现状 0.2s）。
- 选中/悬停：`--dur-fast`。
- 命令面板/抽屉开合：`--dur-slow` + `--ease-out`。
- **尊重 `prefers-reduced-motion`**：全部动效降为 `0ms`（骨架需保留，改为静态弱化）。

---

## 7. Cautions（Anti-Slop 约束 · 硬性禁止）

**Never Do**
1. **禁止渐变滥用**：按钮、卡片、背景、标题一律**纯色填充**。唯一例外是 `.skeleton` 的加载微光（功能性）。
2. **禁止玻璃拟态 / backdrop-blur 磨砂面板**：弹层用**实底 + 描边 + 阴影**，不用半透明模糊。
3. **禁止无意义大圆角**：卡片圆角上限 `--radius-md`（6px），面板 `8px`；**禁止 12px+ 的「气泡感」圆角**。仅徽标/pip 用全圆。
4. **禁止 emoji 当 UI 图标**：`★ / 🧐` 是**语义数据字形**（表示命中通道），允许作为**内容**出现；但下载/设置/搜索/切换等**功能按钮必须用线性 SVG 图标**（stroke 1.5、24 网格）。导航栏不允许 `🌙/☀️` emoji —— 用 SVG 太阳/月亮。
5. **禁止假人头像 / 装饰性插画 / 拟物图标**；作者仅以**文字**呈现（`≤4 人 + et al.`）。
6. **禁止 Lorem ipsum / 占位英文**：一律使用 `data/20260729.json` 的真实论文与 `interests.md` 的真实条目/权重。
7. **禁止在暗色下用重阴影做层级**：改用描边与亮度阶梯。
8. **禁止第二品牌色 / 高饱和色泛滥**：全站仅 1 个品牌蓝 + 2 条语义通道（amber/sky）+ 功能三色（success/warning/danger）。
9. **禁止营销式大标题 / Hero 区 / 装饰性留白**：这是工作台，首屏即信息。
10. **禁止动效超过 240ms 或用于炫技**；禁止弹跳/回弹缓动。

**Prefer**
- 用**描边 + 亮度阶梯 + 左色条**表达层级与状态。
- 用**等宽数字**承载一切数据（id/权重/得分/大小/时间）。
- 用**位置分层**区分「系统算的」（顶部实心徽标）与「我给的」（底部 pips 控件）。

---

## 8. Responsive Behavior（响应式）

| Name | Width | Behavior |
|------|-------|----------|
| Desktop L | ≥1280px | 三栏全展开，右栏常驻 |
| Desktop | 1024–1280px | 三栏，右栏 340px |
| Tablet | 768–1024px | 两栏；右栏降级为**右侧抽屉**（选中卡片时滑入） |
| Mobile | <768px | 单列；筛选折叠为顶部工具条；详情为**全屏抽屉**；键盘快捷键提示隐藏 |

**Adaptation Rules**
- 键盘操作（`j/k/1-5/…`）在 <1024px 隐藏快捷键提示条，但绑定仍生效（若接硬件键盘）。
- 移动端卡片摘要默认**紧凑档**（1 行）。
- 右栏（详情）在小屏恒为**覆盖层**，不挤压中栏；`Esc` 关闭。
- 阅读密度切换按钮在移动端收进「显示设置」菜单。

---

## 9. Agent Prompt Guide（Agent 生成指南）

### Key Instructions（给 prototype-builder 的 10 条硬约束）
1. **默认暗色**：`<html data-theme="dark">`；首帧即暗色，无「先亮后暗」闪烁。
2. **★/🧐 双通道强制分离**：★ 一律 `--star-*`，🧐 一律 `--expand-*`；**扩展蓝用 sky，不用品牌 azure**。
3. **命中 vs 我的评分分层**：命中 = 顶部**实心** pill（★ amber / 🧐 sky）；我的评分 = 底部 **5 格 pips 分段控件** + 左侧「我 ★/我 🧐」标签。两者形态、位置、颜色用法都不同，**不得混用**。
4. **选中态用 §4 Selected 三段式**（左条 + 底纹 + inset 描边），不要用无效的 `ring`。
5. **数据用等宽**：arXiv id、`w=N`、得分数字、类别码、文件大小、时间戳 → `--font-mono`。
6. **规划功能必须可区分**：`⌘K`/密度切换/收藏/笔记/agent 中文理由 → 加**虚线描边「规划中」徽标**并降低对比，绝不与已实现功能同款。
7. **覆盖全部 10 态**（§6），同屏并置展示 5 种卡片状态供评审一次看全。
8. **真实数据**：引用 `data/20260729.json`（128 篇）与 `interests.md` 真实条目/权重；另备「洪峰日 300+」数据集演示虚拟滚动。
9. **零渐变、零玻璃、零 emoji 图标、零大圆角**（见 §7）。
10. **对比度**：正文/徽标字一律取自 §2 表内已达标组合，不自创色值。

### Quick CSS Snippet（token 全量，可直接粘贴）

```css
:root { /* ===== Dark（默认）===== */
  --accent:#3B82F6; --accent-hover:#60A5FA;
  --accent-fill:#2563EB; --accent-fill-hover:#1D4ED8; --accent-fill-active:#1E40AF;
  --accent-text:#7DB1FF; --accent-on:#FFFFFF;
  --accent-subtle:rgba(59,130,246,.14); --accent-border:rgba(96,165,250,.45);
  --bg-canvas:#0B0D10; --bg-surface:#14171C; --bg-surface-2:#1B1F26; --bg-elevated:#22272F;
  --bg-selected:rgba(59,130,246,.12); --bg-hover:rgba(255,255,255,.04);
  --border-subtle:#232833; --border-default:#2E3440; --border-strong:#3D4552;
  --text-primary:#E6E9EF; --text-secondary:#A0A8B4; --text-tertiary:#8B94A3;
  --text-muted:#4E5663; --text-inverse:#0B0D10;
  --star-fg:#FBBF24; --star-solid:#FBBF24; --star-ink:#1C1305;
  --star-subtle:rgba(251,191,36,.14); --star-border:rgba(251,191,36,.42); --star-text:#FCD34D;
  --expand-fg:#38BDF8; --expand-solid:#38BDF8; --expand-ink:#04283C;
  --expand-subtle:rgba(56,189,248,.14); --expand-border:rgba(56,189,248,.42); --expand-text:#7DD3FC;
  --success:#34D399; --success-solid:#10B981; --success-ink:#062E20; --success-subtle:rgba(52,211,153,.14);
  --warning:#FBBF24; --danger:#F87171; --danger-subtle:rgba(248,113,113,.14); --info:#60A5FA;
  --font-sans:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Helvetica Neue",Arial,sans-serif;
  --font-mono:"JetBrains Mono",ui-monospace,"SFMono-Regular","SF Mono","Cascadia Code","Roboto Mono",Menlo,Consolas,monospace;
  --fs-display:24px; --fs-h1:18px; --fs-h2:15px; --fs-title:14px;
  --fs-body:13px; --fs-body-sm:12px; --fs-sm:12px; --fs-xs:11px;
  --fs-mono:12px; --fs-mono-sm:11px; --tracking-wide:.04em;
  --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px;
  --space-5:20px; --space-6:24px; --space-8:32px; --space-10:40px;
  --radius-sm:4px; --radius-md:6px; --radius-lg:8px; --radius-full:999px;
  --shadow-none:none; --shadow-xs:0 1px 2px rgba(0,0,0,.35);
  --shadow-md:0 4px 14px rgba(0,0,0,.45);
  --focus-ring:0 0 0 2px var(--bg-canvas),0 0 0 4px var(--accent);
  --dur-fast:120ms; --dur-base:180ms; --dur-slow:240ms;
  --ease-standard:cubic-bezier(.2,0,0,1); --ease-out:cubic-bezier(.16,1,.3,1);
  --layout-left:260px; --layout-right:380px; --container-max:1600px; --nav-height:48px;
  --z-base:0; --z-sticky:100; --z-drawer:200; --z-palette:300; --z-toast:400;
  --card-pad:16px; --card-gap:12px; --abstract-lines:2;
}

:root[data-theme="light"] { /* ===== Light ===== */
  --accent:#2563EB; --accent-hover:#1D4ED8;
  --accent-fill:#2563EB; --accent-fill-hover:#1D4ED8; --accent-fill-active:#1E40AF;
  --accent-text:#1D4ED8; --accent-on:#FFFFFF;
  --accent-subtle:rgba(37,99,235,.10); --accent-border:rgba(37,99,235,.35);
  --bg-canvas:#F7F8FA; --bg-surface:#FFFFFF; --bg-surface-2:#F1F3F6; --bg-elevated:#FFFFFF;
  --bg-selected:rgba(37,99,235,.07); --bg-hover:rgba(15,23,42,.04);
  --border-subtle:#ECEEF2; --border-default:#DFE3EA; --border-strong:#C7CDD8;
  --text-primary:#14171C; --text-secondary:#4B5563; --text-tertiary:#5F6773;
  --text-muted:#9CA3AF; --text-inverse:#FFFFFF;
  --star-fg:#D97706; --star-solid:#F59E0B; --star-ink:#2A1A02;
  --star-subtle:rgba(217,119,6,.10); --star-border:rgba(217,119,6,.32); --star-text:#B45309;
  --expand-fg:#0EA5E9; --expand-solid:#0284C7; --expand-ink:#FFFFFF;
  --expand-subtle:rgba(2,132,199,.10); --expand-border:rgba(2,132,199,.32); --expand-text:#0369A1;
  --success:#059669; --success-solid:#10B981; --success-subtle:rgba(5,150,105,.10);
  --warning:#D97706; --danger:#DC2626; --danger-subtle:rgba(220,38,38,.10); --info:#2563EB;
  --shadow-xs:0 1px 2px rgba(15,23,42,.06); --shadow-md:0 4px 14px rgba(15,23,42,.12);
}

:root[data-density="compact"] { --card-pad:12px; --card-gap:8px; --abstract-lines:1; --fs-body:12px; }

@media (prefers-reduced-motion: reduce) {
  :root { --dur-fast:0ms; --dur-base:0ms; --dur-slow:0ms; }
}

/* 命中徽标（实心） */
.badge-hit[data-channel="star"]   { background:var(--star-solid);   color:var(--star-ink); }
.badge-hit[data-channel="expand"] { background:var(--expand-solid); color:var(--expand-ink); }
.badge-hit { border-radius:var(--radius-full); padding:2px 9px; font-size:var(--fs-xs); font-weight:600; }

/* 我的评分（pips） */
.rating { display:inline-flex; gap:2px; }
.rating .pip { width:22px; height:6px; border-radius:2px; background:var(--bg-surface-2); border:1px solid var(--border-default); }
.rating .pip[data-on="true"][data-channel="star"]   { background:var(--star-fg);   border-color:var(--star-fg); }
.rating .pip[data-on="true"][data-channel="expand"] { background:var(--expand-fg); border-color:var(--expand-fg); }
```

---

## 附录 A：命中得分 vs 我的评分 —— 视觉分层方案（§8-2 回答）

| 维度 | **命中得分**（系统算的） | **我的评分**（我给的） |
|------|------------------------|----------------------|
| 语义 | 只读 · 系统推荐理由 | 可交互 · 用户反馈 |
| 形态 | **实心圆角 pill**（徽标） | **5 格分段 pips**（控件） |
| 颜色 | 通道**满饱和实心**（amber/sky） | **仅填充已选格**，通道色 + 中性底格 |
| 数字 | 徽标内含等宽数字（`★ 4`） | 每条 pip 无数字；右侧单独等宽 `★3` |
| 位置 | 卡片**顶栏右**（与类别徽标同行） | 卡片**底部操作区** / 详情面板打分区 |
| 可交互 | 否（hover 显命中条目名） | 是（`1-5` / `Shift+1-5`，`click`） |
| 反馈叠加 | 静态 | 打分后角标：`分布式计算与共识 3→4`（等宽、`--success`/`--danger` 箭头色） |
| 区分冗余 | 字形 ★/🧐 + 实心 + 顶部位置 | 形态（条状）+ 底部位置 + 「我」标签 |

> **一句话记忆**：**顶部实心徽标 = 系统的判断；底部条状控件 = 我的判断。** 两者在形态、位置、填充方式上三重区分，即使同为「1–5 数字」也不会混同。

## 附录 B：令牌清单速查（给 prototype-builder）

- **品牌**：`--accent #3B82F6`（链接/选中/焦点/描边）；**实心按钮/CTA 填充** `--accent-fill #2563EB`（白字 5.17:1 ✅）
- **三级文本**：`--text-primary #E6E9EF` / `--text-secondary #A0A8B4` / `--text-tertiary #8B94A3`（暗色）
- **画布**：`--bg-canvas #0B0D10` / `#F7F8FA`；卡片 `--bg-surface #14171C` / `#FFFFFF`
- **★ amber**：实心 `--star-solid #FBBF24` + ink `#1C1305`
- **🧐 sky**：实心 `--expand-solid #38BDF8` + ink `#04283C`
- **选中**：`--bg-selected` + `--accent-border` 左条 + inset 描边
- **字号**：24 / 18 / 15 / 14 / 13 / 12 / 11px；等宽 mono 用于一切数据
- **间距**：4 / 8 / 12 / 16 / 20 / 24 / 32 / 40px
- **圆角**：4 / 6 / 8 / full（**禁止 >8px 卡片圆角**）
- **动效**：120 / 180 / 240ms，`cubic-bezier(.2,0,0,1)`

---

*本文件仅定义设计系统与设计令牌，不含 HTML 实现、不改动项目源码。所有色值经 WCAG AA 校验（组合见 §2.5）。*
