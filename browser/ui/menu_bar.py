"""
Menu Bar - File, View, Bookmarks, History menus
"""

from PySide6.QtWidgets import QMenuBar

class MenuBar(QMenuBar):
    """Custom menu bar"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent