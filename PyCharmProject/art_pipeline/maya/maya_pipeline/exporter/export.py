# Python
import pathlib
from pathlib import Path
import os
import inspect
from enum import Enum

# Maya
import pymel.core as pm

# Internal
import maya_pipeline as mp

__all__ = ["ConstraintType", "FBX_PRESETS_DIR_NAME", "export_asset"]

SCRIPT_DIRECTORY: Path = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
FBX_PRESETS_DIR_NAME = "fbx_presets"
FBX_PRESETS_PATH: Path = SCRIPT_DIRECTORY / FBX_PRESETS_DIR_NAME


def export_asset(node: pm.PyNode, export_folder_path: pathlib.Path):
    pm.saveFile(force=True)  # save file to avoid losing changes to file done during export process
    asset_type = mp.get_asset_type_from_node(node)

    # Based on the asset type, create an export filepath and export
    if asset_type is mp.AssetType.RIG or asset_type is mp.AssetType.SKELETON:
        mp.debug_warning(f"Can't export a {asset_type.value}.", print_to_script_editor=True)
        return

    export_filename = mp.get_current_scene_name_without_ext()
    export_filepath = export_folder_path / export_filename

    if asset_type is mp.AssetType.MESH:
        _export_mesh(node, export_filepath)
    elif asset_type is mp.AssetType.SKINNED_MESH:
        _export_skinned_mesh(node, export_filepath)
    elif asset_type is mp.AssetType.ANIMATION:
        _export_animation(node, export_filepath)


def _export_mesh(node: pm.PyNode, export_filepath: Path):
    mp.debug_log("Exporting Mesh...")

    _export_fbx(node, export_filepath, fbx_preset="mesh.fbxexportpreset")


def _export_skinned_mesh(node: pm.PyNode, export_filepath: Path):
    mp.debug_log("Exporting Skinned Mesh...")
    _export_fbx(node, export_filepath, fbx_preset="skinned_mesh.fbxexportpreset")


def _export_animation(node: pm.PyNode, export_filepath: Path):
    try:
        mp.debug_log("Exporting Animation...")

        # Find the rig
        rig_node = _get_descendent_of_asset_type(node, mp.AssetType.RIG)
        if not rig_node:
            mp.debug_error("Didn't find rig node.", print_to_script_editor=True)
            return

        rig_ref_node = pm.referenceQuery(rig_node, referenceNode=True)
        rig_ref = pm.FileReference(rig_ref_node)

        if not rig_ref:
            mp.debug_error("No rig reference found.", print_to_script_editor=True)
            return

        # Import rig and remove its namespace
        rig_ref.importContents(removeNamespace=True)

        # Find the skeleton
        skeleton_node = _get_descendent_of_asset_type(node, mp.AssetType.SKELETON)
        if not skeleton_node:
            mp.debug_error("No skeleton found.", print_to_script_editor=True)
            return

        # Move Skeleton under the Asset node
        skeleton_node.unlock()
        skeleton_node.setParent(node)

        # Bake animation
        joints = pm.listRelatives(skeleton_node, allDescendents=True, type="joint")
        _bake_joints(joints)  # Bake animation on skeleton

        # Delete constraints
        _delete_constraints_in_descendents(skeleton_node)

        # Delete rig
        _unlock_node_and_descendents(rig_node)
        pm.lockNode(rig_node, lock=False)
        rig_node.unlock()
        pm.delete(rig_node)

        _export_fbx(node, export_filepath, fbx_preset="animation.fbxexportpreset")
    except Exception as e:
        mp.debug_error(f"Exception during animation export: {e}", print_to_script_editor=True)
    else:
        mp.debug_log("Finished animation export.")


def _export_fbx(node: pm.PyNode, export_filepath: Path, fbx_preset: str):
    pm.select(node, replace=True)

    mp.debug_log(f"Trying to export FBX to: {export_filepath}.fbx")
    try:
        export_filepath.parent.mkdir(parents=True, exist_ok=True)
        pm.mel.FBXLoadExportPresetFile(f=FBX_PRESETS_PATH / fbx_preset)
        pm.mel.FBXExport(f=export_filepath, s=True)
    except Exception as e:
        mp.debug_error(f"Exception during export: {e}", print_to_script_editor=True)
        _reopen_current_file()
    else:
        mp.debug_log(f"Exported: {export_filepath}.fbx", print_to_script_editor=True)
        _reopen_current_file()


def _get_descendent_of_asset_type(node: pm.PyNode, asset_type: mp.AssetType) -> pm.PyNode:
    all_descendents = pm.listRelatives(node, allDescendents=True)

    for descendent in all_descendents:
        if hasattr(descendent, mp.ASSET_TYPE_ATTR_NAME):
            descendent_asset_type = mp.get_asset_type_from_node(descendent)
            if descendent_asset_type.value == asset_type.value:
                mp.debug_log(f"Found {asset_type} named: {descendent}")
                return descendent


def _unlock_node_and_descendents(node: pm.PyNode):
    node.unlock()
    all_descendents = pm.listRelatives(node, allDescendents=True)

    for descendent in all_descendents:
        descendent.unlock()


def _reopen_current_file():
    filepath_str = str(mp.get_current_scene_path())
    mp.debug_log(f"Re-opening file: {filepath_str}")
    pm.openFile(filepath=filepath_str, force=True)


def _bake_joints(joints: list[pm.joint]):
    if not joints:
        mp.debug_log("No joints to bake.")
        return

    minTime = (pm.playbackOptions(query=True, minTime=True))
    maxTime = (pm.playbackOptions(query=True, maxTime=True))
    mp.debug_log("Baking animation...")
    pm.bakeResults(joints, time=(minTime, maxTime))


class ConstraintType(Enum):
    aim = "aimConstraint"
    orient = "orientConstraint"
    scale = "scaleConstraint"
    parent = "parentConstraint"
    point = "pointConstraint"
    pole = "poleVectorConstraint"


def _delete_constraints_in_descendents(root_node: pm.PyNode):
    _delete_constraints(root_node, ConstraintType.aim)
    _delete_constraints(root_node, ConstraintType.orient)
    _delete_constraints(root_node, ConstraintType.scale)
    _delete_constraints(root_node, ConstraintType.parent)
    _delete_constraints(root_node, ConstraintType.point)
    _delete_constraints(root_node, ConstraintType.pole)


def _delete_constraints(root_node: pm.PyNode, constraint_type: ConstraintType):
    root_node_name = str(root_node)
    constraints = pm.listRelatives(root_node_name, allDescendents=True, type=constraint_type.value)
    for constraint in constraints:
        mp.debug_log(f"Deleting constraint: {constraint}", print_to_script_editor=True)
        pm.delete(constraint)
