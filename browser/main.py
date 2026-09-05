"""
Main Browser Window
Complete browser with tabs, navigation, bookmarks, history, and dark mode
"""

import sys
import os
from pathlib import Path

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
        
        # Setup UI
        self.setup_ui()
        self.create_menubar()
        self.setup_status_bar()
        
        # Load custom home page
        home_html = self.create_home_page()
        self.tab_manager.add_new_tab_from_html(home_html, "My Search")
        
        # Apply theme
        self.themes.apply_theme("light")
        
        # Show status
        self.statusBar().showMessage("🔍 My Search Engine | Ready")
    
    def setup_ui(self):
        """Setup all UI components with a dedicated search bar"""
        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.toolbar)
        
        # Navigation buttons
        self.navigation.create_buttons(self.toolbar)
        
        # ============================================================
        # SEARCH BAR - Dedicated Search Box
        # ============================================================
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("🔍 Search the web...")
        self.url_bar.setMinimumWidth(500)
        self.url_bar.setMaximumHeight(35)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 20px;
                padding: 8px 20px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4a9eff;
                background-color: #f8f9fa;
            }
        """)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)
        
        # Search button
        search_btn = QPushButton("🔍")
        search_btn.setFixedSize(35, 35)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3a8eff;
            }
        """)
        search_btn.clicked.connect(self.navigate_to_url)
        self.toolbar.addWidget(search_btn)
        
        # New tab button
        new_tab_btn = QPushButton("➕")
        new_tab_btn.setFixedSize(30, 30)
        new_tab_btn.clicked.connect(lambda: self.tab_manager.add_new_tab())
        self.toolbar.addWidget(new_tab_btn)
        
        # Bookmark button
        self.bookmark_btn = QPushButton("⭐")
        self.bookmark_btn.setFixedSize(30, 30)
        self.bookmark_btn.clicked.connect(self.toggle_bookmark)
        self.toolbar.addWidget(self.bookmark_btn)
        
        # Set central widget
        self.setCentralWidget(self.tab_manager)
    
    def create_home_page(self):
        """Create a custom home page with search box"""
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
                    <a href="#" onclick="quickSearch('python')">Python</a>
                    <a href="#" onclick="quickSearch('web development')">Web Dev</a>
                    <a href="#" onclick="quickSearch('machine learning')">ML</a>
                    <a href="#" onclick="quickSearch('javascript')">JavaScript</a>
                    <a href="#" onclick="quickSearch('news')">News</a>
                </div>
                <p class="footer">Powered by Your Search Engine</p>
            </div>
            <script>
                function search() {
                    const query = document.getElementById('searchInput').value;
                    if (query.trim()) {
                        window.location.href = '/search?q=' + encodeURIComponent(query);
                    }
                }
                function quickSearch(query) {
                    window.location.href = '/search?q=' + encodeURIComponent(query);
                }
                // Handle dark mode detection
                if (document.querySelector('.dark-mode')) {
                    document.body.classList.add('dark-mode');
                }
            </script>
        </body>
        </html>
        """
        return html
    
    def create_menubar(self):
        """Create menu bar - NO DuckDuckGo options"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Tab", lambda: self.tab_manager.add_new_tab(), QKeySequence("Ctrl+T"))
        file_menu.addAction("Close Tab", self.tab_manager.close_current_tab, QKeySequence("Ctrl+W"))
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close, QKeySequence("Ctrl+Q"))
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Toggle Dark Mode", self.themes.toggle_theme)
        view_menu.addAction("Reload", self.navigation.refresh, QKeySequence("F5"))
        view_menu.addAction("Zoom In", self.navigation.zoom_in, QKeySequence("Ctrl+="))
        view_menu.addAction("Zoom Out", self.navigation.zoom_out, QKeySequence("Ctrl+-"))
        view_menu.addAction("Reset Zoom", self.navigation.zoom_reset, QKeySequence("Ctrl+0"))
        
        # Bookmarks menu
        bookmarks_menu = menubar.addMenu("Bookmarks")
        bookmarks_menu.addAction("Add Bookmark", self.bookmarks.add_current, QKeySequence("Ctrl+D"))
        bookmarks_menu.addAction("View Bookmarks", self.bookmarks.view_bookmarks, QKeySequence("Ctrl+Shift+B"))
        bookmarks_menu.addSeparator()
        bookmarks_menu.addAction("Import Bookmarks", self.bookmarks.import_bookmarks)
        bookmarks_menu.addAction("Export Bookmarks", self.bookmarks.export_bookmarks)
        
        # History menu
        history_menu = menubar.addMenu("History")
        history_menu.addAction("View History", self.history.view_history, QKeySequence("Ctrl+H"))
        history_menu.addAction("Clear History", self.history.clear_history)
        
        # ============================================================
        # SEARCH MENU - ONLY YOUR SEARCH ENGINE (NO DuckDuckGo)
        # ============================================================
        search_menu = menubar.addMenu("Search")
        search_menu.addAction("🔍 My Search Engine (Default)", self.set_my_search_engine)
        search_menu.addSeparator()
        search_menu.addAction("Search with Google", lambda: self.search_with('google'))
        search_menu.addAction("Search with Bing", lambda: self.search_with('bing'))
        search_menu.addSeparator()
        self.engine_indicator = search_menu.addAction("✅ Current: My Search Engine")
        self.engine_indicator.setEnabled(False)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_label = QLabel("🔍 My Search Engine")
        self.statusBar().addPermanentWidget(self.status_label)
        self.statusBar().showMessage("Ready")
    
    def set_my_search_engine(self):
        """Set My Search Engine as default"""
        self.status_label.setText("🔍 My Search Engine")
        self.statusBar().showMessage("✅ Using My Search Engine")
        self.engine_indicator.setText("✅ Current: My Search Engine")
    
    def navigate_to_url(self):
        """Handle search bar input - ONLY uses your search engine"""
        text = self.url_bar.text().strip()
        if not text:
            return
        
        # ALWAYS use YOUR search engine (NO DuckDuckGo, NO URLs)
        self.search.search(text, self.show_search_results)
    
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
        query = self.url_bar.text().strip()
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