#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arxiv_daily.py — arXiv 每日新增论文摘要器 + 论文下载器

本文件现为 thin wrapper，实际实现已迁移至 glean 包。
保留此文件以维持向后兼容的调用方式。

用法:
  python arxiv_daily.py fetch [--hours 24] [--cap 100] [--date YYYYMMDD]
  python arxiv_daily.py download <id> [<id> ...]
  python arxiv_daily.py feedback <id> [--stars N] [--curiosity N]
  python arxiv_daily.py reanchor [--date YYYYMMDD]
"""

from glean.cli import main

if __name__ == "__main__":
    main()
