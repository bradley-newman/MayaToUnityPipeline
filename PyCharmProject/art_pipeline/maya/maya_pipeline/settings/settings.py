class Settings():
    def __init__(self, parent=None):
        import maya_pipeline as mp
        mp.debug_log(f"Opening Settings....")
        self.model = mp.SettingsModel()
        self.controller = mp.SettingsController(self.model)
        self.view = mp.SettingsView("Settings", self.model, self.controller, parent=parent)
        mp.debug_log(f"Closed Settings.")