"""
History Manager - Track visited pages
"""

import json
import os
from datetime import datetime
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QUrl

from shared.config import HISTORY_FILE

class HistoryDialog(QDialog):
    """Dialog to view history"""
    def __init__(self, history, parent):
        super().__init__(parent)
        self.parent = parent
        self.history = history
        self.setWindowTitle("History")
        self.setGeometry(300, 300, 600, 400)
        
        layout = QVBoxLayout()
        
        self.list = QListWidget()
        for entry in history:
            url = entry.get('url', '')
            title = entry.get('title', url)
            timestamp = entry.get('timestamp', '')
            item = QListWidgetItem(f"{title} - {timestamp}")
            item.setData(Qt.UserRole, url)
            self.list.addItem(item)
        
        self.list.itemDoubleClicked.connect(self.load_history)
        self.list.itemClicked.connect(self.on_select)
        layout.addWidget(self.list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        load_btn = QPushButton("Open")
        load_btn.clicked.connect(self.load_selected)
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_history)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(load_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def load_history(self, item):
        """Load a history entry"""
        url = item.data(Qt.UserRole)
        if self.parent:
            self.parent.tab_manager.add_new_tab(QUrl(url))
        self.close()
    
    def on_select(self, item):
        """Handle selection"""
        pass
    
    def load_selected(self):
        """Load selected history entry"""
        item = self.list.currentItem()
        if item:
            self.load_history(item)
    
    def clear_history(self):
        """Clear all history"""
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear all history?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.parent.history.clear()
            self.list.clear()

class HistoryManager:
    """Manage browsing history"""
    
    MAX_HISTORY = 100
    
    def __init__(self, parent):
        self.parent = parent
        self.history = []
        self.load()
    
    def load(self):
        """Load history from file"""
        try:
            with open(HISTORY_FILE, 'r') as f:
                self.history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
            self.save()
    
    def save(self):
        """Save history to file"""
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add_entry(self, url, title=None):
        """Add a history entry"""
        if not url or url.startswith('data:'):
            return
        
        if title is None:
            browser = self.parent.tab_manager.current_widget()
            if browser:
                title = browser.page().title() or url
            else:
                title = url
        
        # Remove duplicate
        self.history = [h for h in self.history if h['url'] != url]
        
        # Add new entry
        entry = {
            'url': url,
            'title': title,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.history.insert(0, entry)
        
        # Keep only recent entries
        self.history = self.history[:self.MAX_HISTORY]
        self.save()
    
    def clear(self):
        """Clear all history"""
        self.history = []
        self.save()
    
    def clear_history(self):
        """Clear history (called from menu)"""
        self.clear()
        if self.parent:
            self.parent.statusBar().showMessage("History cleared")
    
    def view_history(self):
        """Open history dialog"""
        dialog = HistoryDialog(self.history, self.parent)
        dialog.exec()