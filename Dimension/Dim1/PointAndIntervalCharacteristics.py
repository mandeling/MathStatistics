from scipy.stats import t, norm, kurtosis, moment, skew
import numpy as np
from math import sqrt, pow


def getCharacteristics(data, alpha: float, N: int) -> dict:
    data = np.array(data)
    characteristics = dict()

    characteristics['point'] = {
        'Середнє арифметичне': np.mean(data),
        'Медіана': np.median(data),
        'Медіана середніх Уолша': medianMeanWalsh(data, N),
        'Усічене середнє': truncatedMean(data, alpha, N),
        'Зсунена дисперсія': np.var(data),
        'Дисперсія': dispersion(data, N),
        'Зсунене середнє квадратичне відхилення': shiftedSigma(data, N),
        'Середнє квадратичне відхилення': sigmaS(data),
        'Зсунений коефіцієнт асиметрії': skew(data),
        'Коефіцієнт асиметрії': asymmetryFactor(data, N),
        'Зсунений коефіцієнт ексцесу': kurtosis(data),
        'Коефіцієнт ексцесу': factorExcess(data, N),
        'Коефіцієнт контрексцесу': counterRatio(data, N),
        'Коефіцієнт варіції Пірсона': pearsonVariationFactor(data),
        'Квантилі': quantilesStr(quantileVals(data))
    }

    sigmaPoints = {
        'Середнє арифметичне': sigmaMean(data, N),
        'Середнє квадратичне відхилення': sigmaStd(data, N),
        'Коефіцієнт асиметрії': sigmaAsymmetryFactor(data, N),
        'Коефіцієнт ексцесу': sigmaExcessFactor(data, N),
        'Коефіцієнт контрексцесу': sigmaCounterExcessFactor(data, N),
        'Коефіцієнт варіції Пірсона': sigmaPearsonVariation(data, N)
    }
    characteristics['interval'] = dict()

    for name in sigmaPoints:
        sigma = sigmaPoints[name]
        point = characteristics['point'][name]

        characteristics['interval'][name] = [
            charInterval(point, sigma, alpha, N, lower=True),
            point,
            charInterval(point, sigma, alpha, N, upper=True),
            sigma
        ]

    return characteristics


def quantilesStr(quantiles):
    quantilesS = ""
    for index in quantiles.index:
        quantilesS += '<p><pre>{0}\t{1}</pre></p>'.format(index, quantiles[index])
    return quantilesS


# Point characteristics
#######################################################################################################################
def sigmaS(data: np.array) -> np.ndarray:
    return np.std(data)


def counterRatio(data: np.array, N: int) -> float:
    coefficientExcess = factorExcess(data, N)
    return 1.0 / np.sqrt(abs(coefficientExcess))


def medianMeanWalsh(data: np.array, N: int) -> np.ndarray:
    return np.median([(data[i] + data[j]) for i in range(N) for j in range(i + 1, N)])


def quantileVals(data: np.array) -> np.ndarray:
    import pandas as pd
    data = pd.Series(data)
    return np.round(data.quantile([0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]), 5)


def truncatedMean(data: np.array, alpha: float, N: int) -> np.ndarray:
    k = int(alpha * N)
    return np.sum(data[k:(N - k)]) / (N - 2 * k)


def dispersion(data: np.array, N: int) -> np.ndarray:
    mean = np.mean(data)
    return np.sum(np.power(data - mean, 2)) / (N - 1)


