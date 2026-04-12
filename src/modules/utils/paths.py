import os
import sys
from pathlib import Path


def resolve_asset_path(*parts: str) -> str:
    """Resolve asset paths for both source execution and PyInstaller bundles."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_dir = Path(getattr(sys, "_MEIPASS"))
    else:
        base_dir = Path(__file__).resolve().parents[3]
    return os.fspath(base_dir.joinpath(*parts))
