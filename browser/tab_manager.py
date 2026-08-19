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
        """Add a new tab"""
        if url is None:
            url = QUrl("https://duckduckgo.com")
        elif isinstance(url, str):
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
        
        # Add tab
        index = self.addTab(browser, "Loading...")
        self.setCurrentIndex(index)
        
        return browser
    
    def add_new_tab_from_html(self, html, title="Page"):
        """Add a new tab with HTML content"""
        browser = BrowserTab()
        browser.setHtml(html)
        
        index = self.addTab(browser, title)
        self.setCurrentIndex(index)
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