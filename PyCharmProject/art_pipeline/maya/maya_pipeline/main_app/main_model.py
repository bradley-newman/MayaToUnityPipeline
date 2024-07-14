# Python
from enum import Enum
from pathlib import Path
import pathlib
from typing import Any

# PySide2
from PySide2.QtCore import QObject, Signal

# Maya
import pymel.core as pm
import maya.mel as mel

import maya_pipeline as mp

__all__ = ["AssetType", "AssetTypeSuffix", "ASSET_EXT", "ASSET_EXT_TYPE", "ASSET_NODE_NAME", "ASSET_TYPE_ATTR_NAME",
           "IMPORTED_NODES_NAMESPACE", "STATIC_ATTR_NAME", "LOOP_ATTR_NAME", "ANIMATIONS_DIR_NAME", "Response",
           "Operation","AssetsToImportOrRef", "MainModel", "get_asset_type_from_node"]


class AssetType(Enum):
    NONE = "None"
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
IMPORTED_NODES_NAMESPACE = "ImportedNodes"
STATIC_ATTR_NAME = "static"
LOOP_ATTR_NAME = "loop"
ANIMATIONS_DIR_NAME = "Animations"


class Response(Enum):
    SAVE = "Save"
    DONT_SAVE = "Don't Save"
    CANCEL = "Cancel"
    CONFIRM = "Confirm"
    YES = "Yes"
    NO = "No"


class Operation(Enum):
    IMPORT = "Import"
    REFERENCE = "Reference"


class AssetsToImportOrRef:
    def __init__(self, operation: Operation, path: pathlib.Path):
        self.operation = operation
        self.path = path


