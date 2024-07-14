__all__ = ["Settings"]

class Settings():
    def __init__(self, parent=None):
        import maya_pipeline as mp
        mp.debug_log("Opening Settings....")
        self.model = mp.SettingsModel()
        self.view = mp.SettingsView("Settings", self.model, parent=parent)
        self.controller = mp.SettingsController(self.model, self.view)
        self.view.show_settings()
        mp.debug_log("Closed Settings.")