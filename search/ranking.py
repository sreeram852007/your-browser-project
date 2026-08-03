"""
Search Ranking Algorithm
Person B builds this
"""

from typing import List, Dict

class Ranker:
    """Simple ranking algorithm for search results"""
    
    def __init__(self):
        pass
    
    def rank(self, results: List[Dict], query: str) -> List[Dict]:
        """
        Rank search results by relevance
        
        Args:
            results: List of page results from database
            query: The search query
        
        Returns:
            Sorted list of results with scores
        """
        if not results:
            return []
        
        query_lower = query.lower()
        query_words = query_lower.split()
        
        for result in results:
            score = self._calculate_score(result, query_lower, query_words)
            result['score'] = round(score, 2)
        
        # Sort by score descending
        return sorted(results, key=lambda x: x.get('score', 0), reverse=True)
    
    def _calculate_score(self, result: Dict, query: str, query_words: List[str]) -> float:
        """Calculate relevance score for a single result"""
        score = 0.0
        
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        snippet = result.get('snippet', '').lower()
        
        # Title matches are most important (weight: 3.0)
        for word in query_words:
            if word in title:
                score += 3.0
            if query in title:
                score += 5.0
        
        # Snippet matches (weight: 2.0)
        for word in query_words:
            if word in snippet:
                score += 2.0
            if query in snippet:
                score += 4.0
        
        # Content matches (weight: 1.0)
        for word in query_words:
            if word in content:
                score += 1.0
        
        # Bonus for exact phrase match
        if query in content:
            score += 3.0
        if query in title:
            score += 5.0
        
        # Normalize score to 0-1 range
        max_score = 15.0  # Maximum possible score
        return min(score / max_score, 1.0)