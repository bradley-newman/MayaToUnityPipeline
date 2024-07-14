# Python
from enum import Enum
import pathlib

# Maya
import pymel.core as pm

import maya_pipeline as mp

__all__ = ["AttributeType", "get_current_scene_path", "get_maya_project_scenes_path",
           "get_current_scene_name_without_ext", "get_maya_project_path",
           "get_path_relative_to_maya_project", "get_path_relative_to_maya_project_scenes",
           "get_top_level_node", "get_nodes_in_namespace"]


# Maya Add Attribute Data Types shown in UI = Maya's actual attribute type returned
class AttributeType(Enum):
    Vector = "double3"  # attributeType
    Integer = "long"  # attributeType
    String = "string"  # dataType
    Float = "double"  # attributeType
    Boolean = "bool"  # attributeType
    Enum = "enum"  # attributeType


def get_current_scene_path() -> pathlib.Path:
    current_scene_path = pathlib.Path(pm.sceneName())

    if current_scene_path.exists():
        return current_scene_path
    elif current_scene_path == '':
        mp.debug_warning("Current scene is not saved.", print_to_script_editor=True)
        return None


def get_maya_project_scenes_path() -> pathlib.Path:
    scenes_path = get_maya_project_path() / "scenes"

    if scenes_path.exists():
        return scenes_path
    else:
        mp.debug_error(f"Failed to find Maya Project Scenes Path: {scenes_path}.", print_to_script_editor=True)
        return None


def get_current_scene_name_without_ext() -> str:
    path = get_current_scene_path()
    return path.stem


def get_maya_project_path() -> pathlib.Path:
    return pathlib.Path(pm.workspace(query=1, rootDirectory=1))


def get_path_relative_to_maya_project(absolute_path: pathlib.Path) -> pathlib.Path:
    relative_path = absolute_path.relative_to(get_maya_project_path())
    return relative_path


def get_path_relative_to_maya_project_scenes(absolute_path: pathlib.Path) -> pathlib.Path:
    relative_path = absolute_path.relative_to(get_maya_project_scenes_path())
    return relative_path


def get_top_level_node(node_name: str) -> pm.PyNode:
    target_node: pm.PyNode = None
    top_level_nodes = pm.ls(assemblies=True)

    for node in top_level_nodes:
        if node.nodeName() == node_name:
            target_node = node
            break

    return target_node


def get_nodes_in_namespace(namespace: str) -> list[pm.PyNode]:
    if pm.namespace(exists=namespace) is False:
        mp.debug_warning(f"Namespace {namespace} doesn't exist. Can't find nodes in this namespace.",
                         print_to_script_editor=True)
        return None
    else:
        top_level_nodes = pm.ls(assemblies=True)
        nodes_in_namespace = []

        for node in top_level_nodes:
            if node.namespace() == namespace + ":":
                nodes_in_namespace.append(node)

        return nodes_in_namespace
