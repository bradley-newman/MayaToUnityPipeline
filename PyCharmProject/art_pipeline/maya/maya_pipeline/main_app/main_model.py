#Python
from enum import Enum
from pathlib import Path

#PySide2
from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import *

#Maya
import pymel.core as pm

class AssetType(Enum):
    ANIMATION = "Animation"
    MESH = "Mesh"
    SKELETON = "Skeleton"
    SKINNED_MESH = "SkinnedMesh"
    RIG = "Rig"

class AssetTypeSuffix(Enum):
    MESH = "_MSH"
    SKELETON = "_SKL"
    SKINNED_MESH = "_SKM"
    RIG = "_RIG"

ASSET_EXT = ".ma"
ASSET_EXT_TYPE = "mayaAscii"
ASSET_NODE_NAME = "Asset"
ASSET_TYPE_ATTR_NAME = "asset_type"
STATIC_ATTR_NAME = "static"
LOOP_ATTR_NAME = "loop"

class MainModel(QObject):
    def __init__(self):
        super().__init__()
        self._current_asset_path: Path
        self._current_asset_node: pm.PyNode
        self._current_asset_type:AssetType
        self._new_asset_parent_folder_name:str
        self._new_asset_path: Path
        self._new_asset_type:AssetType
        self._new_asset_name: str
        self._rig_ref_path: Path

    #region Current Asset
    @property
    def current_asset_path(self) -> Path:
        return self._current_asset_path

    @current_asset_path.setter
    def current_asset_path(self, path: Path):
        self._current_asset_path = path

    @property
    def current_asset_node(self) -> pm.PyNode:
        return self._current_asset_node

    @current_asset_node.setter
    def current_asset_node(self, node:pm.PyNode):
        self._current_asset_node = node

    @property
    def current_asset_type(self) -> AssetType:
        return self._current_asset_type

    @current_asset_type.setter
    def current_asset_type(self, type:AssetType):
        self._current_asset_type = type
    #endregion

    #region New Asset
    new_asset_parent_folder_changed = Signal(str)

    @property
    def new_asset_parent_folder(self) -> str:
        return self._new_asset_parent_folder_name

    @new_asset_parent_folder.setter
    def new_asset_parent_folder(self, folder:str):
        self._new_asset_parent_folder_name = folder
        self.new_asset_parent_folder_changed.emit(folder)

    @property
    def new_asset_path(self) -> Path:
        return self._new_asset_path

    @new_asset_path.setter
    def new_asset_path(self, path: Path):
        self._new_asset_path = path
        
    @property
    def new_asset_type(self) -> AssetType:
        return self._new_asset_type

    @new_asset_type.setter
    def new_asset_type(self, type:AssetType):
        self._new_asset_type = type

    @property
    def new_asset_name(self) -> str:
        return self._new_asset_name

    @new_asset_name.setter
    def new_asset_name(self, value:str):
        self._new_asset_name = value

    @property
    def import_asset_path(self) -> Path:
        return self._new_asset_import_path

    @import_asset_path.setter
    def import_asset_path(self, path: Path):
        self._new_asset_import_path = path

    @property
    def current_rig_ref_path(self) -> Path:
        return self._rig_ref_path

    @current_rig_ref_path.setter
    def current_rig_ref_path(self, path: Path):
        self._rig_ref_path = path
        
    #endregion

