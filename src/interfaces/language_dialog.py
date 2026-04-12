import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.modules.utils.paths import resolve_asset_path
from src.interfaces.theme import DARK_BG, TEXT_PRI, ACCENT, PANEL_BG, BORDER, CARD_BG

class LanguageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Language / Idioma / Idioma")
        icon_path = resolve_asset_path("assets", "Icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(320, 200)
        self.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_PRI};")
        
        self.selected_language = "es"
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        
        lbl = QLabel("Select Language\nSeleccione el Idioma\nSelecione o Idioma")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(lbl)
        
        self.combo = QComboBox()
        self.combo.addItem("Español", "es")
        self.combo.addItem("English", "en")
        self.combo.addItem("Português (Brasil)", "pt")
        self.combo.setStyleSheet(f"""
            QComboBox {{
                background: {PANEL_BG}; color: {TEXT_PRI}; 
                border: 1px solid {BORDER}; border-radius: 6px; 
                padding: 6px; font-size: 14px;
            }}
            QComboBox QAbstractItemView {{
                background: {PANEL_BG}; color: {TEXT_PRI};
                selection-background-color: {ACCENT};
            }}
        """)
        layout.addWidget(self.combo)
        
        btn = QPushButton("OK")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white; 
                border-radius: 6px; padding: 8px; 
                font-size: 14px; font-weight: bold;
            }}
            QPushButton:hover {{
                background: #6a44d0;
            }}
        """)
        btn.clicked.connect(self.accept_selection)
        layout.addWidget(btn)
        
    def accept_selection(self):
        self.selected_language = self.combo.currentData()
        self.accept()
