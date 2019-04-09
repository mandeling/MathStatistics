import numpy as np
from scipy.stats import norm
from math import sqrt, pi


# Simulation normal distribution using probability density function
def simulate_distribution(mean: float, std: float, size: int) -> np.array:
    """
    Return the normal sample distribution

    :param mean: float - mean
    :param std: float - standard deviation
    :param size: int - size sample
    :return: np.array - sample normal distribution
    """
    return np.random.normal(mean, std, size)


#
def interval_norm(sample: np.array, mean: float, std: float, alpha: float, sigma_x, sigma_s):
    """

    :param sample:
    :param mean:
    :param std:
    :param alpha:
    :param sigma_x:
    :param sigma_s:
    :return:
    """
    u = np.abs(norm.ppf(alpha / 2))

    return u * sqrt(variance_of_norm(sample, mean, std, sigma_x, sigma_s))


#
def variance_of_norm(x, m, std, sigma_x, sigma_s):
    """

    :param x:
    :param m:
    :param std:
    :param sigma_x:
    :param sigma_s:
    :return:
    """
    cov = 0
    return diff_function_by_mean(x, m, std) ** 2 * sigma_x ** 2 \
           + diff_function_by_std(x, m, std) ** 2 * sigma_s ** 2 \
           + 2 * diff_function_by_std(x, m, std) * diff_function_by_mean(x, m, std) * cov


# Find differential of function by mean
def diff_function_by_mean(mean: float, std: float, sample: np.array) -> np.array:
    """
    Return differential of function by mean

    :param mean: float - mean
    :param std: float - standard deviation
    :param sample: np.array - sample numbers
    :return: np.array - differential of function
    """

    return (-1 / (std * sqrt(2 * pi))) * np.exp(-((sample - mean) ** 2 / (2 * std ** 2)))


# Find differential of function by standard deviation
def diff_function_by_std(mean: float, std: float, sample: np.array) -> np.array:
    """
    Return differential of function by standard deviation

    :param mean: float - mean
    :param std: float - standard deviation
    :param sample: np.array - sample numbers
    :return: np.array - differential of function
    """

    return (-(sample - mean) / (std ** 2 * sqrt(pi * 2))) * np.exp(-((sample - mean) ** 2 / (2 * std ** 2)))
