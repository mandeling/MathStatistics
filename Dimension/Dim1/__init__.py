import pandas as pd
import numpy as np

from Dimension.Dim1.PointAndIntervalCharacteristics import getCharacteristics
from Dimension.Dim1.Graphs import *
from Dimension.Dim1.OperationOnData import countOptimalBins
from Dimension.Dim1.ProtocolRender import showProtocol


class Dim1(object):

    def __init__(self, window, data, alpha):
        self.window = window
        self.data = pd.Series(data)
        self.alpha = alpha
        self.N = len(self)
        self.countOptimalBins = countOptimalBins(self.N)
        self.characteristics = getCharacteristics(data, alpha, self.N)

    def __len__(self):
        return len(self.data)

    def openTab(self):
        if self.window.tabWidgetDataAnalysis.currentIndex() != 0:
            self.window.tabWidgetDataAnalysis.setCurrentIndex(0)

    def enableWidgets(self):
        self.window.tabWidgetDataAnalysis.setEnabled(True)
        self.window.tabWidgetPrimaryStatAnalysis.setEnabled(True)
        self.window.textBrowserProtocol.setEnabled(True)

    def disableWidgets(self):
        self.window.tabWidgetDataAnalysis.setDisabled(True)
        self.window.tabWidgetPrimaryStatAnalysis.setDisabled(True)
        self.window.textBrowserProtocol.setDisabled(True)

    def createGraphics(self):
        hist(self.data, self.countOptimalBins, self.window.histWidget1D.canvas.ax)
        densityFunction(self.data, self.countOptimalBins, self.window.densityWidget1D.canvas.ax)
        probabilityGrid(self.data, self.window.probGridWidget1D.canvas.ax)

    def clearAxes(self):
        clearAxes(self.window.histWidget1D.canvas.ax,
                  self.window.probGridWidget1D.canvas.ax,
                  self.window.densityWidget1D.canvas.ax)

    def drawGraphics(self):
        self.clearAxes()
        self.createGraphics()

        self.window.histWidget1D.canvas.draw()
        self.window.densityWidget1D.canvas.draw()
        self.window.probGridWidget1D.canvas.draw()

    def makeProtocol(self):
        showProtocol(self.characteristics, self.window.textBrowserProtocol)
