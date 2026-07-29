# arXiv Daily Digest — 实现说明

周期性地从 arXiv 类别 **math.LO, cs.AI, cs.LG, cs.DB, cs.DC, cs.FL, cs.LO, cs.PL, cs.SE**
抓取过去 24 小时新增论文，生成每日摘要，并由 agent 根据研究兴趣做推荐与下载。

## 架构：脚本 + agent 混合

```
┌─────────────────────────┐     ┌──────────────────────────────┐
│ arxiv_daily.py fetch    │ ──▶ │ arXiv-schedule.md (## YYYYMMDD) │
│ (确定性, 可独立定时运行) │     │ data/YYYYMMDD.json (原始数据)   │
└─────────────────────────┘     └──────────────┬───────────────┘
                                               │ agent (Qoder Quest) 阅读
                                               ▼
                                ┌──────────────────────────────┐
                                │ 填写 ★ 重点关注 / 🧐 视野扩展   │
                                │ arxiv_daily.py download <id>… │
                                │ → PDF 落盘到 arXiv/ (按命名规则) │
                                └──────────────────────────────┘
```

- **脚本层**（`arxiv_daily.py`，纯标准库，Python ≥ 3.8）：负责抓取、去重、
  生成 digest 章节、根据 `interests.md` 关键词做 🎯 命中标记、下载 PDF。
  无需 agent 也能独立运行（此时 digest 中推荐小节保持"_待 agent 分析填写_"占位）。
- **agent 层**：读取 `data/YYYYMMDD.json`、digest 与兴趣画像 `interests.md`，
  填写两个推荐小节，并调用 `download` 子命令下载入选论文；另负责把用户
  提供的新材料（主页/论文/仓库链接等）解析为兴趣点/扩展点条目。

## 文件清单

| 文件 | 说明 |
|------|------|
| `arxiv_daily.py` | 抓取 + 下载 + 反馈 + 锚点维护脚本（本实现核心） |
| `interests.md` | 兴趣画像：兴趣点（★ 依据）/ 扩展点（🧐 依据）条目 + keywords + weight |
| `feedback.jsonl` | 人工调整推荐指数的反馈日志（画像演化的审计轨迹，agent 推荐时参考） |
| `arXiv-schedule.md` | 每日 digest，按日期章节组织，最新在前 |
| `data/YYYYMMDD.json` | 当天全部论文原始数据（标题/作者/摘要/类别），供 agent 分析与追溯 |
| `plan.md` | 论文推荐 Web 应用设计（头脑风暴稿，未实现） |
| `survey.md` | 现有系统调研与自研/采购决策（含对比矩阵与推荐路径） |
| `README.md` | 本文档 |

## 用法（on demand）

在仓库任意目录执行（Windows 建议加 `-X utf8` 以避免 GBK 控制台编码问题）：

```powershell
# 抓取过去 24h 新增论文, 更新 digest 当天章节(可重复执行, 幂等覆盖)
python -X utf8 arxiv_daily.py fetch

# 常用参数
python -X utf8 arxiv_daily.py fetch --hours 48          # 回补窗口
python -X utf8 arxiv_daily.py fetch --date 20260728     # 指定章节日期
python -X utf8 arxiv_daily.py fetch --cap 50            # 每类别列表上限

# 按 id 下载 PDF 到 arXiv/ 目录, 自动按仓库命名规则命名:
#   arXiv<年份> <id><版本> <去标点标题>.pdf
python -X utf8 arxiv_daily.py download 2607.25916 2607.25793

# 人工调整某篇论文的推荐指数(0-5), 同步更新 digest 表格 + 兴趣画像权重 + 反馈日志
python -X utf8 arxiv_daily.py feedback 2607.25916 --stars 3
python -X utf8 arxiv_daily.py feedback 2607.25992 --curiosity 5

# 为指定日期章节补齐摘要锚点与推荐表 📄 跳转链接(幂等, agent 填表后运行)
python -X utf8 arxiv_daily.py reanchor --date 20260729
```

要点：

- **幂等**：digest 用 `<!-- BEGIN YYYYMMDD --> … <!-- END YYYYMMDD -->` 注释标记
  分节，同一天重复 fetch 会整体替换该章节，不会重复追加；
  且 agent 已填写的 📌/🧐 推荐小节会被**保留**，不会被占位符覆盖。
- **跨类别去重**：同一论文 cross-list 到多个类别时只计一次（按 primary category 归类）。
- **API 礼仪**：每类别请求间隔 3 秒；下载间隔 3 秒。
- **安全**：XML 解析拒绝含 DTD/ENTITY 声明的响应；下载前校验 `%PDF` 魔数。
- **命名规则**：标题去标点（保留连字符），清理常见 LaTeX 记号
  （`\mathbb{Z}` → `Z`、`\varepsilon` → `epsilon` 等），与仓库
  `Conf/Journal + Year + Title` 惯例一致。

