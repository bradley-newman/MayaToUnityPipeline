import gc

import maya_pipeline as mp

class MayaPipeline():
    def __init__(self, title:str, mode:mp.UI_Creation_Mode):
        mp.debug_log(f"\nInitializing MayaPipeline...")
        self.title = title
        self.model = mp.MainModel()
        self.main_controller = mp.MainController(self.model)
        self.main_view = mp.MainView(title, self.model, self.main_controller, mode=mode)
        mp.debug_log(f"\nFinished initializing MayaPipeline.")

mp_obj:MayaPipeline = None

def open(title:str, mode:mp.UI_Creation_Mode):
    global mp_obj

    mp.debug_log(f"\nopen(title={title}, mode={mode})...")

    if (mode == mp.UI_Creation_Mode.RECREATE):
        mp_obj = mp.MayaPipeline(title=title, mode=mp.UI_Creation_Mode.RECREATE)
    elif (mode == mp.UI_Creation_Mode.DEFAULT):
        if mp_obj:
            mp_obj.main_view.ui = mp.create_workspace_control_with_dockable_main_win(
                title, ui_main_window=mp.Ui_MainWindow, mode=mp.UI_Creation_Mode.DEFAULT)
        else:
            mp_obj = mp.MayaPipeline(title=title, mode=mp.UI_Creation_Mode.DEFAULT)
    elif (mode == mp.UI_Creation_Mode.RESTORE_FROM_MAYA_PREFS):
        mp_obj = mp.MayaPipeline(title=title, mode=mp.UI_Creation_Mode.RESTORE_FROM_MAYA_PREFS)

def cleanup():
    import pymel.core as pm
    pm.scriptJob(killAll=True)
    gc.collect()