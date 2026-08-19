"""
Search Integration - Connects browser to search engine API
"""

import requests
import time
from PySide6.QtCore import QUrl
from shared.config import API_BASE_URL  # ← FIXED: Import from config, not api_contract


class SearchIntegration:
    """Handles communication with search engine"""
    
    def __init__(self, parent):
        self.parent = parent
        self.api_base_url = API_BASE_URL
        self.last_ping = 0
        
        print(f"🔍 Using API URL: {self.api_base_url}")  # Debug line
        
        # Ping the server on startup to wake it up
        self.ping_server()
    
    def ping_server(self):
        """Ping the server to keep it alive and wake it up"""
        try:
            print(f"🔍 Pinging server: {self.api_base_url}/status")
            response = requests.get(f"{self.api_base_url}/status", timeout=5)
            if response.status_code == 200:
                print("✅ Server is awake!")
                return True
            else:
                print(f"⚠️ Server returned: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to server - is it running?")
            return False
        except requests.exceptions.Timeout:
            print("❌ Server timeout - waking up...")
            # Try one more time with longer timeout
            try:
                response = requests.get(f"{self.api_base_url}/status", timeout=10)
                return response.status_code == 200
            except:
                return False
        except Exception as e:
            print(f"❌ Ping error: {e}")
            return False
    
    def search(self, query, callback=None):
        """Perform a search"""
        if not query:
            return
        
        print(f"🔍 Searching for: {query}")
        print(f"📡 Using API: {self.api_base_url}/search?q={query}")
        
        try:
            # Use the Render cloud URL (24/7, PC not needed)
            url = f"{self.api_base_url}/search?q={query}"
            response = requests.get(url, timeout=10)  # Increased timeout
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                results = response.json()
                print(f"✅ Got {results.get('total', 0)} results")
                if callback:
                    callback(results)
            else:
                error_msg = f"Search failed: {response.status_code}"
                print(f"❌ {error_msg}")
                if callback:
                    callback({"error": error_msg})
                self.parent.statusBar().showMessage(error_msg)
                
        except requests.exceptions.Timeout:
            print("❌ Search timed out")
            if callback:
                callback({"error": "Search timed out"})
            self.parent.statusBar().showMessage("Search timed out")
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to search engine")
            # Try to ping and wake up the server
            self.parent.statusBar().showMessage("Waking up search engine...")
            if self.ping_server():
                # Retry the search
                self.search(query, callback)
            else:
                if callback:
                    callback({"error": "Cannot connect to search engine"})
                self.parent.statusBar().showMessage("Search engine unavailable")
        except Exception as e:
            print(f"❌ Error: {e}")
            if callback:
                callback({"error": str(e)})
            self.parent.statusBar().showMessage(f"Error: {str(e)}")
    
    def search_with_engine(self, query, engine):
        """Search with different search engines"""
        if not query:
            return
        
        urls = {
            'google': f"https://www.google.com/search?q={query}",
            'duckduckgo': f"https://duckduckgo.com/?q={query}",
            'bing': f"https://www.bing.com/search?q={query}"
        }
        
        url = urls.get(engine, urls['duckduckgo'])
        self.parent.tab_manager.add_new_tab(QUrl(url))