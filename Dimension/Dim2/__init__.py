from Dimension.Dim2.Characteristics import getCharacteristics
from Dimension.Dim2.ProtocolRender import showPointsCharacteristics, protocolLinearMNK, protocolLinearTail
from Dimension.Dim2.Graphs import *
from Dimension.Dim1.OperationOnData import countOptimalBins


class Dim2(object):

    def __init__(self, window, data, alpha):
        self.window = window
        self.x, self.y = data
        self.alpha = alpha
        self.N = len(self)

        self.pointCharacteristics = getCharacteristics(self.x, self.y, self.N)

    def __len__(self):
        return len(self.x)

    def openTab(self):
        if self.window.tabWidgetDataAnalysis.currentIndex() != 1:
            self.window.tabWidgetDataAnalysis.setCurrentIndex(1)

    def enableWidgets(self):
        self.window.tabWidgetDataAnalysis.setEnabled(True)
        self.window.textBrowserProtocol.setEnabled(True)

    def disableWidgets(self):
        self.window.tabWidgetDataAnalysis.setDisabled(True)
        self.window.setDisabled(True)

    def makeProtocol(self):
        showPointsCharacteristics(self.pointCharacteristics, self.window.textBrowserProtocol)

    def createGraphics(self):
        hist(self.x, self.y, countOptimalBins(len(self.x)), countOptimalBins(len(self.y)),
             self.window.histWidget2D.canvas)
        correlationField(self.x, self.y, self.window.correlationField2D.canvas.ax)

    def clearAxes(self):
        clearAxes(self.window.histWidget2D.canvas.fig,
                  self.window.correlationField2D.canvas.ax)

    @staticmethod
    def doLinearMNK(x, y, alpha, window):
        drawLinearRegressionByMNK(x, y, alpha, window.correlationField2D.canvas.ax)
        protocolLinearMNK(x, y, alpha, window.textBrowserProtocol)
        window.correlationField2D.canvas.draw()

    @staticmethod
    def doLinearTail(x, y, alpha, window):
        drawLinearRegressionByTail(x, y, alpha, window.correlationField2D.canvas.ax)
        protocolLinearTail(x, y, alpha, window.textBrowserProtocol)
        window.correlationField2D.canvas.draw()

    @staticmethod
    def doParaboloidRegression(x, y, alpha, window):
        drawParaboloidRegression(x, y, alpha, window.correlationField2D.canvas.ax)
        window.correlationField2D.canvas.draw()

    def drawGraphics(self):
        self.clearAxes()
        self.createGraphics()

        self.window.histWidget2D.canvas.draw()
        self.window.correlationField2D.canvas.draw()
