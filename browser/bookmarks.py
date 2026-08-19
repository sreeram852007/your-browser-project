"""
Bookmarks Manager - Save, view, and manage bookmarks
"""

import json
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt

from shared.config import BOOKMARKS_FILE

class BookmarkDialog(QDialog):
    """Dialog to view bookmarks"""
    def __init__(self, bookmarks, parent):
        super().__init__(parent)
        self.parent = parent
        self.bookmarks = bookmarks
        self.setWindowTitle("Bookmarks")
        self.setGeometry(300, 300, 500, 400)
        
        layout = QVBoxLayout()
        
        self.list = QListWidget()
        for url, title in bookmarks.items():
            item = QListWidgetItem(f"{title} - {url}")
            item.setData(Qt.UserRole, url)
            self.list.addItem(item)
        
        self.list.itemDoubleClicked.connect(self.load_bookmark)
        self.list.itemClicked.connect(self.on_select)
        layout.addWidget(self.list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        load_btn = QPushButton("Open")
        load_btn.clicked.connect(self.load_selected)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_selected)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(load_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def load_bookmark(self, item):
        """Load a bookmark"""
        url = item.data(Qt.UserRole)
        if self.parent:
            self.parent.tab_manager.add_new_tab(QUrl(url))
        self.close()
    
    def on_select(self, item):
        """Handle selection"""
        pass
    
    def load_selected(self):
        """Load selected bookmark"""
        item = self.list.currentItem()
        if item:
            self.load_bookmark(item)
    
    def delete_selected(self):
        """Delete selected bookmark"""
        item = self.list.currentItem()
        if item:
            url = item.data(Qt.UserRole)
            self.parent.bookmarks.remove(url)
            self.list.takeItem(self.list.row(item))

class BookmarkManager:
    """Manage bookmarks"""
    
    def __init__(self, parent):
        self.parent = parent
        self.bookmarks = {}
        self.load()
    
    def load(self):
        """Load bookmarks from file"""
        try:
            with open(BOOKMARKS_FILE, 'r') as f:
                self.bookmarks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.bookmarks = {}
            self.save()
    
    def save(self):
        """Save bookmarks to file"""
        os.makedirs(os.path.dirname(BOOKMARKS_FILE), exist_ok=True)
        with open(BOOKMARKS_FILE, 'w') as f:
            json.dump(self.bookmarks, f, indent=2)
    
    def add(self, url, title=None):
        """Add a bookmark"""
        if title is None:
            # Extract title from page
            browser = self.parent.tab_manager.current_widget()
            if browser:
                title = browser.page().title() or url
            else:
                title = url
        
        self.bookmarks[url] = title
        self.save()
    
    def add_current(self):
        """Bookmark current page"""
        browser = self.parent.tab_manager.current_widget()
        if browser:
            url = browser.url().toString()
            title = browser.page().title() or url
            self.add(url, title)
            self.parent.statusBar().showMessage(f"Bookmarked: {title}")
    
    def remove(self, url):
        """Remove a bookmark"""
        if url in self.bookmarks:
            del self.bookmarks[url]
            self.save()
    
    def is_bookmarked(self, url):
        """Check if URL is bookmarked"""
        return url in self.bookmarks
    
    def get_title(self, url):
        """Get bookmark title"""
        return self.bookmarks.get(url, url)
    
    def view_bookmarks(self):
        """Open bookmarks dialog"""
        dialog = BookmarkDialog(self.bookmarks, self.parent)
        dialog.exec()
    
    def import_bookmarks(self):
        """Import bookmarks from HTML file"""
        # Placeholder for future feature
        self.parent.statusBar().showMessage("Import feature coming soon")
    
    def export_bookmarks(self):
        """Export bookmarks to HTML file"""
        # Placeholder for future feature
        self.parent.statusBar().showMessage("Export feature coming soon")