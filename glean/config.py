"""Configuration and path constants for paper-glean."""

import os
from pathlib import Path

# Base directory is the repository root (where this file's parent parent is)
REPO_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = REPO_DIR / "data"
DIGEST_MD = REPO_DIR / "arXiv-schedule.md"
INTERESTS_MD = REPO_DIR / "interests.md"
FEEDBACK_LOG = REPO_DIR / "feedback.jsonl"

# PDF storage directory (configurable via environment variable)
ARXIV_DIR = Path(os.environ.get("ARXIV_DIR", Path.home() / "papers"))

# arXiv API configuration
API = "http://export.arxiv.org/api/query"
UA = "arxiv-daily-digest/1.0 (personal research paper collection)"

# XML namespaces
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

# Categories to fetch
CATEGORIES = [
    "math.LO", "cs.AI", "cs.LG", "cs.DB", "cs.DC",
    "cs.FL", "cs.LO", "cs.PL", "cs.SE",
]

# Default cap for digest listings per category
DEFAULT_CAP = 100

# Markdown header for arXiv-schedule.md
HEADER = """# arXiv Daily Digest

> 自动生成的 arXiv 每日新增论文摘要。类别: math.LO, cs.AI, cs.LG, cs.DB, cs.DC, cs.FL, cs.LO, cs.PL, cs.SE。
> 由 `arxiv_daily.py` 抓取; ★/🧐 推荐由 agent 根据研究兴趣补充(见 `README.md`)。
> 推荐指数: ★=基于当前研究兴趣(五星强烈推荐); 🧐=视野扩展(五个强烈推荐)。

"""
