"""
Web Crawler - Indexes web pages
Person B builds this
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import time
from shared.config import CRAWLER_TIMEOUT, CRAWLER_DELAY, MAX_PAGES_TO_CRAWL

class Crawler:
    """Simple web crawler"""
    
    def __init__(self):
        self.visited: Set[str] = set()
        self.pages: List[Dict] = []
        self.base_domain = ""
    
    def crawl(self, start_url: str, max_pages: int = MAX_PAGES_TO_CRAWL) -> List[Dict]:
        """Start crawling from a URL"""
        self.base_domain = urlparse(start_url).netloc
        to_visit = [start_url]
        crawled_count = 0
        
        while to_visit and crawled_count < max_pages:
            url = to_visit.pop(0)
            if url in self.visited:
                continue
            
            print(f"🕷️ Crawling: {url}")
            self.visited.add(url)
            
            try:
                # Fetch page
                response = requests.get(
                    url,
                    timeout=CRAWLER_TIMEOUT,
                    headers={'User-Agent': 'MyBrowserCrawler/1.0'}
                )
                response.raise_for_status()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract data
                title = soup.title.string if soup.title else "No title"
                content = ' '.join([p.text for p in soup.find_all('p')][:5])
                text = soup.get_text(separator=' ', strip=True)[:5000]
                
                # Save page
                page_data = {
                    'url': url,
                    'title': title.strip(),
                    'content': text,
                    'snippet': content[:200]
                }
                self.pages.append(page_data)
                crawled_count += 1
                print(f"   ✅ Indexed: {title[:50]}...")
                
                # Find more links (same domain only)
                if crawled_count < max_pages:
                    for link in soup.find_all('a', href=True):
                        href = urljoin(url, link['href'])
                        if (href.startswith('http') and 
                            self.base_domain in href and 
                            href not in self.visited and 
                            href not in to_visit):
                            to_visit.append(href)
                
                time.sleep(CRAWLER_DELAY)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        print(f"✅ Crawled {len(self.pages)} pages")
        return self.pages