"""
Toolbar - Navigation, URL bar, and action buttons
"""

from PySide6.QtWidgets import QToolBar, QLineEdit, QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QAction, QIcon

class Toolbar(QToolBar):
    """Modern toolbar with navigation controls and URL bar"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMovable(False)
        self.setIconSize(QSize(28, 28))
        self.setStyleSheet("""
            QToolBar {
                background: transparent;
                spacing: 6px;
                padding: 6px 12px;
                border: none;
            }
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 6px 10px;
                font-size: 18px;
                color: #555;
                min-width: 32px;
                min-height: 32px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.08);
            }
            QPushButton:pressed {
                background: rgba(0, 0, 0, 0.15);
            }
            QLineEdit {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 24px;
                padding: 8px 20px;
                font-size: 14px;
                min-height: 30px;
                selection-background-color: #4a9eff;
                transition: all 0.3s ease;
            }
            @keyframes glowPulse {
                0% { box-shadow: 0 0 15px rgba(102, 126, 234, 0.2); }
                50% { box-shadow: 0 0 35px rgba(102, 126, 234, 0.6); }
                100% { box-shadow: 0 0 15px rgba(102, 126, 234, 0.2); }
}
            QLineEdit:focus {
                border: 2px solid #4a9eff;
                background: #f8f9fa;
                box-shadow: 0 0 20px rgba(74, 158, 255, 0.4);
                animation: glowPulse 2s infinite;
            }
        """)
        self.setup_toolbar()
    
    def setup_toolbar(self):
        """Setup toolbar components"""
        # ============================================================
        # NAVIGATION BUTTONS
        # ============================================================
        self.back_btn = self.create_nav_button("◀", "Back", self.parent.navigation.back)
        self.forward_btn = self.create_nav_button("▶", "Forward", self.parent.navigation.forward)
        self.refresh_btn = self.create_nav_button("⟳", "Refresh", self.parent.navigation.refresh)
        self.home_btn = self.create_nav_button("🏠", "Home", self.parent.navigation.go_home)
        
        # Add a separator (a little space)
        spacer = QWidget()
        spacer.setFixedWidth(8)
        self.addWidget(spacer)
        
        # ============================================================
        # SEARCH/URL BAR
        # ============================================================
        self.url_bar = self.create_search_bar()
        
        # ============================================================
        # SEARCH BUTTON
        # ============================================================
        self.search_btn = self.create_search_button()
        
        # ============================================================
        # ACTION BUTTONS (New Tab, Bookmark, etc.)
        # ============================================================
        # They will be added later by main.py or you can add them here
        # We'll keep them separate so main can add custom actions
    
    def create_nav_button(self, text, tooltip, callback):
        """Create a navigation button (back, forward, refresh, home)"""
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setFixedSize(36, 36)
        btn.clicked.connect(callback)
        self.addWidget(btn)
        return btn
    
    def create_search_bar(self):
        """Create the main search/URL bar"""
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("🔍 Type to search...")
        self.url_bar.setMinimumWidth(400)
        self.url_bar.setMaximumHeight(38)
        self.url_bar.returnPressed.connect(self.parent.navigate_to_url)
        self.addWidget(self.url_bar)
        return self.url_bar
    
    def create_search_button(self):
        """Create the search button"""
        search_btn = QPushButton("🔍")
        search_btn.setFixedSize(40, 40)
        search_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a6fd6, stop:1 #6a3f96);
            }
        """)
        search_btn.clicked.connect(self.parent.navigate_to_url)
        self.addWidget(search_btn)
        return search_btn
    
    def create_action_button(self, text, tooltip, callback):
        """Create a genericaction button (e.g., New Tab, Bookmark)"""
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setFixedSize(36, 36)
        btn.clicked.connect(callback)
        self.addWidget(btn)
        return btn