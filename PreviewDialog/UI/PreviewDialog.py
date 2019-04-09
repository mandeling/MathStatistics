# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PreviewDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileDialogWindow(object):
    def setupUi(self, FileDialogWindow):
        FileDialogWindow.setObjectName("FileDialogWindow")
        FileDialogWindow.setWindowModality(QtCore.Qt.NonModal)
        FileDialogWindow.resize(558, 192)
        FileDialogWindow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        FileDialogWindow.setSizeGripEnabled(False)
        FileDialogWindow.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(FileDialogWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonLoadFile = QtWidgets.QPushButton(FileDialogWindow)
        self.pushButtonLoadFile.setObjectName("pushButtonLoadFile")
        self.gridLayout.addWidget(self.pushButtonLoadFile, 1, 1, 1, 1)
        self.comboBoxFiles = QtWidgets.QComboBox(FileDialogWindow)
        self.comboBoxFiles.setObjectName("comboBoxFiles")
        self.gridLayout.addWidget(self.comboBoxFiles, 1, 0, 1, 1)
        self.tabWidgetFileDialog = QtWidgets.QTabWidget(FileDialogWindow)
        self.tabWidgetFileDialog.setAcceptDrops(False)
        self.tabWidgetFileDialog.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidgetFileDialog.setObjectName("tabWidgetFileDialog")
        self.tabViewData = QtWidgets.QWidget()
        self.tabViewData.setObjectName("tabViewData")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabViewData)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowserViewFileData = QtWidgets.QTextBrowser(self.tabViewData)
        self.textBrowserViewFileData.setAcceptDrops(False)
        self.textBrowserViewFileData.setObjectName("textBrowserViewFileData")
        self.gridLayout_2.addWidget(self.textBrowserViewFileData, 0, 0, 1, 1)
        self.tabWidgetFileDialog.addTab(self.tabViewData, "")
        self.tabTableViewData = QtWidgets.QWidget()
        self.tabTableViewData.setObjectName("tabTableViewData")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabTableViewData)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidgetViewFileData = QtWidgets.QTableWidget(self.tabTableViewData)
        self.tableWidgetViewFileData.setAcceptDrops(False)
        self.tableWidgetViewFileData.setFrameShape(QtWidgets.QFrame.Panel)
        self.tableWidgetViewFileData.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidgetViewFileData.setDragEnabled(True)
        self.tableWidgetViewFileData.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.tableWidgetViewFileData.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.tableWidgetViewFileData.setObjectName("tableWidgetViewFileData")
        self.tableWidgetViewFileData.setColumnCount(0)
        self.tableWidgetViewFileData.setRowCount(0)
        self.tableWidgetViewFileData.horizontalHeader().setVisible(False)
        self.tableWidgetViewFileData.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetViewFileData.verticalHeader().setVisible(False)
        self.gridLayout_3.addWidget(self.tableWidgetViewFileData, 0, 0, 1, 1)
        self.tabWidgetFileDialog.addTab(self.tabTableViewData, "")
        self.gridLayout.addWidget(self.tabWidgetFileDialog, 0, 0, 1, 2)

        self.retranslateUi(FileDialogWindow)
        self.tabWidgetFileDialog.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FileDialogWindow)

    def retranslateUi(self, FileDialogWindow):
        _translate = QtCore.QCoreApplication.translate
        FileDialogWindow.setWindowTitle(_translate("FileDialogWindow", "Завантаження даних"))
        self.pushButtonLoadFile.setText(_translate("FileDialogWindow", "Завантажити файл"))
        self.tabWidgetFileDialog.setTabText(self.tabWidgetFileDialog.indexOf(self.tabViewData), _translate("FileDialogWindow", "Файл"))
        self.tabWidgetFileDialog.setTabText(self.tabWidgetFileDialog.indexOf(self.tabTableViewData), _translate("FileDialogWindow", "Таблиця з даними"))

