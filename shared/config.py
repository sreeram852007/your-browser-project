"""
Configuration shared across the project
Version: 1.0.0
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
BROWSER_DIR = PROJECT_ROOT / "browser"
SEARCH_DIR = PROJECT_ROOT / "search"

# API Settings (Person B controls these)
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "5000"))
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# Search Settings
DEFAULT_SEARCH_LIMIT = int(os.getenv("DEFAULT_SEARCH_LIMIT", "10"))
MAX_SEARCH_LIMIT = int(os.getenv("MAX_SEARCH_LIMIT", "50"))

# Crawler Settings
CRAWLER_USER_AGENT = "MyBrowserCrawler/1.0"
CRAWLER_TIMEOUT = int(os.getenv("CRAWLER_TIMEOUT", "10"))
CRAWLER_DELAY = float(os.getenv("CRAWLER_DELAY", "1.0"))
MAX_PAGES_TO_CRAWL = int(os.getenv("MAX_PAGES_TO_CRAWL", "100"))

# Database Settings (Person B only)
DATABASE_PATH = SEARCH_DIR / "data" / "pages.db"

# Data files (Person A only - they handle this)
BOOKMARKS_FILE = BROWSER_DIR / "data" / "bookmarks.json"
HISTORY_FILE = BROWSER_DIR / "data" / "history.json"

# Create directories
for dir_path in [BROWSER_DIR / "data", SEARCH_DIR / "data"]:
    dir_path.mkdir(parents=True, exist_ok=True)