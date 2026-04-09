import os
from pathlib import Path

def process_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

screens_replacements = [
    ('from core.state import load_config, save_config', 'from core.state import load_config, save_config\nfrom core.i18n import get_text'),
    ('title = QLabel("PhotoDedup")', 'title = QLabel(get_text("app_title"))'),
    ('subtitle = QLabel("Intelligently find and manage duplicate photos")', 'subtitle = QLabel(get_text("app_subtitle"))'),
    ('folder_group = QGroupBox("Folder to analyze")', 'folder_group = QGroupBox(get_text("grp_folder"))'),
    ('self.folder_label = QLabel("No folder selected")', 'self.folder_label = QLabel(get_text("lbl_no_folder"))'),
    ('btn_browse = QPushButton("  Browse")', 'btn_browse = QPushButton(get_text("btn_browse"))'),
    ('mode_group = QGroupBox("Search Type")', 'mode_group = QGroupBox(get_text("grp_search_type"))'),
    ('mode_layout.addWidget(QLabel("Detect:"))', 'mode_layout.addWidget(QLabel(get_text("lbl_detect")))'),
    ('self.mode_combo.addItems(["Similar photos", "Exact photos"])', 'self.mode_combo.addItems([get_text("opt_similar"), get_text("opt_exact")])'),
    ('sens_group = QGroupBox("Detection Sensitivity")', 'sens_group = QGroupBox(get_text("grp_sensitivity"))'),
    ('sens_desc = QLabel(\n            "Similarity threshold: lower values = stricter (only nearly identical photos)\\n"\n            "Higher values = more permissive (detects similar photos even if not exact)"\n        )', 'sens_desc = QLabel(get_text("desc_sensitivity"))'),
    ('lbl_strict = QLabel("Strict")', 'lbl_strict = QLabel(get_text("lbl_strict"))'),
    ('lbl_permissive = QLabel("Permissive")', 'lbl_permissive = QLabel(get_text("lbl_permissive"))'),
    ('ai_group = QGroupBox("Detección avanzada optimizada")', 'ai_group = QGroupBox(get_text("grp_ai"))'),
    ('self.chk_use_ai = QCheckBox("Activar IA (Mayor precisión en casos dudosos)")', 'self.chk_use_ai = QCheckBox(get_text("chk_use_ai"))'),
    ('ai_level_layout.addWidget(QLabel("Nivel de análisis:"))', 'ai_level_layout.addWidget(QLabel(get_text("lbl_ai_level")))'),
    ('self.ai_level_combo.addItems(["Rápido (Sin IA)", "Equilibrado (IA selectiva)", "Profundo (IA estricta)"])', 'self.ai_level_combo.addItems([get_text("opt_ai_fast"), get_text("opt_ai_balanced"), get_text("opt_ai_deep")])'),
    ('self.btn_start = QPushButton("   Start Analysis")', 'self.btn_start = QPushButton(get_text("btn_start"))'),
    ('fmt_title = QLabel("Supported formats")', 'fmt_title = QLabel(get_text("lbl_formats"))'),
    ('folder = QFileDialog.getExistingDirectory(self, "Select photo folder")', 'folder = QFileDialog.getExistingDirectory(self, get_text("dlg_select_folder"))'),
    
    ('self.title = QLabel("Analyzing photos...")', 'self.title = QLabel(get_text("title_analyzing"))'),
    ('self.status = QLabel("Starting...")', 'self.status = QLabel(get_text("lbl_starting"))'),
    ('self.btn_pause = QPushButton("  Pause")', 'self.btn_pause = QPushButton(get_text("btn_pause"))'),
    ('self.btn_pause.setText("  Pause")', 'self.btn_pause.setText(get_text("btn_pause"))'),
    ('self.btn_pause.setText("  Resume")', 'self.btn_pause.setText(get_text("btn_resume"))'),
    
    ('btn_back = QPushButton("  New Search")', 'btn_back = QPushButton(get_text("btn_new_search"))'),
    ('self.btn_apply_all = QPushButton("  Apply Recommended to All")', 'self.btn_apply_all = QPushButton(get_text("btn_apply_all"))'),
    ('btn_stats = QPushButton("  📊 Statistics")', 'btn_stats = QPushButton(get_text("btn_stats"))'),
    ('no_dup = QLabel("🎉  No duplicates were found in your collection.")', 'no_dup = QLabel(get_text("msg_no_dups"))'),
    ('self.summary_label.setText(\n            f"{len(groups)} duplicate groups  •  {total_photos} involved photos"\n        )', 'self.summary_label.setText(get_text("lbl_summary_groups").format(tot_groups=len(groups), tot_photos=total_photos))'),
    ('QMessageBox.information(self, "No Pending Action",\n                "All groups are already resolved.")', 'QMessageBox.information(self, get_text("title_no_pending"), get_text("msg_all_resolved"))'),
    ('dest_folder = QFileDialog.getExistingDirectory(self, "Select folder to create \'duplicates\'")', 'dest_folder = QFileDialog.getExistingDirectory(self, get_text("dlg_select_dest"))'),
    ('msg = (\n            f"Will process {len(pending)} pending group(s).\\n"\n            f"Will move ~{total_move} duplicate photo(s) to the \'duplicates\' folder inside:\\n{dest_folder}\\n"\n            f"keeping the recommended photo (highest quality) for each group.\\n\\n"\n            f"Continue?"\n        )', 'msg = get_text("msg_apply_all").format(pending=len(pending), to_move=total_move, dest=dest_folder)'),
    ('QMessageBox.question(\n            self, "Apply Recommended to All", msg', 'QMessageBox.question(\n            self, get_text("title_apply_all"), msg'),
    ('w._mark_resolved("NO CHANGES", TEXT_SEC)', 'w._mark_resolved(get_text("status_no_changes"), TEXT_SEC)'),
    ('w._mark_resolved(f"  Resolved ({moved_ok} moved)", SUCCESS)', 'w._mark_resolved(get_text("status_resolved").format(moved=moved_ok), SUCCESS)'),
    ('w._mark_resolved("  Error moving", DANGER)', 'w._mark_resolved(get_text("status_error"), DANGER)'),
    ('w.lbl_selection.setText("Photos kept in this group")', 'w.lbl_selection.setText(get_text("lbl_kept"))'),
    ('QMessageBox.warning(self, "Some errors occurred",\n                f"Completed {resolved_count} groups with errors in some files:\\n\\n{detail}")', 'QMessageBox.warning(self, get_text("title_errors"), get_text("msg_errors").format(resolved=resolved_count, detail=detail))'),
    ('QMessageBox.information(self, "Completed",\n                f"Successfully processed {resolved_count} group(s).")', 'QMessageBox.information(self, get_text("title_completed"), get_text("msg_completed").format(resolved=resolved_count))'),
    ('self.resolved_label.setText(f"✓ {self._resolved}/{total} resolved")', 'self.resolved_label.setText(get_text("lbl_resolved_groups").format(res=self._resolved, tot=total))')
]

