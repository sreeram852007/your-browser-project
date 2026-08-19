"""
Status Bar - Shows messages and loading status
"""

from PySide6.QtWidgets import QStatusBar

class StatusBar(QStatusBar):
    """Custom status bar"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent