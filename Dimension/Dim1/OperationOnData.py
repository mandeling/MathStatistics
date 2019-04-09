import numpy as np
import pandas as pd


def countOptimalBins(N):
    if N < 100:
        if N % 2 == 0:
            num_b = np.sqrt(N) - 1
        else:
            num_b = np.sqrt(N)
    else:
        if N % 2 == 0:
            num_b = np.cbrt(N) - 1
        else:
            num_b = np.cbrt(N)
    return int(np.floor(num_b))


def logData(data):
    return np.log(data)


def standardizeData(data):
    x = pd.Series(data)
    if isinstance(x, pd.Series):
        mean = x.mean()
        sigma = x.std()
        if sigma != 0:
            data = (data - mean) / sigma
    return data


def delAbnormalValues(data):
    data = np.array(data)
    x = pd.Series(data)
    if isinstance(x, pd.Series):
        skew = x.skew()
        kurt = x.kurt()
        t1 = 2 + 0.2 * np.log10(0.04 * len(x))
        t2 = np.sqrt(19 * np.sqrt(kurt + 2) + 1)
        if skew < -0.2:
            a = x.mean() - t2 * x.std()
            b = x.mean() + t1 * x.std()
        elif skew > 0.2:
            a = x.mean() - t1 * x.std()
            b = x.mean() + t2 * x.std()
        elif np.abs(skew) < 0.2:
            a = x.mean() - t1 * x.std()
            b = x.mean() + t1 * x.std()

        data = data[data > a]
        data = data[data < b]
        return data
