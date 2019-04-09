from Dimension.Dim1.OperationOnData import countOptimalBins
from Dimension.Dim2.Characteristics import meanXY
import numpy as np
from math import sqrt
from scipy import stats


def getLinearCorrelationCharacteristics(x: list, y: list, alpha: float):
    characteristics = dict()
    N = len(x)
    meanX = np.mean(x)
    meanY = np.mean(y)
    meanxy = meanXY(x, y, N)
    countBinsX = countOptimalBins(N)
    countBinsXY = (countBinsX * countBinsX)

    # коеф. кореляції
    corrCoefficient = pairCorrelationCoefficient(x, y, meanX, meanY, N)
    estimateCorrCoefficient = corrCoefficientEstimate(meanX, meanY, meanxy, np.std(x), np.std(y), N)
    uppCorrCoef, lowCorrCoef = intervalCorrCoefficient(estimateCorrCoefficient, alpha, N)
    tStatCorr = tStatistic(estimateCorrCoefficient, N)

    # коеф кор. відношення
    corrRatio = correlationRatio(x, y)
    fStat = fStatCorrRatio(corrRatio, N, countBinsX)
    upperRatio, lowerRatio = intervalCorrRatio(corrRatio, N, countBinsX, alpha)

    characteristics['point'] = {
        "t-статистика коефіцієнту кореляції": tStatCorr,
        "f-статистика коефіцієнту кореляційного відношення": fStat
    }

    characteristics['tests'] = {
        "За змінною У при фіксованій Х": getPearsonResult(stats.chisquare(y, ddof=countBinsXY - 1)[1], alpha,
                                                          countBinsXY - 1),
        "За змінною Х у разі фіксованої У": getPearsonResult(stats.chisquare(x, ddof=countBinsXY - 1)[1], alpha,
                                                             countBinsXY - 1),
        "Одночасно за змінними Х та У": getPearsonResult(stats.chisquare(x, y, ddof=countBinsXY - 2)[1], alpha,
                                                         countBinsXY - 2),
        "Коефіцієнт кореляції": validityCheckCorrCoefficient(tStatCorr, alpha, countBinsXY),
        "Коефіцієнт кореляційного відношення": validityCheckCorrRatio(fStat, countBinsX, alpha, N),
    }

    characteristics['interval'] = {
        "Коефіцієнт кореляції": [lowCorrCoef, corrCoefficient, uppCorrCoef],
        "Коефіцієнт кореляційного відношення": [lowerRatio, corrRatio, upperRatio]
    }

    return characteristics


def pairCorrelationCoefficient(x, y, meanX: np.ndarray, meanY: np.ndarray, N: int) -> float:
    return np.mean([(x[i] - meanX) * (y[i] - meanY) for i in range(N)]) \
           / sqrt(np.var(x) * np.var(y))


def corrCoefficientEstimate(meanX: np.ndarray, meanY: np.ndarray, mXY: float, stdX: np.ndarray,
                            stdY: np.ndarray, N: int) -> float:
    return N / (N - 1) * (mXY - meanX * meanY) / (stdX * stdY)


def tStatistic(estimate: float, N: int) -> float:
    return (estimate * sqrt(N - 2)) / sqrt(1 - estimate ** 2)


def intervalCorrCoefficient(corrEstimate: float, alpha: float, N: int) -> tuple:
    tmpEst = corrEstimate + (corrEstimate * (1 - corrEstimate ** 2)) / (2 * N)
    secTmpEst = stats.norm.ppf((1 - alpha) / 2) * (1 - corrEstimate ** 2) / sqrt(N - 1)

    return tmpEst - secTmpEst, tmpEst + secTmpEst


def intervalCorrRatio(ratio: float, N: int, k: int, alpha: float):
    mu1 = ((k - 1 + N * ratio) ** 2) / (k - 1 + 2 * N * ratio)
    mu2 = N - k
    lower = ((N - k) * ratio) / (N * (1 - ratio) * stats.f.ppf(alpha, mu1, mu2)) - ((k - 1) / N)
    upper = ((N - k) * ratio) / (N * (1 - ratio) * stats.f.ppf(1 - alpha, mu1, mu2)) - ((k - 1) / N)

    return lower, upper


