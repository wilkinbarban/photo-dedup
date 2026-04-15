"""
PhotoDedup - Intelligent Duplicate Photo Finder.
Canonical application entry point.
"""

__version__ = "1.0.15"

import sys
import warnings
import logging
import os


# Ensure absolute imports like src.* work when running this file directly
# (python src/main/photo_dedup.py) and when frozen by PyInstaller.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def show_dependency_error(error_msg: str) -> None:
    """
    Displays a dependency error message and instructions on how to install them.
    It attempts to show a graphical message box using tkinter, falling back to
    console output and pausing the console on Windows.

    Args:
        error_msg (str): The specific error message indicating the missing package.

    Returns:
        None
    """
    print("\n" + "=" * 60)
    print(" DEPENDENCY ERROR")
    print("=" * 60)
    print(f" A required package is missing: {error_msg}")
    print("\n Please install dependencies by running the file:")
    print(" -> install_dependencies.bat")
    print("\n Or run manually in the console:")
    print(" -> pip install -r requirements.txt")
    print("=" * 60 + "\n")

    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Dependency Error",
            f"A required package is missing:\n{error_msg}\n\n"
            "Please install dependencies by running the file:\n"
            "install_dependencies.bat\n\n"
            "Or by running in the console:\npip install -r requirements.txt"
        )
        root.destroy()
    except Exception:
        if sys.platform == "win32":
            os.system("pause")

    sys.exit(1)


try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QFont

    from src.modules.utils.paths import resolve_asset_path

    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
    except Exception:
        pass

    warnings.filterwarnings("ignore", category=UserWarning, module="PIL")

    from src.interfaces.main_window import MainWindow
except ImportError as e:
    show_dependency_error(str(e))


def main() -> None:
    """
    Main entry point for the PhotoDedup application.
    Initializes the PyQt6 application, sets the application name and font,
    and displays the main window.

    Returns:
        None
    """
    import multiprocessing
    multiprocessing.freeze_support()

    from src.modules.utils.logger import setup_logger
    setup_logger()

    app = QApplication(sys.argv)

    from PyQt6.QtCore import qInstallMessageHandler

    def qt_message_handler(mode, context, message):
        if "QFont::setPointSize" in message:
            return
        logging.getLogger().debug(f"Qt: {message}")

    qInstallMessageHandler(qt_message_handler)

    from src.interfaces.language_dialog import LanguageDialog
    from src.modules.config.i18n import set_language, get_text

    dialog = LanguageDialog()
    from PyQt6.QtWidgets import QDialog
    if dialog.exec() == QDialog.DialogCode.Accepted:
        set_language(dialog.selected_language)
    else:
        sys.exit(0)

    app.setApplicationName(get_text("app_title"))
    app.setFont(QFont("Segoe UI", 10))

    from PyQt6.QtGui import QIcon
    icon_path = resolve_asset_path("assets", "Icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
