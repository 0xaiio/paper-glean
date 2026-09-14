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

# --- Watch & notify (monitor researchers, push new work) -----------------
# Markdown is the source of truth for *who* we watch; JSON only holds the
# "already seen" fingerprints needed for diffing.
WATCHLIST_MD = REPO_DIR / "watchlist.md"
WATCH_DIGEST_MD = REPO_DIR / "WATCH-digest.md"
WATCH_STATE = DATA_DIR / "watch_state.json"
WATCH_EVENTS = REPO_DIR / "watch_events.jsonl"
# Unacknowledged new items — what the Web UI badges as NEW (cleared on "mark read").
WATCH_NEW = DATA_DIR / "watch_new.json"

# Watch tuning knobs
WATCH_LOOKBACK_YEARS = 2  # ignore anything older than this when first seeding
WATCH_MAX_ITEMS = 300  # per-researcher cap on items kept for diffing
WATCH_TIMEOUT = 30  # seconds, per HTTP request
WATCH_REQUEST_INTERVAL = 1.5  # politeness delay between researchers
WATCH_ITEM_KINDS = ("paper", "video", "report", "talk", "other")

# --- CCF venue monitoring (CCF-A conferences & journals) ------------------
# Parallel to the researcher watchlist, but for venues: ccf.md is the source of
# truth for *which* venues are checked and CCF-digest.md the human-readable log.
CCF_MD = REPO_DIR / "ccf.md"
CCF_DIGEST_MD = REPO_DIR / "CCF-digest.md"
CCF_STATE = DATA_DIR / "ccf_state.json"
CCF_EVENTS = REPO_DIR / "ccf_events.jsonl"
CCF_NEW = DATA_DIR / "ccf_new.json"

CCFDDL_RSS = "https://ccfddl.com/conference/deadlines_en.xml"
CCF_ITEM_KINDS = ("cfp", "program", "papers", "other")
CCF_MAX_ITEMS = 200  # per-venue cap on items kept for diffing
CCF_TIMEOUT = 20  # seconds, per HTTP request
CCF_REQUEST_INTERVAL = 1.5  # politeness delay between venues


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
