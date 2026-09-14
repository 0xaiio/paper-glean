# 快速开始

> 5 分钟上手 Paper-Glean

## 前提条件

- Python >= 3.10
- Git（用于版本化管理论文数据）

## 安装

```powershell
# 克隆仓库
git clone <repository-url>
cd paper-glean

# 安装核心依赖
pip install -e .

# 安装 Web 应用依赖（可选，用于浏览器界面）
pip install -e ".[web]"
```

## 第一次运行

### 1. 抓取今日论文

```powershell
# 抓取过去 24 小时 arXiv 论文
python -X utf8 arxiv_daily.py fetch
```

这会：
- 从 arXiv API 获取论文
- 根据 `interests.md` 中的关键词做命中标记
- 生成/更新 `arXiv-schedule.md` 中的当日 digest
- 保存原始数据到 `data/YYYYMMDD.json`

### 2. 浏览 Digest

```powershell
# 启动 Web 应用
python -m glean.web
```

打开浏览器访问 `http://127.0.0.1:8000`，即可：
- 卡片式浏览论文
- 按类别/命中类型筛选
- 键盘快捷键打分

### 3. 下载感兴趣的论文

```powershell
# 按 arXiv ID 下载 PDF
python -X utf8 arxiv_daily.py download 2607.25916 2607.25793
```

PDF 将保存到 `$ARXIV_DIR`（默认 `~/papers`，可用环境变量覆盖），按命名规则自动命名。

## 下一步

- 详细了解 CLI 命令：[CLI 参考](cli.md)
- 让它每天自动跑：[定时运行](scheduling.md)
- 盯住特定学者的新作：[学者监控与推送](watching.md)
- 盯住 CCF-A 会议/期刊的 CFP / Program / 接收论文列表：[CCF 会议期刊监控](ccf-watching.md)
- 了解 Web 界面操作：[Web 应用](web-app.md)
- 配置你的研究兴趣：[兴趣画像](interest-profile.md)
- 理解反馈机制：[反馈与权重演化](feedback.md)
