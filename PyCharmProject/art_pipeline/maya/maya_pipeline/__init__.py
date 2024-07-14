print("\nInitializing maya_pipeline package...")
from . import misc
from .misc.maya_utilities import (AttributeType, get_current_scene_path, get_maya_project_scenes_path,
                                  get_current_scene_name_without_ext, get_maya_project_path,
                                  get_path_relative_to_maya_project, get_path_relative_to_maya_project_scenes,
                                  get_top_level_node, get_nodes_in_namespace)
from . import mp_logging
from .mp_logging.logging import (FORCE_PRINT_TO_SCRIPT_EDITOR, LogMode, MAX_FILE_COUNT, WRITE_IMMEDIATELY,
                                 create_log, debug_error, debug_log, debug_warning, prune_logs, logging_script_directory)

from .misc.ui_creation_mode import (UI_Creation_Mode)
from .main_app.main_model import (AssetType,AssetTypeSuffix,ASSET_EXT,ASSET_EXT_TYPE,
                                  ASSET_NODE_NAME,ASSET_TYPE_ATTR_NAME, IMPORTED_NODES_NAMESPACE, STATIC_ATTR_NAME,
                                  LOOP_ATTR_NAME,ANIMATIONS_DIR_NAME,Response,Operation, AssetsToImportOrRef,
                                  MainModel,get_asset_type_from_node)
from .main_app.main_view_ui import (Ui_MainWindow)
from .main_app.main_view import (MainView)
from .main_app.main_controller import (MainController)
from .misc.dockable_main_window import (DockableMainWindow, create_dockable_main_win, create_workspace_control,
                                        create_workspace_control_with_dockable_main_win, delete_workspace_control,
                                        delete_workspace_control_widgets, get_dockable_main_win_child,
                                        get_dockable_win_name, get_workspace_control_name, restore_workspace_control,
                                        workspace_control_exists)
from .misc.pyside_utilities import (scale_qobjects, print_qobject_tree)
from . import settings
from .settings.settings import(Settings)
from .settings.settings_model import (settings_script_directory, settings_dir, SETTINGS_FILENAME, settings_filepath,
                                      SettingsKeys, settings_defaults, SettingsModel, unity_project_asset_path,
                                      create_settings_file, load_settings_file, save_settings_to_file, read_setting)
from .settings.settings_controller import(SettingsController)
from .settings.settings_view import (SettingsView)
from .settings.settings_view_ui import (Ui_SettingsDialog)
from . import main_app
from .main_app.main_app import (MayaPipeline, open_mp, on_close, cleanup)
from . import exporter
from .exporter.export import (ConstraintType, FBX_PRESETS_DIR_NAME, export_asset)

__all__ = list(
    set(exporter.export.__all__) |
    set(mp_logging.logging.__all__) |
    set(main_app.main_app.__all__) |
    set(main_app.main_controller.__all__) |
    set(main_app.main_model.__all__) |
    set(main_app.main_view.__all__) |
    set(main_app.main_view_ui.__all__) |
    set(misc.dockable_main_window.__all__) |
    set(misc.maya_utilities.__all__) |
    set(misc.pyside_utilities.__all__) |
    set(misc.ui_creation_mode.__all__) |
    set(settings.settings.__all__) |
    set(settings.settings_controller.__all__) |
    set(settings.settings_model.__all__) |
    set(settings.settings_view.__all__) |
    set(settings.settings_view_ui.__all__)
)

print("Finished initializing maya_pipeline package.\n")