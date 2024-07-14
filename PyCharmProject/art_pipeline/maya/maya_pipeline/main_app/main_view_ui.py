# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_viewQocwoV.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

__all__ = ["Ui_MainWindow"]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(385, 762)
        self.settingsAction = QAction(MainWindow)
        self.settingsAction.setObjectName(u"settingsAction")
        self.exportAction = QAction(MainWindow)
        self.exportAction.setObjectName(u"exportAction")
        self.exportToCustomLocationAction = QAction(MainWindow)
        self.exportToCustomLocationAction.setObjectName(u"exportToCustomLocationAction")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.central_widget_verticalLayout = QVBoxLayout(self.centralwidget)
        self.central_widget_verticalLayout.setObjectName(u"central_widget_verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 5)
        self.currentAssetTypeHeaderLabel = QLabel(self.centralwidget)
        self.currentAssetTypeHeaderLabel.setObjectName(u"currentAssetTypeHeaderLabel")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.currentAssetTypeHeaderLabel.setFont(font)

        self.horizontalLayout.addWidget(self.currentAssetTypeHeaderLabel)

        self.currentAssetTypeLabel = QLabel(self.centralwidget)
        self.currentAssetTypeLabel.setObjectName(u"currentAssetTypeLabel")

        self.horizontalLayout.addWidget(self.currentAssetTypeLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.central_widget_verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.createTab = QWidget()
        self.createTab.setObjectName(u"createTab")
        self.verticalLayout = QVBoxLayout(self.createTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.assetTypeLayout = QHBoxLayout()
        self.assetTypeLayout.setObjectName(u"assetTypeLayout")
        self.assetTypeLayout.setContentsMargins(-1, 0, -1, 0)
        self.assetTypeLabel = QLabel(self.createTab)
        self.assetTypeLabel.setObjectName(u"assetTypeLabel")
        self.assetTypeLabel.setFont(font)

        self.assetTypeLayout.addWidget(self.assetTypeLabel, 0, Qt.AlignLeft)

        self.assetTypeComboBox = QComboBox(self.createTab)
        self.assetTypeComboBox.addItem("")
        self.assetTypeComboBox.addItem("")
        self.assetTypeComboBox.addItem("")
        self.assetTypeComboBox.addItem("")
        self.assetTypeComboBox.addItem("")
        self.assetTypeComboBox.setObjectName(u"assetTypeComboBox")
        self.assetTypeComboBox.setMinimumSize(QSize(100, 0))

        self.assetTypeLayout.addWidget(self.assetTypeComboBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.assetTypeLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.assetTypeLayout)

        self.assetParentFolderTreeWidget = QTreeWidget(self.createTab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setFont(0, font);
        self.assetParentFolderTreeWidget.setHeaderItem(__qtreewidgetitem)
        QTreeWidgetItem(self.assetParentFolderTreeWidget)
        QTreeWidgetItem(self.assetParentFolderTreeWidget)
        QTreeWidgetItem(self.assetParentFolderTreeWidget)
        QTreeWidgetItem(self.assetParentFolderTreeWidget)
        QTreeWidgetItem(self.assetParentFolderTreeWidget)
        QTreeWidgetItem(self.assetParentFolderTreeWidget)
        self.assetParentFolderTreeWidget.setObjectName(u"assetParentFolderTreeWidget")
        self.assetParentFolderTreeWidget.setMinimumSize(QSize(0, 150))
        self.assetParentFolderTreeWidget.setMaximumSize(QSize(16777215, 150))
        self.assetParentFolderTreeWidget.header().setVisible(False)

        self.verticalLayout.addWidget(self.assetParentFolderTreeWidget, 0, Qt.AlignTop)

        self.assetNameLayout = QHBoxLayout()
        self.assetNameLayout.setObjectName(u"assetNameLayout")
        self.assetNameLayout.setContentsMargins(-1, -1, -1, 5)
        self.assetNameLabel = QLabel(self.createTab)
        self.assetNameLabel.setObjectName(u"assetNameLabel")
        self.assetNameLabel.setFont(font)
        self.assetNameLabel.setFrameShadow(QFrame.Plain)

        self.assetNameLayout.addWidget(self.assetNameLabel)

        self.assetNameLineEdit = QLineEdit(self.createTab)
        self.assetNameLineEdit.setObjectName(u"assetNameLineEdit")
        self.assetNameLineEdit.setFocusPolicy(Qt.StrongFocus)

        self.assetNameLayout.addWidget(self.assetNameLineEdit)


        self.verticalLayout.addLayout(self.assetNameLayout)

        self.createAssetLayout = QHBoxLayout()
        self.createAssetLayout.setObjectName(u"createAssetLayout")
        self.createAssetLayout.setContentsMargins(-1, -1, -1, 100)
        self.createAssetButton = QPushButton(self.createTab)
        self.createAssetButton.setObjectName(u"createAssetButton")
        self.createAssetButton.setMinimumSize(QSize(0, 25))
        self.createAssetButton.setMaximumSize(QSize(16777215, 25))

        self.createAssetLayout.addWidget(self.createAssetButton, 0, Qt.AlignTop)


        self.verticalLayout.addLayout(self.createAssetLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.createTab, "")

        self.central_widget_verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 385, 22))
        self.editMenu = QMenu(self.menubar)
        self.editMenu.setObjectName(u"editMenu")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.editMenu.menuAction())
        self.editMenu.addAction(self.settingsAction)
        self.menuFile.addAction(self.exportAction)
        self.menuFile.addAction(self.exportToCustomLocationAction)

        self.retranslateUi(MainWindow)
        self.assetNameLineEdit.returnPressed.connect(self.createAssetButton.click)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.settingsAction.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.settingsAction.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.exportAction.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.exportToCustomLocationAction.setText(QCoreApplication.translate("MainWindow", u"Export to Custom Location", None))
        self.currentAssetTypeHeaderLabel.setText(QCoreApplication.translate("MainWindow", u"Current Asset Type:", None))
        self.currentAssetTypeLabel.setText(QCoreApplication.translate("MainWindow", u"<NONE>", None))
        self.assetTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Asset Type", None))
        self.assetTypeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Mesh", None))
        self.assetTypeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Skeleton", None))
        self.assetTypeComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"SkinnedMesh", None))
        self.assetTypeComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Rig", None))
        self.assetTypeComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Animation", None))

        ___qtreewidgetitem = self.assetParentFolderTreeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Asset Parent Folders", None));

        __sortingEnabled = self.assetParentFolderTreeWidget.isSortingEnabled()
        self.assetParentFolderTreeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.assetParentFolderTreeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Characters", None));
        ___qtreewidgetitem2 = self.assetParentFolderTreeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"Environment", None));
        ___qtreewidgetitem3 = self.assetParentFolderTreeWidget.topLevelItem(2)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"Items", None));
        ___qtreewidgetitem4 = self.assetParentFolderTreeWidget.topLevelItem(3)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"Props", None));
        ___qtreewidgetitem5 = self.assetParentFolderTreeWidget.topLevelItem(4)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"Structures", None));
        ___qtreewidgetitem6 = self.assetParentFolderTreeWidget.topLevelItem(5)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"Vehicles", None));
        self.assetParentFolderTreeWidget.setSortingEnabled(__sortingEnabled)

        self.assetNameLabel.setText(QCoreApplication.translate("MainWindow", u"Asset Name", None))
        self.createAssetButton.setText(QCoreApplication.translate("MainWindow", u"Create Asset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.createTab), QCoreApplication.translate("MainWindow", u"Create", None))
        self.editMenu.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

