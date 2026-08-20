"""
MongoDB Database - Persistent Storage for Search Engine
All data stored on MongoDB Atlas (cloud), never lost!
Person B builds this
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
import pymongo
from pymongo import MongoClient
from urllib.parse import quote_plus

class MongoDatabase:
    """MongoDB Atlas database for storing indexed pages with images and videos"""
    
    def __init__(self):
        # Get connection string from environment variable
        self.connection_string = os.getenv(
            "MONGODB_URI",
            "mongodb+srv://browser_user:Wisdom27@2@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
        )
        self.db_name = os.getenv("MONGODB_DB_NAME", "search_engine")
        self.client = None
        self.db = None
        self.pages = None
        self._connect()
    
    def _connect(self):
        """Connect to MongoDB Atlas"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            self.pages = self.db["pages"]
            
            # Create indexes for faster search
            self.pages.create_index("url", unique=True)
            self.pages.create_index("title")
            self.pages.create_index("timestamp")
            print("✅ Connected to MongoDB Atlas successfully!")
        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            raise
    
    def add_page(self, url: str, title: str, content: str, 
                 snippet: str = None, images: List[Dict] = None, 
                 videos: List[str] = None):
        """Add or update a page with images and videos (stored on cloud)"""
        if snippet is None:
            snippet = content[:200] if content else ""
        
        page_data = {
            "url": url,
            "title": title,
            "content": content,
            "snippet": snippet,
            "images": images or [],
            "videos": videos or [],
            "timestamp": datetime.now(),
            "last_crawled": datetime.now(),
            "status": 200
        }
        
        # Update if exists, insert if not
        self.pages.update_one(
            {"url": url},
            {"$set": page_data},
            upsert=True
        )
        return self.pages.find_one({"url": url})["_id"]
    
    def add_pages(self, pages: List[Dict]) -> int:
        """Add multiple pages"""
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
        """Search pages by keyword"""
        search_pattern = query.lower()
        
        # MongoDB text search
        results = self.pages.find(
            {
                "$or": [
                    {"title": {"$regex": search_pattern, "$options": "i"}},
                    {"content": {"$regex": search_pattern, "$options": "i"}},
                    {"snippet": {"$regex": search_pattern, "$options": "i"}}
                ]
            }
        ).sort("timestamp", -1).skip(offset).limit(limit)
        
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "id": str(doc["_id"]),
                "url": doc.get("url", ""),
                "title": doc.get("title", ""),
                "content": doc.get("content", ""),
                "snippet": doc.get("snippet", ""),
                "images": doc.get("images", []),
                "videos": doc.get("videos", []),
                "timestamp": doc.get("timestamp", "").isoformat() if doc.get("timestamp") else ""
            })
        
        return formatted_results
    
    def get_page_count(self) -> int:
        """Get total number of indexed pages"""
        return self.pages.count_documents({})
    
    def get_all_pages(self, limit: int = 100) -> List[Dict]:
        """Get all pages"""
        results = self.pages.find().sort("timestamp", -1).limit(limit)
        
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "id": str(doc["_id"]),
                "url": doc.get("url", ""),
                "title": doc.get("title", ""),
                "snippet": doc.get("snippet", ""),
                "images": doc.get("images", []),
                "videos": doc.get("videos", []),
                "timestamp": doc.get("timestamp", "").isoformat() if doc.get("timestamp") else ""
            })
        
        return formatted_results
    
    def delete_old_pages(self, days: int = 30) -> int:
        """Delete pages older than X days"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        result = self.pages.delete_many({"timestamp": {"$lt": cutoff}})
        return result.deleted_count
    
    def clear_all(self):
        """Clear all pages (for testing)"""
        self.pages.delete_many({})