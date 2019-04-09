import numpy as np


def getCharacteristics(x: list, y: list, N: int):
    characteristics = {
        "Середнє арифметичне по Х": np.mean(x),
        "Середнє арифметичне по У": np.mean(y),
        "Середнє арифметичне по ХУ": meanXY(x, y, N),
        "Середнє квадратичне відхилення по Х": np.std(x),
        "Середнє квадратичне відхилення по У": np.std(y),
    }

    return characteristics


def meanXY(x: list, y: list, N: int) -> float:
    return sum([x[i] * y[i] for i in range(N)]) / N

