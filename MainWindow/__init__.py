from PreviewDialog import PreviewDialog
from MainWindow.UI.MainWindow import Ui_MainWindow
from CustomWidgets.Tree.Tree1Dim import CustomTree1Dim
from CustomWidgets.Tree.Tree2Dim import CustomTree2Dim
from CustomWidgets.Table.TableShowData import TableData
from MatplotWidget import MplWidget

from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # add widgets into Ui
        self.tree1Dim = CustomTree1Dim(self)
        self.tree2Dim = CustomTree2Dim(self)
        self.tableDataBase = TableData()

        # create plots
        self.histWidget1D = MplWidget()
        self.densityWidget1D = MplWidget()
        self.probGridWidget1D = MplWidget()
        self.histWidget2D = MplWidget()
        self.correlationField2D = MplWidget()

        # create modal file dialog window
        self.fileDialogWindow = PreviewDialog()

        self.initUI()

    def initUI(self):
        # add widgets into layouts
        self.horizontalLayoutTree1Dim.addWidget(self.tree1Dim)
        self.horizontalLayoutTree2Dim.addWidget(self.tree2Dim)
        self.horizontalLayoutTableDataBase.addWidget(self.tableDataBase)

        # actions
        self.actionOpen.triggered.connect(self.fileDialogWindow.show)

        # add to layouts
        self.gridLayoutHistogram.addWidget(self.histWidget1D)
        self.gridLayoutDensityFunction.addWidget(self.densityWidget1D)
        self.gridLayoutProbabilityGrid.addWidget(self.probGridWidget1D)
        self.gridLayoutHistOfRelativeFrequencies.addWidget(self.histWidget2D)
        self.gridLayoutCorreLationField.addWidget(self.correlationField2D)
