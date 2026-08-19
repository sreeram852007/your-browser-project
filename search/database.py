"""
SQLite database for search engine with image/video support
All data stored on Render (cloud), nothing on your PC
Person B builds this
"""

import sqlite3
import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from shared.config import DATABASE_PATH

class SearchDatabase:
    """SQLite database for storing indexed pages with images and videos"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DATABASE_PATH
        self._init_db()
    
    def _init_db(self):
        """Initialize database with schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Pages table with image/video fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                content TEXT,
                snippet TEXT,
                images TEXT,          -- Store images as JSON
                videos TEXT,          -- Store videos as JSON
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
        """Get database connection (data stored on Render)"""
        # This path is on Render's server, NOT your PC!
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        return sqlite3.connect(str(self.db_path))
    
    def add_page(self, url: str, title: str, content: str, 
                 snippet: str = None, images: List[Dict] = None, 
                 videos: List[str] = None):
        """Add or update a page with images and videos (stored on cloud)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if snippet is None:
            snippet = content[:200] if content else ""
        
        images_json = json.dumps(images or [])
        videos_json = json.dumps(videos or [])
        
        cursor.execute('''
            INSERT OR REPLACE INTO pages 
            (url, title, content, snippet, images, videos, last_crawled) 
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (url, title, content, snippet, images_json, videos_json))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def add_pages(self, pages: List[Dict]) -> int:
        """Add multiple pages (stored on cloud)"""
        count = 0
        for page in pages:
            self.add_page(
                url=page.get('url', ''),
                title=page.get('title', ''),
                content=page.get('content', ''),
                snippet=page.get('snippet', None),
                images=page.get('images', []),
                videos=page.get('videos', [])
            )
            count += 1
        return count
    
    def search(self, query: str, limit: int = 10, offset: int = 0) -> List[Dict]:
        """Search pages by keyword (from cloud database)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute('''
            SELECT id, url, title, content, snippet, images, videos, timestamp
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
                'images': json.loads(row[5]) if row[5] else [],
                'videos': json.loads(row[6]) if row[6] else [],
                'timestamp': row[7]
            })
        
        conn.close()
        return results
    
    def get_page_count(self) -> int:
        """Get total number of indexed pages (from cloud)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM pages')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_all_pages(self, limit: int = 100) -> List[Dict]:
        """Get all pages (from cloud)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, url, title, snippet, images, videos, timestamp
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
                'images': json.loads(row[4]) if row[4] else [],
                'videos': json.loads(row[5]) if row[5] else [],
                'timestamp': row[6]
            })
        
        conn.close()
        return results
    
    def delete_old_pages(self, days: int = 30) -> int:
        """Delete pages older than X days (from cloud)"""
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