## 推荐指数约定

- `### 📌 重点关注`：与当前研究兴趣直接相关。★ 数量 = 推荐强度，**★★★★★ 为强烈推荐**。
- `### 🧐 视野扩展`：兴趣之外但值得一看、扩展研究视野。🧐 数量 = 推荐强度，
  **🧐🧐🧐🧐🧐 为强烈推荐**。
- 两类推荐入选论文均下载到 `arXiv/` 目录。
- **跳转链接**：推荐表中每篇论文附 `📄` 链接，点击跳到文档下方分类清单中
  该论文的摘要条目（锚点 `<a id="YYYYMMDD-<arxiv id>">`，由 `fetch` 自动生成，
  `reanchor` 可补齐；GitHub/主流 Markdown 预览器支持，Obsidian 阅读视图下
  对 HTML 锚点的跳转支持有限）。

## 反馈：人工调整推荐指数 → 画像自动演化

对推荐结果不满意时，可人工重调每篇论文的推荐指数，系统据此更新用户画像，
从而调整后续两类推荐：

```powershell
python -X utf8 arxiv_daily.py feedback <id> --stars N       # 重调 ★ (0-5)
python -X utf8 arxiv_daily.py feedback <id> --curiosity N   # 重调 🧐 (0-5)
```

或直接对 Quest 说："把 Hermes 那篇调成三星" / "MemLens 升为五个 🧐"。

每次反馈会依次完成：

1. **更新 digest 表格**：将对应行的 ★/🧐 改为新指数（跨类调整——如 🧐 表升入
   ★ 表——由 agent 处理）。
2. **更新兴趣画像权重**：论文命中的 `interests.md` 条目按新指数升降权重
   （≥4 星 +1，≤2 星 -1，3 星中性；范围 1-10）；若高分论文未命中任何条目，
   提示交由 agent 从该论文提炼新条目。
3. **追加 `feedback.jsonl`**：记录时间/论文/新指数/命中条目/权重变更，作为画像
   演化审计轨迹；agent 每日推荐前会回读近期反馈，做关键词之外的语义纠偏。

**权重如何影响后续推荐**：① `fetch` 时分类清单内按命中条目权重和降序排列，
高权重主题的论文更靠前；`data/*.json` 中记录 `score_star`/`score_expand`；
② agent 推荐时以权重为优先级先验（高权重主题更易入选/星级更高，低权重反之）。

## 兴趣点 / 扩展点管理（interests.md）

推荐依据集中维护在 `interests.md`，分两个小节：
**兴趣点**（★ 重点关注的依据）与**扩展点**（🧐 视野扩展的依据）。

### 如何增加（对 Quest 说一句话 + 提供材料）

支持的材料形式（任选其一）：

| 材料 | 示例说法 | agent 处理方式 |
|------|----------|---------------|
| 研究人员主页 | "把 https://example.edu/~alice 加入兴趣点" | 抓取主页，提炼研究方向与代表作关键词 |
| 论文（上传 PDF） | 上传文件 + "据此增加一个扩展点" | 阅读论文，提取主题/方法关键词 |
| 论文链接 | "关注 arxiv.org/abs/2607.25916 这个方向" | 抓取摘要页，同上 |
| GitHub 仓库 | "把 github.com/tlaplus/tlaplus 加入兴趣点" | 读 README/topics，提炼领域关键词 |
| 其它链接 | 会议主页、课程页、博客等 | 抓取内容，同上 |

agent 会将材料解析为一个 `###` 条目（主题名 + `- keywords:` 行 + `- 来源:` 行）
追加到 `interests.md` 相应小节；删除/降级某个兴趣点同理（"把 XX 从兴趣点移到扩展点"），
也可直接手工编辑该文件。

### 兴趣画像如何生效

1. **脚本层（确定性）**：`fetch` 时读取 `interests.md` 所有 `keywords:` 行，
   对每篇论文的标题+摘要做整词匹配（大小写不敏感，容忍复数），在 digest 条目上标注
   `🎯★ 命中词`（兴趣点）/ `🎯🧐 命中词`（扩展点），章节头部给出命中统计；
   命中信息与条目权重得分同步写入 `data/*.json`
   （`hits_star`/`hits_expand`/`score_star`/`score_expand` 字段）。
2. **agent 层（语义理解）**：做 ★/🧐 推荐时以 `interests.md` 全文为依据
   （而非仅限关键词命中），🎯 标记仅作为候选线索。

> 提示：keywords 宜精准、避免过泛（如 "learning"），否则 🎯 标记会刷屏。

## 定时运行

### 方式 A：Qoder Quest 定时任务（完整流程，含 agent 推荐）

在 Quest 中通过 schedule 功能创建定时任务，提示词模板：

