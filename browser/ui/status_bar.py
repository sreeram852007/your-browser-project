"""
Status Bar - Clean status display with loading indicator
"""

from PySide6.QtWidgets import QStatusBar, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class StatusBar(QStatusBar):
    """Modern status bar with loading indicators"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Status label
        self.status_label = QLabel("🔍 My Search Engine")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                padding: 4px 8px;
            }
        """)
        self.addPermanentWidget(self.status_label)
        
        # Loading indicator (hidden by default)
        self.loading_indicator = QLabel("⏳")
        self.loading_indicator.setStyleSheet("font-size: 16px;")
        self.loading_indicator.hide()
        self.addPermanentWidget(self.loading_indicator, stretch=0)
        
        self.setStyleSheet("""
            QStatusBar {
                background: #f5f5f5;
                border-top: 1px solid #e0e0e0;
                padding: 4px 12px;
            }
        """)
    
    def show_loading(self, show=True):
        """Show/hide loading indicator"""
        if show:
            self.loading_indicator.show()
        else:
            self.loading_indicator.hide()
    
    def set_status(self, message, is_loading=False):
        """Set status message with optional loading"""
        self.showMessage(message)
        self.show_loading(is_loading)
        