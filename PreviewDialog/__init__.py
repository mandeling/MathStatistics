from PreviewDialog.UI.PreviewDialog import Ui_FileDialogWindow
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QTableWidgetItem


class PreviewDialog(QDialog, Ui_FileDialogWindow):
    def __init__(self, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.fileContent = {}

        self.initUi()

    def initUi(self):
        self.pushButtonLoadFile.clicked.connect(self.openFileNameDialog)
        self.comboBoxFiles.currentTextChanged.connect(self.showData)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Open", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)

        if filePath:
            self.loadFileContent(filePath)
            self.addPath(filePath)

    def loadFileContent(self, filePath):
        with open(filePath, 'r') as f:
            self.fileContent[filePath] = f.read()

    def addPath(self, filePath):
        # add file path into combobox
        allItems = [self.comboBoxFiles.itemText(i) for i in range(self.comboBoxFiles.count())]
        if filePath not in allItems:
            self.comboBoxFiles.addItem(filePath)
            self.comboBoxFiles.setCurrentIndex(self.comboBoxFiles.count() - 1)

    def showData(self, filePath):
        # clear widgets
        self.clear()
        dataContent = self.fileContent[filePath]
        self.textBrowserViewFileData.setText(dataContent)
        dataContent = dataContent.split('\n')
        lenFirstCell = len([item for item in dataContent[0].strip().split(' ') if item])

        # add columns and rows to table widget
        self.tableWidgetViewFileData.setRowCount(len(dataContent))
        self.tableWidgetViewFileData.setColumnCount(lenFirstCell)
        for i, row in enumerate(dataContent):
            rowItems = [item for item in row.split(' ') if item]
            for j, value in enumerate(rowItems):
                self.tableWidgetViewFileData.setItem(i, j, QTableWidgetItem(value))

    def clear(self):
        # clear widgets
        self.textBrowserViewFileData.clear()
        self.tableWidgetViewFileData.setRowCount(0)
