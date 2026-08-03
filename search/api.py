"""
Search API Server
Person B builds this
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, request, jsonify
from flask_cors import CORS

from shared.config import API_PORT
from shared.api_contract import validate_search_params
from search.database import SearchDatabase
from search.ranking import Ranker
from search.indexer import Indexer

app = Flask(__name__)
CORS(app)  # Allow browser to connect

# Initialize components
db = SearchDatabase()
ranker = Ranker()
indexer = Indexer(db)

@app.route('/search', methods=['GET'])
def search():
    """Search endpoint - Browser calls this"""
    start_time = time.time()
    
    # Get parameters
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Validate
    is_valid, error = validate_search_params({'q': query, 'limit': limit})
    if not is_valid:
        return jsonify({
            "status": "error",
            "code": "INVALID_PARAMS",
            "message": error
        }), 400
    
    # Perform search
    try:
        results = db.search(query, limit, offset)
        ranked_results = ranker.rank(results, query)
        
        search_time = (time.time() - start_time) * 1000
        
        return jsonify({
            "status": "success",
            "query": query,
            "results": ranked_results,
            "total": len(ranked_results),
            "limit": limit,
            "offset": offset,
            "search_time_ms": round(search_time, 2)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "code": "SEARCH_ERROR",
            "message": str(e)
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint - Check if search engine is running"""
    return jsonify({
        "status": "ok",
        "version": "1.0.0",
        "pages_indexed": db.get_page_count(),
        "uptime_seconds": 0
    })

@app.route('/crawl', methods=['POST'])
def crawl():
    """Start crawling - Admin endpoint"""
    data = request.json
    url = data.get('url', '')
    max_pages = data.get('max_pages', 10)
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    from search.crawler import Crawler
    crawler = Crawler()
    pages = crawler.crawl(url, max_pages)
    db.add_pages(pages)
    
    return jsonify({
        "status": "started",
        "job_id": f"crawl_{int(time.time())}",
        "pages_added": len(pages),
        "estimated_time": len(pages) * 1
    })

@app.route('/pages', methods=['GET'])
def get_pages():
    """Get all indexed pages - For debugging"""
    limit = int(request.args.get('limit', 100))
    return jsonify(db.get_all_pages(limit))

@app.route('/seed', methods=['POST'])
def seed_data():
    """Add sample data for testing"""
    sample_pages = [
        {
            "url": "https://python.org",
            "title": "Python Programming Language",
            "content": "Python is a programming language that lets you work quickly and integrate systems more effectively."
        },
        {
            "url": "https://docs.python.org",
            "title": "Python Documentation",
            "content": "Official Python documentation, tutorials, and library references."
        },
        {
            "url": "https://w3schools.com/python",
            "title": "Python Tutorial - W3Schools",
            "content": "Learn Python step by step with examples and exercises."
        },
        {
            "url": "https://developer.mozilla.org",
            "title": "MDN Web Docs",
            "content": "Resources for developers, by developers. Documentation of web technologies."
        },
        {
            "url": "https://stackoverflow.com",
            "title": "Stack Overflow",
            "content": "Where developers learn, share knowledge, and build their careers."
        }
    ]
    
    count = db.add_pages(sample_pages)
    return jsonify({
        "status": "success",
        "message": f"Added {count} sample pages"
    })

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Search API Server")
    print(f"📍 Running on: http://localhost:{API_PORT}")
    print(f"🔍 Search: http://localhost:{API_PORT}/search?q=test")
    print(f"📊 Status: http://localhost:{API_PORT}/status")
    print(f"🌱 Seed: POST http://localhost:{API_PORT}/seed")
    print("=" * 50)
    app.run(host='0.0.0.0', port=API_PORT, debug=True)