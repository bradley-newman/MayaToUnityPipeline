from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import maya_pipeline as mp

# Python
from pathlib import Path

# PySide2
from PySide2.QtCore import QObject
from PySide2.QtWidgets import *

class SettingsController(QObject):
    def __init__(self, model: mp.SettingsModel):
        super().__init__()
        self._model = model

    def browse_files(self, q_dialog:QDialog):
        import maya_pipeline as mp
        mp.debug_log(f"Launched Browse Files Dialog")
        file_dialog = QFileDialog()
        path = file_dialog.getExistingDirectory(q_dialog, "Select Folder")
        path = Path(path)

        if path:
            mp.debug_log(f"Selected path: {path}")
            self.set_unity_project_export_path(path)
        else:
            mp.debug_log(f"Cancelled Browse Files Dialog.")

    def set_unity_project_export_path(self, path: Path):
        self._model.settings_ui_unity_project_asset_path = path

    def save_settings(self):
        import maya_pipeline as mp
        mp.debug_log("Saving settings...")
        self._model.save_settings()

    def cancel_settings(self):
        import maya_pipeline as mp
        mp.debug_log("Cancelled settings.")
