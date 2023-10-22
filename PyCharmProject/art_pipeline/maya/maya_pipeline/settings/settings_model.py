# Python
from pathlib import Path
import os
import inspect
from enum import Enum
import json

# PySide2
from PySide2.QtCore import QObject, Signal

class SettingsModel(QObject):
    unity_project_asset_path_changed = Signal(Path)

    def __init__(self):
        super().__init__()
        import maya_pipeline as mp

        if mp.settings_filepath.is_file() is False:
            mp.create_settings_file()

        self.settings_temp = mp.load_settings_file()
        print(f"SettingsModel > self.settings_temp: {self.settings_temp}+++++++++++++++++++++++++")

    @property
    def settings_ui_unity_project_asset_path(self) -> Path:
        import maya_pipeline as mp
        return self.settings_temp[mp.SettingsKeys.UNITY_EXPORT_PATH.value]

    @settings_ui_unity_project_asset_path.setter
    def settings_ui_unity_project_asset_path(self, path: Path):
        import maya_pipeline as mp
        self.settings_temp[mp.SettingsKeys.UNITY_EXPORT_PATH.value] = str(path)
        self.unity_project_asset_path_changed.emit(path)

    def save_settings(self):
        import maya_pipeline as mp
        print(f"Saving self.settings_temp: {self.settings_temp}")
        mp.save_settings_to_file(self.settings_temp)