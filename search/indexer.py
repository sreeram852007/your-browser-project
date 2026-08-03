"""
Index Builder
Person B builds this
"""

from typing import List, Dict
from search.database import SearchDatabase

class Indexer:
    """Build and manage search index"""
    
    def __init__(self, db: SearchDatabase):
        self.db = db
    
    def index_page(self, url: str, title: str, content: str, snippet: str = None):
        """Index a single page"""
        return self.db.add_page(url, title, content, snippet)
    
    def index_pages(self, pages: List[Dict]) -> int:
        """Index multiple pages"""
        return self.db.add_pages(pages)
    
    def get_index_stats(self) -> Dict:
        """Get index statistics"""
        return {
            "total_pages": self.db.get_page_count()
        }
    
    def reindex_all(self):
        """Reindex all pages (placeholder)"""
        # This would be used if we need to rebuild the index
        pass