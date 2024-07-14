import gc

# Maya
import pymel.core as pm

import maya_pipeline as mp

__all__ = ["MayaPipeline", "open_mp", "on_close", "cleanup"]


class MayaPipeline:
    def __init__(self, title: str, mode: mp.UI_Creation_Mode):
        mp.debug_log("\nInitializing MayaPipeline...")
        self.model = mp.MainModel()
        self.main_view = mp.MainView(title, mode=mode)
        self.main_controller = mp.MainController(self.model, self.main_view)
        mp.debug_log("\nFinished initializing MayaPipeline.")


mp_obj: MayaPipeline = None


def open_mp(title: str, mode: mp.UI_Creation_Mode):
    global mp_obj

    mp.debug_log(f"\nOpening Maya Pipeline(title={title}, mode={mode})...")

    if mode == mp.UI_Creation_Mode.DEFAULT:
        if not mp_obj:
            # If UI doesn't exist, then create it
            mp.debug_log("Creating UI from scratch")
            mp_obj = mp.MayaPipeline(title=title, mode=mp.UI_Creation_Mode.DEFAULT)
            mp_obj.main_view.ui.on_dock_closed.connect(on_close)
            return
        # Restore the UI that exists (i.e. was previously closed)
        mp.debug_log("Restoring UI that exists")
        mp_obj.main_view.ui = mp.create_workspace_control_with_dockable_main_win(
            title, ui_main_window=mp.Ui_MainWindow, mode=mp.UI_Creation_Mode.DEFAULT)
        mp_obj.model = mp.MainModel()
        mp_obj.main_controller = mp.MainController(mp_obj.model, mp_obj.main_view)
        mp_obj.main_view.ui.on_dock_closed.connect(on_close)
        mp_obj.main_view.ui.on_dock_closed.connect(on_close)
    elif mode == mp.UI_Creation_Mode.RESTORE_FROM_MAYA_PREFS:
        # When Maya starts create the UI and restore its previous state when Maya quit
        mp_obj = mp.MayaPipeline(title=title, mode=mp.UI_Creation_Mode.RESTORE_FROM_MAYA_PREFS)
        mp_obj.main_view.ui.on_dock_closed.connect(on_close)
    elif mode == mp.UI_Creation_Mode.RECREATE:
        # Destroy any existing UI and recreate the UI (for developers)
        mp_obj = mp.MayaPipeline(title=title, mode=mp.UI_Creation_Mode.RECREATE)

def on_close():
    mp.debug_log("Maya Pipeline Closed.")
    if mp_obj is not None:
        mp_obj.main_view.ui.on_dock_closed.disconnect(on_close)
    cleanup()


def cleanup():
    mp.debug_log("Cleaning up Maya Pipeline.")
    pm.scriptJob(killAll=True)
    gc.collect()
