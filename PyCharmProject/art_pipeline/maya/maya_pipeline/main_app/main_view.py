# Maya
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QWidget, QVBoxLayout, QMainWindow
# from PySide2.QtGui import *
import pymel.core as pm

# Internal
import maya_pipeline as mp

__all__ = ["MainView"]


class MainView(QMainWindow):
    def __init__(self, title: str, mode: mp.UI_Creation_Mode):
        super().__init__()
        self.ui: mp.DockableMainWindow = mp.create_workspace_control_with_dockable_main_win(title, mp.Ui_MainWindow(), mode)
        self.parent_widgets: list[QWidget] = []
        self.parent_widgets.append(self.ui.ui_main_window.menubar)
        self.parent_widgets.append(self.ui.ui_main_window.centralwidget)
        self.parent_widgets.append(self.ui.ui_main_window.statusbar)
        self.setup_ui()

    def setup_ui(self):
        # Setup UI
        self.ui.setWindowTitle(self.ui.title)

        # Layout widgets
        layout = QVBoxLayout()

        for widget in self.parent_widgets:
            layout.addWidget(widget)

        self.ui.setLayout(layout)

        main_window_widget: QWidget = self.ui.ui_main_window.centralwidget.parentWidget()
        all_widgets = main_window_widget.findChildren(QObject)

        # Query Maya's current DPI scaling mode.
        if pm.mayaDpiSetting(query=True, mode=True) == 1:  # 1 == Custom scaling
            # Query the current scale value and use it to scale the UI widgets
            scale_value: int = pm.mayaDpiSetting(query=True, scaleValue=True)
            mp.scale_qobjects(all_widgets, scale_value)

    # Update View with Model Changes
    def update_current_asset_type(self, asset_type: mp.AssetType):
        self.ui.ui_main_window.currentAssetTypeLabel.setText(asset_type.value)