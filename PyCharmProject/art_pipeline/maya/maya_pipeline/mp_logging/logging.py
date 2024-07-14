from enum import Enum
from datetime import datetime
import os
from pathlib import Path
import inspect

import pymel.core as pm

__all__ = ["FORCE_PRINT_TO_SCRIPT_EDITOR", "LogMode", "MAX_FILE_COUNT",
           "WRITE_IMMEDIATELY", "create_log", "debug_error", "debug_log",
           "debug_warning", "prune_logs", "logging_script_directory"]

logging_script_directory = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
log_dir: Path = logging_script_directory / "logs"
log_filepath: Path = None
MAX_FILE_COUNT = 15
FORCE_PRINT_TO_SCRIPT_EDITOR = False
WRITE_IMMEDIATELY = True


class LogMode(Enum):
    DEFAULT = 1
    WARNING = 2
    ERROR = 3


def create_log():
    log_filename = "log_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    global log_filepath

    if not log_dir.exists():
        Path.mkdir(log_dir)

    log_filepath = log_dir / log_filename

    with open(log_filepath, "w"):
        print(f"Created log at: {log_filepath}")

    prune_logs()


def prune_logs():
    try:
        global log_dir
        log_files = [f for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]

        if len(log_files) > MAX_FILE_COUNT:
            for file in log_files:
                filepath = os.path.join(log_dir, file)
                debug_log(f"Deleting old log file: {filepath}")
                os.remove(filepath)
                break
    except Exception as e:
        debug_log(f"Exception while trying to prune log: {e}")


def debug_log(message: str, print_to_script_editor: bool=False):
    """
    :param message: Message to log
    :param print_to_script_editor: Whether to print the log to the Maya Script Editor
    :return:
    """
    _write_to_log(message, mode=LogMode.DEFAULT, print_to_script_editor=print_to_script_editor)


def debug_warning(message: str, print_to_script_editor: bool=False):
    """
    :param message: Message to log
    :param print_to_script_editor: Whether to print the log to the Maya Script Editor
    :return:
    """
    _write_to_log(message, mode=LogMode.WARNING, print_to_script_editor=print_to_script_editor)


def debug_error(message: str, print_to_script_editor: bool=False):
    """
    :param message: Message to log
    :param print_to_script_editor: Whether to print the log to the Maya Script Editor
    :return:
    """
    _write_to_log(message, mode=LogMode.ERROR, print_to_script_editor=print_to_script_editor)


def _write_to_log(message: str, mode: LogMode, print_to_script_editor: bool):
    global log_filepath

    if log_filepath is None or not log_filepath.is_file():
        pm.error(f"Can't open log file because it doesn't exist at: {log_filepath}")
        return
    with open(log_filepath, "a") as log_file:
        if print_to_script_editor or FORCE_PRINT_TO_SCRIPT_EDITOR:
            if mode == LogMode.DEFAULT:
                print(message)
            elif mode == LogMode.WARNING:
                pm.warning(message)
            elif mode == LogMode.ERROR:
                pm.error(message)

        if mode == LogMode.DEFAULT:
            log_file.write(f"{message}\n")
        elif mode == LogMode.WARNING:
            log_file.write(f"WARNING: {message}\n")
        elif mode == LogMode.ERROR:
            log_file.write(f"ERROR: {message}\n")

        if WRITE_IMMEDIATELY:
            log_file.flush()
            # os.fsync(log_file.fileno())
