from PyQt5.QtWidgets import QTreeWidget, QMenu, QTreeWidgetItem, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from Dimension.Dim1 import Dim1


class CustomTree1Dim(QTreeWidget):

    def __init__(self, mainWin):
        QTreeWidget.__init__(self)
        self.window = mainWin
        self.__countDim = 1
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

        if (row >= 0) and self.dictDataIsFull(row):
            overWrite.setEnabled(True)
            changeSignificanceLevel.setEnabled(True)
        else:
            overWrite.setEnabled(False)
            changeSignificanceLevel.setEnabled(False)

        # capture click on context menu
        action = contextMenu.exec_(self.mapToGlobal(clickOn))
        if action == addFolderAction:
            self.displayFolder()
        elif action == removeFolderAction:
            self.removeFolder(currentItem, row)
        elif action == overWrite:
            self.rebuild(row)
        elif action == changeSignificanceLevel:
            self.changeSignificanceLevel(currentItem, row)

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

    def rebuild(self, rowItem):
        print(self._droppedData[rowItem]['data'])
        print(self._droppedData[rowItem]['significance level'])

    def displayFolder(self):
        parent = QTreeWidgetItem(self)
        parent.setIcon(0, QIcon('./Icons/EmptyFolderIcon.ico'))

    def removeFolder(self, treeItem, rowItem):
        from PyQt5 import sip

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
            data = self._droppedData[row]['data'][0]
            signLvl = self._droppedData[row]['significance level']

            dim1 = Dim1(self.window, data, signLvl)
            dim1.enableWidgets()
            dim1.openTab()
            dim1.makeProtocol()
            dim1.drawGraphics()
