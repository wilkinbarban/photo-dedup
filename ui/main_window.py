import os
import logging
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt

from core.analyzer import AnalysisWorker
from core.models import DuplicateGroup, Statistics
from core.state import CACHE_FILE
from core.i18n import get_text
from ui.theme import *
from ui.screens import WelcomeScreen, ProgressScreen, ResultsScreen

class MainWindow(QMainWindow):
    """
    Main application window managing the primary UI views (Welcome, Progress, Results).

    Attributes:
        stack (QStackedWidget): Widget used to manage the different screens.
        welcome (WelcomeScreen): The start screen.
        progress_screen (ProgressScreen): The analysis progress screen.
        results (ResultsScreen): The screen showing duplicate groups.
    """

    def __init__(self) -> None:
        """
        Initializes the MainWindow.
        """
        super().__init__()
        self.setWindowTitle(get_text("app_title"))
        self.setMinimumSize(1000, 700)
        self.resize(1280, 800)
        self._worker = None
        self._setup_style()
        self._setup_ui()

    def _setup_style(self) -> None:
        """
        Applies global CSS styling to the main window and common widgets.
        """
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background: {DARK_BG}; color: {TEXT_PRI}; }}
            QLabel {{ color: {TEXT_PRI}; }}
            QMessageBox {{ background: {PANEL_BG}; }}
            QMessageBox QLabel {{ color: {TEXT_PRI}; }}
            QMessageBox QPushButton {{
                color: {TEXT_PRI}; background: {CARD_BG};
                border: 1px solid {BORDER}; border-radius: 6px; padding: 6px 16px;
            }}
        """)

    def _setup_ui(self) -> None:
        """
        Sets up the internal user interface, initializing the stacked widget and its child screens.
        """
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.welcome = WelcomeScreen()
        self.welcome.start_requested.connect(self._start_analysis)

        self.progress_screen = ProgressScreen()
        self.progress_screen.continue_requested.connect(lambda: self.stack.setCurrentIndex(2))
        self.progress_screen.back_requested.connect(self._go_home)

        self.results = ResultsScreen()
        self.results.back_requested.connect(self._go_home)

        self.stack.addWidget(self.welcome)       # 0
        self.stack.addWidget(self.progress_screen)  # 1
        self.stack.addWidget(self.results)       # 2

    def _start_analysis(self, folder: str, threshold: int, duplicate_mode: str = "similar") -> None:
        """
        Starts the duplicate analysis process by launching a worker thread.

        Args:
            folder (str): Folder path to analyze.
            threshold (int): Similarity threshold.
            duplicate_mode (str, optional): Analysis mode ("similar" or "exact"). Defaults to "similar".
        """
        self.stack.setCurrentIndex(1)
        self.progress_screen.set_worker(None)

        from core.state import load_config
        config = load_config()
        use_ai = config.get('use_ai', False)
        ai_level = config.get('ai_level', 'balanced')

        self._worker = AnalysisWorker(folder, threshold, duplicate_mode, use_ai, ai_level)
        self.progress_screen.set_worker(self._worker)
        self._worker.progress.connect(self.progress_screen.update_progress)
        self._worker.finished.connect(self._on_analysis_done)
        self._worker.error.connect(self._on_analysis_error)
        self._worker.start()

    def _on_analysis_done(self, groups: list[DuplicateGroup], extra_stats: dict) -> None:
        """
        Slot called when the analysis worker successfully finishes.
        Calculates total statistics and switches to the results screen.

        Args:
            groups (list[DuplicateGroup]): The duplicate groups identified during analysis.
            extra_stats (dict): Extra statistics such as videos processed and JSONs processed.
        """
        all_photos = []
        for group in groups:
            all_photos.extend(group.photos)
        
        stats = Statistics()
        stats.total_photos = extra_stats.get('total_photos', len(all_photos))
        stats.total_groups = len(groups)
        stats.total_videos = extra_stats.get('videos', 0)
        stats.json_generated = extra_stats.get('jsons', False)
        
        for photo in all_photos:
            stats.total_size_mb += photo.size_mb
        
        for group in groups:
            group_size = sum(p.size_mb for p in group.photos)
            best_size = group.photos[group.best_index].size_mb
            stats.duplicate_size_mb += group_size
            stats.recoverable_mb += group_size - best_size
        
        if groups:
            stats.avg_similarity = sum(g.similarity for g in groups) / len(groups)
        
        formats = {}
        for photo in all_photos:
            ext = Path(photo.path).suffix.lower()
            if ext not in formats:
                formats[ext] = {'count': 0, 'size_mb': 0}
            formats[ext]['count'] += 1
            formats[ext]['size_mb'] += photo.size_mb
        stats.by_format = formats
        
        self.results.load_groups(groups, stats)
        
        dups_found = sum(len(g.photos) - 1 for g in groups) if groups else 0
        self.progress_screen.show_summary(stats, len(groups), dups_found)

    def _on_analysis_error(self, msg: str) -> None:
        """
        Slot called when the analysis worker encounters an error.
        Displays an error dialog and returns to the welcome screen.

        Args:
            msg (str): Error message.
        """
        QMessageBox.critical(self, get_text("title_error"), msg)
        self.stack.setCurrentIndex(0)

    def _go_home(self) -> None:
        """
        Cancels any ongoing analysis and returns to the welcome screen.
        """
        if self._worker and self._worker.isRunning():
            self._worker.stop()
            self._worker.wait()
        self.stack.setCurrentIndex(0)

    def closeEvent(self, event: object) -> None:
        """
        Handles the application close event, stopping background tasks and asking 
        the user if they want to clear the analysis cache.

        Args:
            event (QCloseEvent): The close event.
        """
        if self._worker and self._worker.isRunning():
            self._worker.stop()
            self._worker.wait()

        if Path(CACHE_FILE).exists():
            reply = QMessageBox.question(
                self,
                get_text("title_clear_cache"),
                get_text("msg_clear_cache"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    os.remove(CACHE_FILE)
                except Exception as e:
                    logging.error(f"Error removing cache on exit: {e}")

        event.accept()