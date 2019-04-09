import numpy as np
from Dimension.Dim1.OperationOnData import countOptimalBins


def removeAbnormal(alpha: float, x: list, y: list):
    N = len(x)
    newX = []
    newY = []
    M_x = countOptimalBins(len(x))
    M_y = countOptimalBins(len(y))
    P = np.zeros((M_x, M_y))
    n = np.zeros((M_x, M_y))
    delta_x = (max(x) - min(x)) / (M_x - 1)
    delta_y = (max(y) - min(y)) / (M_y - 1)

    for i in range(N):
        index_x = int((x[i] - min(x)) / delta_x)
        if index_x > M_x:
            index_x -= 1
        index_y = int((y[i] - min(y)) / delta_y)
        if index_y > M_y:
            index_y -= 1
        n[index_x][index_y] += 1

    for l in range(M_x):
        for k in range(M_y):
            P[l][k] += (n[l][k] / N)

    for i in range(N):
        index_x = int((x[i] - min(x)) / delta_x)
        if index_x > M_x:
            index_x -= 1
        index_y = int((y[i] - min(y)) / delta_y)
        if index_y > M_y:
            index_y -= 1
        if P[index_x][index_y] > alpha:
            newX.append(x[i])
            newY.append(y[i])

    result = list([newX, newY])
    return result

