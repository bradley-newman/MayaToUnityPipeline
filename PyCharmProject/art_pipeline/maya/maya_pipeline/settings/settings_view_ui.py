# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_viewHkKbsC.ui'
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

__all__ = ["Ui_SettingsDialog"]

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(553, 324)
        self.settingsDialogHorizontalLayout = QHBoxLayout(SettingsDialog)
        self.settingsDialogHorizontalLayout.setObjectName(u"settingsDialogHorizontalLayout")
        self.centralWidget = QWidget(SettingsDialog)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMinimumSize(QSize(500, 0))
        self.centralWidget_verticalLayout = QVBoxLayout(self.centralWidget)
        self.centralWidget_verticalLayout.setObjectName(u"centralWidget_verticalLayout")
        self.centralWidget_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.unity_label = QLabel(self.centralWidget)
        self.unity_label.setObjectName(u"unity_label")

        self.centralWidget_verticalLayout.addWidget(self.unity_label)

        self.unity_horizontalLayout = QHBoxLayout()
        self.unity_horizontalLayout.setObjectName(u"unity_horizontalLayout")
        self.unity_line_edit = QLineEdit(self.centralWidget)
        self.unity_line_edit.setObjectName(u"unity_line_edit")
        self.unity_line_edit.setReadOnly(True)

        self.unity_horizontalLayout.addWidget(self.unity_line_edit)

        self.unity_browse_button = QPushButton(self.centralWidget)
        self.unity_browse_button.setObjectName(u"unity_browse_button")

        self.unity_horizontalLayout.addWidget(self.unity_browse_button)


        self.centralWidget_verticalLayout.addLayout(self.unity_horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 181, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.centralWidget_verticalLayout.addItem(self.verticalSpacer)

        self.save_cancel_buttons = QDialogButtonBox(self.centralWidget)
        self.save_cancel_buttons.setObjectName(u"save_cancel_buttons")
        self.save_cancel_buttons.setOrientation(Qt.Horizontal)
        self.save_cancel_buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.centralWidget_verticalLayout.addWidget(self.save_cancel_buttons)


        self.settingsDialogHorizontalLayout.addWidget(self.centralWidget)


        self.retranslateUi(SettingsDialog)
        self.save_cancel_buttons.rejected.connect(SettingsDialog.reject)
        self.save_cancel_buttons.accepted.connect(SettingsDialog.accept)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.unity_label.setText(QCoreApplication.translate("SettingsDialog", u"Unity Project Export Path", None))
        self.unity_browse_button.setText(QCoreApplication.translate("SettingsDialog", u"Browse", None))
    # retranslateUi