def shiftedSigma(data: np.array, N: int) -> np.ndarray:
    if N == 2:
        return 0.8862 * (data[1] - data[0])
    elif N == 3:
        return 0.59088 * (data[2] - data[1])
    elif N == 4:
        return 0.4639 * (data[3] - data[0]) + 0.1102 * (data[2] - data[1])
    elif N == 5:
        return 0.3724 * (data[4] - data[0]) + 0.1352 * (data[3] - data[1])
    elif N == 6:
        return 0.3175 * (data[5] - data[0]) + 0.1386 * (data[4] - data[1]) + \
               0.0432 * (data[3] - data[2])
    elif N == 7:
        return 0.2778 * (data[6] - data[0]) + 0.1351 * (data[5] - data[1]) + \
               0.0625 * (data[4] - data[2])
    elif N == 8:
        return 0.2476 * (data[7] - data[0]) + 0.1294 * (data[6] - data[1]) + \
               0.0713 * (data[5] - data[2]) + 0.0230 * (data[4] - data[3])
    elif N == 9:
        return 0.2237 * (data[8] - data[0]) + 0.1233 * (data[7] - data[1]) + \
               0.0750 * (data[6] - data[2]) + 0.0360 * (data[5] - data[3])
    elif N == 10:
        return 0.2044 * (data[9] - data[0]) + 0.1172 * (data[8] - data[1]) + \
               0.0763 * (data[7] - data[2]) + 0.0436 * (data[6] - data[3]) + \
               0.0141 * (data[5] - data[4])
    else:
        return np.std(data)


def asymmetryFactor(data: np.array, N: int) -> float:
    sAsymmetryFactor = skew(data)
    return (sqrt(N * (N - 1))) / (N - 2) * sAsymmetryFactor


def factorExcess(data: np.array, N: int) -> float:
    sFactorExcess = kurtosis(data)
    return ((N ** 2 - 1) / ((N - 2) * N - 3)) * ((sFactorExcess - 3) + (6 / (N + 1)))


def pearsonVariationFactor(data: np.array) -> float or None:
    sigma = sigmaS(data)
    mean = np.mean(data)
    return sigma / mean if sigma != 0 else None


# Interval characteristics
#######################################################################################################################

def sigmaMean(data: np.array, N: int) -> float:
    median = np.median(data)
    return median / sqrt(N)


def sigmaStd(data: np.array, N: int) -> float:
    std = np.std(data)
    return std / sqrt(N * 2)


def sigmaAsymmetryFactor(data: np.array, N: int) -> np.ndarray or None:
    if N > 10:
        return sqrt(np.fabs((1 / 4 * N) * (4 * betta(data, 4) - 12 * betta(data, 3) - 24 * betta(data, 2)
                                           + 9 * betta(data, 2) * betta(data, 1) + 35 * betta(data, 1) - 36)))
    return None


def sigmaExcessFactor(data: np.array, N: int):
    if N > 10:
        return sqrt(np.fabs((1 / N) * (betta(data, 6) - 4 * betta(data, 4) * betta(data, 2) - 8 * betta(data, 3) + 4 * (
            betta(data, 2)) ** 3 - (betta(data, 2)) ** 2 + 16 * betta(data, 2) * betta(data, 1) + 16 * betta(data, 1))))
    return None


def sigmaCounterExcessFactor(data: np.array, N: int):
    kurt = kurtosis(data)
    if N > 10:
        return sqrt(abs(kurt / 29 * N) * pow(abs(kurt ** 2 - 1), 3 / 4))
    return None


def sigmaPearsonVariation(data: np.array, N: int):
    pearsonVar = pearsonVariationFactor(data)
    return pearsonVar * (sqrt((1 + 2 * pearsonVar ** 2) / 2 * N))


def charInterval(estimate: float, sigmaEstimate: float, alpha: float, N: int, lower: float = False,
                 upper: float = False):
    t_critical = t.ppf(q=1 - alpha, df=N - 1) if N >= 60 else abs(norm.ppf(alpha))

    if lower:
        return estimate - t_critical * sigmaEstimate
    elif upper:
        return estimate + t_critical * sigmaEstimate


def betta(data: np.ndarray, k: float) -> np.ndarray or None:
    if k % 2 == 1:
        k = (k - 1) / 2
        return moment(data, 3) * moment(data, 2 * k + 3) / (moment(data, 2) ** (k + 3))
    elif k % 2 == 0:
        k = k / 2
        return moment(data, 2 * k + 2) / (moment(data, 2) ** (k + 1))
    else:
        return None
