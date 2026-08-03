"""
Search Ranking Algorithm - BM25 Implementation
Person B builds this
"""

from typing import List, Dict
import math

class Ranker:
    """BM25 ranking algorithm for search results"""
    
    def __init__(self, k1=1.2, b=0.75):
        self.k1 = k1  # Term frequency saturation
        self.b = b    # Length normalization
        self.avg_doc_length = 0
        self.doc_freq = {}
        self.total_docs = 0
    
    def rank(self, results: List[Dict], query: str) -> List[Dict]:
        """Rank results using BM25"""
        if not results:
            return []
        
        query_words = self._extract_words(query)
        self._update_stats(results)
        
        for result in results:
            score = self._calculate_bm25(result, query_words)
            result['score'] = round(score, 2)
        
        # Sort by score descending
        return sorted(results, key=lambda x: x.get('score', 0), reverse=True)
    
    def _calculate_bm25(self, doc: Dict, query_words: List[str]) -> float:
        """Calculate BM25 score for a document"""
        content = doc.get('content', '') + doc.get('title', '')
        words = self._extract_words(content)
        
        doc_length = len(words)
        score = 0
        
        for word in query_words:
            # Term frequency in document
            tf = words.count(word)
            if tf == 0:
                continue
            
            # Document frequency (how many docs contain this word)
            df = self.doc_freq.get(word, 1)
            
            # IDF component
            idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1)
            
            # TF component with saturation and length normalization
            tf_norm = (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length)))
            
            score += idf * tf_norm
        
        # Boost title matches
        if doc.get('title', '').lower():
            title_words = self._extract_words(doc['title'])
            title_matches = sum(1 for w in query_words if w in title_words)
            if title_matches > 0:
                score *= 1.5  # 50% boost for title matches
        
        return score
    
    def _update_stats(self, results: List[Dict]):
        """Update document statistics"""
        total_length = 0
        self.doc_freq = {}
        self.total_docs = len(results)
        
        for doc in results:
            content = doc.get('content', '') + doc.get('title', '')
            words = self._extract_words(content)
            total_length += len(words)
            
            # Update document frequency
            unique_words = set(words)
            for word in unique_words:
                self.doc_freq[word] = self.doc_freq.get(word, 0) + 1
        
        self.avg_doc_length = total_length / self.total_docs if self.total_docs > 0 else 1
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract and normalize words"""
        import re
        words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 'to', 'by', 'in', 'of', 'with'}
        return [w for w in words if w not in stop_words]