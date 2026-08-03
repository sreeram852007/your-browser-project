"""
Query Parser
Person B builds this
"""

import re
from typing import List, Dict

class QueryParser:
    """Parse and clean search queries"""
    
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'for', 'nor', 'on', 'at', 
            'to', 'by', 'in', 'of', 'with', 'without', 'about', 'for', 'from'
        }
    
    def parse(self, query: str) -> Dict:
        """
        Parse a search query
        
        Returns:
            Dict with:
            - original: Original query string
            - cleaned: Cleaned query string
            - words: List of individual words
            - is_phrase: Whether query is a phrase
        """
        if not query:
            return {
                'original': '',
                'cleaned': '',
                'words': [],
                'is_phrase': False
            }
        
        original = query.strip()
        cleaned = self._clean_query(original)
        words = self._extract_words(cleaned)
        is_phrase = len(words) > 1 and '"' in original
        
        return {
            'original': original,
            'cleaned': cleaned,
            'words': words,
            'is_phrase': is_phrase
        }
    
    def _clean_query(self, query: str) -> str:
        """Clean the query"""
        # Remove extra spaces
        cleaned = ' '.join(query.split())
        # Remove stop words
        words = cleaned.split()
        filtered = [w for w in words if w.lower() not in self.stop_words]
        return ' '.join(filtered) if filtered else cleaned
    
    def _extract_words(self, query: str) -> List[str]:
        """Extract individual words from query"""
        # Remove punctuation and split
        words = re.findall(r'\b[a-zA-Z0-9]+\b', query.lower())
        # Remove stop words
        return [w for w in words if w not in self.stop_words]