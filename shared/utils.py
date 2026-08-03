"""
Shared utilities for both browser and search engine
"""

import json
import hashlib
from datetime import datetime
from typing import Any, Dict

def hash_string(text: str) -> str:
    """Create a hash of a string"""
    return hashlib.md5(text.encode()).hexdigest()[:8]

def format_timestamp(dt: datetime = None) -> str:
    """Format timestamp for consistent output"""
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()

def safe_json_load(filepath: str, default: Any = None) -> Any:
    """Safely load JSON from file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def safe_json_save(filepath: str, data: Any) -> bool:
    """Safely save JSON to file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    return url.startswith(('http://', 'https://'))

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return parsed.netloc