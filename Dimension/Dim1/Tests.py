import numpy as np
from scipy._lib.six import string_types
from scipy.stats import distributions


def ttest(N, model, alternative_params, parapms):
    if model == 'norm':
        m1, s1 = parapms
        m2, s2 = alternative_params

        tt1 = (np.sqrt(N) * (m1 - m2)) / s2
        tt2 = (np.sqrt(2 * N) * (s1 - s2)) / s2

        return tt1, tt2
    elif model == 'expon':
        lam1, = parapms
        lam2, = alternative_params
        tt = (lam2 * (lam1 - lam2)) / np.sqrt(N)

        return tt
    elif model == 'arcsine':
        a1, = parapms
        a2, = alternative_params
        tt = (pow(a2, 2) * (a1 - a2)) / np.sqrt(8 * N)
        return tt


def f1(k):
    return k ** 2 - 0.5 * (1 - (-1) ** k)


def f2(k):
    return 5 * k ** 2 + 22 - 7.5 * (1 - (-1) ** k)


def K(z, N):
    kz = 0
    for k in range(1, 1000):
        kz += (-1) ** k * np.exp(-2 * (k * z) ** 2) * \
              (1 - (2 * k ** 2 * z) / (3 * np.sqrt(N)) - (1 / (18 * N)) *
               ((f1(k) - 4 * (f1(k) + 3)) * k ** 2 * z ** 2 + 8 * k ** 4 * z ** 4) +
               ((k ** 2 * z) / (27 * np.sqrt(N ** 3))) * (f2(k) ** 2 / 5 - (
                              4 * (f2(k) + 45) * k ** 2 * z ** 2) / 15 + 8 * k ** 4 * z ** 4))
    kz *= 2
    kz += 1
    return kz


def ktest(rvs, cdf, args=(), N=20, alternative='two-sided'):
    if isinstance(rvs, string_types):
        if (not cdf) or (cdf == rvs):
            cdf = getattr(distributions, rvs).cdf
            rvs = getattr(distributions, rvs).rvs
        else:
            raise AttributeError("if rvs is string, cdf has to be the "
                                 "same distribution")

    if isinstance(cdf, string_types):
        cdf = getattr(distributions, cdf).cdf
    if callable(rvs):
        kwds = {'size': N}
        vals = np.sort(rvs(*args, **kwds))
    else:
        vals = np.sort(rvs)
        N = len(vals)
    cdfvals = cdf(vals, *args)

    # to not break compatibility with existing code
    if alternative == 'two_sided':
        alternative = 'two-sided'

    if alternative in ['two-sided', 'greater']:
        Dplus = (np.arange(1.0, N + 1) / N - cdfvals).max()
        if alternative == 'greater':
            return Dplus

    if alternative in ['two-sided', 'less']:
        Dmin = (cdfvals - np.arange(0.0, N) / N).max()
        if alternative == 'less':
            return Dmin

    if alternative == 'two-sided':
        D = np.max([Dplus, Dmin])
    return D


def chisquare(rvs, cdf, args=(), M=10, N=20):
    if isinstance(rvs, string_types):
        if (not cdf) or (cdf == rvs):
            cdf = getattr(distributions, rvs).cdf
            rvs = getattr(distributions, rvs).rvs
        else:
            raise AttributeError("if rvs is string, cdf has to be the"
                                 "same distribution")
    if isinstance(cdf, string_types):
        cdf = getattr(distributions, cdf).cdf
        if callable(rvs):
            kwds = {'size': N}
            vals = np.sort(rvs(*args, **kwds))
        else:
            vals = np.sort(rvs)
            N = len(vals)

    histVals, binsVals = np.histogram(vals, bins=M)
    diff = np.abs(binsVals[1] - binsVals[0])
    n0 = np.array([(cdf(binsVals[i] + diff, *args) - cdf(binsVals[i], *args)) * N for i in range(M)])
    chisquareVal = np.sum((histVals - n0) ** 2 / n0)

    return chisquareVal
