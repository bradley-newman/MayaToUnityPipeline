# Python
from enum import Enum
import pathlib
import os

# PySide2
from PySide2.QtCore import QObject
from PySide2.QtWidgets import *

# Maya
import pymel.core as pm
import maya.mel as mel

import maya_pipeline as mp

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

class AssetsToImportOrRef():
    def __init__(self, operation:Operation, path:pathlib.Path):
        self.operation = operation
        self.path = path

IMPORTED_NODES_NAMESPACE = "ImportedNodes"

class MainController(QObject):
    def __init__(self, model: mp.MainModel):
        super().__init__()
        self._model = model
        self._init_data_model()
        pm.scriptJob(event=("SceneOpened", self._on_scene_opened))

    def _on_scene_opened(self):
        mp.debug_log(f"Opened scene: {mp.get_current_scene_path()}")
        self._init_data_model()

    def _init_data_model(self):
        if self._current_asset_is_valid():
            mp.debug_log(f"Init Data Model.")
            self._set_current_asset_path(mp.get_current_scene_path())
            self._set_current_asset_node(self._get_asset_node())
            self._set_current_asset_type(mp.AssetType(pm.getAttr(self._model.current_asset_node + "." + mp.ASSET_TYPE_ATTR_NAME)))
            self._set_current_asset_type(get_asset_type_from_node(self._model.current_asset_node))

    # region File Menu

    # File > Export
    def export_to_default_path(self):
        if not self._current_asset_is_valid():
            mp.debug_warning(f"Asset is invalid. Can't export.", print_to_script_editor=True)
            return

        scene_relative_path = mp.get_path_relative_to_maya_project_scenes(mp.get_current_scene_path())
        export_folder_path = mp.unity_project_asset_path() / scene_relative_path.parent
        mp.export_asset(self._model.current_asset_node, export_folder_path=export_folder_path)

    # File > Export To Custom Location
    def export_asset_to_custom_path(self):
        if not self._current_asset_is_valid():
            mp.debug_warning(f"Asset is invalid. Can't export.", print_to_script_editor=True)
            return

        # Select path
        path_selected:pathlib.Path = self._select_path("Select path.", "Select path to export asset to.", mp.unity_project_asset_path())

        if path_selected:
            mp.export_asset(self._model.current_asset_node, export_folder_path=path_selected)

    # endregion

    # region Edit Menu

    # Edit > Settings
    def open_settings(self, parent=None):
        mp.debug_log(f"main_controller > open_settings clicked.")
        mp.Settings(parent=parent)

    # endregion

    # region Create Tab
    def set_new_asset_parent_folder(self, item: QTreeWidgetItem, column: int):
        self._model.new_asset_parent_folder = item.text(column)

    def set_new_asset_type(self, type: mp.AssetType):
        self._model.new_asset_type = type
        mp.debug_log(f"set_new_asset_type: {type}")

    def set_new_asset_name(self, name: str):
        self._model.new_asset_name = name

    def create_new_asset(self):
        try:
            # Get the folder, name, and type of asset
            if self._model.new_asset_parent_folder is None:
                mp.debug_warning(
                    f"Can't create new asset because no Asset Parent Folder is selected. Please select an Asset Parent Folder.",
                    print_to_script_editor=True)
                return

            if self._model.new_asset_name == "" or self._model.new_asset_name is None:
                mp.debug_warning(f"Can't create new asset because no Asset Name is entered. Please enter an Asset Name.",
                                 print_to_script_editor=True)
                return

            # If the file has been saved previously, then save it to avoid data loss.
            if pm.sceneName():
                pm.saveFile(force=True)
            else:  # Prompt user to choose whether they want to save the scene.
                should_save_scene = self._save_scene_prompt()

                # TODO: Use an async function to allow for the user to cancel the SaveSceneAs dialog.
                # Maybe there's a way to listen for the fileOptionsCancel; command that is called to close the SaveSceneAs dialog?
                if should_save_scene is Response.SAVE:
                    mel.eval('SaveSceneAs')
                elif should_save_scene is Response.CANCEL:
                    mp.debug_log("Cancelled during prompt to save current file.")
                    return

            # Init values for properties
            current_asset_type = self._model.current_asset_type
            current_asset_path = self._model.current_asset_path
            new_asset_parent_folder = self._model.new_asset_parent_folder
            new_asset_type = self._model.new_asset_type
            new_asset_name = self._model.new_asset_name
            assets_to_import_or_ref: list[AssetsToImportOrRef] = []

            mp.debug_log(f"\nCreating {new_asset_type.value}...")

            # Prompt user to choose to import or ref other assets based on what type of asset they are creating
            if new_asset_type == mp.AssetType.SKELETON:
                mesh_path_selected = self._perform_operation_on_current_or_different_asset(Operation.REFERENCE, mp.AssetType.MESH)
                if mesh_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.REFERENCE, mesh_path_selected))
            elif new_asset_type == mp.AssetType.SKINNED_MESH:
                mesh_path_selected = self._perform_operation_on_current_or_different_asset(Operation.IMPORT, mp.AssetType.MESH)
                if mesh_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.IMPORT, mesh_path_selected))
                skeleton_path_selected = self._perform_operation_on_current_or_different_asset(Operation.IMPORT, mp.AssetType.SKELETON)
                if skeleton_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.IMPORT, skeleton_path_selected))
            elif new_asset_type == mp.AssetType.RIG:
                skinned_mesh_path_selected = self._perform_operation_on_current_or_different_asset(Operation.IMPORT, mp.AssetType.SKINNED_MESH)
                if skinned_mesh_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.IMPORT, skinned_mesh_path_selected))
            elif new_asset_type == mp.AssetType.ANIMATION:
                rig_path_selected = self._perform_operation_on_current_or_different_asset(Operation.REFERENCE, mp.AssetType.RIG)
                if rig_path_selected:
                    assets_to_import_or_ref.append(AssetsToImportOrRef(Operation.REFERENCE, rig_path_selected))
                    self._set_current_rig_ref_path(rig_path_selected)


            # Create file
            new_asset_path = self._create_new_asset_path()

            if new_asset_path.exists():
                overwrite_file = self._should_we_overwrite_existing_asset(new_asset_path)

                if overwrite_file is Response.YES:
                    self._create_file(new_asset_path)
                else:
                    mp.debug_log(f"Cancelled during asset file creation.")
                    return
            else:
                self._create_file(new_asset_path)

            # Create Asset Node
            current_asset_node = self._create_current_asset_node(asset_type=new_asset_type)

            # Add Attributes to Asset Node
            self._add_attr_to_asset_node(mp.ASSET_TYPE_ATTR_NAME, mp.AttributeType.String, new_asset_type.value)

            if new_asset_type == mp.AssetType.MESH:
                is_static = self._yes_no_prompt(f"Will this be a static mesh?")
                if is_static is Response.YES:
                    self._add_attr_to_asset_node(mp.STATIC_ATTR_NAME, mp.AttributeType.Boolean, True)
            if new_asset_type == mp.AssetType.ANIMATION:
                is_looping = self._yes_no_prompt(f"Will this animation loop?")
                if is_looping is Response.YES:
                    self._add_attr_to_asset_node(mp.LOOP_ATTR_NAME, mp.AttributeType.Boolean, True)

            # If the new asset is a rig, we don't want to lock it because then we can't move under an animation node later.
            # But we do want to lock anything else.
            if new_asset_type is not mp.AssetType.RIG:
                current_asset_node.setLocked(lock=True)

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
            mp.debug_log(f"Created asset at: {new_asset_path}", print_to_script_editor=True)

    # endregion

    # region Current Asset
    def _current_asset_is_valid(self) -> bool:
        current_scene_path = mp.get_current_scene_path()

        if current_scene_path:
            if self._asset_node_exists():
                return True
            else:
                mp.debug_log(f"Scene is an invalid asset because there is no valid Asset node.")
                return False
        else:
            mp.debug_warning(f"Scene is an invalid asset because it is not saved.",print_to_script_editor=True)
            return False

    def _set_current_asset_path(self, path: pathlib.Path):
        self._model.current_asset_path = path

    def _set_current_asset_node(self, node: pm.PyNode):
        self._model.current_asset_node = node

    def _set_current_asset_type(self, type: mp.AssetType):
        self._model.current_asset_type = type

    def _set_current_rig_ref_path(self, path: pathlib.Path):
        self._model.current_rig_ref_path = mp.get_path_relative_to_maya_project(path)
        mp.debug_log(f"Set self._model.current_rig_ref_path: {self._model.current_rig_ref_path}")

    # endregion

    # region New Asset Creation
    def _perform_operation_on_current_or_different_asset(self, operation:Operation, asset_type:mp.AssetType) -> pathlib.Path:
        current_asset_is_valid = self._current_asset_is_valid()
        current_asset_type = self._model.current_asset_type
        current_asset_path = self._model.current_asset_path
        asset_path_selected = None

        if current_asset_is_valid and current_asset_type is asset_type:
            operate_on_current_asset = self._yes_no_prompt(message=f"Do you want to {operation.value} the currently opened {asset_type.value}?")
            if operate_on_current_asset is Response.YES:
                asset_path_selected = current_asset_path

        if not asset_path_selected:
            process_different_asset = self._yes_no_prompt(message=f"Do you want to {operation.value} a {asset_type.value}?")

            if process_different_asset is Response.YES:
                asset_path_selected = self._select_asset_to_process(operation, asset_type)

        return asset_path_selected

    def _yes_no_prompt(self, message:str) -> Response:
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

    def _select_asset_to_process(self, operation:Operation, asset_type:mp.AssetType) -> pathlib.Path:
        message = f"Please select a {asset_type.value} to {operation.value}"
        asset_path: pathlib.Path = None
        selected_file_path: str = None

        mp.debug_log(f"Selecting {asset_type.value} file we will {operation.value.lower()} later on.")
        selected_file_path = pm.fileDialog2(
            fileMode=1,
            caption=f"Select {asset_type.value} file",
            startingDirectory=str(mp.get_maya_project_scenes_path() / self._model.new_asset_parent_folder),
            fileFilter="Maya Files (*.ma *.mb)",
            okCaption='Select',
            dialogStyle=2)

        if selected_file_path:
            mp.debug_log(f"Selected {asset_type.value} file: {selected_file_path[0]}.")
            asset_path = pathlib.Path(selected_file_path[0])
        else:
            mp.debug_log(f"Cancelled {operation.value.lower()}ing a {asset_type}")

        return asset_path

    def _select_path(self, message:str, caption:str, starting_path:pathlib.Path) -> pathlib.Path:
        selected_path: pathlib.Path = None

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
            mp.debug_log(f"Cancelled path selection.")

        return selected_path

    def _create_new_asset_path(self) -> pathlib.Path:
        current_asset_type = self._model.current_asset_type
        current_asset_path = self._model.current_asset_path
        new_asset_parent_folder = self._model.new_asset_parent_folder
        new_asset_type = self._model.new_asset_type
        new_asset_name = self._model.new_asset_name
        new_asset_path:pathlib.Path = None

        if new_asset_type == mp.AssetType.ANIMATION:
            rig_basename = self._model.current_rig_ref_path.name[0:-len(mp.ASSET_EXT)]  # remove extension
            rig_basename = rig_basename[0:-len(mp.AssetTypeSuffix.RIG.value)]  # remove RIG suffix
            rig_dir = self._model.current_rig_ref_path.parent.name
            animation_filename = rig_basename + "@" + new_asset_name + mp.ASSET_EXT
            new_asset_path = mp.get_maya_project_scenes_path() / new_asset_parent_folder / rig_dir / ANIMATIONS_DIR_NAME / animation_filename
        elif new_asset_type == mp.AssetType.MESH:
            mesh_filename = new_asset_name + mp.AssetTypeSuffix.MESH.value + mp.ASSET_EXT
            new_asset_path = mp.get_maya_project_scenes_path() / new_asset_parent_folder / new_asset_name / mesh_filename
        elif new_asset_type == mp.AssetType.SKELETON:
            skeleton_filename = new_asset_name + mp.AssetTypeSuffix.SKELETON.value + mp.ASSET_EXT
            new_asset_path = mp.get_maya_project_scenes_path() / new_asset_parent_folder / new_asset_name / skeleton_filename
        elif new_asset_type == mp.AssetType.SKINNED_MESH:
            skinned_mesh_filename = new_asset_name + mp.AssetTypeSuffix.SKINNED_MESH.value + mp.ASSET_EXT
            new_asset_path = mp.get_maya_project_scenes_path() / new_asset_parent_folder / new_asset_name / skinned_mesh_filename
        elif new_asset_type == mp.AssetType.RIG:
            rig_filename = new_asset_name + mp.AssetTypeSuffix.RIG.value + mp.ASSET_EXT
            new_asset_path = mp.get_maya_project_scenes_path() / new_asset_parent_folder / new_asset_name / rig_filename

        return new_asset_path

    def _should_we_overwrite_existing_asset(self, filepath: pathlib.Path) -> Response:
        message = f"{filepath.name} exists, do you want to overwrite the file?"
        mp.debug_warning(f"{message} Full Path: {filepath}",print_to_script_editor=True)

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
        pm.mel.eval(f'addRecentFile("{str(filepath.as_posix())}","{mp.ASSET_EXT_TYPE}")')

    def _ref_asset_from_file(self, filepath:pathlib.Path) -> pm.FileReference:
        mp.debug_log(f"Referencing: {filepath}...")
        ref_basename = filepath.name[0:-len(mp.ASSET_EXT)]
        ref = pm.createReference(filepath=str(filepath), namespace=ref_basename, mergeNamespacesOnClash=True)
        pm.saveFile(force=True)
        return ref

    def _import_asset_node_from_file(self, filepath:pathlib.Path):
        mp.debug_log(f"\nBeginning process to import asset node inside: {filepath}")
        pm.saveFile(force=True)
        original_file = pm.sceneName()

        # Open the file with the asset node we want to export and then import later
        mp.debug_log(f"Opening {filepath}")
        pm.openFile(filepath=filepath, force=True)
        self._init_data_model()

        asset_node = self._model.current_asset_node

        if asset_node is None:
            mp.debug_error(f"No asset node found in: {filepath}. Can't import.", print_to_script_editor=True)
            return
        else:
            # Export Asset node only
            pm.select(asset_node, replace=True)
            export_file_basename = filepath.name[0:-len(mp.ASSET_EXT)]
            export_filepath = filepath.parent / pathlib.Path(export_file_basename + "_AssetNode" + mp.ASSET_EXT)
            mp.debug_log(f"Exporting Asset Node to: {export_filepath}")
            pm.exportSelected(str(export_filepath), type=mp.ASSET_EXT_TYPE, force=True, preserveReferences=False)

            # Re-open original file
            mp.debug_log(f"Re-opening: {original_file}")
            pm.openFile(filepath=str(original_file), force=True)
            self._init_data_model()

            # Import file with Asset node
            mp.debug_log(f"Importing {export_filepath}")
            pm.importFile(filepath=export_filepath, namespace=IMPORTED_NODES_NAMESPACE, mergeNamespacesOnClash=True)

            # Delete exported Asset node file
            mp.debug_log(f"Deleting {export_filepath} \n")
            export_filepath.unlink(missing_ok=True)
            pm.saveFile(force=True)

    def _move_imported_nodes_to_asset_node(self):
        if pm.namespace(exists=IMPORTED_NODES_NAMESPACE) is False:
            return
        else:
            # Get the imported nodes, move them under the Asset Node, and rename them based on their Asset Type
            nodes = mp.get_nodes_in_namespace(IMPORTED_NODES_NAMESPACE)

            if nodes is None:
                return
            else:
                for node in nodes:
                    was_locked = node.isLocked()
                    if was_locked:
                        node.unlock()

                    mp.debug_log(f"Moving {node} under {self._model.current_asset_node}")
                    node.setParent(self._model.current_asset_node)
                    asset_type = get_asset_type_from_node(node)
                    pm.rename(node, asset_type.value)
                    if was_locked:
                        pm.lockNode(node, lock=True)
                        node.setLocked(lock=True)

                pm.namespace(removeNamespace=IMPORTED_NODES_NAMESPACE, mergeNamespaceWithRoot=True)
                pm.saveFile(force=True)

    def _move_ref_nodes_to_asset_node(self, references:list[pm.FileReference]):
        # Move the ref nodes under the Asset Node
        for ref in references:
            namespace = ref.namespace
            node = mp.get_nodes_in_namespace(namespace)[0]
            node.setParent(self._model.current_asset_node)

        pm.saveFile(force=True)

    def _asset_node_exists(self) -> bool:
        node = self._get_asset_node()

        if node is None:
            return False
        else:
            return True

    def _create_current_asset_node(self, asset_type: mp.AssetType) -> pm.PyNode:
        mp.debug_log(f"Creating {mp.ASSET_NODE_NAME} node for Asset Type: {asset_type}.")
        self._set_current_asset_node(pm.group(name=mp.ASSET_NODE_NAME, empty=True))
        asset_node = self._model.current_asset_node
        mp.debug_log(f"Finished creating {mp.ASSET_NODE_NAME} node.")
        pm.saveFile(force=True)

        return asset_node

    def _add_attr_to_asset_node(self, name:str, type:mp.AttributeType, value):
        asset_node = self._model.current_asset_node
        was_locked = asset_node.isLocked()

        if was_locked:
            asset_node.unlock()

        if type is mp.AttributeType.String:
            pm.addAttr(asset_node, longName=name, dataType=type.value)
        else:
            pm.addAttr(asset_node, longName=name, attributeType=type.value)

        pm.setAttr(asset_node + "." + name, value, lock=True)
        mp.debug_log(f"Finished adding attribue: {name} of type: {type} with value: {value}.")

        if was_locked:
            asset_node.setLocked(lock=True)

        pm.saveFile(force=True)


    def _get_asset_node(self) -> pm.PyNode:
        node = mp.get_top_level_node(mp.ASSET_NODE_NAME)

        if node is None:
            return None
        else:
            has_asset_type_attr = pm.hasAttr(node, mp.ASSET_TYPE_ATTR_NAME)
            if has_asset_type_attr is False:
                return None
            else:
                return node

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

def get_asset_type_from_node(node:pm.PyNode) -> mp.AssetType:
    asset_type:mp.AssetType = None

    if node is None:
        return None
    else:
        has_asset_type_attr = pm.hasAttr(node, mp.ASSET_TYPE_ATTR_NAME)
        if has_asset_type_attr is False:
            return None
        else:
            return mp.AssetType(pm.getAttr(node + "." + mp.ASSET_TYPE_ATTR_NAME))