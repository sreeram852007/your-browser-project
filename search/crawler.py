"""
Web Crawler - Extracts text, images, and videos
Person B builds this
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import time
from shared.config import CRAWLER_TIMEOUT, CRAWLER_DELAY, MAX_PAGES_TO_CRAWL

class Crawler:
    """Web crawler that extracts text, images, and videos"""
    
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
                text = soup.get_text(separator=' ', strip=True)[:5000]
                
                # ============================================
                # NEW: Extract Images
                # ============================================
                images = []
                for img in soup.find_all('img'):
                    src = img.get('src')
                    if src:
                        img_url = urljoin(url, src)
                        # Filter out tiny images, icons, etc.
                        if not img_url.endswith(('.ico', '.svg')):
                            images.append({
                                'url': img_url,
                                'alt': img.get('alt', ''),
                                'width': img.get('width', ''),
                                'height': img.get('height', '')
                            })
                
                # ============================================
                # NEW: Extract Videos
                # ============================================
                videos = []
                # Find video tags
                for video in soup.find_all('video'):
                    src = video.get('src')
                    if src:
                        videos.append(urljoin(url, src))
                    # Also check for source tags inside video
                    for source in video.find_all('source'):
                        src = source.get('src')
                        if src:
                            videos.append(urljoin(url, src))
                
                # Also find video links (YouTube, Vimeo, etc.)
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if any(domain in href for domain in ['youtube.com', 'youtu.be', 'vimeo.com']):
                        videos.append(href)
                
                # Save page data with images and videos
                page_data = {
                    'url': url,
                    'title': title.strip(),
                    'content': text,
                    'snippet': text[:200],
                    'images': images[:10],  # Limit to 10 images
                    'videos': videos[:5],    # Limit to 5 videos
                }
                self.pages.append(page_data)
                crawled_count += 1
                print(f"   ✅ Indexed: {title[:50]}... ({len(images)} images, {len(videos)} videos)")
                
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