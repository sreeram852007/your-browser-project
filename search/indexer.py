"""
Index Builder - Creates search index
Person B builds this
"""

from typing import List, Dict, Set
from search.database import SearchDatabase

class Indexer:
    """Build and manage search index with TF-IDF"""
    
    def __init__(self, db: SearchDatabase):
        self.db = db
        self.index = {}
        self.doc_freq = {}
        self.total_docs = 0
    
    def index_page(self, url: str, title: str, content: str, snippet: str = None):
        """Index a single page with TF-IDF"""
        # Save to database
        page_id = self.db.add_page(url, title, content, snippet)
        
        # Build index entry
        words = self._extract_words(title + " " + content)
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Store word frequencies
        self.index[url] = word_count
        for word in word_count:
            self.doc_freq[word] = self.doc_freq.get(word, 0) + 1
        
        self.total_docs += 1
        return page_id
    
    def index_pages(self, pages: List[Dict]) -> int:
        """Index multiple pages"""
        count = 0
        for page in pages:
            self.index_page(
                url=page.get('url', ''),
                title=page.get('title', ''),
                content=page.get('content', ''),
                snippet=page.get('snippet', None)
            )
            count += 1
        return count
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search using TF-IDF scoring"""
        query_words = self._extract_words(query)
        scores = {}
        
        # Calculate TF-IDF for each document
        for url, word_counts in self.index.items():
            score = 0
            for word in query_words:
                if word in word_counts:
                    # TF = frequency in document / total words in document
                    tf = word_counts[word] / sum(word_counts.values())
                    # IDF = log(total docs / docs containing word)
                    idf = self._total_docs / (self._doc_freq.get(word, 1) + 1)
                    score += tf * idf
            if score > 0:
                scores[url] = score
        
        # Sort by score
        sorted_urls = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        # Fetch full page data from database
        results = []
        for url, score in sorted_urls:
            # Query database for page details
            # This is simplified - you'd need a database method for this
            results.append({
                'url': url,
                'score': score
            })
        
        return results
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract and normalize words"""
        import re
        # Remove punctuation and split
        words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        # Remove stop words
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 'to', 'by', 'in', 'of', 'with'}
        return [w for w in words if w not in stop_words]
    
    def get_index_stats(self) -> Dict:
        """Get index statistics"""
        return {
            "total_pages": self.total_docs,
            "unique_words": len(self.doc_freq),
            "index_size": sum(len(words) for words in self.index.values())
        }