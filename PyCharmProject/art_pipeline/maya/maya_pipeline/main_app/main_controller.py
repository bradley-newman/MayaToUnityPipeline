# PySide2
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QTreeWidgetItem

# Maya
import pymel.core as pm

import maya_pipeline as mp

__all__ = ["MainController"]


class MainController(QObject):

    def __init__(self, model: mp.MainModel, view: mp.MainView):
        super().__init__()
        self._model = model
        self._model.init_model()
        self._view = view

        # Listen for View Changes -----------------------------------------
        # Settings Menu 
        self._view.ui.ui_main_window.settingsAction.triggered.connect(self.on_settings_clicked)

        # File Menu 
        self._view.ui.ui_main_window.exportAction.triggered.connect(self.on_export_clicked)
        self._view.ui.ui_main_window.exportToCustomLocationAction.triggered.connect(
            self.on_export_to_custom_location_clicked)

        # Create Tab
        # Asset Parent Folder TODO: Add support for nested folders
        # Auto select the first item in the tree
        if self._view.ui.ui_main_window.assetParentFolderTreeWidget.topLevelItemCount() > 0:
            first_item: QTreeWidgetItem = self._view.ui.ui_main_window.assetParentFolderTreeWidget.topLevelItem(0)
            first_item.setSelected(True)
            self.on_asset_parent_folder_tree_clicked(first_item, 0)

        self._view.ui.ui_main_window.assetParentFolderTreeWidget.itemClicked.connect(
            self.on_asset_parent_folder_tree_clicked)

        # Asset Type
        # Auto select the first item in the combo box so the model is initialized
        self.on_asset_type_combobox_changed(0)
        self._view.ui.ui_main_window.assetTypeComboBox.activated.connect(self.on_asset_type_combobox_changed)

        # Asset Name
        self._view.ui.ui_main_window.assetNameLineEdit.textEdited.connect(self.on_asset_name_edited)

        # Create Asset
        self._view.ui.ui_main_window.createAssetButton.clicked.connect(self.on_create_asset_clicked)

        # Listen for Model Changes -----------------------------------------
        self.on_asset_type_changed(self._model.current_asset_type)
        self._model.on_asset_type_changed.connect(self.on_asset_type_changed)

        # Script Jobs -----------------------------------------
        pm.scriptJob(event=("SceneOpened", self._on_scene_opened))

    def _on_scene_opened(self):
        mp.debug_log(f"Opened scene: {mp.get_current_scene_path()}")
        self._model.init_model()

    def on_settings_clicked(self):
        mp.debug_log("main_controller > open_settings clicked.")
        mp.Settings(parent=self._view)

    # File > Export
    def on_export_clicked(self):
        self._model.export()

    # File > Export To Custom Location
    def on_export_to_custom_location_clicked(self):
        self._model.export_to_custom_location()

    # Asset Parent Folder
    def on_asset_parent_folder_tree_clicked(self, item: QTreeWidgetItem, column: int):
        # set new asset parent folder
        self._model.new_asset_parent_folder = item.text(column)

    # Asset Type
    def on_asset_type_combobox_changed(self, index: int):
        asset_type = mp.AssetType(self._view.ui.ui_main_window.assetTypeComboBox.itemText(index))
        self._model.new_asset_type = mp.AssetType(asset_type)

    # Asset Name
    def on_asset_name_edited(self):
        name = self._view.ui.ui_main_window.assetNameLineEdit.text()
        self._model.new_asset_name = name

    # Create Asset
    def on_create_asset_clicked(self):
        name = self._view.ui.ui_main_window.assetNameLineEdit.text()
        self._model.new_asset_name = name
        self._model.create_asset()

    # Update View with Model Changes -----------------------------------------
    # Asset Type Changed in Model
    def on_asset_type_changed(self, asset_type: mp.AssetType):
        mp.debug_log(f"Asset Type Changed to: {asset_type.value}")
        self._view.update_current_asset_type(asset_type)
