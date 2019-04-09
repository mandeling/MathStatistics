import numpy as np
from scipy.stats import norm, arcsine
from math import pi, sqrt, asin


def find_a_for_arsine(dist):
    return np.sqrt(2) * (np.sqrt(np.mean(np.power(dist, 2)) - (np.power(np.mean(dist), 2))))


def arcsin_rvs(N, a):
    x = arcsine.rvs(loc=0, scale=a, size=N)
    return x


def pdf_arcsine(x):
    a = find_a_for_arsine(x)
    new_dist = []
    for i in sorted(x):
        if i < (-1) * a or i > a:
            new_dist.append(0)
        else:
            f = 1 / (pi * sqrt(pow(a, 2) - pow(i, 2)))
            new_dist.append(f)

    return new_dist


def cdf_arcsine(x):
    a = find_a_for_arsine(x)
    new_dist = []
    for i in x:
        if i < a * (-1):
            new_dist.append(0)
        elif (-1) * a <= i <= a:
            new_dist.append(0.5 + (1 / pi) * asin(i / a))
        elif i > a:
            new_dist.append(1)
    return new_dist


def variance_of_arcsin(x):
    N = len(x)
    x = np.array(x)
    a = find_a_for_arsine(x)
    F = x / (np.pi * a * np.sqrt(a ** 2 - np.power(x, 2)))

    return F ** 2 * pow(a, 4) / (8 * N)


def interval_arcsin(x, alpha):
    u = np.abs(norm.ppf(alpha / 2))
    return u * np.sqrt(variance_of_arcsin(x))
