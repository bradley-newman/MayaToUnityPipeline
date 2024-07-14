from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maya_pipeline as mp

# Python
from pathlib import Path

# PySide2
from PySide2.QtCore import QObject

from maya_pipeline.mp_logging import logging

__all__ = ["SettingsController"]


class SettingsController(QObject):
    def __init__(self, model: mp.SettingsModel, view: mp.SettingsView):
        logging.debug_log("Init SettingsController...")
        super().__init__()
        self._model = model
        self._view = view

        # Listen for View Changes
        logging.debug_log("Listen for View Changes...")
        self._view.ui.unity_browse_button.clicked.connect(self._on_browse_button_clicked)
        self._view.ui.save_cancel_buttons.accepted.connect(self._on_save_settings)

        # Listen for Model Changes
        logging.debug_log("Listen for Model Changes")
        self._model.unity_project_asset_path_changed.connect(self._on_unity_project_asset_path_changed)

    # Update Model with View Changes
    def _on_browse_button_clicked(self):
        logging.debug_log("Browse button clicked...")
        self._model.browse_files(q_dialog=self._view)

    def _on_save_settings(self):
        self._model.save_settings()

    # Update View with Model Changes
    def _on_unity_project_asset_path_changed(self, path: Path):
        self._view.update_unity_project(path)
