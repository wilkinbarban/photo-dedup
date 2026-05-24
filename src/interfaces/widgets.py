import csv
import os
import shutil
from pathlib import Path
from typing import Optional

from PIL import Image
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QCursor, QImage, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.interfaces.theme import *
from src.modules.config.i18n import get_text
from src.modules.config.state import log_history
from src.modules.services.models import DuplicateGroup, PhotoInfo, Statistics
from src.modules.utils.errors import file_error_message


def make_thumbnail(path: str, size: int = 220) -> QPixmap:
    """Create a thumbnail, returning a neutral placeholder if the image cannot be read."""
    try:
        with Image.open(path) as img:
            img = img.convert("RGB")
            img.thumbnail((size, size), Image.LANCZOS)
            data = img.tobytes("raw", "RGB")
            qimg = QImage(data, img.width, img.height, img.width * 3, QImage.Format.Format_RGB888)
            return QPixmap.fromImage(qimg)
    except Exception:
        px = QPixmap(size, size)
        px.fill(QColor(CARD_BG))
        return px


class PhotoCard(QFrame):
    """Selectable photo card inside a duplicate group."""

    selected = pyqtSignal(bool)

    def __init__(self, photo: PhotoInfo, is_best: bool = False, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.photo = photo
        self.is_best = is_best
        self._selected = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setFixedWidth(244)
        self.setMinimumHeight(348)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._update_style(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(7)

        badge_row = QHBoxLayout()
        if self.is_best:
            badge = QLabel(get_text("badge_rec"))
            badge.setStyleSheet(badge_style(SUCCESS, SUCCESS_BG))
            badge_row.addWidget(badge)
        badge_row.addStretch()

        self.chk = QCheckBox()
        self.chk.stateChanged.connect(self._on_check)
        badge_row.addWidget(self.chk)
        layout.addLayout(badge_row)

        thumb_label = QLabel()
        thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb_label.setFixedHeight(204)
        thumb_label.setPixmap(make_thumbnail(self.photo.path, 204))
        thumb_label.setStyleSheet(f"border-radius: 10px; background: {SURFACE};")
        layout.addWidget(thumb_label)

        name = QLabel(self.photo.filename)
        name.setStyleSheet(f"color: {TEXT_PRI}; font-size: 11px; font-weight: 800;")
        name.setWordWrap(True)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name)

        location_str = ""
        if getattr(self.photo, "geo_data", None):
            lat = self.photo.geo_data.get("latitude", 0)
            lon = self.photo.geo_data.get("longitude", 0)
            location_str = f"\nLOC {abs(lat):.4f} deg {'N' if lat >= 0 else 'S'}, {abs(lon):.4f} deg {'E' if lon >= 0 else 'W'}"

        stats = QLabel(
            f"{self.photo.width}x{self.photo.height}  |  {self.photo.megapixels:.1f}MP\n"
            f"{self.photo.size_mb:.2f} MB"
            f"{'  |  EXIF' if self.photo.has_exif else ''}\n"
            + get_text("lbl_sharpness").format(shp=f"{self.photo.sharpness:.0f}")
            + location_str
        )
        stats.setStyleSheet(f"color: {TEXT_SEC}; font-size: 10px; line-height: 1.4;")
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stats)

        score_pct = min(int(self.photo.score), 100)
        color = SUCCESS if score_pct >= 60 else (WARNING if score_pct >= 30 else DANGER)

        score_bar = QFrame()
        score_bar.setFixedHeight(5)
        score_bar.setStyleSheet(f"background: {SURFACE_ALT}; border-radius: 2px;")
        fill = QFrame(score_bar)
        fill.setFixedHeight(5)
        fill.setFixedWidth(int(224 * score_pct / 100))
        fill.setStyleSheet(f"background: {color}; border-radius: 2px;")
        layout.addWidget(score_bar)

        score_lbl = QLabel(get_text("lbl_quality").format(pct=score_pct))
        score_lbl.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: 800;")
        score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(score_lbl)
        layout.addStretch()

        if self.is_best:
            self.chk.setChecked(True)

    def _on_check(self, state: int) -> None:
        self._selected = state == Qt.CheckState.Checked.value
        self._update_style(self._selected)
        self.selected.emit(self._selected)

    def _update_style(self, selected: bool) -> None:
        border_color = ACCENT if selected else BORDER
        bg = "#12312f" if selected else CARD_BG
        self.setStyleSheet(f"""
            PhotoCard {{
                background: {bg};
                border: 2px solid {border_color};
                border-radius: 14px;
            }}
            PhotoCard:hover {{
                background: {CARD_HOV};
                border-color: {ACCENT_LT};
            }}
        """)

    def mousePressEvent(self, event: object) -> None:
        self.chk.setChecked(not self.chk.isChecked())

    def is_checked(self) -> bool:
        return self.chk.isChecked()

    def set_checked(self, value: bool) -> None:
        self.chk.setChecked(value)


