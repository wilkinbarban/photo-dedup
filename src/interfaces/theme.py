"""
Design tokens and reusable Qt stylesheet helpers for the PhotoDedup UI.
"""

DARK_BG = "#080a0f"
PANEL_BG = "#10151d"
CARD_BG = "#151b24"
CARD_HOV = "#1d2632"
SURFACE = "#0d1118"
SURFACE_ALT = "#19212c"
BORDER = "#263140"
BORDER_LT = "#39485c"
ACCENT = "#15b8a6"
ACCENT_LT = "#37d4c2"
ACCENT_DK = "#0e7f74"
ACCENT2 = "#ffb020"
TEXT_PRI = "#f5f7fb"
TEXT_SEC = "#aab5c4"
TEXT_MUT = "#667386"
SUCCESS = "#3ddc84"
SUCCESS_BG = "#0c2a1b"
WARNING = "#ffbf47"
WARNING_BG = "#2b210b"
DANGER = "#ff5c70"
DANGER_BG = "#2b1016"
INFO = "#62c7ff"
INFO_BG = "#0c2434"

FONT_STACK = "'Segoe UI Variable', 'Segoe UI', 'Aptos', sans-serif"
MONO_STACK = "'Cascadia Mono', Consolas, 'Courier New', monospace"


def app_stylesheet() -> str:
    """Returns the global Qt stylesheet for the whole application."""
    return f"""
        QMainWindow, QWidget {{
            background: {DARK_BG};
            color: {TEXT_PRI};
            font-family: {FONT_STACK};
        }}
        QLabel {{
            color: {TEXT_PRI};
            letter-spacing: 0px;
        }}
        QToolTip {{
            color: {TEXT_PRI};
            background: {SURFACE_ALT};
            border: 1px solid {BORDER_LT};
            border-radius: 6px;
            padding: 6px 8px;
        }}
        QComboBox {{
            color: {TEXT_PRI};
            background: {SURFACE_ALT};
            border: 1px solid {BORDER_LT};
            border-radius: 8px;
            padding: 7px 12px;
            min-height: 20px;
        }}
        QComboBox:hover {{
            border-color: {ACCENT};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        QComboBox QAbstractItemView {{
            color: {TEXT_PRI};
            background: {PANEL_BG};
            selection-background-color: {ACCENT_DK};
            border: 1px solid {BORDER};
            outline: none;
        }}
        QCheckBox {{
            color: {TEXT_PRI};
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 5px;
            border: 2px solid {BORDER_LT};
            background: {SURFACE};
        }}
        QCheckBox::indicator:checked {{
            background: {ACCENT};
            border-color: {ACCENT};
        }}
        QMessageBox {{
            background: {PANEL_BG};
        }}
        QMessageBox QLabel {{
            color: {TEXT_PRI};
        }}
        QMessageBox QPushButton {{
            color: {TEXT_PRI};
            background: {SURFACE_ALT};
            border: 1px solid {BORDER_LT};
            border-radius: 8px;
            padding: 7px 18px;
            min-width: 80px;
        }}
        QMessageBox QPushButton:hover {{
            border-color: {ACCENT};
            background: {CARD_HOV};
        }}
        QScrollBar:vertical {{
            width: 10px;
            background: {SURFACE};
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical {{
            background: {BORDER_LT};
            border-radius: 5px;
            min-height: 42px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {ACCENT};
        }}
        QScrollBar:horizontal {{
            height: 8px;
            background: {SURFACE};
            border-radius: 4px;
        }}
        QScrollBar::handle:horizontal {{
            background: {BORDER_LT};
            border-radius: 4px;
            min-width: 42px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {ACCENT};
        }}
    """


def panel_style(radius: int = 12, bg: str = CARD_BG, border: str = BORDER) -> str:
    """Reusable framed panel style."""
    return f"""
        background: {bg};
        border: 1px solid {border};
        border-radius: {radius}px;
    """


def group_box_style() -> str:
    """Consistent section panel styling for form groups."""
    return f"""
        QGroupBox {{
            color: {TEXT_SEC};
            font-size: 12px;
            font-weight: 700;
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 12px;
            margin-top: 12px;
            padding: 14px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            left: 16px;
            color: {ACCENT_LT};
        }}
    """


def button_style(kind: str = "ghost", compact: bool = False) -> str:
    """Returns a button stylesheet for primary, secondary, danger, success and ghost actions."""
    padding = "6px 12px" if compact else "8px 18px"
    radius = "8px" if compact else "10px"
    base = f"border-radius: {radius}; padding: {padding}; font-size: 12px; font-weight: 700;"
    variants = {
        "primary": (TEXT_PRI, ACCENT, "none", ACCENT_LT, ACCENT_DK),
        "secondary": (TEXT_PRI, SURFACE_ALT, f"1px solid {BORDER_LT}", CARD_HOV, SURFACE),
        "ghost": (TEXT_SEC, "transparent", f"1px solid {BORDER_LT}", CARD_HOV, SURFACE_ALT),
        "success": (SUCCESS, SUCCESS_BG, f"1px solid {SUCCESS}", "#123c26", SUCCESS_BG),
        "danger": (DANGER, DANGER_BG, f"1px solid {DANGER}", "#3a141b", DANGER_BG),
    }
    color, bg, border, hover_bg, pressed_bg = variants.get(kind, variants["ghost"])
    hover_color = TEXT_PRI if kind in {"ghost", "secondary"} else color
    if kind == "primary":
        hover_color = "#ffffff"
    return f"""
        QPushButton {{
            color: {color};
            background: {bg};
            border: {border};
            {base}
        }}
        QPushButton:hover {{
            color: {hover_color};
            background: {hover_bg};
            border-color: {ACCENT};
        }}
        QPushButton:pressed {{
            background: {pressed_bg};
            padding-top: 9px;
            padding-bottom: 7px;
        }}
        QPushButton:disabled {{
            color: {TEXT_MUT};
            background: {SURFACE};
            border: 1px solid {BORDER};
        }}
    """


def badge_style(color: str, bg: str) -> str:
    """Small status badge style."""
    return f"""
        color: {color};
        background: {bg};
        border: 1px solid {color};
        border-radius: 10px;
        padding: 3px 9px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0px;
    """


def muted_label(size: int = 12) -> str:
    """Muted secondary text label style."""
    return f"color: {TEXT_SEC}; font-size: {size}px;"
