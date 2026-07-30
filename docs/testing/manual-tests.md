# 手工测试用例

> Web UI 与 CLI 的手工测试步骤

## Web UI 测试

### TC-WEB-01: 页面加载

**步骤**：
1. 启动 Web 应用：`python -m glean.web`
2. 打开浏览器访问 `http://127.0.0.1:8000`

**预期**：
- 自动重定向到 `/digest`
- 左侧显示日期导航和过滤器
- 中间显示论文卡片列表
- 右侧显示详情面板（或提示选择论文）

### TC-WEB-02: 论文筛选

**步骤**：
1. 在 Digest 流页面
2. 取消勾选某个类别（如 cs.LG）

**预期**：
- 卡片列表即时更新（HTMX 局部刷新）
- 该类别论文不再显示
- URL 参数同步更新

### TC-WEB-03: 键盘导航与打分

**步骤**：
1. 点击一张卡片选中
2. 按 `j` 键多次，观察卡片高亮移动
3. 按 `4` 键打 ★★★★☆
4. 按 `Shift+2` 键打 🧐🧐☆☆☆

**预期**：
- 卡片高亮随 j/k 正确移动
- 打分后卡片角标更新
- 文件系统 interests.md 和 feedback.jsonl 更新

### TC-WEB-04: 论文下载

**步骤**：
1. 选中一篇未下载的论文
2. 按 `d` 键或点击下载按钮

**预期**：
- PDF 下载到 `arXiv/` 目录
- 文件名符合命名规则
- 下载按钮状态变为"已下载"

### TC-WEB-05: 搜索功能

**步骤**：
1. 按 `/` 键聚焦搜索框
2. 输入关键词如 "consensus"
3. 按 Enter

**预期**：
- 卡片列表过滤为含 "consensus" 的论文
- 高亮匹配的关键词
- 清除搜索后恢复全部显示

## CLI 测试

### TC-CLI-01: Fetch 命令

**步骤**：
```powershell
python -X utf8 arxiv_daily.py fetch --hours 24
```

**预期**：
- 命令成功执行
- `data/YYYYMMDD.json` 被创建/更新
- `arXiv-schedule.md` 包含当日章节

### TC-CLI-02: Download 命令

**步骤**：
```powershell
python -X utf8 arxiv_daily.py download 2607.25916
```

**预期**：
- PDF 下载到 `arXiv/` 目录
- 文件以 `%PDF` 开头
- 文件名符合命名规则

### TC-CLI-03: Feedback 命令

**步骤**：
```powershell
python -X utf8 arxiv_daily.py feedback 2607.25916 --stars 4
```

**预期**：
- 命令成功执行
- `interests.md` 权重更新
- `feedback.jsonl` 追加记录
- `arXiv-schedule.md` 表格更新

### TC-CLI-04: Reanchor 命令

**步骤**：
```powershell
python -X utf8 arxiv_daily.py reanchor
```

**预期**：
- 命令成功执行
- 推荐表中的 `📄` 链接可正确跳转
- 论文摘要包含锚点 `<a id="...">`

## 兼容性测试

### TC-COMP-01: 早期数据文件

**步骤**：
1. 确保存在早期格式的 `data/*.json`（不含 hits/score 字段）
2. 启动 Web 应用
3. 浏览该日期的论文

**预期**：
- 页面正常加载
- 论文列表正确显示
- 无报错

### TC-COMP-02: Windows 编码

**步骤**：
1. 在 Windows PowerShell 中运行（不使用 -X utf8）
2. 观察控制台输出

**预期**：
- 建议用户使用 `-X utf8`
- 或提示设置 `$env:PYTHONUTF8 = "1"`
