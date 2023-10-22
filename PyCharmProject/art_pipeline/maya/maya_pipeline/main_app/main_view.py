# Maya
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import pymel.core as pm

# Internal
import maya_pipeline as mp

class MainView(QMainWindow):
    def __init__(self, title:str, model: mp.MainModel, main_controller: mp.MainController,
                 mode: mp.UI_Creation_Mode):
        super().__init__()
        self.model = model
        self.main_controller = main_controller
        self.ui = mp.create_workspace_control_with_dockable_main_win(title, mp.Ui_MainWindow(), mode)
        self.setup_ui()

        #region Settings Menu ------------------------------------------------------
        self.ui.ui_main_window.settingsAction.triggered.connect(self.on_settings_clicked)
        #endregion

        #region File Menu ------------------------------------------------------
        self.ui.ui_main_window.exportAction.triggered.connect(self.main_controller.export_to_default_path)
        self.ui.ui_main_window.exportToCustomLocationAction.triggered.connect(self.main_controller.export_asset_to_custom_path)
        #endregion

        #region Create Tab  -----------------------------------------

        #Asset Parent Folder
        #TODO: Add support for nested folders
        self.ui.ui_main_window.assetParentFolderTreeWidget.itemClicked.connect(self.main_controller.set_new_asset_parent_folder)
        self.model.new_asset_parent_folder_changed.connect(self.on_asset_folder_changed) #Signal Listener

        #Asset Type
        type = mp.AssetType(self.ui.ui_main_window.assetTypeComboBox.currentText())
        self.main_controller.set_new_asset_type(type)
        self.ui.ui_main_window.assetTypeComboBox.activated.connect(self.on_asset_type_changed)

        #Asset Name
        self.ui.ui_main_window.assetNameLineEdit.textEdited.connect(self.on_asset_name_edited)

        #Create Asset
        self.ui.ui_main_window.createAssetButton.clicked.connect(self.main_controller.create_new_asset)
        #endregion

    def setup_ui(self):
        # Setup UI
        mp.debug_log(f"DockableMainWindow > setup()")
        self.ui.setWindowTitle(self.ui.title)

        # Layout widgets
        layout = QVBoxLayout()
        self.parent_widgets: list[QWidget] = []
        self.parent_widgets.append(self.ui.ui_main_window.menubar)
        self.parent_widgets.append(self.ui.ui_main_window.centralwidget)
        self.parent_widgets.append(self.ui.ui_main_window.statusbar)

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

    def on_settings_clicked(self):
        self.main_controller.open_settings(self)

    #region Create Tab > Slots -----------------------------------------------
    def on_asset_folder_changed(self, folder: str):
        pass

    def on_asset_type_changed(self, index: int):
        type = mp.AssetType(self.ui.ui_main_window.assetTypeComboBox.itemText(index))
        self.main_controller.set_new_asset_type(type)

    def on_asset_name_edited(self):
        asset_name = self.ui.ui_main_window.assetNameLineEdit.text()
        self.main_controller.set_new_asset_name(asset_name)
    #endregion