class MainModel(QObject):
    def __init__(self):
        super().__init__()
        self._current_asset_path: Path
        self._current_asset_node: pm.PyNode
        self._current_asset_type: AssetType = AssetType.NONE
        self._new_asset_parent_folder_name: str
        self._new_asset_path: Path
        self._new_asset_type: AssetType = AssetType.MESH
        self._new_asset_name: str = ""
        self._rig_ref_path: Path

    on_asset_type_changed = Signal(AssetType)

    # region Current Asset Properties
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
    def current_asset_node(self, node: pm.PyNode):
        self._current_asset_node = node

    @property
    def current_asset_type(self) -> AssetType:
        return self._current_asset_type

    @current_asset_type.setter
    def current_asset_type(self, asset_type: AssetType):
        self._current_asset_type = asset_type
        mp.debug_log(f"Current Asset Type changed to: {asset_type.value}.")
        self.on_asset_type_changed.emit(asset_type)

    # endregion

    # region New Asset Properties
    @property
    def new_asset_parent_folder(self) -> str:
        return self._new_asset_parent_folder_name

    new_asset_parent_folder_changed = Signal(str)

    @new_asset_parent_folder.setter
    def new_asset_parent_folder(self, folder: str):
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
    def new_asset_type(self, asset_type: AssetType):
        self._new_asset_type = asset_type
        self.on_asset_type_changed.emit(asset_type)

    @property
    def new_asset_name(self) -> str:
        return self._new_asset_name

    @new_asset_name.setter
    def new_asset_name(self, value: str):
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
        relative_path = mp.get_path_relative_to_maya_project(path)
        self._rig_ref_path = relative_path

    # endregion

    def init_model(self):
        mp.debug_log("Model > init_model()")

        if not self._current_asset_is_valid():
            self.current_asset_type = AssetType.NONE
            return

        mp.debug_log("Initializing valid asset...")
        self.current_asset_path = mp.get_current_scene_path()
        self.current_asset_node = self._get_asset_node()
        self.current_asset_type = get_asset_type_from_node(self.current_asset_node)

    # region Current Asset
    def _get_asset_node(self) -> pm.PyNode:
        node = mp.get_top_level_node(ASSET_NODE_NAME)

        if node is None:
            return None
        else:
            has_asset_type_attr = pm.hasAttr(node, ASSET_TYPE_ATTR_NAME)
            if has_asset_type_attr is False:
                return None
            else:
                return node

    def _asset_node_exists(self) -> bool:
        node = self._get_asset_node()

        if node is None:
            return False
        else:
            return True

    def _current_asset_is_valid(self) -> bool:
        current_scene_path = mp.get_current_scene_path()

        if not current_scene_path:
            mp.debug_warning("Scene is an invalid asset because it is not saved.", print_to_script_editor=True)
            return False

        if not self._asset_node_exists():
            mp.debug_warning("Scene is an invalid asset because there is no valid Asset node.")
            return False

        return True
            
    # endregion

    # region New Asset Creation
    def create_asset(self):
        mp.debug_log("Model: create_asset()")
        try:
            # Make sure a name has been entered
            if self.new_asset_name == "" or self.new_asset_name is None:
                self._error_msg("Can't create new asset because no Asset Name is entered. Please enter an Asset Name.")
                mp.debug_error("Can't create new asset because no Asset Name is entered. Please enter an Asset Name.",
                                 print_to_script_editor=True)
                return
            # If the file has been saved previously, then save it to avoid data loss.
            if pm.sceneName():
                pm.saveFile(force=True)
            else:  # Prompt user to choose whether they want to save the scene.
                should_save_scene = self._save_scene_prompt()

                # TODO: Use an async function to allow for the user to cancel the SaveSceneAs dialog.
                # Maybe there's a way to listen for the fileOptionsCancel;
                # command that is called to close the SaveSceneAs dialog?
                if should_save_scene is Response.SAVE:
                    mel.eval('SaveSceneAs')
                elif should_save_scene is Response.CANCEL:
                    mp.debug_log("Cancelled during prompt to save current file.")
                    return

            assets_to_import_or_ref: list[AssetsToImportOrRef] = []

            mp.debug_log(f"\nCreating {self.new_asset_type.value}...")

            # Prompt user to choose to import or ref other assets based on what type of asset they are creating
            if self.new_asset_type == AssetType.SKELETON:
                mesh_path_selected = self._perform_operation_on_current_or_different_asset(Operation.REFERENCE, AssetType.MESH)
                if mesh_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.REFERENCE, mesh_path_selected))
            elif self.new_asset_type == AssetType.SKINNED_MESH:
                mesh_path_selected = self._perform_operation_on_current_or_different_asset(Operation.IMPORT, AssetType.MESH)
                if mesh_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.IMPORT, mesh_path_selected))
                skeleton_path_selected = self._perform_operation_on_current_or_different_asset(Operation.IMPORT, AssetType.SKELETON)
                if skeleton_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.IMPORT, skeleton_path_selected))
            elif self.new_asset_type == AssetType.RIG:
                skinned_mesh_path_selected = self._perform_operation_on_current_or_different_asset(Operation.IMPORT, AssetType.SKINNED_MESH)
                if skinned_mesh_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.IMPORT, skinned_mesh_path_selected))
            elif self.new_asset_type == AssetType.ANIMATION:
                rig_path_selected = self._perform_operation_on_current_or_different_asset(Operation.REFERENCE, AssetType.RIG)
                if rig_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.REFERENCE, rig_path_selected))
                    self.current_rig_ref_path = rig_path_selected

            # Create file
            self.new_asset_path = self._create_new_asset_path()

            if self.new_asset_path.exists():
                overwrite_file = self._should_we_overwrite_existing_asset(self.new_asset_path)

                if overwrite_file is Response.YES:
                    self._create_file(self.new_asset_path)
                else:
                    mp.debug_log("Cancelled during asset file creation.")
                    return
            else:
                self._create_file(self.new_asset_path)

            # Create Asset Node
            self.current_asset_node = self._create_current_asset_node(asset_type=self.new_asset_type)

            # Add Attributes to Asset Node
            self._add_attr_to_asset_node(ASSET_TYPE_ATTR_NAME, mp.AttributeType.String, self.new_asset_type.value)

            # Prompt the user to add any additional extra attributes
            if self.new_asset_type == AssetType.MESH:
                is_static = self._yes_no_prompt("Will this be a static mesh?")
                if is_static is Response.YES:
                    self._add_attr_to_asset_node(STATIC_ATTR_NAME, mp.AttributeType.Boolean, True)
            if self.new_asset_type == AssetType.ANIMATION:
                is_looping = self._yes_no_prompt("Will this animation loop?")
                if is_looping is Response.YES:
                    self._add_attr_to_asset_node(LOOP_ATTR_NAME, mp.AttributeType.Boolean, True)

            # If the new asset is a rig, we don't want to lock it
            # because then we can't move under an animation node later.
            # But we do want to lock anything else.
            if self.new_asset_type is not AssetType.RIG:
                self.current_asset_node.setLocked(lock=True)

            # Ref or Import Assets
            references: list[pm.FileReference] = []

            for asset in assets_to_import_or_ref:
                if asset.operation is Operation.IMPORT:
                    self._import_asset_node_from_file(asset.path)
                elif asset.operation is Operation.REFERENCE:
                    references.append(self._ref_asset_from_file(asset.path))

            # Move Imported / Referenced Assets to Asset Node
            self._move_imported_nodes_to_asset_node()
            self._move_ref_nodes_to_asset_node(references)

            pm.saveFile(force=True)
        except Exception as e:
            mp.debug_error(f"Exception during asset creation: {e}", print_to_script_editor=True)
        else:
            mp.debug_log(f"Created asset at: {self.new_asset_path}", print_to_script_editor=True)

    def _perform_operation_on_current_or_different_asset(self, operation: Operation,
                                                         asset_type: AssetType) -> pathlib.Path:
        asset_path_selected = None

        if self._current_asset_is_valid() and self.current_asset_type is asset_type:
            operate_on_current_asset = self._yes_no_prompt(
                message=f"Do you want to {operation.value} the currently opened {asset_type.value}?")
            if operate_on_current_asset is Response.YES:
                asset_path_selected = self.current_asset_path

        if not asset_path_selected:
            process_different_asset = self._yes_no_prompt(
                message=f"Do you want to {operation.value} a {asset_type.value}?")

            if process_different_asset is Response.YES:
                asset_path_selected = self._select_asset_to_process(operation, asset_type)

        return asset_path_selected

    def _yes_no_prompt(self, message: str) -> Response:
        mp.debug_log(f"{message}")

        response = pm.confirmDialog(
            title=Response.CONFIRM.value,
            message=message,
            button=[Response.YES.value, Response.NO.value],
            defaultButton=Response.YES.value,
            cancelButton=Response.NO.value,
            dismissString=Response.NO.value)

        mp.debug_log(f"User Response: {response}")
        return Response(response)

    def _error_msg(self, message: str):
        mp.debug_log(f"{message}")

        response = pm.confirmDialog(
            title="Error",
            message=message,
            button=["OK"],
            defaultButton="OK")

    def _select_asset_to_process(self, operation: Operation, asset_type: AssetType) -> pathlib.Path:
        asset_path: pathlib.Path
        selected_file_path: str

        mp.debug_log(f"Selecting {asset_type.value} file we will {operation.value.lower()} later on.")
        selected_file_path = pm.fileDialog2(
            fileMode=1,
            caption=f"Select {asset_type.value} file",
            startingDirectory=str(mp.get_maya_project_scenes_path() / self.new_asset_parent_folder),
            fileFilter="Maya Files (*.ma *.mb)",
            okCaption='Select',
            dialogStyle=2)

        if selected_file_path:
            mp.debug_log(f"Selected {asset_type.value} file: {selected_file_path[0]}.")
            asset_path = pathlib.Path(selected_file_path[0])
        else:
            mp.debug_log(f"Cancelled {operation.value.lower()}ing a {asset_type}")
            asset_path = pathlib.Path()

        return asset_path

    def _select_path(self, caption: str, starting_path: pathlib.Path) -> pathlib.Path:
        selected_path: pathlib.Path

        selected_path_str = pm.fileDialog2(
            fileMode=3,
            caption=caption,
            startingDirectory=str(starting_path),
            okCaption='Select',
            dialogStyle=2)

        if selected_path_str:
            selected_path = pathlib.Path(selected_path_str[0])
            mp.debug_log(f"Selected path: {selected_path}")
        else:
            mp.debug_log("Cancelled path selection.")
            selected_path = pathlib.Path()

        return selected_path

    def _create_new_asset_path(self) -> pathlib.Path:
        if self.new_asset_type == AssetType.ANIMATION:
            rig_basename = self.current_rig_ref_path.name[0:-len(ASSET_EXT)]  # remove extension
            rig_basename = rig_basename[0:-len(AssetTypeSuffix.RIG.value)]  # remove RIG suffix
            rig_dir = self.current_rig_ref_path.parent.name
            animation_filename = rig_basename + "@" + self.new_asset_name + ASSET_EXT
            self.new_asset_path = mp.get_maya_project_scenes_path() /self.new_asset_parent_folder/ rig_dir / ANIMATIONS_DIR_NAME / animation_filename
        elif self.new_asset_type == AssetType.MESH:
            mesh_filename = self.new_asset_name + AssetTypeSuffix.MESH.value + ASSET_EXT
            self.new_asset_path = mp.get_maya_project_scenes_path() /self.new_asset_parent_folder/ self.new_asset_name / mesh_filename
        elif self.new_asset_type == AssetType.SKELETON:
            skeleton_filename = self.new_asset_name + AssetTypeSuffix.SKELETON.value + ASSET_EXT
            self.new_asset_path = mp.get_maya_project_scenes_path() /self.new_asset_parent_folder/ self.new_asset_name / skeleton_filename
        elif self.new_asset_type == AssetType.SKINNED_MESH:
            skinned_mesh_filename = self.new_asset_name + AssetTypeSuffix.SKINNED_MESH.value + ASSET_EXT
            self.new_asset_path = mp.get_maya_project_scenes_path() /self.new_asset_parent_folder/ self.new_asset_name / skinned_mesh_filename
        elif self.new_asset_type == AssetType.RIG:
            rig_filename = self.new_asset_name + AssetTypeSuffix.RIG.value + ASSET_EXT
            self.new_asset_path = mp.get_maya_project_scenes_path() /self.new_asset_parent_folder/ self.new_asset_name / rig_filename

        return self.new_asset_path

    def _should_we_overwrite_existing_asset(self, filepath: pathlib.Path) -> Response:
        message = f"{filepath.name} exists, do you want to overwrite the file?"
        mp.debug_warning(f"{message} Full Path: {filepath}", print_to_script_editor=True)

        user_response_str = pm.confirmDialog(
            title=Response.CONFIRM.value,
            message=message,
            button=[Response.YES.value, Response.NO.value],
            defaultButton=Response.NO.value,
            cancelButton=Response.NO.value,
            dismissString=Response.NO.value)

        mp.debug_log(f"Prompt Result: {user_response_str}")
        return Response(user_response_str)

    def _create_file(self, filepath: pathlib.Path):
        # If the asset folder doesn't exist, then create it
        if not filepath.parent.exists():
            filepath.parent.mkdir(parents=True)

        pm.newFile(force=1)
        pm.renameFile(filepath)
        mp.debug_log(f"Created asset file: {filepath}")
        pm.saveFile(force=True)
        pm.mel.eval(f'addRecentFile("{str(filepath.as_posix())}","{ASSET_EXT_TYPE}")')

    def _ref_asset_from_file(self, filepath: pathlib.Path) -> pm.FileReference:
        mp.debug_log(f"Referencing: {filepath}...")
        ref_basename = filepath.name[0:-len(ASSET_EXT)]
        ref = pm.createReference(filepath=str(filepath), namespace=ref_basename, mergeNamespacesOnClash=True)
        pm.saveFile(force=True)
        return ref

    def _import_asset_node_from_file(self, filepath: pathlib.Path):
        mp.debug_log(f"\nBeginning process to import asset node from: {filepath} into {mp.get_current_scene_path()}")
        pm.saveFile(force=True)
        original_file = pm.sceneName()

        # Open the file with the asset node we want to export and then import later
        mp.debug_log(f"Opening {filepath}")
        pm.openFile(filepath=filepath, force=True)
        self.init_model()

        asset_node = self.current_asset_node

        if asset_node is None:
            mp.debug_error(f"No asset node found in: {filepath}. Can't import.", print_to_script_editor=True)
            return
        else:
            # Export Asset node only
            pm.select(asset_node, replace=True)
            export_file_basename = filepath.name[0:-len(ASSET_EXT)]
            export_filepath = filepath.parent / pathlib.Path(export_file_basename + "_AssetNode" + ASSET_EXT)
            mp.debug_log(f"Exporting Asset Node to: {export_filepath}")
            pm.exportSelected(str(export_filepath), type=ASSET_EXT_TYPE, force=True, preserveReferences=False)

            # Re-open original file
            mp.debug_log(f"Re-opening: {original_file}")
            pm.openFile(filepath=str(original_file), force=True)
            self.init_model()

            # Import file with Asset node
            mp.debug_log(f"Importing {export_filepath}")
            pm.importFile(filepath=export_filepath, namespace=IMPORTED_NODES_NAMESPACE, mergeNamespacesOnClash=True)

            # Delete exported Asset node file
            mp.debug_log(f"Deleting {export_filepath} \n")
            export_filepath.unlink(missing_ok=True)
            pm.saveFile(force=True)

    def _move_imported_nodes_to_asset_node(self):
        if not pm.namespace(exists=IMPORTED_NODES_NAMESPACE):
            return

        # Get the imported nodes, move them under the Asset Node, and rename them based on their Asset Type
        nodes = mp.get_nodes_in_namespace(IMPORTED_NODES_NAMESPACE)

        if nodes is None:
            return

        for node in nodes:
            was_locked = node.isLocked()
            if was_locked:
                node.unlock()

            mp.debug_log(f"Moving {node} under {self.current_asset_node}")
            node.setParent(self.current_asset_node)
            asset_type = get_asset_type_from_node(node)
            pm.rename(node, asset_type.value)
            if was_locked:
                pm.lockNode(node, lock=True)
                node.setLocked(lock=True)

        pm.namespace(removeNamespace=IMPORTED_NODES_NAMESPACE, mergeNamespaceWithRoot=True)
        pm.saveFile(force=True)

    def _move_ref_nodes_to_asset_node(self, references: list[pm.FileReference]):
        # Move the ref nodes under the Asset Node
        for ref in references:
            namespace = ref.namespace
            node = mp.get_nodes_in_namespace(namespace)[0]

            was_locked = node.isLocked()
            if was_locked:
                node.unlock()

            node.setParent(self.current_asset_node)

            if was_locked:
                pm.lockNode(node, lock=True)
                node.setLocked(lock=True)

        pm.saveFile(force=True)

    def _create_current_asset_node(self, asset_type: AssetType) -> pm.PyNode:
        mp.debug_log(f"Creating {ASSET_NODE_NAME} node for Asset Type: {asset_type}.")
        self.current_asset_node = pm.group(name=ASSET_NODE_NAME, empty=True)
        mp.debug_log(f"Finished creating {ASSET_NODE_NAME} node.")
        pm.saveFile(force=True)

        return self.current_asset_node

    def _add_attr_to_asset_node(self, name: str, attribute_type: mp.AttributeType, value: Any):
        was_locked = self.current_asset_node.isLocked()

        if was_locked:
            self.current_asset_node.unlock()

        if attribute_type is mp.AttributeType.String:
            pm.addAttr(self.current_asset_node, longName=name, dataType=attribute_type.value)
        else:
            pm.addAttr(self.current_asset_node, longName=name, attributeType=attribute_type.value)

        pm.setAttr(self.current_asset_node + "." + name, value, lock=True)
        mp.debug_log(f"Finished adding attribute: {name} of type: {attribute_type} with value: {value}.")

        if was_locked:
            self.current_asset_node.setLocked(lock=True)

        pm.saveFile(force=True)

    def _save_scene_prompt(self) -> Response:
        message = "Save changes to untitled scene?"
        mp.debug_log(message)

        user_response_str = pm.confirmDialog(
            title='Warning: Scene Not Saved',
            message=message,
            button=[Response.SAVE.value, Response.DONT_SAVE.value, Response.CANCEL.value],
            defaultButton=Response.SAVE.value,
            cancelButton=Response.CANCEL.value,
            dismissString=Response.CANCEL.value)

        mp.debug_log(f"User Response: {user_response_str}")
        return Response(user_response_str)

    # endregion

    # region Export
    def export(self):
        mp.debug_log("Model > export")
        if not self._current_asset_is_valid():
            mp.debug_warning("Asset is invalid. Can't export.", print_to_script_editor=True)
            return

        scene_relative_path = mp.get_path_relative_to_maya_project_scenes(mp.get_current_scene_path())
        export_folder_path = mp.unity_project_asset_path() / scene_relative_path.parent
        mp.export_asset(self.current_asset_node, export_folder_path=export_folder_path)

    def export_to_custom_location(self):
        mp.debug_log("Model > export to custom location")
        if not self._current_asset_is_valid():
            mp.debug_warning("Asset is invalid. Can't export.", print_to_script_editor=True)
            return

        # Select path
        path_selected: pathlib.Path = self._select_path("Select path to export asset to.", mp.unity_project_asset_path())

        if path_selected:
            mp.export_asset(self.current_asset_node, export_folder_path=path_selected)
    # endregion


def get_asset_type_from_node(node: pm.PyNode) -> AssetType:
    has_asset_type_attr = pm.hasAttr(node, ASSET_TYPE_ATTR_NAME)
    if has_asset_type_attr is False:
        mp.debug_log(f"{node} node does not have attribute: {ASSET_TYPE_ATTR_NAME}")
        return AssetType.NONE

    asset_type: AssetType = AssetType(pm.getAttr(node + "." + ASSET_TYPE_ATTR_NAME))
    if asset_type is None:
        mp.debug_log(f"{node} does not have attribute value {asset_type}")
        return AssetType.NONE
    return asset_type
