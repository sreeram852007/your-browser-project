"""
Toolbar - Navigation and URL bar
"""

from PySide6.QtWidgets import QToolBar, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QSize

class Toolbar(QToolBar):
    """Custom toolbar with navigation controls"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMovable(False)
        self.setIconSize(QSize(24, 24))
        self.setup_toolbar()
    
    def setup_toolbar(self):
        """Setup toolbar components"""
        # Navigation buttons will be added by NavigationControls
        pass