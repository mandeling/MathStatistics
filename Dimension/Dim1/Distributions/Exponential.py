import numpy as np


def pdf_expon(l, x):
    x = list(x)
    new_list = []
    for i in x:
        if i < 0:
            new_list.append(0)
        else:
            new_list.append(l * np.exp(-l * i))
    return new_list


def cdf_expon(l, x):
    x = list(x)
    new_list = []
    for i in x:
        if i < 0:
            new_list.append(0)
        else:
            new_list.append(1 - np.exp(-l * i))
    return new_list


def expon_rvs(l, size):
    rnd = np.random.uniform(0, 1, size)
    if l <= 0:
        l = 1
    return -l * np.log(rnd)


def variance_of_expon(x, lam):
    N = len(x)
    x = np.array(x)
    return x ** 2 * np.exp(-2 * lam * x) * (lam ** 2 / N)


def interval_exp(alpha, x, mean):
    u = np.abs(stats.norm.ppf(alpha / 2))

    return u * np.sqrt(Expon.variance_of_expon(x, 1 / mean))
