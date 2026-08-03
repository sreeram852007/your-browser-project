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
from search.crawler import Crawler

app = Flask(__name__)
CORS(app)

# Initialize components
db = SearchDatabase()
ranker = Ranker()
indexer = Indexer(db)
crawler = Crawler()

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
    
    try:
        # Get results from database
        results = db.search(query, limit, offset)
        
        # Apply BM25 ranking
        ranked_results = ranker.rank(results, query)
        
        # Format results for API contract
        formatted_results = []
        for r in ranked_results:
            formatted_results.append({
                "title": r.get('title', ''),
                "url": r.get('url', ''),
                "snippet": r.get('snippet', r.get('content', '')[:200]),
                "score": r.get('score', 0.5),
                "timestamp": r.get('timestamp', time.strftime('%Y-%m-%dT%H:%M:%S'))
            })
        
        search_time = (time.time() - start_time) * 1000
        
        return jsonify({
            "status": "success",
            "query": query,
            "results": formatted_results,
            "total": len(formatted_results),
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

@app.route('/crawl', methods=['POST'])
def start_crawl():
    """Start web crawling"""
    data = request.json
    url = data.get('url', '')
    max_pages = data.get('max_pages', 10)
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        # Use the crawler
        pages = crawler.crawl(url, max_pages)
        
        # Index the pages
        count = indexer.index_pages(pages)
        
        return jsonify({
            "status": "success",
            "message": f"Crawled and indexed {count} pages",
            "pages_added": count,
            "job_id": f"crawl_{int(time.time())}"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint - Check if search engine is running"""
    return jsonify({
        "status": "ok",
        "version": "2.0.0",
        "pages_indexed": db.get_page_count(),
        "uptime_seconds": 0
    })

@app.route('/seed', methods=['POST'])
def seed_data():
    """Add sample data for testing"""
    sample_pages = [
        {
            "url": "https://python.org",
            "title": "Python Programming Language",
            "content": "Python is a programming language that lets you work quickly and integrate systems more effectively. Python is great for beginners."
        },
        {
            "url": "https://docs.python.org",
            "title": "Python Documentation",
            "content": "Official Python documentation, tutorials, and library references. Learn Python programming."
        },
        {
            "url": "https://w3schools.com/python",
            "title": "Python Tutorial - W3Schools",
            "content": "Learn Python step by step with examples and exercises. Python is easy to learn."
        },
        {
            "url": "https://developer.mozilla.org",
            "title": "MDN Web Docs",
            "content": "Resources for developers, by developers. Documentation of web technologies including JavaScript, CSS, and HTML."
        },
        {
            "url": "https://stackoverflow.com",
            "title": "Stack Overflow",
            "content": "Where developers learn, share knowledge, and build their careers. Ask programming questions."
        },
        {
            "url": "https://github.com",
            "title": "GitHub",
            "content": "Where the world builds software. Millions of developers use GitHub to collaborate on projects."
        }
    ]
    
    count = indexer.index_pages(sample_pages)
    return jsonify({
        "status": "success",
        "message": f"Added {count} sample pages"
    })

@app.route('/suggest', methods=['GET'])
def suggest():
    """Get search suggestions (autocomplete)"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])
    
    suggestions = []
    pages = db.get_all_pages(limit=100)
    for page in pages:
        title = page.get('title', '')
        if query.lower() in title.lower():
            suggestions.append(title)
        if len(suggestions) >= 10:
            break
    
    return jsonify(suggestions)

@app.route('/index/stats', methods=['GET'])
def index_stats():
    """Get index statistics"""
    stats = indexer.get_index_stats()
    return jsonify(stats)

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Search API Server (v2.0)")
    print(f"📍 Running on: http://localhost:{API_PORT}")
    print(f"🔍 Search: http://localhost:{API_PORT}/search?q=test")
    print(f"📊 Status: http://localhost:{API_PORT}/status")
    print(f"🌱 Seed: POST http://localhost:{API_PORT}/seed")
    print(f"🕷️ Crawl: POST http://localhost:{API_PORT}/crawl")
    print(f"💡 Suggest: http://localhost:{API_PORT}/suggest?q=py")
    print("=" * 50)
    app.run(host='0.0.0.0', port=API_PORT, debug=True)