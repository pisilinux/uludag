# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/packages.ui'
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

class Ui_PackagesDialog(object):
    def setupUi(self, PackagesDialog):
        PackagesDialog.setObjectName(_fromUtf8("PackagesDialog"))
        PackagesDialog.resize(714, 520)
        self.gridLayout_3 = QtGui.QGridLayout(PackagesDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.splitter = QtGui.QSplitter(PackagesDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.treeComponents = QtGui.QTreeWidget(self.layoutWidget)
        self.treeComponents.setSizeIncrement(QtCore.QSize(1, 0))
        self.treeComponents.setRootIsDecorated(False)
        self.treeComponents.setAllColumnsShowFocus(True)
        self.treeComponents.setHeaderHidden(False)
        self.treeComponents.setObjectName(_fromUtf8("treeComponents"))
        self.treeComponents.header().setVisible(True)
        self.verticalLayout_2.addWidget(self.treeComponents)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.searchPackage = QtGui.QLineEdit(self.layoutWidget1)
        self.searchPackage.setObjectName(_fromUtf8("searchPackage"))
        self.horizontalLayout.addWidget(self.searchPackage)
        self.comboFilter = QtGui.QComboBox(self.layoutWidget1)
        self.comboFilter.setObjectName(_fromUtf8("comboFilter"))
        self.comboFilter.addItem(_fromUtf8(""))
        self.comboFilter.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboFilter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treePackages = QtGui.QTreeWidget(self.layoutWidget1)
        self.treePackages.setSizeIncrement(QtCore.QSize(3, 0))
        self.treePackages.setRootIsDecorated(False)
        self.treePackages.setAllColumnsShowFocus(True)
        self.treePackages.setObjectName(_fromUtf8("treePackages"))
        self.verticalLayout.addWidget(self.treePackages)
        self.frame_2 = QtGui.QFrame(self.layoutWidget1)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.labelTotalSize = QtGui.QLabel(self.frame_2)
        self.labelTotalSize.setObjectName(_fromUtf8("labelTotalSize"))
        self.gridLayout_2.addWidget(self.labelTotalSize, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.frame_2)
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PackagesDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(PackagesDialog)
        QtCore.QMetaObject.connectSlotsByName(PackagesDialog)

    def retranslateUi(self, PackagesDialog):
        PackagesDialog.setWindowTitle(_translate("PackagesDialog", "Packages", None))
        self.treeComponents.setSortingEnabled(True)
        self.treeComponents.headerItem().setText(0, _translate("PackagesDialog", "Component", None))
        self.comboFilter.setItemText(0, _translate("PackagesDialog", "All Packages", None))
        self.comboFilter.setItemText(1, _translate("PackagesDialog", "Selected Packages", None))
        self.treePackages.setSortingEnabled(True)
        self.treePackages.headerItem().setText(0, _translate("PackagesDialog", "Package", None))
        self.treePackages.headerItem().setText(1, _translate("PackagesDialog", "Size", None))
        self.treePackages.headerItem().setText(2, _translate("PackagesDialog", "Version", None))
        self.treePackages.headerItem().setText(3, _translate("PackagesDialog", "Release", None))
        self.labelTotalSize.setText(_translate("PackagesDialog", "0 MB", None))
        self.label.setText(_translate("PackagesDialog", "Total Size:", None))

