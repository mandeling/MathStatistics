import numpy as np


def setHistTitle(ax):
    ax.set_title("Гістограма")
    ax.set_xlabel("X")
    ax.set_ylabel("P")
    ax.grid(linestyle='--', linewidth=0.6)


def setDensityTitle(ax):
    ax.set_title("Емпірична функція розподілу")
    ax.grid(linestyle='--', linewidth=0.6)
    ax.set_xlabel("X")
    ax.set_ylabel("F(x)")


def setProbGridTitle(ax):
    ax.set_title("Ймовірнісна сітка")
    ax.grid(linestyle='--', linewidth=0.6)
    ax.set_xlabel("X")
    ax.set_ylabel("Квантиль")


def hist(data, countBins, ax):
    setHistTitle(ax)
    weights = np.ones_like(data) / float(len(data))
    ax.hist(data, weights=weights, bins=countBins, color='black')
    ax.set_ylim([0, 1])


def densityFunction(data, countBins, ax):
    hist, bin_edges = np.histogram(data, density=True, bins=countBins)
    emp_values = np.cumsum(hist * np.diff(bin_edges))
    setDensityTitle(ax)
    ax.plot([bin_edges[0:len(bin_edges) - 1], bin_edges[1:len(bin_edges)]],
            [emp_values[0:len(emp_values)], emp_values[0:len(emp_values)]],
            color="black")
    ax.plot([bin_edges[0] - 100, bin_edges[0]], [0, 0], color="black")
    ax.plot([bin_edges[len(bin_edges) - 1], bin_edges[len(bin_edges) - 1] + 100],
            [1, 1], color="black")
    ax.set_xlim([data.min() - 1, data.max() + 1])


def probabilityGrid(data, ax):
    import scipy.stats as stats
    (quantiles, values), (slope, intercept, r) = stats.probplot(data)
    setProbGridTitle(ax)
    ax.plot(values, quantiles, 'ob', color='gray')
    ax.plot(quantiles * slope + intercept, quantiles, 'black')
    ax.grid(True)
    ax.set_ylim(quantiles.min(), quantiles.max())


def clearAxes(*args):
    for ax in args:
        ax.cla()
