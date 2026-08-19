"""
Themes Manager - Dark and Light mode support
"""

from PySide6.QtCore import Qt

class ThemeManager:
    """Manage browser themes"""
    
    DARK_STYLE = """
        QMainWindow { background-color: #1a1a1a; }
        QToolBar { background-color: #2d2d2d; border: none; }
        QLineEdit { background-color: #3c3c3c; color: #e0e0e0; border: 1px solid #555; padding: 4px; border-radius: 4px; }
        QLineEdit:focus { border: 1px solid #4a9eff; }
        QTabWidget::pane { background-color: #1a1a1a; border: none; }
        QTabBar::tab { background-color: #2d2d2d; color: #e0e0e0; padding: 8px 16px; }
        QTabBar::tab:selected { background-color: #3c3c3c; }
        QTabBar::tab:hover { background-color: #3c3c3c; }
        QMenuBar { background-color: #2d2d2d; color: #e0e0e0; }
        QMenuBar::item:selected { background-color: #3c3c3c; }
        QMenu { background-color: #2d2d2d; color: #e0e0e0; border: 1px solid #555; }
        QMenu::item:selected { background-color: #3c3c3c; }
        QStatusBar { background-color: #2d2d2d; color: #e0e0e0; }
        QPushButton { background-color: #3c3c3c; color: #e0e0e0; border: 1px solid #555; padding: 4px; border-radius: 4px; }
        QPushButton:hover { background-color: #4a4a4a; }
        QDialog { background-color: #1a1a1a; }
        QListWidget { background-color: #2d2d2d; color: #e0e0e0; border: 1px solid #555; }
        QListWidget::item:selected { background-color: #3c3c3c; }
        QMessageBox { background-color: #1a1a1a; color: #e0e0e0; }
        QScrollBar:vertical { background-color: #2d2d2d; width: 12px; }
        QScrollBar::handle:vertical { background-color: #555; border-radius: 6px; }
    """
    
    LIGHT_STYLE = """
        QMainWindow { background-color: #f0f0f0; }
        QToolBar { background-color: #e0e0e0; border: none; }
        QLineEdit { background-color: white; color: #333; border: 1px solid #ccc; padding: 4px; border-radius: 4px; }
        QLineEdit:focus { border: 1px solid #4a9eff; }
        QTabWidget::pane { background-color: white; border: none; }
        QTabBar::tab { background-color: #e0e0e0; color: #333; padding: 8px 16px; }
        QTabBar::tab:selected { background-color: white; }
        QTabBar::tab:hover { background-color: #d0d0d0; }
        QMenuBar { background-color: #e0e0e0; color: #333; }
        QMenuBar::item:selected { background-color: #d0d0d0; }
        QMenu { background-color: white; color: #333; border: 1px solid #ccc; }
        QMenu::item:selected { background-color: #e0e0e0; }
        QStatusBar { background-color: #e0e0e0; color: #333; }
        QPushButton { background-color: white; color: #333; border: 1px solid #ccc; padding: 4px; border-radius: 4px; }
        QPushButton:hover { background-color: #e0e0e0; }
        QDialog { background-color: white; }
        QListWidget { background-color: white; color: #333; border: 1px solid #ccc; }
        QListWidget::item:selected { background-color: #e0e0e0; }
        QMessageBox { background-color: white; color: #333; }
        QScrollBar:vertical { background-color: #e0e0e0; width: 12px; }
        QScrollBar::handle:vertical { background-color: #ccc; border-radius: 6px; }
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.current_theme = "light"
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        if self.current_theme == "light":
            self.apply_theme("dark")
        else:
            self.apply_theme("light")
    
    def apply_theme(self, theme):
        """Apply a specific theme"""
        self.current_theme = theme
        if theme == "dark":
            self.parent.setStyleSheet(self.DARK_STYLE)
            self.parent.statusBar().showMessage("Dark mode enabled")
        else:
            self.parent.setStyleSheet(self.LIGHT_STYLE)
            self.parent.statusBar().showMessage("Light mode enabled")