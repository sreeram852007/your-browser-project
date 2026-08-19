"""
Navigation Controls - Back, Forward, Refresh, Home
"""

from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction

class NavigationControls:
    """Handles browser navigation"""
    
    def __init__(self, parent):
        self.parent = parent
    
    def create_buttons(self, toolbar):
        """Create navigation buttons on toolbar"""
        # Back button
        back_btn = toolbar.addAction("◀")
        back_btn.triggered.connect(self.back)
        back_btn.setToolTip("Back")
        
        # Forward button
        forward_btn = toolbar.addAction("▶")
        forward_btn.triggered.connect(self.forward)
        forward_btn.setToolTip("Forward")
        
        # Refresh button
        refresh_btn = toolbar.addAction("⟳")
        refresh_btn.triggered.connect(self.refresh)
        refresh_btn.setToolTip("Refresh")
        
        # Home button
        home_btn = toolbar.addAction("🏠")
        home_btn.triggered.connect(self.go_home)
        home_btn.setToolTip("Home")
    
    def back(self):
        """Go back in history"""
        browser = self.parent.tab_manager.current_widget()
        if browser:
            browser.back()
    
    def forward(self):
        """Go forward in history"""
        browser = self.parent.tab_manager.current_widget()
        if browser:
            browser.forward()
    
    def refresh(self):
        """Refresh current page"""
        browser = self.parent.tab_manager.current_widget()
        if browser:
            browser.reload()
    
    def go_home(self):
        """Go to home page"""
        from shared.config import HOME_PAGE
        browser = self.parent.tab_manager.current_widget()
        if browser:
            browser.setUrl(QUrl(HOME_PAGE))
    
    def zoom_in(self):
        """Zoom in"""
        browser = self.parent.tab_manager.current_widget()
        if browser:
            browser.setZoomFactor(browser.zoomFactor() + 0.1)
    
    def zoom_out(self):
        """Zoom out"""
        browser = self.parent.tab_manager.current_widget()
        if browser:
            browser.setZoomFactor(max(0.3, browser.zoomFactor() - 0.1))
    
    def zoom_reset(self):
        """Reset zoom"""
        browser = self.parent.tab_manager.current_widget()
        if browser:
            browser.setZoomFactor(1.0)