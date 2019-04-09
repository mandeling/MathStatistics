from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QMenu, QHeaderView


class TableData(QTableWidget):

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.droppedData = {}

        self.init()

    def init(self):
        # set drag and drop action
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def dragMoveEvent(self, event):
        if event.source() is not self:
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.source():
            event.acceptProposedAction()
        else:
            super(TableData, self).dragEnterEvent(event)

    def dropEvent(self, event):
        if event.source() is not self:
            source = event.source()
            selectedColumns = source.selectionModel().selectedColumns()
            selectedRows = source.selectionModel().selectedIndexes()
            columnCount = len(selectedColumns)
            rowCount = source.rowCount()
            columnCount, rowCount = rowCount, columnCount

            self.setSize(rowCount, columnCount)
            self.updateVerticalHeaderContext(rowCount, columnCount)
            self.setData(rowCount, selectedRows)

    def setSize(self, rowCount, columnCount):
        self.setRowCount(self.rowCount() + rowCount)
        if columnCount > self.columnCount():
            self.setColumnCount(columnCount)

    def updateVerticalHeaderContext(self, addedRowCount, columnCount):
        rowCount = self.rowCount()
        for i in range(addedRowCount + 1):
            currentRow = rowCount - i
            self.setVerticalHeaderItem(currentRow, QTableWidgetItem("X{0}, N={1}".format(currentRow, columnCount)))

    def setData(self, addedRowCount, selectedRows):
        rowCount = self.rowCount()
        for i, row in enumerate(selectedRows):
            for j in range(addedRowCount + 1):
                currentRow = rowCount - j
                self.setItem(currentRow, i, QTableWidgetItem(row.data().replace(",", ".")))

    def contextMenuEvent(self, event):
        clickOn = event.pos()
        indexRow = self.indexAt(clickOn).row()
        contextMenu = QMenu(self)

        # add actions
        generateSample = contextMenu.addAction('Згенерувати вибірку')
        removeAbnormalData = contextMenu.addAction('Видалити аномальні спостереження')
        standardizeData = contextMenu.addAction('Стандартизувати дані')
        logData = contextMenu.addAction('Логарифмувати дані')
        shiftData = contextMenu.addAction('Зсунути дані')

        if indexRow >= 0:
            removeAbnormalData.setEnabled(True)
            standardizeData.setEnabled(True)
            logData.setEnabled(True)
            shiftData.setEnabled(True)
        else:
            removeAbnormalData.setEnabled(False)
            standardizeData.setEnabled(False)
            logData.setEnabled(False)
            shiftData.setEnabled(False)

        # capture click on context menu
        action = contextMenu.exec_(self.mapToGlobal(clickOn))
        if action == removeAbnormalData:
            self.removeAbnormalData(indexRow)
        elif action == standardizeData:
            self.standardizeData(indexRow)
        elif action == logData:
            self.logData(indexRow)
        elif action == shiftData:
            self.shiftData(indexRow)
        elif action == generateSample:
            self.generateSample()

    def generateSample(self):
        pass

    def removeAbnormalData(self, row):
        print(row)

    def standardizeData(self, row):
        pass

    def logData(self, row):
        pass

    def shiftData(self, row):
        pass
