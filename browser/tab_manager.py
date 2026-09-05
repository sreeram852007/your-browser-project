"""
Tab Manager - Handles all tab operations
"""

from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWebEngineView):
    """Individual browser tab"""
    def __init__(self, parent=None):
        super().__init__(parent)

class TabManager(QTabWidget):
    """Manages all browser tabs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        
        # Setup tab properties
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        
        # Connect signals
        self.tabCloseRequested.connect(self.close_tab)
        self.tabBarDoubleClicked.connect(self.on_tab_double_click)
        self.currentChanged.connect(self.on_tab_changed)
    
    def add_new_tab(self, url=None):
        """Add a new tab - shows search page instead of DuckDuckGo"""
        if url is None:
            # Show a clean search page
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>My Search</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        text-align: center;
                        background: white;
                        padding: 40px 60px;
                        border-radius: 20px;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    }
                    .logo { font-size: 48px; font-weight: bold; color: #4a9eff; }
                    .logo span { color: #764ba2; }
                    .search-box {
                        display: flex;
                        align-items: center;
                        border: 2px solid #ddd;
                        border-radius: 30px;
                        padding: 5px;
                        background: white;
                        margin: 20px 0;
                    }
                    .search-box input {
                        flex: 1;
                        border: none;
                        padding: 12px 20px;
                        font-size: 16px;
                        outline: none;
                        border-radius: 30px;
                    }
                    .search-box button {
                        background: #4a9eff;
                        color: white;
                        border: none;
                        padding: 12px 25px;
                        border-radius: 30px;
                        cursor: pointer;
                    }
                    .search-box button:hover { background: #3a8eff; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="logo">🔍 My<span>Search</span></div>
                    <p>Search the web with your own search engine</p>
                    <div class="search-box">
                        <input type="text" id="searchInput" placeholder="Search anything..." onkeypress="if(event.key==='Enter') search()">
                        <button onclick="search()">Search</button>
                    </div>
                </div>
                <script>
                    function search() {
                        const query = document.getElementById('searchInput').value;
                        if (query.trim()) {
                            window.location.href = 'http://mysite/search?q=' + encodeURIComponent(query);
                        }
                    }
                </script>
            </body>
            </html>
            """
            self.add_new_tab_from_html(html, "My Search")
            return
        
        # For URLs (like when clicking links)
        if isinstance(url, str):
            if not url.startswith("http"):
                url = "https://" + url
            url = QUrl(url)
        
        browser = BrowserTab()
        browser.setUrl(url)
        
        # Connect signals
        browser.urlChanged.connect(lambda qurl: self.update_url(qurl))
        browser.loadFinished.connect(lambda: self.update_title(browser))
        browser.iconChanged.connect(lambda: self.update_icon(browser))
        browser.titleChanged.connect(lambda title: self.update_tab_title(browser, title))
        
        # Connect URL interceptor
        if self.parent_window and hasattr(self.parent_window, 'on_url_changed'):
            browser.urlChanged.connect(self.parent_window.on_url_changed)
        
        # Add tab
        index = self.addTab(browser, "Loading...")
        self.setCurrentIndex(index)
        
        return browser
    
    def add_new_tab_from_html(self, html, title="Page"):
        """Add a new tab with HTML content"""
        browser = BrowserTab()
        browser.setHtml(html)
        
        # Connect URL interceptor
        if self.parent_window and hasattr(self.parent_window, 'on_url_changed'):
            browser.urlChanged.connect(self.parent_window.on_url_changed)
        
        # Add tab and switch to it
        index = self.addTab(browser, title[:20])
        self.setCurrentIndex(index)
        
        # Update title when loaded
        def update_title():
            self.setTabText(index, title[:20])
        
        browser.loadFinished.connect(update_title)
        return browser
    
    def close_tab(self, index):
        """Close a tab"""
        if self.count() > 1:
            self.removeTab(index)
        else:
            self.parent_window.close()
    
    def close_current_tab(self):
        """Close the current tab"""
        self.close_tab(self.currentIndex())
    
    def current_widget(self):
        """Get the current browser widget"""
        return self.currentWidget()
    
    def on_tab_double_click(self, index):
        """Handle double click on tab bar"""
        self.add_new_tab()
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        if index >= 0:
            browser = self.widget(index)
            if browser:
                self.update_url(browser.url())
                self.update_title(browser)
    
    def update_url(self, url):
        """Update URL bar"""
        if self.parent_window:
            self.parent_window.url_bar.setText(url.toString())
    
    def update_title(self, browser):
        """Update tab title"""
        index = self.indexOf(browser)
        if index >= 0:
            title = browser.page().title() or "New Tab"
            self.setTabText(index, title[:20])
    
    def update_tab_title(self, browser, title):
        """Update tab title from signal"""
        index = self.indexOf(browser)
        if index >= 0:
            self.setTabText(index, title[:20] if title else "New Tab")
    
    def update_icon(self, browser):
        """Update tab icon (placeholder)"""
        pass