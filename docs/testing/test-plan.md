# 测试计划

> 各组件测试覆盖详情

## 单元测试

### `tests/test_core.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_load_interest_entries` | 解析 interests.md | ✅ |
| `test_match_keywords` | 关键词匹配逻辑 | ✅ |
| `test_annotate_hits` | 命中标记生成 | ✅ |
| `test_apply_feedback` | 反馈应用与权重更新 | ✅ |
| `test_save_day_data` | JSON 文件原子写入 | ✅ |
| `test_upsert_digest` | Markdown 章节更新 | ✅ |

### `tests/test_web.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_digest_page` | GET /digest 返回 HTML | ✅ |
| `test_api_papers` | GET /api/papers 返回 JSON | ✅ |
| `test_api_feedback` | POST /api/feedback 更新数据 | ✅ |
| `test_htmx_paper_list` | GET /htmx/paper-list 返回片段 | ✅ |

### `tests/test_cli.py`

| 测试函数 | 测试内容 | 状态 |
|----------|----------|------|
| `test_cli_fetch` | fetch 子命令执行 | ✅ |
| `test_cli_download` | download 子命令执行 | ✅ |
| `test_cli_feedback` | feedback 子命令执行 | ✅ |

## 集成测试场景

### 场景 1：完整 Fetch 工作流

```gherkin
Given  interests.md 已配置
When   运行 arxiv_daily.py fetch
Then   data/YYYYMMDD.json 被创建
And    arXiv-schedule.md 包含当日章节
And    章节内论文按权重排序
```

### 场景 2：Feedback 闭环

```gherkin
Given  某篇论文已存在 digest 中
When   运行 feedback --stars 5
Then   interests.md 中对应条目权重 +1
And    feedback.jsonl 追加新记录
And    arXiv-schedule.md 表格更新
```

### 场景 3：Web 打分

```gherkin
Given  Web 应用已启动
When   在 /digest 页面给论文打 4 星
Then   API 返回成功
And    文件系统同步更新
```

## 回归测试清单

每次发布前必须验证：

- [ ] `pytest tests/ -v` 全部通过
- [ ] CLI 四个子命令均可正常执行
- [ ] Web 应用可启动，三个页面可访问
- [ ] 键盘快捷键工作正常
- [ ] 反馈打分后文件正确更新
- [ ] 幂等：重复 fetch 不产生重复数据
