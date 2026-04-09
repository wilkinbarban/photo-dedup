import os
import csv
import shutil
from pathlib import Path
from PIL import Image
from typing import Optional

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QMessageBox, QScrollArea, QWidget, QPushButton, QComboBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QColor, QCursor

from core.models import PhotoInfo, DuplicateGroup, Statistics
from core.state import log_history
from core.i18n import get_text
from ui.theme import *

def make_thumbnail(path: str, size: int = 220) -> QPixmap:
    """
    Creates a thumbnail for a given image path.

    Args:
        path (str): File path of the image.
        size (int, optional): The target size of the thumbnail (square). Defaults to 220.

    Returns:
        QPixmap: A QPixmap object containing the generated thumbnail or a solid color block if generation fails.
    """
    try:
        with Image.open(path) as img:
            img = img.convert('RGB')
            img.thumbnail((size, size), Image.LANCZOS)
            data = img.tobytes('raw', 'RGB')
            qimg = QImage(data, img.width, img.height, img.width * 3, QImage.Format.Format_RGB888)
            return QPixmap.fromImage(qimg)
    except Exception:
        px = QPixmap(size, size)
        px.fill(QColor(CARD_BG))
        return px

class PhotoCard(QFrame):
    """
    A widget representing a single photo within a duplicate group, 
    allowing the user to select or deselect it.

    Signals:
        selected (bool): Emits the current selection state.
    """
    selected = pyqtSignal(bool)

    def __init__(self, photo: PhotoInfo, is_best: bool = False, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the PhotoCard widget.

        Args:
            photo (PhotoInfo): Photo information object.
            is_best (bool, optional): Indicates whether this photo is the recommended one in the group. Defaults to False.
            parent (Optional[QWidget]): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.photo = photo
        self.is_best = is_best
        self._selected = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Sets up the internal user interface for the photo card.
        """
        self.setFixedWidth(240)
        self.setMinimumHeight(340)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._update_style(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        badge_row = QHBoxLayout()
        if self.is_best:
            badge = QLabel(get_text("badge_rec"))
            badge.setStyleSheet(f"""
                color: {SUCCESS}; background: {SUCCESS_BG};
                border: 1px solid {SUCCESS}; border-radius: 20px;
                padding: 3px 10px; font-size: 9px; font-weight: 700; letter-spacing: 0.5px;
            """)
            badge_row.addWidget(badge)
        badge_row.addStretch()

        self.chk = QCheckBox()
        self.chk.setStyleSheet(f"""
            QCheckBox::indicator {{ width: 18px; height: 18px; border-radius: 4px;
                border: 2px solid {BORDER}; background: {CARD_BG}; }}
            QCheckBox::indicator:checked {{ background: {ACCENT}; border-color: {ACCENT}; }}
        """)
        self.chk.stateChanged.connect(self._on_check)
        badge_row.addWidget(self.chk)
        layout.addLayout(badge_row)

        thumb_label = QLabel()
        thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb_label.setFixedHeight(200)
        px = make_thumbnail(self.photo.path, 200)
        thumb_label.setPixmap(px)
        thumb_label.setStyleSheet(f"border-radius: 8px; background: {DARK_BG};")
        layout.addWidget(thumb_label)

        name = QLabel(self.photo.filename)
        name.setStyleSheet(f"color: {TEXT_PRI}; font-size: 11px; font-weight: 600;")
        name.setWordWrap(True)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name)

        location_str = ""
        if getattr(self.photo, 'geo_data', None):
            lat = self.photo.geo_data.get('latitude', 0)
            lon = self.photo.geo_data.get('longitude', 0)
            location_str = f"\n📍 {abs(lat):.4f}°{'N' if lat >= 0 else 'S'}, {abs(lon):.4f}°{'E' if lon >= 0 else 'W'}"

        stats = QLabel(
            f"📐 {self.photo.width}×{self.photo.height}  •  {self.photo.megapixels:.1f}MP\n"
            f"💾 {self.photo.size_mb:.2f} MB"
            f"{'  •  📷 EXIF' if self.photo.has_exif else ''}\n"
            + get_text("lbl_sharpness").format(shp=f"{self.photo.sharpness:.0f}") + location_str
        )
        stats.setStyleSheet(f"color: {TEXT_SEC}; font-size: 10px; line-height: 1.4;")
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stats)

        score_pct = min(int(self.photo.score), 100)
        score_bar = QFrame()
        score_bar.setFixedHeight(4)
        score_bar.setStyleSheet(f"background: {BORDER}; border-radius: 2px;")
        fill = QFrame(score_bar)
        fill.setFixedHeight(4)
        fill.setFixedWidth(int(220 * score_pct / 100))
        color = SUCCESS if score_pct >= 60 else (WARNING if score_pct >= 30 else DANGER)
        fill.setStyleSheet(f"background: {color}; border-radius: 2px;")
        layout.addWidget(score_bar)

        score_lbl = QLabel(get_text("lbl_quality").format(pct=score_pct))
        score_lbl.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: bold;")
        score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(score_lbl)

        layout.addStretch()

        if self.is_best:
            self.chk.setChecked(True)

    def _on_check(self, state: int) -> None:
        """
        Slot triggered when the checkbox state changes.

        Args:
            state (int): The new check state.
        """
        self._selected = state == Qt.CheckState.Checked.value
        self._update_style(self._selected)
        self.selected.emit(self._selected)

    def _update_style(self, sel: bool) -> None:
        """
        Updates the card's visual style depending on its selection state.

        Args:
            sel (bool): Whether the card is selected.
        """
        border_color = ACCENT if sel else BORDER
        bg = "#22223a" if sel else CARD_BG
        self.setStyleSheet(f"""
            PhotoCard {{
                background: {bg};
                border: 2px solid {border_color};
                border-radius: 12px;
            }}
        """)

    def mousePressEvent(self, event: object) -> None:
        """
        Toggles the checkbox when the card itself is clicked.

        Args:
            event (object): The mouse event.
        """
        self.chk.setChecked(not self.chk.isChecked())

    def is_checked(self) -> bool:
        """
        Returns whether the card is checked.

        Returns:
            bool: True if checked, False otherwise.
        """
        return self.chk.isChecked()

    def set_checked(self, val: bool) -> None:
        """
        Sets the checked state of the card.

        Args:
            val (bool): The check state.
        """
        self.chk.setChecked(val)


class StatisticsDialog(QMessageBox):
    """
    A dialog displaying analysis statistics.
    """
    def __init__(self, stats: Statistics, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the statistics dialog.

        Args:
            stats (Statistics): The generated statistics.
            parent (Optional[QWidget]): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.setWindowTitle(get_text("title_stats"))
        self.setIcon(QMessageBox.Icon.Information)
        
        text = get_text("stats_html").format(
            total_photos=stats.total_photos,
            total_groups=stats.total_groups,
            avg_sim=stats.avg_similarity,
            total_size=stats.total_size_mb,
            dup_size=stats.duplicate_size_mb,
            recov_size=stats.recoverable_mb
        )
        
        for ext, data in sorted(stats.by_format.items(), key=lambda x: x[1]['size_mb'], reverse=True):
            text += f"\n• {ext.upper()}: {data['count']} photos ({data['size_mb']:.2f} MB)"
        
        self.setText(text)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)


class GroupWidget(QFrame):
    """
    A widget representing an entire group of duplicates, rendering multiple PhotoCards
    and action buttons to process them.

    Signals:
        action_taken: Emitted when the group's duplicates are successfully resolved.
    """
    action_taken = pyqtSignal()

    def __init__(self, group: DuplicateGroup, group_number: int, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the GroupWidget.

        Args:
            group (DuplicateGroup): The duplicate group object.
            group_number (int): The index of the group.
            parent (Optional[QWidget]): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.group = group
        self.group_number = group_number
        self.cards: list[PhotoCard] = []
        self._resolved = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Sets up the internal user interface for the group, adding photo cards 
        and action buttons.
        """
        self.setStyleSheet(f"""
            GroupWidget {{
                background: {PANEL_BG};
                border: 1px solid {BORDER_LT};
                border-radius: 18px;
                margin: 4px 2px;
            }}
            GroupWidget:hover {{
                border-color: {ACCENT};
            }}
        """)

        main = QVBoxLayout(self)
        main.setContentsMargins(16, 16, 16, 16)
        main.setSpacing(12)

        header = QHBoxLayout()
        
        header_vbox = QVBoxLayout()
        title = QLabel(get_text("lbl_group").format(num=self.group_number))
        title.setStyleSheet(f"color: {ACCENT}; font-size: 14px; font-weight: bold;")
        
        n = len(self.group.photos)
        sim_pct = f"{self.group.similarity:.0f}%"
        match_type = getattr(self.group, 'match_type', 'similar (hash)')
        
        subtitle_layout = QHBoxLayout()
        subtitle = QLabel(get_text("lbl_group_sub").format(n=n, sim=sim_pct))
        subtitle.setStyleSheet(f"color: {TEXT_SEC}; font-size: 12px;")
        subtitle_layout.addWidget(subtitle)
        
        match_badge = QLabel(match_type.upper())
        if "IA" in match_type:
            match_color = "#9b51e0"
            match_bg = "#2a163d"
        elif "exact" in match_type:
            match_color = SUCCESS
            match_bg = SUCCESS_BG
        else:
            match_color = "#3498db"
            match_bg = "#1a3a52"
            
        match_badge.setStyleSheet(f"""
            color: {match_color}; background: {match_bg};
            border: 1px solid {match_color}; border-radius: 8px;
            padding: 2px 8px; font-size: 9px; font-weight: bold;
        """)
        subtitle_layout.addWidget(match_badge)
        subtitle_layout.addStretch()

        header_vbox.addWidget(title)
        header_vbox.addLayout(subtitle_layout)
        
        header.addLayout(header_vbox)
        header.addStretch()

        self.status_badge = QLabel(get_text("badge_pending"))
        self.status_badge.setStyleSheet(f"""
            color: {WARNING}; background: {WARNING_BG};
            border: 1px solid {WARNING}; border-radius: 20px;
            padding: 3px 12px; font-size: 10px; font-weight: 700;
            letter-spacing: 0.5px;
        """)
        header.addWidget(self.status_badge)
        main.addLayout(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER};")
        main.addWidget(sep)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)
        for i, photo in enumerate(self.group.photos):
            card = PhotoCard(photo, is_best=(i == self.group.best_index))
            card.selected.connect(self._on_selection_changed)
            self.cards.append(card)
            cards_layout.addWidget(card)
        cards_layout.addStretch()

        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(380)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:horizontal {{ height: 6px; background: {BORDER}; border-radius: 3px; }}
            QScrollBar::handle:horizontal {{ background: {ACCENT}; border-radius: 3px; }}
        """)

        container = QWidget()
        container.setLayout(cards_layout)
        container.setStyleSheet("background: transparent;")
        scroll.setWidget(container)
        main.addWidget(scroll)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.lbl_selection = QLabel(get_text("lbl_select_keep"))
        self.lbl_selection.setStyleSheet(f"color: {TEXT_SEC}; font-size: 11px;")
        btn_row.addWidget(self.lbl_selection)
        btn_row.addStretch()

        action_row = QHBoxLayout()
        action_row.addWidget(QLabel(get_text("lbl_action")))
        self.action_combo = QComboBox()
        self.action_combo.addItems([get_text("opt_move"), get_text("opt_delete")])
        action_row.addWidget(self.action_combo)
        action_row.addStretch()
        main.addLayout(action_row)

        btn_best = QPushButton(get_text("btn_use_rec"))
        btn_best.setStyleSheet(self._btn_style("success"))
        btn_best.clicked.connect(self._select_best_only)

        btn_all = QPushButton(get_text("btn_all"))
        btn_all.setStyleSheet(self._btn_style("ghost_sm"))
        btn_all.clicked.connect(self._select_all)

        btn_none = QPushButton(get_text("btn_none"))
        btn_none.setStyleSheet(self._btn_style("ghost_sm"))
        btn_none.clicked.connect(self._select_none)

        self.btn_apply = QPushButton(get_text("btn_apply_action"))
        self.btn_apply.setStyleSheet(self._btn_style("primary"))
        self.btn_apply.clicked.connect(self._apply_action)

        btn_export = QPushButton(get_text("btn_export_csv"))
        btn_export.setStyleSheet(self._btn_style("ghost"))
        btn_export.clicked.connect(self._export_csv)

        for b in [btn_best, btn_all, btn_none, self.btn_apply, btn_export]:
            btn_row.addWidget(b)

        main.addLayout(btn_row)

    def _btn_style(self, kind: str = "ghost") -> str:
        """
        Returns the CSS style string for a specific kind of button.

        Args:
            kind (str, optional): The style type (primary, success, danger, ghost, ghost_sm). Defaults to "ghost".

        Returns:
            str: The corresponding CSS string.
        """
        styles = {
            "primary": f"""
                QPushButton {{
                    color: #ffffff; background: {ACCENT};
                    border: none; border-radius: 10px;
                    padding: 8px 20px; font-size: 12px; font-weight: 700;
                    letter-spacing: 0.3px;
                }}
                QPushButton:hover {{ background: {ACCENT_LT}; }}
                QPushButton:pressed {{ background: {ACCENT_DK}; padding-top: 9px; padding-bottom: 7px; }}
                QPushButton:disabled {{ background: {BORDER}; color: {TEXT_MUT}; }}
            """,
            "success": f"""
                QPushButton {{
                    color: {SUCCESS}; background: {SUCCESS_BG};
                    border: 1px solid {SUCCESS}; border-radius: 10px;
                    padding: 7px 18px; font-size: 12px; font-weight: 700;
                }}
                QPushButton:hover {{ background: #163d26; border-color: #50e890; color: #50e890; }}
                QPushButton:pressed {{ padding-top: 8px; padding-bottom: 6px; }}
            """,
            "danger": f"""
                QPushButton {{
                    color: {DANGER}; background: #2a0f0f;
                    border: 1px solid {DANGER}; border-radius: 10px;
                    padding: 7px 18px; font-size: 12px; font-weight: 700;
                }}
                QPushButton:hover {{ background: #3a1414; }}
                QPushButton:pressed {{ padding-top: 8px; padding-bottom: 6px; }}
            """,
            "ghost": f"""
                QPushButton {{
                    color: {TEXT_SEC}; background: transparent;
                    border: 1px solid {BORDER_LT}; border-radius: 10px;
                    padding: 7px 16px; font-size: 12px; font-weight: 600;
                }}
                QPushButton:hover {{ color: {TEXT_PRI}; border-color: {ACCENT}; background: #1e1e30; }}
                QPushButton:pressed {{ padding-top: 8px; padding-bottom: 6px; }}
            """,
            "ghost_sm": f"""
                QPushButton {{
                    color: {TEXT_SEC}; background: transparent;
                    border: 1px solid {BORDER}; border-radius: 8px;
                    padding: 5px 12px; font-size: 11px; font-weight: 600;
                }}
                QPushButton:hover {{ color: {TEXT_PRI}; border-color: {BORDER_LT}; background: {CARD_HOV}; }}
                QPushButton:pressed {{ padding-top: 6px; padding-bottom: 4px; }}
            """,
        }
        return styles.get(kind, styles["ghost"])

    def _on_selection_changed(self) -> None:
        """
        Updates the UI to reflect the number of currently selected photos to keep.
        """
        selected = sum(1 for c in self.cards if c.is_checked())
        total = len(self.cards)
        self.lbl_selection.setText(get_text("lbl_selection").format(sel=selected, tot=total))

    def _select_best_only(self) -> None:
        """
        Selects only the recommended photo, deselecting the rest.
        """
        for i, card in enumerate(self.cards):
            card.set_checked(i == self.group.best_index)

    def _select_all(self) -> None:
        """
        Selects all photo cards in the group.
        """
        for card in self.cards:
            card.set_checked(True)

    def _select_none(self) -> None:
        """
        Deselects all photo cards in the group.
        """
        for card in self.cards:
            card.set_checked(False)

    def _apply_action(self) -> None:
        """
        Applies the selected action (move or delete) to the unselected photos in the group.
        """
        to_keep = [c.photo for c in self.cards if c.is_checked()]
        to_move = [c.photo for c in self.cards if not c.is_checked()]

        if len(to_keep) == 0:
            QMessageBox.warning(self, get_text("title_no_sel"), get_text("msg_no_keep"))
            return

        if len(to_move) == 0:
            QMessageBox.information(self, get_text("title_no_changes"), get_text("msg_no_move"))
            self._mark_resolved(get_text("status_no_changes"), TEXT_SEC)
            return

        action = self.action_combo.currentText()

        if action == "Delete permanently":
            msg = get_text("msg_del").format(move=len(to_move), files="\n".join(f"  • {p.filename}" for p in to_move), keep=len(to_keep))
            reply = QMessageBox.question(self, get_text("title_del"), msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return

            errors = []
            for photo in to_move:
                try:
                    try:
                        import send2trash
                        send2trash.send2trash(photo.path)
                    except ImportError:
                        os.remove(photo.path)
                    log_history("delete", {"file": photo.path, "group": self.group_number})
                except Exception as e:
                    errors.append(f"{photo.filename}: {e}")

            moved_ok = len(to_move) - len(errors)
            if errors:
                detail = "\n".join(errors)
                QMessageBox.warning(self, get_text("title_del_err"), get_text("msg_del_err").format(ok=moved_ok, tot=len(to_move), detail=detail))
            if moved_ok > 0:
                self._mark_resolved(get_text("status_deleted").format(ok=moved_ok), SUCCESS)
                self.action_taken.emit()
                for card in self.cards:
                    if not card.is_checked():
                        card.hide()
                self.lbl_selection.setText(get_text("lbl_kept"))
        else:
            dest_folder = QFileDialog.getExistingDirectory(self.window(), get_text("dlg_select_dest"))
            if not dest_folder:
                return

            msg = get_text("msg_move").format(move=len(to_move), dest=dest_folder, files="\n".join(f"  • {p.filename}" for p in to_move), keep=len(to_keep))
            reply = QMessageBox.question(self, get_text("title_move"), msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return

            errors = []
            for photo in to_move:
                try:
                    src = Path(photo.path).resolve()
                    if not src.exists():
                        errors.append(f"{photo.filename}: origin file not found ({src})")
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

            moved_ok = len(to_move) - len(errors)
            if errors:
                detail = "\n".join(errors)
                QMessageBox.warning(self, get_text("title_move_err"), get_text("msg_move_err").format(ok=moved_ok, tot=len(to_move), detail=detail))
            if moved_ok > 0:
                successfully_moved = [p.path for i, p in enumerate(to_move) if i < len(to_move) - len(errors)]
                log_history("move", {
                    "files": successfully_moved,
                    "destination": str(dest_folder),
                    "group": self.group_number,
                    "count": moved_ok
                })
                self._mark_resolved(get_text("status_moved").format(ok=moved_ok), SUCCESS)
                self.action_taken.emit()
                for card in self.cards:
                    if not card.is_checked():
                        card.hide()
                self.lbl_selection.setText(get_text("lbl_kept"))

    def _mark_resolved(self, text: str, color: str) -> None:
        """
        Marks the group as resolved, updating its badge status and disabling the apply button.

        Args:
            text (str): The text to show in the status badge.
            color (str): The color code for the badge text and border.
        """
        self._resolved = True
        self.status_badge.setText(text)
        bg = SUCCESS_BG if color == SUCCESS else WARNING_BG if color == WARNING else "#1a0a0a"
        self.status_badge.setStyleSheet(f"""
            color: {color}; background: {bg};
            border: 1px solid {color}; border-radius: 20px;
            padding: 3px 12px; font-size: 10px; font-weight: 700;
            letter-spacing: 0.5px;
        """)
        self.btn_apply.setEnabled(False)
        self.btn_apply.setText(get_text("btn_resolved"))
        self.btn_apply.setStyleSheet(f"""
            QPushButton {{
                color: {TEXT_MUT}; background: {BORDER};
                border: none; border-radius: 10px;
                padding: 8px 20px; font-size: 12px; font-weight: 700;
            }}
        """)

    def _export_csv(self) -> None:
        """
        Exports the details of the photos in this group to a CSV file.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, get_text("dlg_save_csv"), "", "CSV Files (*.csv)")
        if not file_path:
            return
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Group', 'File', 'Size (MB)', 'Resolution', 'Sharpness', 'EXIF Date', 'Location', 'Title', 'Description', 'Quality'])
                for i, photo in enumerate(self.group.photos):
                    loc = ""
                    if getattr(photo, 'geo_data', None):
                        loc = f"{photo.geo_data.get('latitude', 0)}, {photo.geo_data.get('longitude', 0)}"
                    writer.writerow([
                        self.group_number,
                        photo.path,
                        f"{photo.size_mb:.2f}",
                        f"{photo.width}x{photo.height}",
                        f"{photo.sharpness:.0f}",
                        photo.exif_date or 'N/A',
                        loc,
                        getattr(photo, 'title', '') or '',
                        getattr(photo, 'description', '') or '',
                        f"{photo.score:.1f}"
                    ])
            QMessageBox.information(self, get_text("title_exported"), get_text("msg_exported").format(file=file_path))
        except Exception as e:
            QMessageBox.warning(self, get_text("title_export_err"), get_text("msg_export_err").format(err=e))