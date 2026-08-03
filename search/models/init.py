"""
Search Engine Package
Person B's work
"""

from search.api import app
from search.database import SearchDatabase
from search.crawler import Crawler
from search.indexer import Indexer
from search.ranking import Ranker
from search.query_parser import QueryParser

__all__ = [
    'app',
    'SearchDatabase',
    'Crawler',
    'Indexer',
    'Ranker',
    'QueryParser'
]

__version__ = '2.0.0'