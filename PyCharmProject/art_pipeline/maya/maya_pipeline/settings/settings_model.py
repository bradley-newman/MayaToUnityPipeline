# Python
from pathlib import Path
import os
import inspect
from enum import Enum
import json

# PySide2
from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QDialog, QFileDialog

from maya_pipeline.mp_logging import logging

__all__ = ["settings_script_directory", "settings_dir", "SETTINGS_FILENAME", "settings_filepath", "SettingsKeys",
           "settings_defaults", "SettingsModel", "unity_project_asset_path", "create_settings_file",
           "load_settings_file", "save_settings_to_file", "read_setting"]

settings_script_directory: Path = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
settings_dir: Path = settings_script_directory
SETTINGS_FILENAME = "Settings.json"
settings_filepath: Path = settings_dir / SETTINGS_FILENAME


class SettingsKeys(Enum):
    UNITY_EXPORT_PATH = "UnityExportPath"


settings_defaults = {
    SettingsKeys.UNITY_EXPORT_PATH.value: "",
}


class SettingsModel(QObject):
    def __init__(self):
        print("Init Settings Model....")
        super().__init__()

        if not settings_filepath.is_file():
            create_settings_file()

        self.settings_temp: dict[str,str] = load_settings_file() # type: ignore
        logging.debug_log(f"SettingsModel > self.settings_temp: {self.settings_temp}")

    @property
    def unity_project_asset_path(self) -> Path:
        return Path(self.settings_temp[SettingsKeys.UNITY_EXPORT_PATH.value])

    unity_project_asset_path_changed = Signal(Path)

    @unity_project_asset_path.setter
    def unity_project_asset_path(self, path: Path):
        self.settings_temp[SettingsKeys.UNITY_EXPORT_PATH.value] = str(path)
        self.unity_project_asset_path_changed.emit(path)

    def save_settings(self):
        logging.debug_log(f"Saving self.settings_temp: {self.settings_temp}")
        save_settings_to_file(self.settings_temp)

    def browse_files(self, q_dialog: QDialog):
        logging.debug_log("Launched Browse Files Dialog")
        file_dialog = QFileDialog()
        path: Path = Path(file_dialog.getExistingDirectory(q_dialog, "Select Folder"))
        
        if not path.exists() or path == Path("."):
            logging.debug_log("Cancelled Browse Files Dialog.")
            return
        else:
            logging.debug_log(f"Selected path: {path}")
            self.set_unity_project_export_path(path)
            
    def set_unity_project_export_path(self, path: Path):
        self.unity_project_asset_path = path


# Functions

def unity_project_asset_path() -> Path:
    path_str = read_setting(SettingsKeys.UNITY_EXPORT_PATH)
    return Path(path_str)


def create_settings_file():
    with open(settings_filepath, "w", encoding="utf-8") as file:
        json.dump(settings_defaults, file, indent=4, sort_keys=True)
        logging.debug_log(f"Created default {SETTINGS_FILENAME} at: {settings_filepath}")
        logging.debug_log(f"With these default settings: {settings_defaults}")


def load_settings_file() -> dict[str,str]:
    if not settings_filepath.is_file():
        logging.debug_error(f"Can't open {SETTINGS_FILENAME} because it doesn't exist at: {settings_filepath}",
                       print_to_script_editor=True)
        return {"":""}

    with open(settings_filepath, "r", encoding="utf-8") as file:
        json_decoded = json.load(file)
        return json_decoded
        

def save_settings_to_file(settings: dict[str,str]):
    if not settings_filepath.is_file():
        logging.debug_error(f"Can't save {SETTINGS_FILENAME} because it doesn't exist at: {settings_filepath}",
                print_to_script_editor=True)

    with open(settings_filepath, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, sort_keys=True)
        logging.debug_log(f"Saved {SETTINGS_FILENAME} with settings: {settings}")


def read_setting(key: SettingsKeys) -> str:
    settings: dict[str,str] = load_settings_file()
    return settings[key.value]
