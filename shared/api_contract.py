"""
API CONTRACT - DO NOT CHANGE WITHOUT BOTH AGREEING!
This is the ONLY integration point between browser and search engine.

Version: 1.0.0
Last Updated: 2024-08-03
Author: Person B (Search Engine Developer)
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# ============================================
# 1. SEARCH ENDPOINT
# ============================================

SEARCH_ENDPOINT = "/search"
SEARCH_METHOD = "GET"

# Request Parameters
SEARCH_PARAMS = {
    "q": {
        "type": "string",
        "required": True,
        "description": "The search query",
        "example": "python programming"
    },
    "limit": {
        "type": "integer",
        "required": False,
        "default": 10,
        "min": 1,
        "max": 50,
        "description": "Maximum results to return"
    },
    "offset": {
        "type": "integer",
        "required": False,
        "default": 0,
        "description": "Pagination offset"
    }
}

# ============================================
# 2. DATA MODELS
# ============================================

@dataclass
class SearchResult:
    """Single search result"""
    title: str
    url: str
    snippet: str
    score: float  # 0.0 to 1.0
    timestamp: str

@dataclass
class SearchResponse:
    """Complete search response"""
    status: str  # "success" or "error"
    query: str
    results: List[SearchResult]
    total: int
    limit: int
    offset: int
    search_time_ms: float

@dataclass
class ErrorResponse:
    """Error response"""
    status: str  # "error"
    code: str
    message: str

# ============================================
# 3. STATUS ENDPOINT (Health Check)
# ============================================

STATUS_ENDPOINT = "/status"
STATUS_METHOD = "GET"

@dataclass
class StatusResponse:
    """Status check response"""
    status: str  # "ok" or "error"
    version: str
    pages_indexed: int
    uptime_seconds: int

# ============================================
# 4. CONSTANTS
# ============================================

DEFAULT_SEARCH_LIMIT = 10
MAX_SEARCH_LIMIT = 50
DEFAULT_API_PORT = 5000
API_HOST = "localhost"
API_BASE_URL = f"http://{API_HOST}:{DEFAULT_API_PORT}"

# ============================================
# 5. MOCK DATA (For testing without backend)
# ============================================

MOCK_SEARCH_RESPONSE = {
    "status": "success",
    "query": "python",
    "results": [
        {
            "title": "Python Programming Language",
            "url": "https://python.org",
            "snippet": "Python is a programming language that lets you work quickly...",
            "score": 0.95,
            "timestamp": datetime.now().isoformat()
        },
        {
            "title": "Python Tutorial - W3Schools",
            "url": "https://w3schools.com/python",
            "snippet": "Learn Python step by step with examples...",
            "score": 0.87,
            "timestamp": datetime.now().isoformat()
        }
    ],
    "total": 2,
    "limit": 10,
    "offset": 0,
    "search_time_ms": 45.6
}

# ============================================
# 6. VALIDATION HELPERS
# ============================================

def validate_search_params(params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Validate search parameters"""
    if 'q' not in params or not params['q'].strip():
        return False, "Missing 'q' parameter"
    
    if 'limit' in params:
        try:
            limit = int(params['limit'])
            if limit < 1 or limit > MAX_SEARCH_LIMIT:
                return False, f"Limit must be between 1 and {MAX_SEARCH_LIMIT}"
        except ValueError:
            return False, "Limit must be an integer"
    
    return True, None

def build_search_url(query: str, limit: Optional[int] = None, offset: Optional[int] = None) -> str:
    """Build the full search URL"""
    url = f"{API_BASE_URL}{SEARCH_ENDPOINT}?q={query}"
    if limit:
        url += f"&limit={limit}"
    if offset:
        url += f"&offset={offset}"
    return url

def search_response_to_dict(response: SearchResponse) -> Dict[str, Any]:
    """Convert SearchResponse to dict for JSON serialization"""
    return {
        "status": response.status,
        "query": response.query,
        "results": [asdict(r) for r in response.results],
        "total": response.total,
        "limit": response.limit,
        "offset": response.offset,
        "search_time_ms": response.search_time_ms
    }

# ============================================
# 7. SAMPLE API CALLS (For your friend to test)
# ============================================

SAMPLE_CALLS = {
    "search_python": "GET http://localhost:5000/search?q=python",
    "search_python_limit": "GET http://localhost:5000/search?q=python&limit=5",
    "status": "GET http://localhost:5000/status",
}

# Example curl commands for testing
CURL_EXAMPLES = """
# Test search
curl "http://localhost:5000/search?q=python"

# Test with limit
curl "http://localhost:5000/search?q=python&limit=5"

# Check status
curl "http://localhost:5000/status"
"""