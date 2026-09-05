"""
Main Browser Window
Complete browser with tabs, navigation, bookmarks, history, and dark mode
"""

import sys
import os
from pathlib import Path
from urllib.parse import unquote

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit, 
    QStatusBar, QVBoxLayout, QWidget, QPushButton,
    QMenu, QMenuBar, QMessageBox, QDialog, QListWidget,
    QListWidgetItem, QLabel, QHBoxLayout, QCheckBox
)
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWebEngineWidgets import QWebEngineView

from browser.tab_manager import TabManager
from browser.navigation import NavigationControls
from browser.bookmarks import BookmarkManager
from browser.history import HistoryManager
from browser.themes import ThemeManager
from browser.search_integration import SearchIntegration
from browser.ui.toolbar import Toolbar          # ← NEW
from browser.ui.menu_bar import MenuBar        # ← NEW
from browser.ui.status_bar import StatusBar    # ← NEW
from shared.config import BROWSER_TITLE, BROWSER_WIDTH, BROWSER_HEIGHT, HOME_PAGE

class BrowserWindow(QMainWindow):
    """Main browser window - ONLY uses your search engine"""
    
    def __init__(self):
        super().__init__()
        
        # Setup window
        self.setWindowTitle(BROWSER_TITLE)
        self.setGeometry(100, 100, BROWSER_WIDTH, BROWSER_HEIGHT)
        
        # Initialize managers
        self.tab_manager = TabManager(self)
        self.navigation = NavigationControls(self)
        self.bookmarks = BookmarkManager(self)
        self.history = HistoryManager(self)
        self.themes = ThemeManager(self)
        self.search = SearchIntegration(self)

        # ========== CREATE TOOLBAR ==========
        self.toolbar = Toolbar(self)      # ← ADD THIS
        self.addToolBar(self.toolbar)     # ← ADD THIS

        # New tab button
        new_tab_btn = self.toolbar.create_action_button("➕", "New Tab", 
            lambda: self.tab_manager.add_new_tab())

        # Bookmark button
        self.bookmark_btn = self.toolbar.create_action_button("⭐", "Bookmark", 
            self.toggle_bookmark)

        # Menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.engine_indicator = self.menu_bar.engine_indicator 

        # Status bar
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        # Set central widget
        self.setCentralWidget(self.tab_manager)

        # Load custom home page
        home_html = self.create_home_page()
        self.tab_manager.add_new_tab_from_html(home_html, "My Search")
        
        # Apply theme
        self.themes.apply_theme("light")
        
        # Show status
        self.statusBar().showMessage("🔍 My Search Engine | Ready")
        
        # Connect URL interceptor for home page search
        self.tab_manager.currentChanged.connect(self.check_url)
    
    def create_home_page(self):
        """Create a custom home page with working search box"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Search Engine</title>
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
                    max-width: 600px;
                    width: 100%;
                }
                .logo {
                    font-size: 48px;
                    font-weight: bold;
                    color: #4a9eff;
                    margin-bottom: 10px;
                }
                .logo span {
                    color: #764ba2;
                }
                .subtitle {
                    color: #666;
                    font-size: 16px;
                    margin-bottom: 25px;
                }
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
                .search-box input:focus {
                    border: none;
                }
                .search-box button {
                    background: #4a9eff;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 30px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                .search-box button:hover {
                    background: #3a8eff;
                }
                .footer {
                    color: #999;
                    font-size: 12px;
                    margin-top: 15px;
                }
                .quick-links {
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin-top: 15px;
                    flex-wrap: wrap;
                }
                .quick-links a {
                    color: #4a9eff;
                    text-decoration: none;
                    font-size: 14px;
                    cursor: pointer;
                }
                .quick-links a:hover {
                    text-decoration: underline;
                }
                .dark-mode {
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                }
                .dark-mode .container {
                    background: #2d2d3d;
                }
                .dark-mode .logo {
                    color: #8ab4f8;
                }
                .dark-mode .logo span {
                    color: #b39ddb;
                }
                .dark-mode .subtitle {
                    color: #bbb;
                }
                .dark-mode .search-box {
                    background: #3c3c4d;
                    border-color: #555;
                }
                .dark-mode .search-box input {
                    background: #3c3c4d;
                    color: white;
                }
                .dark-mode .footer {
                    color: #888;
                }
                .dark-mode .quick-links a {
                    color: #8ab4f8;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">🔍 My<span>Search</span></div>
                <p class="subtitle">Search the web with your own search engine</p>
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="Search anything..." onkeypress="if(event.key==='Enter') search()">
                    <button onclick="search()">Search</button>
                </div>
                <div class="quick-links">
                    <a onclick="quickSearch('python')">Python</a>
                    <a onclick="quickSearch('web development')">Web Dev</a>
                    <a onclick="quickSearch('machine learning')">ML</a>
                    <a onclick="quickSearch('javascript')">JavaScript</a>
                    <a onclick="quickSearch('news')">News</a>
                </div>
                <p class="footer">Powered by Your Search Engine</p>
            </div>
            <script>
                function search() {
                    const query = document.getElementById('searchInput').value;
                    if (query.trim()) {
                        window.location.href = 'http://mysite/search?q=' + encodeURIComponent(query);
                    }
                }
                function quickSearch(query) {
                    window.location.href = 'http://mysite/search?q=' + encodeURIComponent(query);
                }
            </script>
        </body>
        </html>
        """
        return html
    
    def set_my_search_engine(self):
        """Set My Search Engine as default"""
        self.status_bar.status_label.setText("🔍 My Search Engine")
        self.statusBar().showMessage("✅ Using My Search Engine")
        self.engine_indicator.setText("✅ Current: My Search Engine")
    
    def navigate_to_url(self):
        """Handle search bar input - ONLY uses your search engine"""
        text = self.toolbar.url_bar.text().strip()  # ← Changed to self.toolbar.url_bar
        if not text:
            return
        self.search.search(text, self.show_search_results)

    def check_url(self, index):
        """Check if the current tab URL is our search trigger"""
        print(f"🔄 Tab changed to index {index}")   # Debug
        browser = self.tab_manager.widget(index)
        if browser:
            try:
                browser.urlChanged.disconnect()
            except:
                pass
            browser.urlChanged.connect(self.on_url_changed)
            print("✅ Connected urlChanged for this tab")

    def on_url_changed(self, url):
        """Handle URL changes before page loads"""
        print(f"🔔 URL changed: {url.toString()}")   # Debug
        url_str = url.toString()
        if url_str.startswith('http://mysite/search?q='):
            print("✅ Intercepted home-page search!")
            query = url_str.split('q=')[-1]
            query = unquote(query)
            browser = self.sender()
            if browser:
                browser.stop()
                index = self.tab_manager.indexOf(browser)
                if index >= 0:
                    self.tab_manager.removeTab(index)
                self.search.search(query, self.show_search_results)

    def show_search_results(self, results):
        """Display search results in browser"""
        if 'error' in results:
            self.statusBar().showMessage(f"Error: {results['error']}")
            return
        html = self.create_results_html(results)
        self.tab_manager.add_new_tab_from_html(html, f"Search: {results.get('query', '')}")

    def create_results_html(self, results):
        """Create HTML page for search results"""
        query = results.get('query', '')
        total = results.get('total', 0)
        search_time = results.get('search_time_ms', 0)
        results_list = results.get('results', [])

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Search: {query}</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
                .result {{ margin: 20px 0; padding: 15px; border-bottom: 1px solid #eee; }}
                .title {{ color: #1a0dab; font-size: 18px; text-decoration: none; }}
                .title:hover {{ text-decoration: underline; }}
                .url {{ color: #006621; font-size: 14px; }}
                .snippet {{ color: #545454; font-size: 14px; margin-top: 5px; }}
                .stats {{ color: #666; font-size: 13px; margin-bottom: 20px; }}
                .score {{ color: #999; font-size: 12px; }}
                .dark-mode {{ background: #1a1a1a; color: #e0e0e0; }}
                .dark-mode .title {{ color: #8ab4f8; }}
                .dark-mode .url {{ color: #bdc1c6; }}
                .dark-mode .snippet {{ color: #e0e0e0; }}
                .dark-mode .stats {{ color: #9aa0a6; }}
            </style>
        </head>
        <body>
            <h1>🔍 Search Results for "{query}"</h1>
            <div class="stats">About {total} results ({search_time} ms)</div>
        """
        
        for result in results_list:
            title = result.get('title', 'No title')
            url = result.get('url', '#')
            snippet = result.get('snippet', 'No description')
            score = result.get('score', 0)
            
            html += f"""
            <div class="result">
                <a class="title" href="{url}">{title}</a>
                <div class="url">{url}</div>
                <div class="snippet">{snippet}</div>
                <div class="score">Score: {score}</div>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        return html

    def toggle_bookmark(self):
        """Toggle bookmark for current page"""
        current_browser = self.tab_manager.current_widget()
        if current_browser:
            url = current_browser.url().toString()
            if self.bookmarks.is_bookmarked(url):
                self.bookmarks.remove(url)
                self.bookmark_btn.setText("☆")
                self.statusBar().showMessage("Bookmark removed")
            else:
                self.bookmarks.add(url)
                self.bookmark_btn.setText("⭐")
                self.statusBar().showMessage("Bookmark added")

    def search_with(self, engine):
        """Search with different engines (Google, Bing)"""
        query = self.toolbar.url_bar.text().strip()  # ← Changed
        if not query:
            return
        self.search.search_with_engine(query, engine)

    def show_about(self):
        """Show About dialog"""
        QMessageBox.about(
            self,
            "About",
            f"{BROWSER_TITLE} v1.0.0\n\n"
            "A custom web browser with integrated search engine.\n\n"
            "Built with Python and PySide6.\n"
            "Search engine powered by Flask and SQLite.\n"
            "Deployed on Render.com (24/7).\n\n"
            "© 2025 Your Name"
        )

    def closeEvent(self, event):
        """Handle close event"""
        self.bookmarks.save()
        self.history.save()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())