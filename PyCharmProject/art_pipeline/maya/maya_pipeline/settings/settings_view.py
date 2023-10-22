from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import maya_pipeline as mp

# Python
from pathlib import Path

# PySide2
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

# Maya
import pymel.core as pm

class SettingsView(QDialog):
    def __init__(self, title:str, model: mp.SettingsModel, controller: mp.SettingsController, parent=None):
        import maya_pipeline as mp
        mp.debug_log(f"SettingsView init to parent={parent}")
        super().__init__(parent)
        self.ui = mp.Ui_SettingsDialog()
        self.ui.setupUi(self)
        parent_widget: QWidget = self.ui.settingsDialogHorizontalLayout.parentWidget()
        qobjects = parent_widget.findChildren(QObject)

        # Query Maya's current DPI scaling mode.
        if pm.mayaDpiSetting(query=True, mode=True) == 1:  # 1 == Custom scaling
            # Query the current scale value and use it to scale the UI widgets
            scale_value: int = pm.mayaDpiSetting(query=True, scaleValue=True)
            mp.scale_qobjects(qobjects, scale_value)

        self._model = model
        self._controller = controller

        # init settings
        self.ui.unity_line_edit.setText(str(self._model.settings_ui_unity_project_asset_path))

        # controller connections
        self.ui.unity_browse_button.clicked.connect(self.on_browse_button_clicked)
        self.ui.save_cancel_buttons.accepted.connect(self.on_save_settings)
        self.ui.save_cancel_buttons.rejected.connect(self.on_cancel_settings)

        # listen for model events
        print(f"connect to signal")
        self._model.unity_project_asset_path_changed.connect(self.on_unity_project_asset_path_changed)

        #self._model.init_settings()
        print(f"Showing settings dialog")
        self.exec_() # show dialog

    # Controller Event Listeners
    def on_browse_button_clicked(self):
        self._controller.browse_files(q_dialog=self)

    def on_save_settings(self):
        self._controller.save_settings()

    def on_cancel_settings(self):
        self._controller.cancel_settings()
        pass

    # Model Event Listeners
    def on_unity_project_asset_path_changed(self, path:Path):
        print(f"on_unity_project_asset_path_changed(path:{path})")
        self.ui.unity_line_edit.setText(str(path))

