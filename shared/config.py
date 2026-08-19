"""
Configuration shared across the project
Version: 2.0.0
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
BROWSER_DIR = PROJECT_ROOT / "browser"
SEARCH_DIR = PROJECT_ROOT / "search"

# ============================================
# BROWSER SETTINGS (Person A)
# ============================================

BROWSER_TITLE = os.getenv("BROWSER_TITLE", "My Browser")
BROWSER_WIDTH = int(os.getenv("BROWSER_WIDTH", "1200"))
BROWSER_HEIGHT = int(os.getenv("BROWSER_HEIGHT", "800"))
HOME_PAGE = os.getenv("HOME_PAGE", "https://duckduckgo.com")

# Browser data files
BOOKMARKS_FILE = BROWSER_DIR / "data" / "bookmarks.json"
HISTORY_FILE = BROWSER_DIR / "data" / "history.json"

# ============================================
# API Settings (Person B)
# ============================================

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "5000"))

# Use Render cloud URL by default (24/7, PC not needed)
# Override with environment variable if needed
API_BASE_URL = os.getenv(
    "API_BASE_URL", 
    "https://your-browser-project.onrender.com"
)

# For local testing (PC must be ON), uncomment this line:
# API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# ============================================
# Search Settings
# ============================================

DEFAULT_SEARCH_LIMIT = int(os.getenv("DEFAULT_SEARCH_LIMIT", "10"))
MAX_SEARCH_LIMIT = int(os.getenv("MAX_SEARCH_LIMIT", "50"))

# ============================================
# Crawler Settings
# ============================================

CRAWLER_USER_AGENT = os.getenv("CRAWLER_USER_AGENT", "MyBrowserCrawler/1.0")
CRAWLER_TIMEOUT = int(os.getenv("CRAWLER_TIMEOUT", "10"))
CRAWLER_DELAY = float(os.getenv("CRAWLER_DELAY", "1.0"))
MAX_PAGES_TO_CRAWL = int(os.getenv("MAX_PAGES_TO_CRAWL", "100"))
MAX_CRAWL_DEPTH = int(os.getenv("MAX_CRAWL_DEPTH", "2"))

# ============================================
# Database Settings (Person B only)
# ============================================

DATABASE_PATH = SEARCH_DIR / "data" / "pages.db"

# ============================================
# Create directories
# ============================================

for dir_path in [BROWSER_DIR / "data", SEARCH_DIR / "data"]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============================================
# Logging
# ============================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================
# Print configuration on startup (for debugging)
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 Configuration")
    print("=" * 50)
    print(f"BROWSER_TITLE: {BROWSER_TITLE}")
    print(f"BROWSER_SIZE: {BROWSER_WIDTH}x{BROWSER_HEIGHT}")
    print(f"HOME_PAGE: {HOME_PAGE}")
    print(f"API_BASE_URL: {API_BASE_URL}")
    print(f"BOOKMARKS_FILE: {BOOKMARKS_FILE}")
    print(f"HISTORY_FILE: {HISTORY_FILE}")
    print(f"DATABASE_PATH: {DATABASE_PATH}")
    print("=" * 50)