def fStatCorrRatio(ratioEstimate: float, N: int, k: int):
    return (ratioEstimate / (1 - ratioEstimate)) * ((N - k) / (k - 1))


def correlationRatio(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return r_value


def getPearsonResult(pvalue: np.float, alpha: float, bins: int) -> str:
    chi2ppf = stats.chi2.ppf(1 - alpha, bins - 1)
    if pvalue <= chi2ppf:
        return "Значущий"
    return "Не значущий"


def validityCheckCorrCoefficient(tValue: float, alpha: float, bins: int) -> str:
    tppf = stats.t.ppf((1 - alpha), bins - 2)
    if abs(tValue) > tppf:
        return "Значущий"
    return "Не значущий"


def validityCheckCorrRatio(fValue: float, k: int, alpha: float, N: int):
    fppf = stats.f.ppf(1 - alpha, k - 1, N - k)
    if fValue > fppf:
        return "Значущий"
    return "Не значущий"


def getRangCorrelationCharacteristics(x: list, y: list, alpha: float):
    characteristics = dict()
    N = len(x)
    sperman = spermanCorrCoef(x, y)
    kendall = kendallCorrCoef(x, y)
    tStatS = tStatSperman(sperman, N)
    uStatK = uStatKendall(kendall, N)
    lowerS, upperS = intervalSperman(sperman, N, alpha)
    lowerK, upperK = intervalKendall(kendall, alpha, N)

    characteristics['point'] = {
        "t-статистика рангового коефіцієнту Спірмана": tStatS if tStatS else "-",
        "u-статистика рангового коефіцієнту Кендалла": uStatK
    }
    characteristics['interval'] = {
        'Ранговий коефіцієнт Спірмана': [lowerS, sperman, upperS],
        'Ранговий коефіцієнт Кендалла': [lowerK, kendall, upperK]
    }
    characteristics['tests'] = {
        'Ранговий коефіцієнт Спірмана': getSpermanResult(tStatS, alpha, N) if tStatS else "-",
        'Ранговий коефіцієнт Кендалла': getKendallResult(uStatK, N)
    }

    return characteristics


def spermanCorrCoef(x, y):
    return stats.spearmanr(x, y)[0]


def kendallCorrCoef(x, y):
    return stats.kendalltau(x, y)[0]


def tStatSperman(spermanStat, N):
    if sqrt(1 - spermanStat ** 2) != 0:
        return (spermanStat * sqrt(N - 2)) / (sqrt(1 - spermanStat ** 2))
    return None


def getSpermanResult(tStatSperman, alpha, N):
    tppf = stats.t.ppf((1 - alpha), N - 2)
    if abs(tStatSperman) < tppf:
        return "Значущий"
    return "Не значущий"


def uStatKendall(kendallStat, N):
    return ((3 * kendallStat) / (sqrt(2 * (2 * N + 5)))) * sqrt(N * (N - 1))


def getKendallResult(uStatKendall, alpha):
    uppf = stats.norm.ppf(1 - alpha / 2)
    if abs(uStatKendall) > uppf:
        return "Значущий"
    return "Не значущий"


def intervalSperman(spearmanStat, N, alpha):
    sigmaS = sqrt((1 - spearmanStat ** 2) / (N - 2))
    tppf = stats.t.ppf((1 - alpha), N - 2)
    return spearmanStat - sigmaS * tppf, spearmanStat + sigmaS * tppf


def intervalKendall(kendallStat, alpha, N):
    sigmaK = sqrt((4 * N + 10) / (9 * (N ** 2 - N)))
    uppf = stats.norm.ppf(1 - alpha / 2)
    return kendallStat - sigmaK * uppf, kendallStat + sigmaK * uppf


def getCombinationTable2x2(x, y):
    xMean = np.mean(x)
    yMean = np.mean(y)
    n00 = 0
    n01 = 0
    n10 = 0
    n11 = 0
    for i in range(len(x)):
        if x[i] >= xMean and y[i] >= yMean:
            n11 += 1
        if x[i] >= xMean and y[i] < yMean:
            n01 += 1
        if x[i] < xMean and y[i] >= yMean:
            n10 += 1
        if x[i] < xMean and y[i] < yMean:
            n00 += 1
    m0 = n00 + n10
    m1 = n01 + n11
    n0 = n00 + n01
    n1 = n10 + n11

    return [n00, n01, n10, n11], [m0, m1], [n0, n1], n0 + n1


def getCombinationTable2x2Indexes(alpha, table, mi, ni, N):
    characteristics = dict()
    n00, n01, n10, n11 = table
    n0, n1 = ni
    m0, m1 = mi

    fehner = fehnerIndex(n00, n01, n10, n11)
    coefPhi = phiCoefficient(n00, n01, n10, n11, n0, n1, m0, m1)
    qUll, yUll = ullCoef(n00, n01, n10, n11)

    characteristics['point'] = {
        "Індекс Фехнера": fehner,
        "Коефіцієнт сполучень Фі": coefPhi,
        "Коефіцієнт сполучень Юлла Q: ": qUll,
        "Коефіцієнт сполучень Юлла Y: ": yUll
    }

    characteristics['tests'] = {
        "Індекс Фехнера": getFehnerResult(fehner),
        "Коефіцієнт сполучень Фі": gePhiCoefResult(coefPhi, N, alpha, n00, n01, n10, n11, n0, n1, m0, m1),
        "Коефіцієнт сполучень Юлла Q: ": getUllQResult(qUll, alpha, n00, n01, n10, n11),
        "Коефіцієнт сполучень Юлла Y": getUllQResult(yUll, alpha, n00, n01, n10, n11)
    }

    return characteristics


def fehnerIndex(N00, N11, N01, N10):
    return (N00 + N11 - N10 - N01) / (N00 + N11 + N10 + N01)


def getFehnerResult(indexFehner):
    if indexFehner > 0:
        return "Додатна кореляція"
    elif 0 <= indexFehner <= 0.05:
        return "Зв'язок відсутній"
    else:
        return "Від'ємна кореляція"


def phiCoefficient(N00, N11, N01, N10, N0, N1, M0, M1):
    return (N00 * N11 - N01 * N10) / sqrt(N0 * N1 * M0 * M1)


def gePhiCoefResult(phiCoef, N, alpha, N00, N11, N01, N10, N0, N1, M0, M1):
    if N < 40:
        chi2 = N * ((N00 * N11 - N01 * N10 - 0.5) ** 2) / (N0 * N1 * M0 * M1)
    else:
        chi2 = N * (phiCoef ** 2)

    chi2ppf = stats.chi2.ppf(1 - alpha, 1)
    if chi2 >= chi2ppf:
        return "Значущий"
    return "Не значущий"


def ullCoef(N00, N11, N01, N10):
    q = (N00 * N11 - N01 * N10) / (N00 * N11 + N01 * N10)
    y = (sqrt(N00 * N11) - sqrt(N01 * N10)) / (sqrt(N00 * N11) + sqrt(N01 * N10))

    return q, y


def getUllQResult(q, alpha, N00, N11, N01, N10):
    uppf = stats.norm.ppf(1 - alpha / 2)
    sq = (1 / 2) * (1 - q ** 2) * sqrt((1 / N00) + (1 / N01) + (1 / N10) + (1 / N11))
    uq = q / sq

    if abs(uq) <= uppf:
        return "Значущий"
    return "Не значущий"


def getUllYResult(y, alpha, N00, N11, N01, N10):
    uppf = stats.norm.ppf(1 - alpha / 2)
    sy = (1 / 4) * (1 - y ** 2) * sqrt((1 / N00) + (1 / N01) + (1 / N10) + (1 / N11))
    uy = y / sy

    if abs(uy) <= uppf:
        return "Значущий"
    return "Не значущий"


def getCombinationTablemxn(x, y):
    mX = countOptimalBins(len(x))
    mY = countOptimalBins(len(y))
    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    #############
    table = [[0 for i in range(mY)] for j in range(mY)]
    deltaX = getH(xmax, xmin, mX)
    deltaY = getH(ymax, ymin, mY)

    for i in range(len(x)):
        index_x = int((x[i] - xmin) / deltaX)
        if index_x > mX:
            index_x -= 1
        index_y = int((y[i] - ymin) / deltaY)
        if index_y > mY:
            index_y -= 1
        table[index_y][index_x] += 1
    mj = [sum(col) for col in zip(*table)]
    ni = [sum(row) for row in table]
    N = sum(ni)

    return table, mX, mY, mj, ni, N


def getCombinationTablemxnIndexes(alpha, table, mX, mY, ni, mj, N):
    characteristics = dict()
    chi2Stat = getChi2Stat(table, mX, mY, ni, mj, N)
    coefPearsonRatio = pearsonRatioOfCombinations(chi2Stat, N)

    if mX == mY:
        name, stat = "Міра зв'язку Кендалла", coefKendall(table, mX, mY, ni, mj, N)
        res = getKendallResult(stat, alpha)
    else:
        name, stat = "Статистика Стюарда", coefStuart(table, mX, mY, N)
        res = getSpermanResult(stat, alpha, N)

    characteristics['point'] = {
        "X^2": chi2Stat,
        "Коефіцієнт сполучень Пірсона": coefPearsonRatio,
        name: stat
    }

    characteristics['tests'] = {
        "X^2": getChi2StatResult(chi2Stat, alpha, mX, mY),
        "Коефіцієнт сполучень Пірсона": getPearsonRatioOfCombinationsResult(coefPearsonRatio, alpha),
        name: res

    }

    return characteristics


def getH(max, min, countCla):
    return (max - min) / (countCla - 1)


def getChi2Stat(table, mX, mY, ni, mj, N):
    chi2 = []
    for i in range(mY):
        tmp = list()
        for j in range(mX):
            Nij = ni[i] * mj[j] / N
            if Nij:
                tmp.append((table[i][j] - Nij) ** 2 / Nij)
        chi2.append(sum(tmp))
    chi2_ = sum(chi2)
    return sqrt(chi2_ / (N + chi2_))


def getChi2StatResult(chi2, alpha, mX, mY):
    chi2ppf = stats.chi2.ppf(1 - alpha, (mX - 1) * (mY - 1))
    if chi2 >= chi2ppf:
        return "Значущий"
    return "Не значущий"


def pearsonRatioOfCombinations(chi2, N):
    return sqrt(chi2 / (N + chi2))


def getPearsonRatioOfCombinationsResult(C, alpha):
    chi2ppf = stats.chi2.ppf(1 - alpha, 1)
    if C >= chi2ppf:
        return "Значущий"
    return "Не значущий"


def coefKendall(table, mX, mY, ni, mj, N):
    T1 = 0.5 * sum(ni)
    T2 = 0.5 * sum(mj)
    P = 0
    for i in range(mY):
        for j in range(mX):
            d_sum = 0
            for k in range(i + 1, mY):
                for l in range(j + 1, mX):
                    d_sum += table[k][l]
            P += table[i][j] * d_sum
    Q = 0
    for i in range(mY):
        for j in range(mX):
            d_sum = 0
            for k in range(i + 1, mY):
                for l in range(j):
                    d_sum += table[k][l]
            Q += table[i][j] * d_sum

    return (P - Q) / sqrt(((1 / 2) * N * (N - 1) - T1) * ((1 / 2) * N * (N - 1) - T2))


def coefStuart(table, mX, mY, N):
    P = 0
    for i in range(mY):
        for j in range(mX):
            d_sum = 0
            for k in range(i + 1, mY):
                for l in range(j + 1, mX):
                    d_sum += table[k][l]
            P += table[i][j] * d_sum
    Q = 0
    for i in range(mY):
        for j in range(mX):
            d_sum = 0
            for k in range(i + 1, mY):
                for l in range(j):
                    d_sum += table[k][l]
            Q += table[i][j] * d_sum

    return (2 * (P - Q) * min(mX, mY)) / ((N ** 2) * min(mX, mY) - 1)
