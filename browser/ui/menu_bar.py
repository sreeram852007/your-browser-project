"""
Menu Bar - Modern menu with keyboard shortcuts
"""

from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence

class MenuBar(QMenuBar):
    """Modern menu bar with all browser menus"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("""
            QMenuBar {
                background: transparent;
                color: #333;
                padding: 4px 8px;
                font-size: 13px;
            }
            QMenuBar::item {
                padding: 6px 12px;
                border-radius: 6px;
            }
            QMenuBar::item:selected {
                background: rgba(0, 0, 0, 0.08);
            }
            QMenu {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 6px 0;
                font-size: 13px;
            }
            QMenu::item {
                padding: 8px 32px 8px 20px;
                border-radius: 4px;
                margin: 2px 4px;
            }
            QMenu::item:selected {
                background: #4a9eff;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background: #e0e0e0;
                margin: 4px 8px;
            }
        """)
        self.setup_menus()
    
    def setup_menus(self):
        """Create all menus"""
        # File menu
        file_menu = self.addMenu("📁 File")
        file_menu.addAction("New Tab", self.parent.tab_manager.add_new_tab, QKeySequence("Ctrl+T"))
        file_menu.addAction("Close Tab", self.parent.tab_manager.close_current_tab, QKeySequence("Ctrl+W"))
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.parent.close, QKeySequence("Ctrl+Q"))
        
        # View menu
        view_menu = self.addMenu("👁 View")
        view_menu.addAction("Toggle Dark Mode", self.parent.themes.toggle_theme)
        view_menu.addSeparator()
        view_menu.addAction("Reload", self.parent.navigation.refresh, QKeySequence("F5"))
        view_menu.addAction("Zoom In", self.parent.navigation.zoom_in, QKeySequence("Ctrl+="))
        view_menu.addAction("Zoom Out", self.parent.navigation.zoom_out, QKeySequence("Ctrl+-"))
        view_menu.addAction("Reset Zoom", self.parent.navigation.zoom_reset, QKeySequence("Ctrl+0"))
        
        # Bookmarks menu
        bookmarks_menu = self.addMenu("⭐ Bookmarks")
        bookmarks_menu.addAction("Add Bookmark", self.parent.bookmarks.add_current, QKeySequence("Ctrl+D"))
        bookmarks_menu.addAction("View Bookmarks", self.parent.bookmarks.view_bookmarks, QKeySequence("Ctrl+Shift+B"))
        bookmarks_menu.addSeparator()
        bookmarks_menu.addAction("Import Bookmarks", self.parent.bookmarks.import_bookmarks)
        bookmarks_menu.addAction("Export Bookmarks", self.parent.bookmarks.export_bookmarks)
        
        # History menu
        history_menu = self.addMenu("📜 History")
        history_menu.addAction("View History", self.parent.history.view_history, QKeySequence("Ctrl+H"))
        history_menu.addAction("Clear History", self.parent.history.clear_history)
        
        # Search menu
        search_menu = self.addMenu("🔍 Search")
        search_menu.addAction("My Search Engine (Default)", self.parent.set_my_search_engine)
        search_menu.addSeparator()
        search_menu.addAction("Google", lambda: self.parent.search_with('google'))
        search_menu.addAction("Bing", lambda: self.parent.search_with('bing'))
        search_menu.addSeparator()
        # Store the indicator as an attribute so parent can access it
        self.engine_indicator = search_menu.addAction("✅ Current: My Search Engine")
        self.engine_indicator.setEnabled(False)
        
        # Help menu
        help_menu = self.addMenu("❓ Help")
        help_menu.addAction("About", self.parent.show_about)