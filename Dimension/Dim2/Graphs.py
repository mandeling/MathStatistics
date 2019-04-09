import statsmodels.api as sm
import numpy as np
from statsmodels.stats.outliers_influence import summary_table
import operator
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures


def setHistTitle(ax):
    ax.set_title("Вигляд зверху на двовимірну гістограму")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(linestyle='--', linewidth=0.6)


def setCorrelationFieldTitle(ax):
    ax.set_title("Кореляційне поле")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(linestyle='--', linewidth=0.6)


def hist(x, y, countBinsX, countBinsY, canvas):
    from matplotlib.pyplot import colorbar, cm

    canvas.ax = canvas.fig.add_subplot(111)
    h = canvas.ax.hist2d(x, y, bins=[countBinsX, countBinsY], normed=True, cmap=cm.Greys)
    colorbar(h[3], ax=canvas.ax)
    setHistTitle(canvas.ax)


def correlationField(x, y, ax):
    setCorrelationFieldTitle(ax)
    ax.scatter(x, y, marker='o', edgecolors='black', c='gray')


def clearAxes(hist, corrField):
    hist.clf()
    corrField.clear()
    if corrField.get_legend():
        corrField.get_legend().remove()


def drawLinearRegressionByMNK(x, y, alpha, ax):
    x = np.array(x)
    res = sm.OLS(y, x).fit()

    st, data, ss2 = summary_table(res, alpha=alpha)
    fittedvalues = data[:, 2]
    predict_mean_ci_low, predict_mean_ci_upp = data[:, 4:6].T
    predict_ci_low, predict_ci_upp = data[:, 6:8].T

    ax.plot(x, fittedvalues, 'r-', label='Параметрична пряма')
    ax.plot(x, predict_ci_low, 'black', label='Толерантні межі', linestyle='dashed')
    ax.plot(x, predict_ci_upp, 'black', linestyle='dashed')
    ax.plot(x, predict_mean_ci_low, 'gray', label='Довірчий інтервал', linestyle='dashed')
    ax.plot(x, predict_mean_ci_upp, 'gray', linestyle='dashed')
    ax.legend(loc='best', fontsize='x-small')


def drawLinearRegressionByTail(x, y, alpha, ax):
    x = np.array(x)
    res = sm.OLS(y, x).fit()

    st, data, ss2 = summary_table(res, alpha=alpha)
    fittedvalues = data[:, 2]
    predict_mean_ci_low, predict_mean_ci_upp = data[:, 4:6].T
    predict_ci_low, predict_ci_upp = data[:, 6:8].T

    ax.plot(x, fittedvalues, 'r-', label='Параметрична пряма')
    ax.plot(x, predict_ci_low, 'black', label='Толерантні межі', linestyle='dashed')
    ax.plot(x, predict_ci_upp, 'black', linestyle='dashed')
    ax.plot(x, predict_mean_ci_low, 'gray', label='Довірчий інтервал', linestyle='dashed')
    ax.plot(x, predict_mean_ci_upp, 'gray', linestyle='dashed')
    ax.legend(loc='best', fontsize='x-small')


def drawParaboloidRegression(x, y, alpha, ax):
    x = np.array(x)
    y = np.array(y)
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]

    polynomial_features = PolynomialFeatures(degree=2)
    x_poly = polynomial_features.fit_transform(x)

    model = LinearRegression()
    model.fit(x_poly, y)
    y_poly_pred = model.predict(x_poly)

    rmse = np.sqrt(mean_squared_error(y, y_poly_pred))
    r2 = r2_score(y, y_poly_pred)

    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x, y_poly_pred), key=sort_axis)
    x, y_poly_pred = zip(*sorted_zip)
    ax.plot(x, y_poly_pred, color='red', label='Параболічна крива')
    ax.legend(loc='best', fontsize='x-small')


