# 产品愿景

> Paper-Glean 的产品定义与愿景

## 一句话定义

**研究者个人的、画像可审计的、多源论文推荐与归档工作台**

（a personal, auditable-profile, multi-source paper recommendation & archiving workbench）

## 目标用户

单一用户：本仓库的所有者（研究者本人）。

## 核心场景

| 场景 | 描述 | 对应功能 |
|------|------|----------|
| 晨间浏览 | 每日浏览新论文，快速打分标记兴趣度 | Digest 流 + 键盘快捷键 |
| 画像维护 | 管理研究兴趣方向，跟踪权重演化 | 兴趣画像页面 |
| 下载归档 | 一键下载感兴趣的论文，自动命名归档 | 下载按钮 + 归档库 |

## 四大设计原则

1. **本地优先（Local-first）**
   - 数据全部落在本仓库内
   - 可 Git 版本化、可离线、可随时退出
   - 不引入云端账号体系

2. **Markdown/JSON 为唯一事实源**
   - Web 应用只是「视图层」
   - `interests.md`、`data/*.json`、`feedback.jsonl` 仍是权威数据
   - 文件可随时手工编辑

3. **CLI 永远是 fallback**
   - Web 挂了脚本照跑
   - 任何 Web 功能都不得使 CLI/Obsidian 工作流失效

4. **可解释推荐**
   - 每条推荐必须能回答「为什么推荐给我」
   - 命中了哪个画像条目、权重得分多少、agent 给出什么理由
   - 拒绝黑盒

## 命名

**摘星 StarDigest** — Interest-driven paper digest & recommender

- 「摘」= 文摘（digest）+ 摘取
- 「星」= ★ 推荐星级 + "仰望星空"（🧐 视野扩展）
- 中英文意象完全同构
