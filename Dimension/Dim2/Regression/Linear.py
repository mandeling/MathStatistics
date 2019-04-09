from Dimension.Dim2.CorrelationCharacteristics import corrCoefficientEstimate, meanXY, countOptimalBins
import numpy as np
from math import sqrt
from scipy import stats


def getMNKParams(x: list, y: list):
    N = len(x)
    meanX = np.mean(x)
    meanY = np.mean(y)
    meanxy = meanXY(x, y, N)
    sigmaX = np.std(x)
    sigmaY = np.std(y)

    estimateCorrCoefficient = corrCoefficientEstimate(meanX, meanY, meanxy, sigmaX, sigmaY, N)
    b_ = estimateCorrCoefficient * (sigmaX / sigmaY)
    a_ = meanY - b_ * meanX
    sKvadrZal = (1 / (N - 2)) * sum([y[l] - a_ - b_ * x[l] for l in range(N)])

    return a_, b_, sKvadrZal


def getTailParams(x: list, y: list, alpha: float):
    N = len(x)
    k = int(alpha * N)

    b_ = MED(sorted([((y[j] - y[i]) / (x[j] - x[i])) for i in range(N - 1) for j in range(i + 1, N) if x[i] != x[j]]),
             N, k)
    a_ = MED(sorted([(y[l] - (b_ * x[l])) for l in range(N)]), N, k)

    return a_, b_


def MED(data, N, k):
    if N % 2 == 1:
        return data[k + 1]
    return (data[k] + data[k + 1]) / 2


def getCharacteristics(x, y, a_, b_, alpha):
    characteristics = dict()
    N = len(x)
    meanX = np.mean(x)
    meanY = np.mean(y)
    meanxy = meanXY(x, y, N)
    sigmaX = np.std(x)
    sigmaY = np.std(y)
    rxy_ = corrCoefficientEstimate(meanX, meanY, meanxy, sigmaX, sigmaY, N)

    determination = rxy_ ** 2 * 100
    Seps = sigmaY * sqrt((1 - rxy_) * ((N - 1) / (N - 2)))
    Sa = Seps * sqrt((1 / N) + (meanX ** 2) / (sigmaX ** 2) / (N - 1))
    Sb = Seps / (sigmaX * sqrt(N - 1))
    tSa = (a_ - meanxy) / Sa
    tSb = (b_ - sigmaY) / Sb
    lowerA, upperA, lowerB, upperB = getIntervalParams(a_, b_, Sa, Sb, alpha, N)
    fStat = (Seps ** 2) / (sigmaY ** 2)

    characteristics['point'] = {
        "Коефіцієнт детермінації": determination,
        "t-статистика, точності оцінки параметру a": tSa,
        "t-статистика, точності оцінки параметру b": tSb,
        "Оцінка відхилень окремих значень спостережень від лінії регресії": Seps,
        "f-статистика перевірки адекватності відтвореної моделі регресії": fStat
    }

    characteristics['tests'] = {
        "Рівність оцінки а значенню параметру а_": getTtestResult(tSa, N, alpha),
        "Рівність оцінки b значенню параметру b_": getTtestResult(tSb, N, alpha),
        "Гіпотеза про вигляд регресійної залежності": getFStatRest(fStat, N, alpha)
    }

    characteristics['interval'] = {
        "Інтервальне оцінювання параметру а": [lowerA, meanX, upperA],
        "Інтервальне оцінювання параметру b": [lowerB, sigmaY, upperB],
    }

    return characteristics


def getFStatRest(fStat, N, alpha):
    fppf = stats.f.ppf(1 - alpha, N - 1, N - 3)
    if fStat <= fppf:
        return "Значущий"
    return "Не значущий"


def rsquared(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return r_value ** 2


def getIntervalParams(a_, b_, Sa, Sb, alpha, N):
    lowerA = a_ - stats.t.ppf((1 - alpha), N - 2) * Sa
    upperA = a_ + stats.t.ppf((1 - alpha), N - 2) * Sa

    lowerB = b_ - stats.t.ppf((1 - alpha), N - 2) * Sb
    upperB = b_ + stats.t.ppf((1 - alpha), N - 2) * Sb

    return lowerA, upperA, lowerB, upperB


def getTtestResult(tSb, alpha, N):
    tppf = stats.t.ppf((1 - alpha), N - 2)
    if abs(tSb) > tppf:
        return "Значущий"
    return "Не значущий"


def getTollerantBorderIntervalMNK(x, y, alpha):
    N = len(x)
    meanX = np.mean(x)
    meanY = np.mean(y)
    meanxy = meanXY(x, y, N)
    sigmaX = np.std(x)
    sigmaY = np.std(y)
    rxy_ = corrCoefficientEstimate(meanX, meanY, meanxy, sigmaX, sigmaY, N)
    Seps = np.std(y) * sqrt((1 - rxy_) * ((N - 1) / (N - 2)))

    aM_, bM_, _ = getMNKParams(x, y)
    x = np.array(x)

    yQM_ = [aM_ + bM_ * i for i in x]

    lowerM = np.array(yQM_) - stats.t.ppf((1 - alpha), N - 2) * Seps
    upperM = np.array(yQM_) + stats.t.ppf((1 - alpha), N - 2) * Seps

    return lowerM, upperM


def getTollerantBorderIntervalTail(x, y, alpha):
    N = len(x)
    meanX = np.mean(x)
    meanY = np.mean(y)
    meanxy = meanXY(x, y, N)
    sigmaX = np.std(x)
    sigmaY = np.std(y)
    rxy_ = corrCoefficientEstimate(meanX, meanY, meanxy, sigmaX, sigmaY, N)
    Seps = np.std(y) * sqrt((1 - rxy_) * ((N - 1) / (N - 2)))

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    aT_ = float(slope)
    bT_ = float(intercept)
    yQT_ = [aT_ + bT_ * i for i in x]
    lowerT = np.array(yQT_) - stats.t.ppf((1 - alpha), N - 2) * Seps
    upperT = np.array(yQT_) + stats.t.ppf((1 - alpha), N - 2) * Seps

    return lowerT, upperT
