# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/packagecollection.ui'
#
# Created: Sun Dec 30 10:54:04 2012
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
        PackageCollectionDialog.resize(576, 306)
        self.gridLayout_2 = QtGui.QGridLayout(PackageCollectionDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.icon = QtGui.QLabel(PackageCollectionDialog)
        self.icon.setMinimumSize(QtCore.QSize(96, 96))
        self.icon.setMaximumSize(QtCore.QSize(96, 96))
        self.icon.setFrameShape(QtGui.QFrame.Box)
        self.icon.setFrameShadow(QtGui.QFrame.Plain)
        self.icon.setTextFormat(QtCore.Qt.RichText)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.vboxlayout.addWidget(self.icon)
        self._2 = QtGui.QHBoxLayout()
        self._2.setSpacing(5)
        self._2.setObjectName(_fromUtf8("_2"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self._2.addItem(spacerItem)
        self.selectIcon = QtGui.QToolButton(PackageCollectionDialog)
        self.selectIcon.setWhatsThis(_fromUtf8(""))
        self.selectIcon.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/raw/pics/view-preview.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectIcon.setIcon(icon)
        self.selectIcon.setObjectName(_fromUtf8("selectIcon"))
        self._2.addWidget(self.selectIcon)
        self.clearIcon = QtGui.QToolButton(PackageCollectionDialog)
        self.clearIcon.setStatusTip(_fromUtf8(""))
        self.clearIcon.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/raw/pics/edit-clear-locationbar-rtl.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearIcon.setIcon(icon1)
        self.clearIcon.setObjectName(_fromUtf8("clearIcon"))
        self._2.addWidget(self.clearIcon)
        self.vboxlayout.addLayout(self._2)
        self.gridLayout_2.addLayout(self.vboxlayout, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(16, 130, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.titleLabel = QtGui.QLabel(PackageCollectionDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.titleText = QtGui.QLineEdit(PackageCollectionDialog)
        self.titleText.setObjectName(_fromUtf8("titleText"))
        self.gridLayout.addWidget(self.titleText, 0, 1, 1, 1)
        self.descriptionText = QtGui.QTextEdit(PackageCollectionDialog)
        self.descriptionText.setObjectName(_fromUtf8("descriptionText"))
        self.gridLayout.addWidget(self.descriptionText, 1, 1, 4, 1)
        self.descriptionLabel = QtGui.QLabel(PackageCollectionDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptionLabel.sizePolicy().hasHeightForWidth())
        self.descriptionLabel.setSizePolicy(sizePolicy)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.gridLayout.addWidget(self.descriptionLabel, 1, 0, 1, 1)
        self.saveButton = QtGui.QPushButton(PackageCollectionDialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/raw/pics/document-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon2)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.gridLayout.addWidget(self.saveButton, 1, 2, 1, 1)
        self.languagesCombo = QtGui.QComboBox(PackageCollectionDialog)
        self.languagesCombo.setObjectName(_fromUtf8("languagesCombo"))
        self.gridLayout.addWidget(self.languagesCombo, 0, 2, 1, 1)
        self.packagesButton = QtGui.QPushButton(PackageCollectionDialog)
        self.packagesButton.setObjectName(_fromUtf8("packagesButton"))
        self.gridLayout.addWidget(self.packagesButton, 2, 2, 1, 1)
        self.packagesLabel = QtGui.QLabel(PackageCollectionDialog)
        self.packagesLabel.setText(_fromUtf8(""))
        self.packagesLabel.setObjectName(_fromUtf8("packagesLabel"))
        self.gridLayout.addWidget(self.packagesLabel, 3, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PackageCollectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 2, 1, 1)
        self.titleLabel.setBuddy(self.titleText)

        self.retranslateUi(PackageCollectionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PackageCollectionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PackageCollectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PackageCollectionDialog)

    def retranslateUi(self, PackageCollectionDialog):
        PackageCollectionDialog.setWindowTitle(_translate("PackageCollectionDialog", "Dialog", None))
        self.icon.setText(_translate("PackageCollectionDialog", "No Icon", None))
        self.selectIcon.setToolTip(_translate("PackageCollectionDialog", "Select Photo", None))
        self.clearIcon.setToolTip(_translate("PackageCollectionDialog", "Clear Photo", None))
        self.titleLabel.setText(_translate("PackageCollectionDialog", "Title:", None))
        self.descriptionLabel.setText(_translate("PackageCollectionDialog", "Description:", None))
        self.saveButton.setText(_translate("PackageCollectionDialog", "Save", None))
        self.packagesButton.setText(_translate("PackageCollectionDialog", "Packages", None))

import raw_rc
