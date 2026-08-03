"""
SQLite database for search engine
Person B builds this
"""

import sqlite3
import os
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from shared.config import DATABASE_PATH

class SearchDatabase:
    """SQLite database for storing indexed pages"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DATABASE_PATH
        self._init_db()
    
    def _init_db(self):
        """Initialize database with schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT,
                snippet TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_crawled DATETIME DEFAULT CURRENT_TIMESTAMP,
                status INTEGER DEFAULT 200
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_url ON pages(url)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_title ON pages(title)
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(str(self.db_path))
    
    def add_page(self, url: str, title: str, content: str, snippet: str = None):
        """Add or update a page"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if snippet is None:
            snippet = content[:200] if content else ""
        
        cursor.execute('''
            INSERT OR REPLACE INTO pages 
            (url, title, content, snippet, last_crawled) 
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (url, title, content, snippet))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def add_pages(self, pages: List[Dict]) -> int:
        """Add multiple pages"""
        count = 0
        for page in pages:
            self.add_page(
                url=page.get('url', ''),
                title=page.get('title', ''),
                content=page.get('content', ''),
                snippet=page.get('snippet', None)
            )
            count += 1
        return count
    
    def search(self, query: str, limit: int = 10, offset: int = 0) -> List[Dict]:
        """Search pages by keyword"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute('''
            SELECT id, url, title, content, snippet, timestamp
            FROM pages
            WHERE title LIKE ? OR content LIKE ? OR snippet LIKE ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (search_pattern, search_pattern, search_pattern, limit, offset))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'content': row[3],
                'snippet': row[4],
                'timestamp': row[5]
            })
        
        conn.close()
        return results
    
    def get_page_count(self) -> int:
        """Get total number of indexed pages"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM pages')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_all_pages(self, limit: int = 100) -> List[Dict]:
        """Get all pages"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, url, title, snippet, timestamp
            FROM pages
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'snippet': row[3],
                'timestamp': row[4]
            })
        
        conn.close()
        return results
    
    def delete_old_pages(self, days: int = 30) -> int:
        """Delete pages older than X days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM pages WHERE timestamp < datetime("now", ?)',
            (f"-{days} days",)
        )
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted