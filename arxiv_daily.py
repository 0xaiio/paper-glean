#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arxiv_daily.py — arXiv 每日新增论文摘要器 + 论文下载器

本文件现为 thin wrapper，实际实现已迁移至 glean 包。
保留此文件以维持向后兼容的调用方式。

用法:
  python arxiv_daily.py fetch [--hours 24] [--cap 100] [--date YYYYMMDD]
  python arxiv_daily.py daily [--hours 24] [--cap 100] [--date YYYYMMDD] [--serve] [--host H] [--port P]
  python arxiv_daily.py serve [--host H] [--port P] [--reload]
  python arxiv_daily.py download <id> [<id> ...]
  python arxiv_daily.py feedback <id> [--stars N] [--curiosity N]
  python arxiv_daily.py reanchor [--date YYYYMMDD]

定时运行: 见 docs/user-guide/scheduling.md (平台定时任务 / Windows 计划任务 schtasks)。
"""

from glean.cli import main

if __name__ == "__main__":
    main()