"""

def drawLinearRegressionTolerantIntervalsMNK(x, y, alpha, ax):
    from Dimension.Dim2.Regression.Linear import getTollerantBorderIntervalMNK
    yMNK_L, yMNK_U = getTollerantBorderIntervalMNK(x, y, alpha)
    yMNK_L = list(sorted(yMNK_L))
    yMNK_U = list(sorted(yMNK_U))

    ax.plot(min(yMNK_L), max(x), '-g', label='Толерантні межі МНК')
    ax.plot(min(x), max(yMNK_U), '-g', label='Толерантні межі МНК')


def drawLinearRegressionTolerantIntervalsTail(x, y, alpha, ax):
    from Dimension.Dim2.Regression.Linear import getTollerantBorderIntervalTail
    yT_L, yT_U = getTollerantBorderIntervalTail(x, y, alpha)
    yT_L = list(sorted(yT_L))
    yT_U = list(sorted(yT_U))
    ax.plot(min(yT_L), max(x), '-g', label='Толерантні межі Тейла')
    ax.plot(min(x), max(yT_U), '-g', label='Толерантні межі Тейла')


def drawLinearRegressionConfidenceIntervalsTail(x, y, ax):
    import statsmodels.api as sm
    from statsmodels.stats.outliers_influence import summary_table

    X = sm.add_constant(x)
    res = sm.OLS(y, X).fit()

    st, data, ss2 = summary_table(res, alpha=0.05)
    fittedvalues = data[:, 2]
    predict_mean_se = data[:, 3]
    predict_mean_ci_low, predict_mean_ci_upp = data[:, 4:6].T
    predict_ci_low, predict_ci_upp = data[:, 6:8].T

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, 'o', label="data")
    ax.plot(X, fittedvalues, 'r-', label='OLS')
    ax.plot(X, predict_ci_low, 'b--')
    ax.plot(X, predict_ci_upp, 'b--')
    ax.plot(X, predict_mean_ci_low, 'g--')
    ax.plot(X, predict_mean_ci_upp, 'g--')
    ax.legend(loc='best')
    # f = lambda x, *p: polyval(p, x)
    # p, cov = curve_fit(f, x, y, [1, 1])
    # 
    # xi = linspace(np.min(x), np.max(x), 100)
    # ps = np.random.multivariate_normal(p, cov, 10000)
    # ysample = np.asarray([f(xi, *pi) for pi in ps])
    # lower = percentile(ysample, 2.5, axis=0)
    # upper = percentile(ysample, 97.5, axis=0)
    # y_fit = poly1d(p)(xi)
    # 
    # ax.plot(xi, y_fit, '-g')
    # ax.plot(xi, lower, '-r')
    # ax.plot(xi, upper, '-r')


def drawLinearRegressionConfidenceIntervalsMNK(x, y, ax):
    f = lambda x, *p: polyval(p, x)
    p, cov = curve_fit(f, x, y, [1, 1])

    xi = linspace(np.min(x), np.max(x), 100)
    ps = np.random.multivariate_normal(p, cov, 10000)
    ysample = np.asarray([f(xi, *pi) for pi in ps])
    lower = percentile(ysample, 2.5, axis=0)
    upper = percentile(ysample, 97.5, axis=0)
    y_fit = poly1d(p)(xi)

    ax.plot(xi, y_fit, '-g')
    ax.plot(xi, lower, '-g')
    ax.plot(xi, upper, '-g')


def drawLinearRegressionConfidenceIntervalsForecastValue(x, y, x0, alpha, ax):
    # Get an OLS model based on output y and the prepared vector X (as in your notation):
    model = sm.OLS(endog=y, exog=x)
    results = model.fit()
    # Get two-tailed t-values:
    (t_minus, t_plus) = stats.t.interval(alpha=(1.0 - alpha), df=len(results.resid) - x0)
    y_value_at_x0 = np.dot(results.params, x0)
    lower_bound = y_value_at_x0 + t_minus * np.sqrt(
        results.mse_resid * (np.dot(np.dot(x0.T, results.normalized_cov_params), x0)))
    upper_bound = y_value_at_x0 + t_plus * np.sqrt(
        results.mse_resid * (np.dot(np.dot(x0.T, results.normalized_cov_params), x0)))

    ax.plot(x, lower_bound, '-b')
    ax.plot(x, upper_bound, '-b')


def drawPolynomialRegression(x, y, ax):
    import numpy as np

    x = np.array(x)
    y = np.array(y)
    z = np.polyfit(x, y, 2)
    p = np.poly1d(z)
    xp = np.linspace(x.min(), x.max(), 100)
    ax.plot(x, y, '.', xp, p(xp), '-')
"""
