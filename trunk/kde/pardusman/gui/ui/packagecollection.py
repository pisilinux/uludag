# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/packagecollection.ui'
#
# Created: Sun Dec 30 10:32:38 2012
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PackageCollectionDialog(object):
    def setupUi(self, PackageCollectionDialog):
        PackageCollectionDialog.setObjectName(_fromUtf8("PackageCollectionDialog"))
        PackageCollectionDialog.resize(493, 304)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PackageCollectionDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame = QtGui.QFrame(PackageCollectionDialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.titleLabel = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.titleText = QtGui.QLineEdit(self.frame)
        self.titleText.setObjectName(_fromUtf8("titleText"))
        self.gridLayout.addWidget(self.titleText, 0, 1, 1, 1)
        self.languagesCombo = QtGui.QComboBox(self.frame)
        self.languagesCombo.setObjectName(_fromUtf8("languagesCombo"))
        self.gridLayout.addWidget(self.languagesCombo, 0, 2, 1, 1)
        self.descriptionLabel = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptionLabel.sizePolicy().hasHeightForWidth())
        self.descriptionLabel.setSizePolicy(sizePolicy)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.gridLayout.addWidget(self.descriptionLabel, 1, 0, 1, 1)
        self.descriptionText = QtGui.QTextEdit(self.frame)
        self.descriptionText.setObjectName(_fromUtf8("descriptionText"))
        self.gridLayout.addWidget(self.descriptionText, 1, 1, 2, 1)
        self.packagesButton = QtGui.QPushButton(self.frame)
        self.packagesButton.setObjectName(_fromUtf8("packagesButton"))
        self.gridLayout.addWidget(self.packagesButton, 1, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(18, 13, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.icon = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setMinimumSize(QtCore.QSize(96, 96))
        self.icon.setMaximumSize(QtCore.QSize(96, 96))
        self.icon.setFrameShape(QtGui.QFrame.Box)
        self.icon.setFrameShadow(QtGui.QFrame.Plain)
        self.icon.setTextFormat(QtCore.Qt.RichText)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.horizontalLayout_2.addWidget(self.icon)
        spacerItem1 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self._2 = QtGui.QHBoxLayout()
        self._2.setSpacing(5)
        self._2.setObjectName(_fromUtf8("_2"))
        spacerItem2 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self._2.addItem(spacerItem2)
        self.selectIcon = QtGui.QToolButton(self.frame)
        self.selectIcon.setWhatsThis(_fromUtf8(""))
        self.selectIcon.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/raw/pics/view-preview.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectIcon.setIcon(icon)
        self.selectIcon.setObjectName(_fromUtf8("selectIcon"))
        self._2.addWidget(self.selectIcon)
        self.clearIcon = QtGui.QToolButton(self.frame)
        self.clearIcon.setStatusTip(_fromUtf8(""))
        self.clearIcon.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/raw/pics/edit-clear-locationbar-rtl.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearIcon.setIcon(icon1)
        self.clearIcon.setObjectName(_fromUtf8("clearIcon"))
        self._2.addWidget(self.clearIcon)
        spacerItem3 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self._2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self._2)
        self.gridLayout.addLayout(self.verticalLayout, 2, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.frame)
        spacerItem4 = QtGui.QSpacerItem(20, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.buttonBox = QtGui.QDialogButtonBox(PackageCollectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.titleLabel.setBuddy(self.titleText)

        self.retranslateUi(PackageCollectionDialog)
        QtCore.QMetaObject.connectSlotsByName(PackageCollectionDialog)

    def retranslateUi(self, PackageCollectionDialog):
        PackageCollectionDialog.setWindowTitle(_translate("PackageCollectionDialog", "Dialog", None))
        self.titleLabel.setText(_translate("PackageCollectionDialog", "Title:", None))
        self.descriptionLabel.setText(_translate("PackageCollectionDialog", "Description:", None))
        self.packagesButton.setText(_translate("PackageCollectionDialog", "Packages", None))
        self.icon.setText(_translate("PackageCollectionDialog", "No Icon", None))
        self.selectIcon.setToolTip(_translate("PackageCollectionDialog", "Select Photo", None))
        self.clearIcon.setToolTip(_translate("PackageCollectionDialog", "Clear Photo", None))

import raw_rc
