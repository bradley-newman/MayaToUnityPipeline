from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import maya_pipeline

import sys
import gc

module_names = [
    "userSetup",
    "maya_pipeline",
    "maya_pipeline.exporter.export",
    "maya_pipeline.logging.logging",
    "maya_pipeline.misc.ui_creation_mode",
    "maya_pipeline.main_app.main_model",
    "maya_pipeline.main_app.main_controller",
    "maya_pipeline.main_app.main_view",
    "maya_pipeline.main_app.main_view_ui",
    "maya_pipeline.misc.dockable_main_window",
    "maya_pipeline.misc.maya_utilities",
    "maya_pipeline.misc.pyside_utilities",
    "maya_pipeline.settings.settings",
    "maya_pipeline.settings.settings_file",
    "maya_pipeline.settings.settings_model",
    "maya_pipeline.settings.settings_controller",
    "maya_pipeline.settings.settings_view",
    "maya_pipeline.settings.settings_view_ui",
    "maya_pipeline.main_app.main_app"
]

def cleanup_memory():
    print(f"Cleaning up Maya Pipeline memory...")
    _cleanup_workspace_control("Maya Pipeline")
    _cleanup_main_app()
    _delete_modules_and_reimport_mp()

def _cleanup_workspace_control(title:str):
    print(f"Cleanup Workspace Control: {title}...")
    import maya_pipeline as mp
    workspace_control_name = mp.get_workspace_control_name(title)
    mp.delete_workspace_control_widgets(workspace_control_name)
    mp.delete_workspace_control(workspace_control_name)

def _cleanup_main_app():
    print(f"Cleanup Maya Pipeline...")
    import maya_pipeline as mp
    mp.cleanup()
    gc.collect()

def _delete_modules_and_reimport_mp():
    try:
        print("\nDeleting and re-importing Maya Pipeline package modules...")

        MayaPipeline_objs = _get_MayaPipeline_objs()
        _del_MayaPipeline_objs(MayaPipeline_objs)

        sys_module_names = _get_mp_module_names_in_sys_modules()
        _del_sys_modules(sys_module_names)

        global_module_names = _get_mp_module_names_in_global_modules()
        _del_global_modules(global_module_names)

        gc.collect()

        print(f"importing maya_pipeline...")
        import maya_pipeline
    except Exception as e:
        print(f"\nException trying to delete and re-importing maya_pipeline modules: {e}")
    else:
        print(f"\nSuccessfully deleted and re-imported maya_pipeline modules.")

def _get_MayaPipeline_objs() -> list[maya_pipeline.MayaPipeline]:
    import maya_pipeline
    print(f"\nGetting MayaPipeline objs in memory...")
    objects = gc.get_objects()
    MayaPipeline_objs = [x for x in objects if isinstance(x, maya_pipeline.MayaPipeline)]

    if len(MayaPipeline_objs) == 0:
        print("No MayaPipeline objs found.")
    else:
        print(f"- Found {len(MayaPipeline_objs)} MayaPipeline obj.")

    return MayaPipeline_objs

def _del_MayaPipeline_objs(MayaPipeline_objs:list):
    if len(MayaPipeline_objs) > 0:
        print(f"\nDeleting MayaPipeline_objs in memory...")
        for mp_obj in MayaPipeline_objs:
            try:
                print(f"- Trying to delete MayaPipeline object: {mp_obj}")
                del mp_obj
            except Exception as e:
                print(f"- Exception: {e}")
            else:
                print(f"- Successfully deleted MayaPipeline objects.")
    else:
        print(f"No MayaPipeline objects to delete.")

def _get_mp_module_names_in_sys_modules() -> list[str]:
    print(f"\nGetting mp modules in sys.modules...")
    module_names_found = []
    for module_name in module_names:
        if module_name in sys.modules:
            print(f"- Found {module_name} in sys.modules")
            module_names_found.append(module_name)

    if len(module_names_found) == 0:
        print("No mp modules found in sys.modules.")

    return module_names_found

def _del_sys_modules(module_names:list[str]):
    if len(module_names) > 0:
        print(f"\nDeleting mp modules in sys.modules...")
        for module_name in module_names:
            try:
                print(f"- Trying to delete sys.modules[{module_name}]")
                del sys.modules[module_name]
            except Exception as e:
                print(f"- Exception: {e}")
            else:
                print(f"- Successfully deleted sys.modules[{module_name}].")
    else:
        print("No mp modules to delete in sys.modules.")

def _get_mp_module_names_in_global_modules() -> list[str]:
    print(f"\nGetting mp modules in globals...")
    module_names_found = []
    for module_name in module_names:
        if module_name in globals():
            print(f"- Found {module_name} in globals()")
            module_names_found.append(module_name)

    if len(module_names_found) == 0:
        print("No mp modules found in globals().")

    return module_names_found

def _del_global_modules(module_names:list[str]):
    if len(module_names) > 0:
        print(f"\nDeleting mp modules in globals()...")
        for module_name in module_names:
            try:
                print(f"- Trying to deleted global module {module_name}")
                del globals()[module_name]
            except Exception as e:
                print(f"- Exception: {e}")
            else:
                print(f"- Successfully deleted global module {module_name}.")
    else:
        print("No mp modules to delete in global modules.")