class StatisticsDialog(QMessageBox):
    """Dialog displaying analysis statistics."""

    def __init__(self, stats: Statistics, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(get_text("title_stats"))
        self.setIcon(QMessageBox.Icon.Information)

        text = get_text("stats_html").format(
            total_photos=stats.total_photos,
            total_groups=stats.total_groups,
            avg_sim=stats.avg_similarity,
            total_size=stats.total_size_mb,
            dup_size=stats.duplicate_size_mb,
            recov_size=stats.recoverable_mb,
        )
        for ext, data in sorted(stats.by_format.items(), key=lambda item: item[1]["size_mb"], reverse=True):
            text += f"\n- {ext.upper()}: {data['count']} photos ({data['size_mb']:.2f} MB)"

        self.setText(text)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)


class GroupWidget(QFrame):
    """Widget representing a duplicate group and its available actions."""

    action_taken = pyqtSignal()

    def __init__(self, group: DuplicateGroup, group_number: int, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.group = group
        self.group_number = group_number
        self.cards: list[PhotoCard] = []
        self._resolved = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setStyleSheet(f"""
            GroupWidget {{
                background: {PANEL_BG};
                border: 1px solid {BORDER_LT};
                border-radius: 16px;
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
        title.setStyleSheet(f"color: {TEXT_PRI}; font-size: 15px; font-weight: 900;")
        header_vbox.addWidget(title)

        n = len(self.group.photos)
        sim_pct = f"{self.group.similarity:.0f}%"
        match_type = getattr(self.group, "match_type", "similar (hash)")

        subtitle_layout = QHBoxLayout()
        subtitle = QLabel(get_text("lbl_group_sub").format(n=n, sim=sim_pct))
        subtitle.setStyleSheet(muted_label(12))
        subtitle_layout.addWidget(subtitle)

        match_color, match_bg = self._match_badge_colors(match_type)
        match_badge = QLabel(match_type.upper())
        match_badge.setStyleSheet(badge_style(match_color, match_bg))
        subtitle_layout.addWidget(match_badge)
        subtitle_layout.addStretch()

        header_vbox.addLayout(subtitle_layout)
        header.addLayout(header_vbox)
        header.addStretch()

        self.status_badge = QLabel(get_text("badge_pending"))
        self.status_badge.setStyleSheet(badge_style(WARNING, WARNING_BG))
        header.addWidget(self.status_badge)
        main.addLayout(header)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER};")
        main.addWidget(sep)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)
        for index, photo in enumerate(self.group.photos):
            card = PhotoCard(photo, is_best=(index == self.group.best_index))
            card.selected.connect(self._on_selection_changed)
            self.cards.append(card)
            cards_layout.addWidget(card)
        cards_layout.addStretch()

        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(388)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container.setLayout(cards_layout)
        container.setStyleSheet("background: transparent;")
        scroll.setWidget(container)
        main.addWidget(scroll)

        action_row = QHBoxLayout()
        action_row.addWidget(QLabel(get_text("lbl_action")))
        self.action_combo = QComboBox()
        self.action_combo.addItems([get_text("opt_move"), get_text("opt_delete")])
        action_row.addWidget(self.action_combo)
        action_row.addStretch()
        main.addLayout(action_row)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.lbl_selection = QLabel(get_text("lbl_select_keep"))
        self.lbl_selection.setStyleSheet(muted_label(11))
        btn_row.addWidget(self.lbl_selection)
        btn_row.addStretch()

        buttons = [
            (get_text("btn_use_rec"), "success", self._select_best_only),
            (get_text("btn_all"), "ghost", self._select_all),
            (get_text("btn_none"), "ghost", self._select_none),
        ]
        for text, kind, callback in buttons:
            button = QPushButton(text)
            button.setStyleSheet(button_style(kind, compact=True))
            button.clicked.connect(callback)
            btn_row.addWidget(button)

        self.btn_apply = QPushButton(get_text("btn_apply_action"))
        self.btn_apply.setStyleSheet(button_style("primary", compact=True))
        self.btn_apply.clicked.connect(self._apply_action)
        btn_row.addWidget(self.btn_apply)

        btn_export = QPushButton(get_text("btn_export_csv"))
        btn_export.setStyleSheet(button_style("secondary", compact=True))
        btn_export.clicked.connect(self._export_csv)
        btn_row.addWidget(btn_export)
        main.addLayout(btn_row)

    def _match_badge_colors(self, match_type: str) -> tuple[str, str]:
        if "IA" in match_type:
            return ACCENT2, WARNING_BG
        if "exact" in match_type or "exacta" in match_type:
            return SUCCESS, SUCCESS_BG
        return INFO, INFO_BG

    def _on_selection_changed(self) -> None:
        selected = sum(1 for card in self.cards if card.is_checked())
        total = len(self.cards)
        self.lbl_selection.setText(get_text("lbl_selection").format(sel=selected, tot=total))

    def _select_best_only(self) -> None:
        for index, card in enumerate(self.cards):
            card.set_checked(index == self.group.best_index)

    def _select_all(self) -> None:
        for card in self.cards:
            card.set_checked(True)

    def _select_none(self) -> None:
        for card in self.cards:
            card.set_checked(False)

    def _apply_action(self) -> None:
        to_keep = [card.photo for card in self.cards if card.is_checked()]
        to_process = [card.photo for card in self.cards if not card.is_checked()]

        if not to_keep:
            QMessageBox.warning(self, get_text("title_no_sel"), get_text("msg_no_keep"))
            return

        if not to_process:
            QMessageBox.information(self, get_text("title_no_changes"), get_text("msg_no_move"))
            self._mark_resolved(get_text("status_no_changes"), TEXT_SEC)
            return

        if self.action_combo.currentIndex() == 1:
            self._delete_photos(to_keep, to_process)
        else:
            self._move_photos(to_keep, to_process)

    def _delete_photos(self, to_keep: list[PhotoInfo], to_delete: list[PhotoInfo]) -> None:
        files = "\n".join(f"  - {photo.filename}" for photo in to_delete)
        msg = get_text("msg_del").format(move=len(to_delete), files=files, keep=len(to_keep))
        reply = QMessageBox.question(
            self,
            get_text("title_del"),
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        errors = []
        for photo in to_delete:
            try:
                try:
                    import send2trash
                    send2trash.send2trash(photo.path)
                except ImportError:
                    os.remove(photo.path)
                log_history("delete", {"file": photo.path, "group": self.group_number})
            except Exception as error:
                errors.append(file_error_message(get_text("err_action_delete"), photo.filename, error))

        self._finish_action(to_delete, errors, get_text("title_del_err"), get_text("msg_del_err"), get_text("status_deleted"), "delete")

    def _move_photos(self, to_keep: list[PhotoInfo], to_move: list[PhotoInfo]) -> None:
        dest_folder = QFileDialog.getExistingDirectory(self.window(), get_text("dlg_select_dest"))
        if not dest_folder:
            return

        files = "\n".join(f"  - {photo.filename}" for photo in to_move)
        msg = get_text("msg_move").format(move=len(to_move), dest=dest_folder, files=files, keep=len(to_keep))
        reply = QMessageBox.question(
            self,
            get_text("title_move"),
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        errors = []
        moved_paths = []
        for photo in to_move:
            try:
                src = Path(photo.path).resolve()
                if not src.exists():
                    errors.append(get_text("err_file_not_found").format(file=photo.filename))
                    continue

                dest_dir = Path(dest_folder) / "duplicados"
                dest_dir.mkdir(parents=True, exist_ok=True)

                dest = dest_dir / src.name
                counter = 1
                while dest.exists():
                    dest = dest_dir / f"{src.stem}_dup{counter}{src.suffix}"
                    counter += 1

                shutil.move(str(src), str(dest))
                moved_paths.append(str(dest))
            except Exception as error:
                errors.append(file_error_message(get_text("err_action_move"), photo.filename, error))

        if moved_paths:
            log_history(
                "move",
                {
                    "files": moved_paths,
                    "destination": str(dest_folder),
                    "group": self.group_number,
                    "count": len(moved_paths),
                },
            )

        self._finish_action(to_move, errors, get_text("title_move_err"), get_text("msg_move_err"), get_text("status_moved"), "move")

    def _finish_action(
        self,
        processed: list[PhotoInfo],
        errors: list[str],
        error_title: str,
        error_template: str,
        status_template: str,
        action: str,
    ) -> None:
        ok = len(processed) - len(errors)
        if errors:
            detail = "\n".join(errors)
            QMessageBox.warning(self, error_title, error_template.format(ok=ok, tot=len(processed), detail=detail))
        if ok <= 0:
            self._mark_resolved(get_text("status_error"), DANGER)
            return

        self._mark_resolved(status_template.format(ok=ok), SUCCESS)
        self.action_taken.emit()
        for card in self.cards:
            if not card.is_checked():
                card.hide()
        self.lbl_selection.setText(get_text("lbl_kept"))

    def _mark_resolved(self, text: str, color: str) -> None:
        self._resolved = True
        self.status_badge.setText(text)
        bg = SUCCESS_BG if color == SUCCESS else WARNING_BG if color == WARNING else DANGER_BG
        self.status_badge.setStyleSheet(badge_style(color, bg))
        self.btn_apply.setEnabled(False)
        self.btn_apply.setText(get_text("btn_resolved"))
        self.btn_apply.setStyleSheet(button_style("ghost", compact=True))

    def _export_csv(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(self, get_text("dlg_save_csv"), "", "CSV Files (*.csv)")
        if not file_path:
            return
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    "Group",
                    "File",
                    "Size (MB)",
                    "Resolution",
                    "Sharpness",
                    "EXIF Date",
                    "Location",
                    "Title",
                    "Description",
                    "Quality",
                ])
                for photo in self.group.photos:
                    loc = ""
                    if getattr(photo, "geo_data", None):
                        loc = f"{photo.geo_data.get('latitude', 0)}, {photo.geo_data.get('longitude', 0)}"
                    writer.writerow([
                        self.group_number,
                        photo.path,
                        f"{photo.size_mb:.2f}",
                        f"{photo.width}x{photo.height}",
                        f"{photo.sharpness:.0f}",
                        photo.exif_date or "N/A",
                        loc,
                        getattr(photo, "title", "") or "",
                        getattr(photo, "description", "") or "",
                        f"{photo.score:.1f}",
                    ])
            QMessageBox.information(self, get_text("title_exported"), get_text("msg_exported").format(file=file_path))
        except Exception as error:
            QMessageBox.warning(
                self,
                get_text("title_export_err"),
                get_text("msg_export_err").format(err=file_error_message(get_text("err_action_export"), file_path, error)),
            )
