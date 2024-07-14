from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maya_pipeline as mp

# Python
from pathlib import Path

# PySide2
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QWidget, QDialog

# Maya
import pymel.core as pm

from maya_pipeline.mp_logging import logging
from maya_pipeline.misc import pyside_utilities
from maya_pipeline.settings import settings_view_ui
__all__ = ["SettingsView"]


class SettingsView(QDialog):
    def __init__(self, title: str, model: mp.SettingsModel, parent=None):
        super().__init__(parent)
        self._model = model
        self.ui = settings_view_ui.Ui_SettingsDialog()
        self.title = title
        self.setup_ui()

        # init settings
        self.ui.unity_line_edit.setText(str(self._model.unity_project_asset_path))

    def setup_ui(self):
        self.ui.setupUi(self)
        #self.ui.setWindowTitle(self.title)
        parent_widget: QWidget = self.ui.settingsDialogHorizontalLayout.parentWidget()
        qobjects = parent_widget.findChildren(QObject)

        # Query Maya's current DPI scaling mode.
        if pm.mayaDpiSetting(query=True, mode=True) == 1:  # 1 == Custom scaling
            # Query the current scale value and use it to scale the UI widgets
            scale_value: int = pm.mayaDpiSetting(query=True, scaleValue=True)
            pyside_utilities.scale_qobjects(qobjects, scale_value)

    def show_settings(self):
        logging.debug_log("Showing settings dialog")
        self.exec_()  # show dialog

    def update_unity_project(self, path: Path):
        self.ui.unity_line_edit.setText(str(path))
