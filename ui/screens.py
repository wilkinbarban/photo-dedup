import os
import shutil
import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QPushButton, QComboBox, QSlider, QProgressBar, QScrollArea,
    QMessageBox, QFileDialog, QFrame, QPlainTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QObject

from core.models import DuplicateGroup, PhotoInfo, Statistics
from core.state import load_config, save_config
from core.i18n import get_text
from ui.theme import *
from ui.widgets import GroupWidget, StatisticsDialog

class LogEmitter(QObject):
    log_signal = pyqtSignal(str)

class QPlainTextEditLogger(logging.Handler):
    def __init__(self):
        super().__init__()
        self.emitter = LogEmitter()
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.emitter.log_signal.emit(msg)

class WelcomeScreen(QWidget):
    """
    The initial welcome screen where the user selects the folder to analyze
    and configures the search parameters.

    Signals:
        start_requested (str, int, str): Emits the folder path, threshold, and duplicate mode to start analysis.
    """
    start_requested = pyqtSignal(str, int, str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the welcome screen.

        Args:
            parent (Optional[QWidget]): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.config = load_config()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Sets up the user interface elements for the welcome screen.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel(get_text("app_title"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            color: {TEXT_PRI};
            font-size: 48px;
            font-weight: 900;
            letter-spacing: -2px;
        """)
        layout.addWidget(title)

        subtitle = QLabel(get_text("app_subtitle"))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(f"color: {TEXT_SEC}; font-size: 14px;")
        layout.addWidget(subtitle)

        accent_line = QFrame()
        accent_line.setFixedHeight(3)
        accent_line.setFixedWidth(80)
        accent_line.setStyleSheet(f"background: {ACCENT}; border-radius: 2px;")
        layout.addWidget(accent_line, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        folder_group = QGroupBox(get_text("grp_folder"))
        folder_group.setMaximumWidth(600)
        folder_group.setStyleSheet(f"""
            QGroupBox {{
                color: {TEXT_SEC}; font-size: 12px;
                border: 1px solid {BORDER}; border-radius: 12px;
                margin-top: 8px; padding: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin; subcontrol-position: top left;
                padding: 0 8px; left: 16px;
            }}
        """)
        folder_layout = QHBoxLayout(folder_group)

        self.folder_label = QLabel(get_text("lbl_no_folder"))
        self.folder_label.setStyleSheet(f"color: {TEXT_SEC}; font-size: 12px;")
        self.folder_label.setWordWrap(True)

        btn_browse = QPushButton(get_text("btn_browse"))
        btn_browse.setFixedWidth(130)
        btn_browse.setStyleSheet(f"""
            QPushButton {{
                color: {TEXT_PRI}; background: {CARD_BG};
                border: 1px solid {BORDER_LT}; border-radius: 10px;
                padding: 9px 18px; font-size: 12px; font-weight: 600;
            }}
            QPushButton:hover {{ border-color: {ACCENT}; color: {ACCENT_LT}; background: {CARD_HOV}; }}
            QPushButton:pressed {{ padding-top: 10px; padding-bottom: 8px; }}
        """)
        btn_browse.clicked.connect(self._browse)

        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(btn_browse)
        layout.addWidget(folder_group, alignment=Qt.AlignmentFlag.AlignCenter)

        mode_group = QGroupBox(get_text("grp_search_type"))
        mode_group.setMaximumWidth(600)
        mode_group.setStyleSheet(folder_group.styleSheet())
        mode_layout = QHBoxLayout(mode_group)
        
        mode_layout.addWidget(QLabel(get_text("lbl_detect")))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([get_text("opt_similar"), get_text("opt_exact")])
        self.mode_combo.setCurrentIndex(0 if self.config.get('duplicate_mode') == 'similar' else 1)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addWidget(mode_group, alignment=Qt.AlignmentFlag.AlignCenter)

        sens_group = QGroupBox(get_text("grp_sensitivity"))
        sens_group.setMaximumWidth(600)
        sens_group.setStyleSheet(folder_group.styleSheet())
        sens_layout = QVBoxLayout(sens_group)

        sens_desc = QLabel(get_text("desc_sensitivity"))
        sens_desc.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px;")
        sens_layout.addWidget(sens_desc)

        slider_row = QHBoxLayout()
        lbl_strict = QLabel(get_text("lbl_strict"))
        lbl_strict.setStyleSheet(f"color: {TEXT_SEC}; font-size: 10px;")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(2, 20)
        self.slider.setValue(self.config.get('threshold', 10))
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{ height: 4px; background: {BORDER}; border-radius: 2px; }}
            QSlider::handle:horizontal {{
                width: 16px; height: 16px; margin: -6px 0;
                background: {ACCENT}; border-radius: 8px;
            }}
            QSlider::sub-page:horizontal {{ background: {ACCENT}; border-radius: 2px; }}
        """)
        lbl_permissive = QLabel(get_text("lbl_permissive"))
        lbl_permissive.setStyleSheet(f"color: {TEXT_SEC}; font-size: 10px;")
        self.lbl_threshold = QLabel(str(self.slider.value()))
        self.lbl_threshold.setFixedWidth(30)
        self.lbl_threshold.setStyleSheet(f"color: {ACCENT}; font-weight: bold;")
        self.slider.valueChanged.connect(lambda v: self.lbl_threshold.setText(str(v)))

        slider_row.addWidget(lbl_strict)
        slider_row.addWidget(self.slider)
        slider_row.addWidget(lbl_permissive)
        slider_row.addWidget(self.lbl_threshold)
        sens_layout.addLayout(slider_row)
        layout.addWidget(sens_group, alignment=Qt.AlignmentFlag.AlignCenter)

        ai_group = QGroupBox(get_text("grp_ai"))
        ai_group.setMaximumWidth(600)
        ai_group.setStyleSheet(folder_group.styleSheet())
        ai_layout = QVBoxLayout(ai_group)
        
        from PyQt6.QtWidgets import QCheckBox
        self.chk_use_ai = QCheckBox(get_text("chk_use_ai"))
        self.chk_use_ai.setChecked(self.config.get('use_ai', False))
        self.chk_use_ai.setStyleSheet(f"color: {TEXT_PRI}; font-size: 12px; font-weight: bold;")
        
        ai_level_layout = QHBoxLayout()
        ai_level_layout.addWidget(QLabel(get_text("lbl_ai_level")))
        self.ai_level_combo = QComboBox()
        self.ai_level_combo.addItems([get_text("opt_ai_fast"), get_text("opt_ai_balanced"), get_text("opt_ai_deep")])
        
        level_idx = {"fast": 0, "balanced": 1, "deep": 2}.get(self.config.get('ai_level', 'balanced'), 1)
        if not self.config.get('use_ai', False):
            level_idx = 0
            
        self.ai_level_combo.setCurrentIndex(level_idx)
        ai_level_layout.addWidget(self.ai_level_combo)
        ai_level_layout.addStretch()
        
        def on_ai_check(state):
            use_ai = (state == Qt.CheckState.Checked.value)
            self.ai_level_combo.setEnabled(use_ai)
            if use_ai and self.ai_level_combo.currentIndex() == 0:
                self.ai_level_combo.setCurrentIndex(1)
            elif not use_ai:
                self.ai_level_combo.setCurrentIndex(0)
                
        self.chk_use_ai.stateChanged.connect(on_ai_check)
        self.ai_level_combo.setEnabled(self.chk_use_ai.isChecked())
        
        def on_combo_change(idx):
            if idx == 0:
                self.chk_use_ai.setChecked(False)
            elif not self.chk_use_ai.isChecked():
                self.chk_use_ai.setChecked(True)
                
        self.ai_level_combo.currentIndexChanged.connect(on_combo_change)
        
        ai_layout.addWidget(self.chk_use_ai)
        ai_layout.addLayout(ai_level_layout)
        layout.addWidget(ai_group, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_start = QPushButton(get_text("btn_start"))
        self.btn_start.setFixedSize(240, 40)
        self.btn_start.setEnabled(False)
        self.btn_start.setStyleSheet(f"""
            QPushButton {{
                color: #ffffff; background: {ACCENT};
                border: none; border-radius: 14px;
                font-size: 15px; font-weight: 800; letter-spacing: 0.5px;
            }}
            QPushButton:hover {{ background: {ACCENT_LT}; }}
            QPushButton:pressed {{ background: {ACCENT_DK}; padding-top: 3px; }}
            QPushButton:disabled {{ background: {BORDER}; color: {TEXT_MUT}; border: 1px solid {BORDER_LT}; }}
        """)
        self.btn_start.clicked.connect(self._start)
        layout.addWidget(self.btn_start, alignment=Qt.AlignmentFlag.AlignCenter)

        fmt_container = QWidget()
        fmt_container.setMaximumWidth(600)
        fmt_layout = QVBoxLayout(fmt_container)
        fmt_layout.setContentsMargins(0, 0, 0, 0)
        fmt_layout.setSpacing(8)

        fmt_title = QLabel(get_text("lbl_formats"))
        fmt_title.setStyleSheet(f"color: {TEXT_MUT}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        fmt_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fmt_layout.addWidget(fmt_title)

        fmt_row = QHBoxLayout()
        fmt_row.setSpacing(6)
        fmt_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        formats = ["JPG", "JPEG", "PNG", "BMP", "TIFF", "TIF", "WEBP", "HEIC", "HEIF"]
        for fmt in formats:
            pill = QLabel(fmt)
            pill.setStyleSheet(f"""
                color: {TEXT_SEC}; background: {CARD_BG};
                border: 1px solid {BORDER_LT}; border-radius: 6px;
                padding: 3px 9px; font-size: 10px; font-weight: 700;
                letter-spacing: 0.5px;
            """)
            fmt_row.addWidget(pill)
        fmt_layout.addLayout(fmt_row)
        layout.addWidget(fmt_container, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)
        
        # Donation Button
        self.btn_donate = QPushButton(get_text("btn_donate"))
        self.btn_donate.setFixedSize(140, 32)
        self.btn_donate.setStyleSheet(f"""
            QPushButton {{
                color: {TEXT_SEC}; background: transparent;
                border: 1px solid {BORDER_LT}; border-radius: 16px;
                font-size: 12px; font-weight: 600;
            }}
            QPushButton:hover {{ 
                color: #0079C1; border-color: #0079C1; 
                background: rgba(0, 121, 193, 0.1); 
            }}
            QPushButton:pressed {{ background: rgba(0, 121, 193, 0.2); }}
        """)
        self.btn_donate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_donate.clicked.connect(self._show_donation)
        layout.addWidget(self.btn_donate, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self._folder = None

    def _show_donation(self) -> None:
        """Shows the donation dialog with a QR code."""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
        from PyQt6.QtGui import QPixmap
        import os
        
        dialog = QDialog(self)
        dialog.setWindowTitle(get_text("title_donate"))
        dialog.setFixedSize(350, 450)
        dialog.setStyleSheet(f"QDialog {{ background: {DARK_BG}; }}")
        
        l = QVBoxLayout(dialog)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.setSpacing(15)
        
        msg = QLabel(get_text("msg_donate"))
        msg.setStyleSheet(f"color: {TEXT_PRI}; font-size: 14px;")
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addWidget(msg)
        
        qr_label = QLabel()
        qr_path = os.path.join("assets", "QR_Paypal.png")
        if os.path.exists(qr_path):
            pixmap = QPixmap(qr_path)
            qr_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            qr_label.setText("QR not found")
            qr_label.setStyleSheet(f"color: {TEXT_MUT};")
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addWidget(qr_label)
        
        dialog.exec()

    def _browse(self) -> None:
        """
        Opens a folder selection dialog for the user to pick a target directory.
        """
        folder = QFileDialog.getExistingDirectory(self, get_text("dlg_select_folder"))
        if folder:
            self._folder = folder
            self.folder_label.setText(folder)
            self.folder_label.setStyleSheet(f"color: {TEXT_PRI}; font-size: 12px;")
            self.btn_start.setEnabled(True)

    def _start(self) -> None:
        """
        Emits the start_requested signal with the current configuration values.
        """
        if self._folder:
            mode = "exact" if self.mode_combo.currentIndex() == 1 else "similar"
            self.config['duplicate_mode'] = mode
            self.config['threshold'] = self.slider.value()
            self.config['use_ai'] = self.chk_use_ai.isChecked()
            
            ai_level_map = {0: "fast", 1: "balanced", 2: "deep"}
            self.config['ai_level'] = ai_level_map.get(self.ai_level_combo.currentIndex(), "balanced")
            
            save_config(self.config)
            self.start_requested.emit(self._folder, self.slider.value(), mode)


class ProgressScreen(QWidget):
    """
    Screen showing the progress bar and current status of the analysis.
    """
    continue_requested = pyqtSignal()
    back_requested = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the progress screen.

        Args:
            parent (Optional[QWidget]): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self._setup_ui()
        self.worker = None
        self.log_handler = QPlainTextEditLogger()
        self.log_handler.emitter.log_signal.connect(self._append_log)
        logging.getLogger().addHandler(self.log_handler)

    def _setup_ui(self) -> None:
        """
        Sets up the user interface elements for the progress screen.
        """
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(80, 80, 80, 80)

        self.title = QLabel(get_text("title_analyzing"))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(f"color: {TEXT_PRI}; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title)

        self.progress = QProgressBar()
        self.progress.setFixedHeight(8)
        self.progress.setMaximumWidth(500)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet(f"""
            QProgressBar {{ background: {BORDER}; border-radius: 4px; border: none; }}
            QProgressBar::chunk {{ background: {ACCENT}; border-radius: 4px; }}
        """)
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)

        self.status = QLabel(get_text("lbl_starting"))
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet(f"color: {TEXT_SEC}; font-size: 12px;")
        layout.addWidget(self.status)
        
        # Real-time Log Viewer
        log_label = QLabel(get_text("lbl_logs", "Visor de Logs"))
        log_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        log_label.setStyleSheet(f"color: {TEXT_MUT}; font-size: 12px; font-weight: bold;")
        layout.addWidget(log_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.log_viewer = QPlainTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setMinimumWidth(900)
        self.log_viewer.setMinimumHeight(300)
        self.log_viewer.setStyleSheet(f"""
            QPlainTextEdit {{
                font-family: Consolas, 'Courier New', monospace;
                font-size: 11px;
                background: #1e1e2e;
                color: #a0a0b0;
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        layout.addWidget(self.log_viewer, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_pause = QPushButton(get_text("btn_pause"))
        self.btn_pause.setStyleSheet(f"""
            QPushButton {{
                color: {TEXT_PRI}; background: {ACCENT};
                border: none; border-radius: 10px;
                padding: 8px 20px; font-size: 12px; font-weight: 700;
            }}
            QPushButton:hover {{ background: {ACCENT_LT}; }}
            QPushButton:pressed {{ background: {ACCENT_DK}; }}
        """)
        self.btn_pause.clicked.connect(self._toggle_pause)
        btn_layout.addWidget(self.btn_pause)
        
        layout.addLayout(btn_layout)

        self.summary_container = QWidget()
        self.summary_layout = QVBoxLayout(self.summary_container)
        self.summary_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.summary_container.hide()
        layout.addWidget(self.summary_container, alignment=Qt.AlignmentFlag.AlignCenter)

    def _append_log(self, msg: str) -> None:
        """Appends a new log message and auto-scrolls to bottom."""
        self.log_viewer.appendPlainText(msg)
        bar = self.log_viewer.verticalScrollBar()
        bar.setValue(bar.maximum())

    def update_progress(self, pct: int, msg: str) -> None:
        """
        Updates the progress bar percentage and the status label.

        Args:
            pct (int): Completion percentage.
            msg (str): The current status message.
        """
        self.progress.setValue(pct)
        self.status.setText(msg)
    
    def set_worker(self, worker: object) -> None:
        """
        Associates the analysis worker with this screen to allow pausing and resuming.

        Args:
            worker (object): The worker thread.
        """
        self.worker = worker
        self.log_viewer.clear()
        self.summary_container.hide()
        self.btn_pause.show()
        self.progress.show()
        self.status.show()

    def show_summary(self, stats: object, total_groups: int, dups_found: int) -> None:
        self.btn_pause.hide()
        self.progress.hide()
        self.status.hide()
        
        while self.summary_layout.count():
            item = self.summary_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        summary_panel = QGroupBox(get_text("lbl_summary_title", "Resumen Final"))
        summary_panel.setMinimumWidth(600)
        summary_panel.setStyleSheet(f"""
            QGroupBox {{
                background: {CARD_BG};
                border: 1px solid {BORDER};
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                left: 15px;
                color: {ACCENT};
                font-weight: bold;
            }}
        """)
        s_layout = QVBoxLayout(summary_panel)
        
        lbl_img = QLabel(get_text("lbl_total_images", "Total de imágenes analizadas: {n}").format(n=stats.total_photos))
        lbl_vid = QLabel(get_text("lbl_total_videos", "Total de videos analizados: {n}").format(n=stats.total_videos))
        lbl_dup = QLabel(get_text("lbl_duplicates_found", "Archivos duplicados encontrados: {n}").format(n=dups_found))
        str_yes = get_text("status_yes", "Sí")
        str_no = get_text("status_no", "No")
        json_str = str_yes if stats.json_generated else str_no
        lbl_json = QLabel(get_text("lbl_json_generated", "Archivo .json generado: {status}").format(status=json_str))
        
        for lbl in [lbl_img, lbl_vid, lbl_dup, lbl_json]:
            lbl.setStyleSheet(f"color: {TEXT_PRI}; font-size: 13px;")
            s_layout.addWidget(lbl)
            
        self.summary_layout.addWidget(summary_panel)

        btn_dynamic = QPushButton()
        btn_dynamic.setFixedHeight(40)
        btn_dynamic.setMinimumWidth(200)
        btn_dynamic.setStyleSheet(f"""
            QPushButton {{
                color: #ffffff; background: {ACCENT};
                border: none; border-radius: 8px;
                font-size: 14px; font-weight: bold;
                margin-top: 10px;
            }}
            QPushButton:hover {{ background: {ACCENT_LT}; }}
            QPushButton:pressed {{ background: {ACCENT_DK}; }}
        """)
        
        if total_groups > 0:
            btn_dynamic.setText(get_text("btn_continue", "Continuar"))
            btn_dynamic.clicked.connect(self.continue_requested.emit)
        else:
            btn_dynamic.setText(get_text("btn_back", "Volver"))
            btn_dynamic.clicked.connect(self.back_requested.emit)
            
        self.summary_layout.addWidget(btn_dynamic, alignment=Qt.AlignmentFlag.AlignCenter)
        self.summary_container.show()
    
    def _toggle_pause(self) -> None:
        """
        Toggles the pause state of the worker thread.
        """
        if self.worker:
            if self.worker._paused:
                self.worker.resume()
                self.btn_pause.setText(get_text("btn_pause"))
            else:
                self.worker.pause()
                self.btn_pause.setText(get_text("btn_resume"))


class ResultsScreen(QWidget):
    """
    Screen that presents the user with the found groups of duplicate photos.

    Signals:
        back_requested: Emitted to return to the welcome screen.
    """
    back_requested = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the results screen.

        Args:
            parent (Optional[QWidget]): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self._groups: list[DuplicateGroup] = []
        self._group_widgets: list = []
        self._photos: list[PhotoInfo] = []
        self._stats: Optional[Statistics] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Sets up the layout, buttons, and scrollable area for the results screen.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(64)
        header.setStyleSheet(f"background: {PANEL_BG}; border-bottom: 1px solid {BORDER};")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 0, 20, 0)

        btn_back = QPushButton(get_text("btn_new_search"))
        btn_back.setStyleSheet(f"""
            QPushButton {{
                color: {TEXT_SEC}; background: transparent;
                border: 1px solid {BORDER_LT}; border-radius: 10px;
                padding: 7px 16px; font-size: 12px; font-weight: 600;
            }}
            QPushButton:hover {{ color: {TEXT_PRI}; border-color: {ACCENT}; background: #1e1e30; }}
            QPushButton:pressed {{ padding-top: 8px; padding-bottom: 6px; }}
        """)
        btn_back.clicked.connect(self.back_requested.emit)

        self.summary_label = QLabel()
        self.summary_label.setStyleSheet(f"color: {TEXT_PRI}; font-size: 14px; font-weight: bold;")

        self.resolved_label = QLabel()
        self.resolved_label.setStyleSheet(f"color: {SUCCESS}; font-size: 12px;")

        self.btn_apply_all = QPushButton(get_text("btn_apply_all"))
        self.btn_apply_all.setVisible(False)
        self.btn_apply_all.setStyleSheet(f"""
            QPushButton {{
                color: #ffffff; background: {ACCENT};
                border: none; border-radius: 10px;
                padding: 8px 20px; font-size: 12px; font-weight: 700;
                letter-spacing: 0.3px;
            }}
            QPushButton:hover {{ background: {ACCENT_LT}; }}
            QPushButton:pressed {{ background: {ACCENT_DK}; padding-top: 9px; padding-bottom: 7px; }}
        """)
        self.btn_apply_all.clicked.connect(self._apply_all)

        btn_stats = QPushButton(get_text("btn_stats"))
        btn_stats.setStyleSheet(f"""
            QPushButton {{
                color: {TEXT_SEC}; background: transparent;
                border: 1px solid {BORDER_LT}; border-radius: 10px;
                padding: 7px 16px; font-size: 12px; font-weight: 600;
            }}
            QPushButton:hover {{ color: {TEXT_PRI}; border-color: {ACCENT}; background: #1e1e30; }}
            QPushButton:pressed {{ padding-top: 8px; padding-bottom: 6px; }}
        """)
        btn_stats.clicked.connect(self._show_statistics)

        h_layout.addWidget(btn_back)
        h_layout.addSpacing(20)
        h_layout.addWidget(self.summary_label)
        h_layout.addStretch()
        h_layout.addWidget(btn_stats)
        h_layout.addSpacing(12)
        h_layout.addWidget(self.btn_apply_all)
        h_layout.addSpacing(12)
        h_layout.addWidget(self.resolved_label)
        layout.addWidget(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: {DARK_BG}; }}
            QScrollBar:vertical {{ width: 8px; background: {PANEL_BG}; border-radius: 4px; }}
            QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 4px; min-height: 40px; }}
            QScrollBar::handle:vertical:hover {{ background: {ACCENT}; }}
        """)

        self.content = QWidget()
        self.content.setStyleSheet(f"background: {DARK_BG};")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(16)

        self.scroll.setWidget(self.content)
        layout.addWidget(self.scroll)

    def load_groups(self, groups: list[DuplicateGroup], stats: Optional[Statistics] = None) -> None:
        """
        Loads the duplicate groups into the UI.

        Args:
            groups (list[DuplicateGroup]): The list of duplicate groups to display.
            stats (Optional[Statistics]): The generated statistics from the analysis.
        """
        self._groups = groups
        self._stats = stats
        self._resolved = 0

        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._group_widgets = []

        if not groups:
            no_dup = QLabel(get_text("msg_no_dups"))
            no_dup.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_dup.setStyleSheet(f"color: {SUCCESS}; font-size: 18px; padding: 40px;")
            self.content_layout.addWidget(no_dup)
            self.btn_apply_all.setVisible(False)
        else:
            for i, group in enumerate(groups):
                widget = GroupWidget(group, i + 1)
                widget.action_taken.connect(self._on_action_taken)
                self.content_layout.addWidget(widget)
                self._group_widgets.append(widget)
            self.content_layout.addStretch()
            self.btn_apply_all.setVisible(True)

        total_photos = sum(len(g.photos) for g in groups)
        self.summary_label.setText(get_text("lbl_summary_groups").format(tot_groups=len(groups), tot_photos=total_photos))
        self._update_resolved_label()

    def _apply_all(self) -> None:
        """
        Applies the 'use recommended' action across all pending duplicate groups,
        moving unselected duplicates to a selected folder.
        """
        pending = [w for w in self._group_widgets if not w._resolved]
        if not pending:
            QMessageBox.information(self, get_text("title_no_pending"), get_text("msg_all_resolved"))
            return

        total_move = sum(
            len([c for c in w.cards if not c.is_checked()]) for w in pending
        )
        for w in pending:
            if not any(c.is_checked() for c in w.cards):
                w._select_best_only()

        total_move = sum(
            len([c for c in w.cards if not c.is_checked()]) for w in pending
        )

        dest_folder = QFileDialog.getExistingDirectory(self, get_text("dlg_select_dest"))
        if not dest_folder:
            return

        msg = get_text("msg_apply_all").format(pending=len(pending), to_move=total_move, dest=dest_folder)
        reply = QMessageBox.question(
            self, get_text("title_apply_all"), msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        errors_total = []
        resolved_count = 0
        for w in pending:
            w._select_best_only()
            to_move = [c.photo for c in w.cards if not c.is_checked()]
            if not to_move:
                w._mark_resolved(get_text("status_no_changes"), TEXT_SEC)
                resolved_count += 1
                continue

            errors = []
            for photo in to_move:
                try:
                    src = Path(photo.path).resolve()
                    if not src.exists():
                        errors.append(f"{photo.filename}: not found")
                        continue
                    dest_dir = Path(dest_folder) / "duplicados"
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    dest = dest_dir / src.name
                    counter = 1
                    while dest.exists():
                        dest = dest_dir / f"{src.stem}_dup{counter}{src.suffix}"
                        counter += 1
                    shutil.move(str(src), str(dest))
                except Exception as e:
                    errors.append(f"{photo.filename}: {e}")

            if errors:
                errors_total.extend(errors)
            moved_ok = len(to_move) - len(errors)
            if moved_ok > 0:
                w._mark_resolved(get_text("status_resolved").format(moved=moved_ok), SUCCESS)
                w.btn_apply.setEnabled(False)
                for card in w.cards:
                    if not card.is_checked():
                        card.hide()
                w.lbl_selection.setText(get_text("lbl_kept"))
                resolved_count += 1
            else:
                w._mark_resolved(get_text("status_error"), DANGER)

        self._resolved = sum(1 for w in self._group_widgets if w._resolved)
        self._update_resolved_label()

        if errors_total:
            detail = "\n".join(errors_total[:10]) + ("\n..." if len(errors_total) > 10 else "")
            QMessageBox.warning(self, get_text("title_errors"), get_text("msg_errors").format(resolved=resolved_count, detail=detail))
        else:
            QMessageBox.information(self, get_text("title_completed"), get_text("msg_completed").format(resolved=resolved_count))

        if self._resolved == len(self._groups):
            QTimer.singleShot(1000, self.back_requested.emit)

    def _on_action_taken(self) -> None:
        """
        Slot triggered when a specific group resolves its duplicates.
        Updates the total count of resolved groups.
        """
        self._resolved += 1
        self._update_resolved_label()

    def _update_resolved_label(self) -> None:
        """
        Updates the label showing the number of resolved groups vs total groups.
        """
        total = len(self._groups)
        self.resolved_label.setText(get_text("lbl_resolved_groups").format(res=self._resolved, tot=total))

    def _show_statistics(self) -> None:
        """
        Displays a dialog with the generated statistics.
        """
        if self._stats:
            dialog = StatisticsDialog(self._stats, self)
            dialog.exec()