from enum import Enum

__all__ = ["UI_Creation_Mode"]


class UI_Creation_Mode(Enum):
    DEFAULT = 1
    RESTORE_FROM_MAYA_PREFS = 2
    RECREATE = 3