> 运行 `python -X utf8 arxiv_daily.py fetch`；然后阅读
> `data/<今天YYYYMMDD>.json`，按 README 的推荐指数约定，
> 以 `interests.md` 兴趣画像（含条目权重）与近期 `feedback.jsonl`
> 反馈为依据，在 `arXiv-schedule.md` 当天章节填写"📌 重点关注"（★）与
> "🧐 视野扩展"（🧐）推荐表格（各约 5 篇）；填完后运行
> `arxiv_daily.py reanchor` 补齐表格 📄 跳转链接；最后用
> `arxiv_daily.py download <id>…` 将入选论文下载到 `arXiv/`。

当前平台的 schedule 为**单次任务**：每次执行完成后需（由 agent 或手动）再创建下一次。
本次会话已创建次日的任务；后续如中断，重新对 Quest 说"明早 9 点跑 arXiv digest"即可。

### 方式 B：Windows 任务计划程序（仅脚本抓取，无推荐）

每天 09:00 自动抓取（管理员或当前用户均可）：

```powershell
schtasks /Create /TN "arXivDailyDigest" /SC DAILY /ST 09:00 `
  /TR "python -X utf8 D:\code-repos\paper-glean\arxiv_daily.py fetch"
```

管理：`schtasks /Run /TN arXivDailyDigest`（立即执行）、
`schtasks /Delete /TN arXivDailyDigest /F`（删除）。
之后可随时在 Quest 中说"根据今天的 arXiv digest 做推荐"，由 agent 补齐 ★/🧐 小节。

## 其它实用功能

- 兴趣点/扩展点可随时增删（见上文），次日 digest 自动生效；重跑当天 `fetch`
  可立即刷新 🎯 命中标记（已填推荐表不会丢失）。
- `feedback` 反馈闭环：人工重调推荐指数 → 画像权重演化 → 影响后续排序与推荐（见上文）。
- `--hours N`：窗口可调，漏跑一天后可用 `--hours 48` 回补。
- `--date YYYYMMDD`：将抓取结果写入指定日期章节（配合回补）。
- `data/*.json`：保留全量结构化数据，便于后续检索、统计或重新推荐。
- 高产类别（如 cs.LG）在 digest 中受 `--cap` 限制防刷屏，超出部分仍完整保存在 JSON。

## Web 应用命名推荐

已决定开发 `plan.md` 所述 Web 应用（2026-07-29；调研见 `survey.md`）。
命名原则：**不含 arXiv 字样**（应用定位多源，不限于 arXiv）；中英文意象一体；
简短、可兼作 CLI 命令名与域名；无重大同名冲突（检索于 2026-07-29）。
参考关键词：paper / digest / interest / recommend。

| 推荐 | 中文名 | 英文名 | 寓意与理由 | 同名冲突检查 |
|------|--------|--------|-----------|-------------|
| ⭐ 首选 | 摘星 | StarDigest | 「摘」= 文摘（digest）+ 摘取，「星」= ★ 推荐星级；「手可摘星辰」——从每日论文洪流中摘下最亮的几颗，🧐 视野扩展恰是"仰望星空"。中英同构（star + digest），二字中文短而有诗意 | 仅一个已归档的 GitHub-stars 新闻信小项目（领域不同、已停更），风险低 |
| 备选 | 拾穗 | PaperGlean | 米勒《拾穗者》：每日在论文田野俯身拾取遗珠；glean 兼有"拾穗 / 用心搜集"义，暗合"从海量 feed 中捡出少数值得读的" | 检索无同名产品；但 Glean 为企业 AI 搜索大厂，商标邻近需留意 |
| 备选 | 知潮 | PaperTide | 论文每日如潮汐涨落，应用即"潮汐表"——告诉你今天该看哪几朵浪；中文"知潮 / 弄潮"呼应把握前沿 | 无软件类冲突（仅海洋潮汐 App 使用 tide 一词） |
| 备选 | 纸鸢 | PaperKite | 纸鸢即风筝：paper 与"放飞视野"（🧐）兼得；风筝线始终握在手中 = 本地数据主权（survey.md H1/H4） | 新西兰有同名开发公司 PaperKite，冲突中等 |
| 弃用 | — | PaperDigest / PaperCompass / arXiv\* | 关键词最直白的组合，但均不可用 | PaperDigest 为成熟商业产品（paperdigest.org）；PaperCompass 已有多个同名产品与论文；arXiv 前缀与多源定位冲突且涉 arXiv 商标 |

**首选理由**：「摘星 · StarDigest」一次命中本系统的三个标识——每日 digest、
★ 星级推荐、🧐 "仰望星空"式视野扩展——中英文意象完全同构，冲突风险在候选中最低。
interest / recommend 两个关键词由副标题承载，建议完整署名：

> **摘星 StarDigest** — Interest-driven paper digest & recommender
> （兴趣驱动的论文摘要与推荐工作台）