widgets_replacements = [
    ('from core.state import log_history', 'from core.state import log_history\nfrom core.i18n import get_text'),
    ('badge = QLabel("  Recommended")', 'badge = QLabel(get_text("badge_rec"))'),
    ('score_lbl = QLabel(f"Quality: {score_pct}/100")', 'score_lbl = QLabel(get_text("lbl_quality").format(pct=score_pct))'),
    ('f"🔍 Sharpness: {self.photo.sharpness:.0f}{location_str}"', 'get_text("lbl_sharpness").format(shp=f"{self.photo.sharpness:.0f}") + location_str'),
    ('self.setWindowTitle("Analysis Statistics")', 'self.setWindowTitle(get_text("title_stats"))'),
    ('text = f"""\n        <b>ANALYSIS STATISTICS</b>\n        \n        <b>Analyzed photos:</b> {stats.total_photos}\n        <b>Duplicate groups:</b> {stats.total_groups}\n        <b>Average similarity:</b> {stats.avg_similarity:.1f}%\n        \n        <b>Storage usage:</b>\n        • Total: {stats.total_size_mb:.2f} MB\n        • Duplicates: {stats.duplicate_size_mb:.2f} MB\n        • <span style="color: green;"><b>Recoverable: {stats.recoverable_mb:.2f} MB</b></span>\n        \n        <b>Format distribution:</b>\n        """', 'text = get_text("stats_html").format(\n            total_photos=stats.total_photos,\n            total_groups=stats.total_groups,\n            avg_sim=stats.avg_similarity,\n            total_size=stats.total_size_mb,\n            dup_size=stats.duplicate_size_mb,\n            recov_size=stats.recoverable_mb\n        )'),
    ('title = QLabel(f"Group #{self.group_number}")', 'title = QLabel(get_text("lbl_group").format(num=self.group_number))'),
    ('subtitle = QLabel(f"{n} similar photos  •  similarity {sim_pct}")', 'subtitle = QLabel(get_text("lbl_group_sub").format(n=n, sim=sim_pct))'),
    ('self.status_badge = QLabel("  Pending")', 'self.status_badge = QLabel(get_text("badge_pending"))'),
    ('self.lbl_selection = QLabel("Select photos to KEEP")', 'self.lbl_selection = QLabel(get_text("lbl_select_keep"))'),
    ('action_row.addWidget(QLabel("Action:"))', 'action_row.addWidget(QLabel(get_text("lbl_action")))'),
    ('self.action_combo.addItems(["Move to duplicates", "Delete permanently"])', 'self.action_combo.addItems([get_text("opt_move"), get_text("opt_delete")])'),
    ('btn_best = QPushButton("  Use Recommended")', 'btn_best = QPushButton(get_text("btn_use_rec"))'),
    ('btn_all = QPushButton("  All")', 'btn_all = QPushButton(get_text("btn_all"))'),
    ('btn_none = QPushButton("  None")', 'btn_none = QPushButton(get_text("btn_none"))'),
    ('self.btn_apply = QPushButton("  Apply Action")', 'self.btn_apply = QPushButton(get_text("btn_apply_action"))'),
    ('btn_export = QPushButton("  Export CSV")', 'btn_export = QPushButton(get_text("btn_export_csv"))'),
    ('self.lbl_selection.setText(f"{selected}/{total} photos selected to KEEP")', 'self.lbl_selection.setText(get_text("lbl_selection").format(sel=selected, tot=total))'),
    ('QMessageBox.warning(self, "No selection",\n                "You must select at least one photo to keep.")', 'QMessageBox.warning(self, get_text("title_no_sel"), get_text("msg_no_keep"))'),
    ('QMessageBox.information(self, "No changes",\n                "There are no photos marked to move. All will be kept.")', 'QMessageBox.information(self, get_text("title_no_changes"), get_text("msg_no_move"))'),
    ('self._mark_resolved("NO CHANGES", TEXT_SEC)', 'self._mark_resolved(get_text("status_no_changes"), TEXT_SEC)'),
    ('msg = f"Will permanently delete {len(to_move)} photo(s):\\n\\n"\n            msg += "\\n".join(f"  • {p.filename}" for p in to_move)\n            msg += f"\\n\\nWill keep {len(to_keep)} photo(s).\\n\\nAre you sure? This action cannot be undone."', 'msg = get_text("msg_del").format(move=len(to_move), files="\\n".join(f"  • {p.filename}" for p in to_move), keep=len(to_keep))'),
    ('reply = QMessageBox.question(self, "Confirm Deletion", msg', 'reply = QMessageBox.question(self, get_text("title_del"), msg'),
    ('QMessageBox.warning(self, "Deletion Errors", f"Deleted {moved_ok} out of {len(to_move)}.\\n\\nErrors:\\n{detail}")', 'QMessageBox.warning(self, get_text("title_del_err"), get_text("msg_del_err").format(ok=moved_ok, tot=len(to_move), detail=detail))'),
    ('self._mark_resolved(f"✓ DELETED ({moved_ok})", SUCCESS)', 'self._mark_resolved(get_text("status_deleted").format(ok=moved_ok), SUCCESS)'),
    ('self.lbl_selection.setText("Photos kept in this group")', 'self.lbl_selection.setText(get_text("lbl_kept"))'),
    ('dest_folder = QFileDialog.getExistingDirectory(self.window(), "Select folder to create \'duplicates\'")', 'dest_folder = QFileDialog.getExistingDirectory(self.window(), get_text("dlg_select_dest"))'),
    ('msg = f"Will move {len(to_move)} photo(s) to the \'duplicates\' folder inside:\\n{dest_folder}\\n\\n"\n            msg += "\\n".join(f"  • {p.filename}" for p in to_move)\n            msg += f"\\n\\nWill keep {len(to_keep)} photo(s)."', 'msg = get_text("msg_move").format(move=len(to_move), dest=dest_folder, files="\\n".join(f"  • {p.filename}" for p in to_move), keep=len(to_keep))'),
    ('reply = QMessageBox.question(self, "Confirm Move", msg', 'reply = QMessageBox.question(self, get_text("title_move"), msg'),
    ('QMessageBox.warning(self, "Move Errors", f"Moved {moved_ok} out of {len(to_move)}.\\n\\nErrors:\\n{detail}")', 'QMessageBox.warning(self, get_text("title_move_err"), get_text("msg_move_err").format(ok=moved_ok, tot=len(to_move), detail=detail))'),
    ('self._mark_resolved(f"✓ MOVED ({moved_ok})", SUCCESS)', 'self._mark_resolved(get_text("status_moved").format(ok=moved_ok), SUCCESS)'),
    ('self.btn_apply.setText("  Resolved")', 'self.btn_apply.setText(get_text("btn_resolved"))'),
    ('file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")', 'file_path, _ = QFileDialog.getSaveFileName(self, get_text("dlg_save_csv"), "", "CSV Files (*.csv)")'),
    ('QMessageBox.information(self, "Exported", f"Groups exported to {file_path}")', 'QMessageBox.information(self, get_text("title_exported"), get_text("msg_exported").format(file=file_path))'),
    ('QMessageBox.warning(self, "Error", f"Failed to export: {e}")', 'QMessageBox.warning(self, get_text("title_export_err"), get_text("msg_export_err").format(err=e))')
]

main_replacements = [
    ('from core.state import CACHE_FILE\nfrom ui.theme import *', 'from core.state import CACHE_FILE\nfrom core.i18n import get_text\nfrom ui.theme import *'),
    ('self.setWindowTitle("PhotoDedup")', 'self.setWindowTitle(get_text("app_title"))'),
    ('QMessageBox.critical(self, "Analysis Error", msg)', 'QMessageBox.critical(self, get_text("title_error"), msg)'),
    ('reply = QMessageBox.question(\n                self,\n                "Clear Cache",\n                "Do you want to clear the analysis cache before exiting?\\n\\nIf you keep it, future analysis of the same photos will be much faster. If you delete it, you\'ll free up disk space.",', 'reply = QMessageBox.question(\n                self,\n                get_text("title_clear_cache"),\n                get_text("msg_clear_cache"),')
]

process_file('ui/screens.py', screens_replacements)
process_file('ui/widgets.py', widgets_replacements)
process_file('ui/main_window.py', main_replacements)
