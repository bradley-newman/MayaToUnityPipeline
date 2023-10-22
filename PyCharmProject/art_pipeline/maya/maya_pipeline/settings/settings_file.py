# Python
from pathlib import Path
import os
import inspect
from enum import Enum
import json

# PySide2
from PySide2.QtCore import QObject, Signal

script_directory: Path = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
settings_dir: Path = script_directory
SETTINGS_FILENAME = "Settings.json"
settings_filepath: Path = settings_dir / SETTINGS_FILENAME

class SettingsKeys(Enum):
    UNITY_EXPORT_PATH = "UnityExportPath"
    FOO_BAR = "Foo_Bar"

settings_defaults = {
    SettingsKeys.UNITY_EXPORT_PATH.value: "",
    SettingsKeys.FOO_BAR.value: ""
}


def unity_project_asset_path() -> Path:
    import maya_pipeline as mp
    path_str = read_setting(mp.SettingsKeys.UNITY_EXPORT_PATH)
    return Path(path_str)

def create_settings_file():
    import maya_pipeline as mp
    global settings_filepath
    global SETTINGS_FILENAME
    global settings_defaults

    with open(settings_filepath, "w") as file:
        json.dump(settings_defaults, file, indent=4, sort_keys=True)
        mp.debug_log(f"Created default {SETTINGS_FILENAME} at: {settings_filepath}")
        mp.debug_log(f"With these default settings: {settings_defaults}")

def load_settings_file() -> dict:
    import maya_pipeline as mp
    global settings_filepath
    global SETTINGS_FILENAME

    if settings_filepath.is_file():
        with open(settings_filepath, "r") as file:
            json_decoded = json.load(file)
            return json_decoded
    else:
        mp.debug_error(f"Can't open {SETTINGS_FILENAME} because it doesn't exist at: {settings_filepath}", print_to_script_editor=True)
        return None

def save_settings_to_file(settings:dict):
    import maya_pipeline as mp
    global settings_filepath
    global SETTINGS_FILENAME

    if settings_filepath.is_file():
        with open(settings_filepath, "w") as file:
            json.dump(settings, file, indent=4, sort_keys=True)
            mp.debug_log(f"Saved {SETTINGS_FILENAME} with settings: {settings}")
    else:
        mp.debug_error(f"Can't save {SETTINGS_FILENAME} because it doesn't exist at: {settings_filepath}", print_to_script_editor=True)

def read_setting(key: SettingsKeys):
    import maya_pipeline as mp
    global settings_filepath
    global SETTINGS_FILENAME

    settings = load_settings_file()
    return settings[key.value]