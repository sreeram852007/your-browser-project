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
    """Main browser window"""
    
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
        
        # Set default search engine to "my" (your search engine)
        self.current_search_engine = "my"
        
        # Setup UI
        self.setup_ui()
        self.create_menubar()
        self.setup_status_bar()
        
        # Load initial page
        self.tab_manager.add_new_tab(QUrl(HOME_PAGE))
        
        # Apply theme
        self.themes.apply_theme("light")
        
        # Show status
        self.statusBar().showMessage("🔍 My Search Engine | Ready")
    
    def setup_ui(self):
        """Setup all UI components"""
        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.toolbar)
        
        # Navigation buttons
        self.navigation.create_buttons(self.toolbar)
        
        # URL/Search bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter URL...")
        self.url_bar.setMinimumWidth(400)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)
        
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
    
    def create_menubar(self):
        """Create menu bar"""
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
        # SEARCH MENU - UPDATED WITH ENGINE SELECTION
        # ============================================================
        search_menu = menubar.addMenu("Search")
        
        # Default search engine indicator
        search_menu.addAction("🔍 Set My Search Engine as Default", self.set_my_search_engine)
        search_menu.addAction("🦆 Set DuckDuckGo as Default", self.set_duckduckgo_engine)
        search_menu.addSeparator()
        
        # Quick search options
        search_menu.addAction("Search with Google", lambda: self.search_with('google'))
        search_menu.addAction("Search with DuckDuckGo", lambda: self.search_with('duckduckgo'))
        search_menu.addAction("Search with Bing", lambda: self.search_with('bing'))
        search_menu.addSeparator()
        
        # Show current engine
        self.engine_indicator = search_menu.addAction("✅ Current: My Search Engine")
        self.engine_indicator.setEnabled(False)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)
    
    def setup_status_bar(self):
        """Setup status bar"""
        # Add search engine indicator to status bar
        self.status_label = QLabel("🔍 My Search Engine")
        self.statusBar().addPermanentWidget(self.status_label)
        self.statusBar().showMessage("Ready")
    
    # ============================================================
    # SEARCH ENGINE SELECTION METHODS
    # ============================================================
    
    def set_my_search_engine(self):
        """Set My Search Engine as default"""
        self.current_search_engine = "my"
        self.status_label.setText("🔍 My Search Engine")
        self.statusBar().showMessage("✅ Using My Search Engine")
        # Update menu indicator
        self.update_engine_indicator()
    
    def set_duckduckgo_engine(self):
        """Set DuckDuckGo as default"""
        self.current_search_engine = "duckduckgo"
        self.status_label.setText("🦆 DuckDuckGo")
        self.statusBar().showMessage("✅ Using DuckDuckGo")
        # Update menu indicator
        self.update_engine_indicator()
    
    def update_engine_indicator(self):
        """Update the menu indicator"""
        if self.current_search_engine == "my":
            self.engine_indicator.setText("✅ Current: My Search Engine")
        else:
            self.engine_indicator.setText("✅ Current: DuckDuckGo")
    
    # ============================================================
    # NAVIGATION
    # ============================================================
    
    def navigate_to_url(self):
        """Handle URL bar input"""
        text = self.url_bar.text().strip()
        if not text:
            return
        
        # ============================================================
        # DUCKDUCKGO PREFIX: Type "d " or "!" to force DuckDuckGo
        # ============================================================
        if text.startswith('d ') or text.startswith('!'):
            query = text[2:] if text.startswith('d ') else text[1:]
            url = f"https://duckduckgo.com/?q={query}"
            current_browser = self.tab_manager.current_widget()
            if current_browser:
                current_browser.setUrl(QUrl(url))
                self.history.add_entry(url)
            return
        
        # ============================================================
        # CHECK IF IT'S A URL (has dot, no spaces, starts with http)
        # ============================================================
        is_url = ('.' in text or text.startswith('http')) and ' ' not in text
        
        if is_url:
            # It's a URL - open it directly
            if not text.startswith('http'):
                text = 'https://' + text
            current_browser = self.tab_manager.current_widget()
            if current_browser:
                current_browser.setUrl(QUrl(text))
                self.history.add_entry(text)
        else:
            # ============================================================
            # DEFAULT: Use the selected search engine
            # ============================================================
            if self.current_search_engine == "duckduckgo":
                # Use DuckDuckGo
                url = f"https://duckduckgo.com/?q={text}"
                current_browser = self.tab_manager.current_widget()
                if current_browser:
                    current_browser.setUrl(QUrl(url))
                    self.history.add_entry(url)
            else:
                # DEFAULT: Use YOUR search engine
                self.search.search(text, self.show_search_results)
    
    # ============================================================
    # SEARCH RESULTS DISPLAY
    # ============================================================
    
    def show_search_results(self, results):
        """Display search results in browser"""
        if 'error' in results:
            self.statusBar().showMessage(f"Error: {results['error']}")
            return
        
        # Create HTML to display results
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
    
    # ============================================================
    # BOOKMARKS
    # ============================================================
    
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
    
    # ============================================================
    # SEARCH WITH EXTERNAL ENGINES
    # ============================================================
    
    def search_with(self, engine):
        """Search with different engines"""
        query = self.url_bar.text().strip()
        if not query:
            return
        self.search.search_with_engine(query, engine)
    
    # ============================================================
    # ABOUT
    # ============================================================
    
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
    
    # ============================================================
    # CLOSE EVENT
    # ============================================================
    
    def closeEvent(self, event):
        """Handle close event"""
        # Save settings
        self.bookmarks.save()
        self.history.save()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())