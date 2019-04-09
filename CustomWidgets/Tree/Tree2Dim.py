from contextlib import contextmanager
from PyQt5 import sip
from PyQt5.QtWidgets import QTreeWidget, QMenu, QMessageBox, QTreeWidgetItem, QInputDialog, QApplication, QLineEdit
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt

from Dimension.Dim2 import Dim2
from Dimension.Dim2.ProtocolRender import showLinearCorrelation, showRangCorrelation, showCombinationsTable2x2, \
    showCombinationsTable2x2Indexes, showCombinationsTableMxN, showCombinationsTableMxNIndexes
from Dimension.Dim2.OperationOnData import removeAbnormal


class CustomTree2Dim(QTreeWidget):

    def __init__(self, mainWin):
        QTreeWidget.__init__(self)
        self.window = mainWin
        self.__countDim = 2
        self._droppedData = {}

        self.initTree()

    def initTree(self):
        self.setHeaderHidden(True)
        self.setFocusPolicy(Qt.NoFocus)

        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def dragEnterEvent(self, event):
        if event.source():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        dragOn = self.itemAt(event.pos())
        if event.source() and dragOn and not dragOn.parent():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        dropIn = self.itemAt(event.pos())
        if event.mimeData() and dropIn:
            source = event.source()
            dropOnRow = self.indexFromItem(dropIn, 0).row()
            self.updateDataDict(dropIn, dropOnRow, source)
        else:
            event.ignore()

    @contextmanager
    def wait_cursor(self):
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            yield
        finally:
            QApplication.restoreOverrideCursor()

    def updateDataDict(self, curItem, row, source):
        self.makeKeyDict(row)
        if self.dictDataIsAvailable(row):
            self._droppedData[row]['data'].append(self.getData(source))
            self._droppedData[row]['significance level'] = 0.05
            self._droppedData[row]['name'] += ' X{}'.format(source.currentRow())

            self.setTextItem(curItem, row)

        if self.dictDataIsFull(row) and not curItem.childCount():
            self.updateFolder(curItem, row)

    def makeKeyDict(self, row):
        if row not in self._droppedData.keys():
            self._droppedData[row] = {
                'data': [],
                'significance level': 0,
                'name': ''
            }

    def dictDataIsAvailable(self, row):
        if row in self._droppedData.keys() and (len(self._droppedData[row]['data']) < self.__countDim):
            return True
        return False

    def dictDataIsFull(self, row):
        if row in self._droppedData.keys() and (len(self._droppedData[row]['data']) == self.__countDim):
            return True
        return False

    def getData(self, source):
        return [float(source.item(source.currentRow(), column).text())
                for column in range(source.columnCount())
                if source.item(source.currentRow(), column)]

    def updateFolder(self, item, key):
        item.setIcon(0, QIcon('./Icons/FullFolderIcon.png'))
        # add child nodes with significance level
        alpha = QTreeWidgetItem(["α: {}".format(self._droppedData[key]['significance level'])])
        N = QTreeWidgetItem(["N: {}".format(len(self._droppedData[key]['data'][0]))])
        item.addChild(alpha)
        item.addChild(N)

    def setTextItem(self, item, key):
        item.setText(0, self._droppedData[key]['name'])

    def contextMenuEvent(self, event):
        clickOn = event.pos()
        currentItem = self.itemAt(clickOn)
        row = self.indexFromItem(currentItem, 0).row()
        contextMenu = QMenu(self)
        # add actions
        addFolderAction = contextMenu.addAction('Створити папку')
        removeFolderAction = contextMenu.addAction('Видалити папку')
        contextMenu.addSeparator()
        overWrite = contextMenu.addAction('Перерахувати')
        contextMenu.addSeparator()

        changeSignificanceLevel = contextMenu.addAction('Змінити степінь довіри')
        removeAbnormalVal = contextMenu.addAction('Видалити аномальні спостереження')
        regressionAnalysis = contextMenu.addMenu('Регресійний аналіз')
        linearRegression = regressionAnalysis.addMenu('Лінійна регресія')
        linearRegressionMNK = linearRegression.addAction('За МНК')
        linearRegressionTail = linearRegression.addAction('За методом Тейла')
        paraboloidRegression = regressionAnalysis.addAction('Відтворити параболічну регресію')
        quasilinearRegression = regressionAnalysis.addAction('Відтворити квазілінійну регресію')
        correlationAnalysis = contextMenu.addMenu('Кореляційний аналіз')
        linearCorrelation = correlationAnalysis.addAction('Лінійна кореляція')
        rangCorrelation = correlationAnalysis.addAction('Рангова кореляція')
        combinationsTablesMenu = correlationAnalysis.addMenu('Таблиці сполучень')
        combinationsTable2x2 = combinationsTablesMenu.addAction('2x2')
        combinationsTableMxN = combinationsTablesMenu.addAction('mxn')

        if (row >= 0) and self.dictDataIsFull(row):
            self.showOrDisableActions(overWrite, changeSignificanceLevel, removeAbnormalVal,
                                      correlationAnalysis, combinationsTablesMenu, regressionAnalysis, flag=True)
        else:
            self.showOrDisableActions(overWrite, changeSignificanceLevel, removeAbnormalVal,
                                      correlationAnalysis, combinationsTablesMenu, regressionAnalysis, flag=False)
        # capture click on context menu
        action = contextMenu.exec_(self.mapToGlobal(clickOn))
        if action == addFolderAction:
            self.displayFolder()
        elif action == removeFolderAction:
            self.removeFolder(currentItem, row)
        elif action == removeAbnormalVal:
            self.removeAbnormalData(currentItem, row)
        elif action == overWrite:
            self.overWrite()
        elif action == changeSignificanceLevel:
            self.changeSignificanceLevel(currentItem, row)
        elif action == linearCorrelation:
            self.doLinearCorrelation(row)
        elif action == rangCorrelation:
            self.doRangCorrelation(row)
        elif action == combinationsTable2x2:
            self.doCombinationsTable2x2(row)
        elif action == combinationsTableMxN:
            self.doCombinationsTableMxN(row)
        elif action == linearRegressionMNK:
            self.doLinearRegressionMNK(row)
        elif action == linearRegressionTail:
            self.doLinearRegressionTail(row)
        elif action == paraboloidRegression:
            self.doParaboloidRegression(row)
        elif action == quasilinearRegression:
            self.doQuasilinearRegression(row)

    def doLinearRegressionMNK(self, rowItem):
        x, y = self._droppedData[rowItem]['data']
        alpha = self._droppedData[rowItem]['significance level']
        Dim2.doLinearMNK(x, y, alpha, self.window)

    def doLinearRegressionTail(self, rowItem):
        x, y = self._droppedData[rowItem]['data']
        alpha = self._droppedData[rowItem]['significance level']
        Dim2.doLinearTail(x, y, alpha, self.window)

    def getTextX0(self):
        text, okPressed = QInputDialog.getText(self, "Задати прогнозне значення","x0:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return float(text)

    def doParaboloidRegression(self, rowItem):
        x, y = self._droppedData[rowItem]['data']
        alpha = self._droppedData[rowItem]['significance level']
        Dim2.doParaboloidRegression(x, y, alpha, self.window)

    def showOrDisableActions(self, *args, flag):
        for action in args:
            action.setEnabled(flag)

    def displayFolder(self):
        parent = QTreeWidgetItem(self)
        parent.setIcon(0, QIcon('./Icons/EmptyFolderIcon.ico'))

    def removeAbnormalData(self, treeItem, rowItem):
        alpha = self._droppedData[rowItem]['significance level']
        x, y = self._droppedData[rowItem]['data']
        with self.wait_cursor():
            data = removeAbnormal(alpha, x, y)
            N = len(data[0])
            self._droppedData[rowItem]['data'] = list(data)
            self.showAnalysis(data, alpha)
            treeItem.child(1).setText(0, "N: {}".format(N))

    def changeSignificanceLevel(self, treeItem, rowItem):
        significanceLevel = treeItem.child(0)
        newLevel = self.getDouble()
        if newLevel:
            self._droppedData[rowItem]['significance level'] = newLevel
            significanceLevel.setText(0, "α: {}".format(newLevel))

    def getDouble(self):
        d, okPressed = QInputDialog.getDouble(self, "Змінити степінь довіри", "Рівень:", 0.05, 0, 1)
        if okPressed:
            return d

    def overWrite(self):
        self.onItemDoubleClicked()

    def removeFolder(self, treeItem, rowItem):
        if treeItem:
            del self._droppedData[rowItem]
            sip.delete(treeItem)
        else:
            QMessageBox.warning(self, "Warning!", "There is no folder.")

    def onItemDoubleClicked(self):
        # get data and do analysis  when user double click on item
        item = self.selectedItems()[0]
        row = self.indexFromItem(item, 0).row()

        if row in self._droppedData.keys():
            data = self._droppedData[row]['data']
            signLvl = self._droppedData[row]['significance level']

            if len(data[0]) == len(data[1]):
                self.showAnalysis(data, signLvl)
            else:
                QMessageBox.warning(self, "Warning!", "Дані не одного розміру.")

    def showAnalysis(self, data, signLvl):
        with self.wait_cursor():
            dim2 = Dim2(self.window, data, signLvl)
            try:
                dim2.enableWidgets()
                dim2.openTab()
                dim2.drawGraphics()
                dim2.makeProtocol()
            except ValueError:
                QMessageBox.warning(self, "Warning!", "Невірні дані.")
            del dim2

    def doLinearCorrelation(self, rowItem):
        x, y = self._droppedData[rowItem]['data']
        alpha = self._droppedData[rowItem]['significance level']
        with self.wait_cursor():
            try:
                showLinearCorrelation(x, y, alpha, self.window.textBrowserProtocol)
            except ValueError:
                QMessageBox.warning(self, "Warning!", "Невірні дані.")

    def doRangCorrelation(self, rowItem):
        x, y = self._droppedData[rowItem]['data']
        alpha = self._droppedData[rowItem]['significance level']
        with self.wait_cursor():
            try:
                showRangCorrelation(x, y, alpha, self.window.textBrowserProtocol)
            except OverflowError:
                QMessageBox.warning(self, "Warning!", "Невірні дані.")

    def doCombinationsTable2x2(self, rowItem):
        x, y = self._droppedData[rowItem]['data']
        alpha = self._droppedData[rowItem]['significance level']
        with self.wait_cursor():
            showCombinationsTable2x2(x, y, self.window.textBrowserProtocol)
            try:
                showCombinationsTable2x2Indexes(x, y, alpha, self.window.textBrowserProtocol)
            except ZeroDivisionError:
                QMessageBox.warning(self, "Warning!", "Невірні дані.")

    def doCombinationsTableMxN(self, rowItem):
        x, y = self._droppedData[rowItem]['data']
        alpha = self._droppedData[rowItem]['significance level']
        with self.wait_cursor():
            showCombinationsTableMxN(x, y, self.window.textBrowserProtocol)
            try:
                showCombinationsTableMxNIndexes(x, y, alpha, self.window.textBrowserProtocol)
            except Exception:
                QMessageBox.warning(self, "Warning!", "Невірні дані.")
