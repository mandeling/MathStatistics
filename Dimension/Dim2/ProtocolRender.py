from jinja2 import Template
from scipy.stats import linregress
import numpy as np
from PyQt5.QtWidgets import QTextBrowser
from Dimension.Dim2.CorrelationCharacteristics import getLinearCorrelationCharacteristics, \
    getRangCorrelationCharacteristics, getCombinationTable2x2, getCombinationTablemxn, getCombinationTable2x2Indexes, \
    getCombinationTablemxnIndexes


def showPointsCharacteristics(characteristics: dict, textBrowser: QTextBrowser):
    textBrowser.clear()
    textBrowser.append("АНАЛІЗ ДВОВИМІРНОГО ОБ'ЄКТУ\n \t\t\t|---Точкові статистичні оцінки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics))


def showLinearCorrelation(x: list, y: list, alpha: float, textBrowser: QTextBrowser):
    characteristics = getLinearCorrelationCharacteristics(x, y, alpha)

    textBrowser.append("\n|---Лінійна кореляція---|\n \t\t\t|---Точкові оцінки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['point']))
    textBrowser.append("\t\t\t|---Інтервальні статистичні оцінки---|\n")
    textBrowser.append(getIntervalCharacteristicsTable(characteristics['interval']))
    textBrowser.append("\t\t\t|---Залежність двовимірної вибірки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['tests']))


def showRangCorrelation(x: list, y: list, alpha: float, textBrowser: QTextBrowser):
    characteristics = getRangCorrelationCharacteristics(x, y, alpha)
    textBrowser.append("\n|---Рангова кореляція---|\n \t\t\t|---Точкові оцінки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['point']))
    textBrowser.append("\t\t\t|---Інтервальні статистичні оцінки---|\n")
    textBrowser.append(getIntervalCharacteristicsTable(characteristics['interval']))
    textBrowser.append("\t\t\t|---Залежність двовимірної вибірки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['tests']))


def showCombinationsTable2x2(x: list, y: list, textBrowser: QTextBrowser):
    table, mj, ni, N = getCombinationTable2x2(x, y)
    textBrowser.append("\n|---Таблиця сполучень 2х2---|\n")
    textBrowser.append(getCombinations2x2Table(table, mj, ni, N))


def showCombinationsTable2x2Indexes(x: list, y: list, alpha: float, textBrowser: QTextBrowser):
    table, mj, ni, N = getCombinationTable2x2(x, y)
    characteristics = getCombinationTable2x2Indexes(alpha, table, mj, ni, N)
    textBrowser.append("\n|---Індекси та коефіцієнти таблиці 2х2---|\n \t\t\t|---Точкові оцінки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['point']))
    textBrowser.append("\t\t\t\t\t|---Залежність двовимірної вибірки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['tests']))


def showCombinationsTableMxN(x: list, y: list, textBrowser: QTextBrowser):
    table, mX, mY, mj, ni, N = getCombinationTablemxn(x, y)
    textBrowser.append("\n|---Таблиця сполучень mхn---|\n")
    textBrowser.append(getCombinationsMxNTable(table, mX, mY, mj, ni, N))


def showCombinationsTableMxNIndexes(x: list, y: list, alpha: float, textBrowser: QTextBrowser):
    table, mX, mY, mj, ni, N = getCombinationTablemxn(x, y)
    characteristics = getCombinationTablemxnIndexes(alpha, table, mX, mY, ni, mj, N)
    textBrowser.append("\n|---Міри зв'язку та коефіцієнти таблиці mхn---|\n \t\t\t|---Точкові оцінки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['point']))
    textBrowser.append("\t\t\t|---Залежність двовимірної вибірки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['tests']))


def getPointCharacteristicsTable(pointCharacteristics: dict):
    headers = ['Характеристика', 'Значення']
    rows = [[key, pointCharacteristics[key]] for key in pointCharacteristics.keys()]
    table = generateTable(headers, rows)

    return Template(table).render(headers=headers, rows=rows)


def getIntervalCharacteristicsTable(intervalCharacteristics: dict):
    headers = ['Характеристика', 'INF', 'Значення']
    rows = []
    for key in intervalCharacteristics.keys():
        tmpList = list()
        tmpList.append(key)
        for value in intervalCharacteristics[key]:
            tmpList.append(value)
        rows.append(tmpList)

    table = generateTable(headers, rows)

    return Template(table).render(headers=headers, rows=rows)


def getCombinations2x2Table(table, mj, ni, N):
    headers = ["Y \ X", "0", "1", "Sum"]
    rows = [[0, table[0], table[1], ni[0]],
            [1, table[2], table[3], ni[1]],
            ["", mj[0], mj[1], N]]

    table_ = generateTable(headers, rows)

    return Template(table_).render(headers=headers, rows=rows)


def getCombinationsMxNTable(table, mX, mY, mj, ni, N):
    headers = ["Y \ X"]
    rows = []

    for i in range(mX):
        headers.append(str(i + 1))
    headers.append("")

    for i in range(mX):
        tmp = list()
        tmp.append(i + 1)
        for j in range(mY):
            tmp.append(table[i][j])
        tmp.append(ni[i])
        rows.append(tmp)

    lastRow = []
    lastRow.append("")
    for i in mj:
        lastRow.append(i)
    lastRow.append(N)
    rows.append(lastRow)

    table_ = generateTable(headers, rows)

    return Template(table_).render(headers=headers, rows=rows)


def protocolLinearMNK(x, y, alpha, textBrowser):
    from Dimension.Dim2.Regression.Linear import getCharacteristics, getMNKParams

    aM_, bM_, Sqr = getMNKParams(x, y)
    characteristicsMNK = getCharacteristics(x, y, aM_, bM_, alpha)
    textBrowser.append("\n|---Лінійна регресія---|\n "
                       "\n|---МНК---|\n"
                       "\t\t\t|---Точкові оцінки---|\n")
    characteristicsMNK['point']['S квадрат залишкове'] = float(Sqr)
    textBrowser.append(getPointCharacteristicsTable(characteristicsMNK['point']))
    textBrowser.append("\t\t\t|---Інтервальні оцінки---|\n")
    textBrowser.append(getIntervalCharacteristicsTable(characteristicsMNK['interval']))
    textBrowser.append("\t\t\t|---Залежність двовимірної вибірки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristicsMNK['tests']))


def protocolLinearTail(x, y, alpha, textBrowser):
    from Dimension.Dim2.Regression.Linear import getCharacteristics

    x = np.array(x)
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    aT_ = float(slope)
    bT_ = float(intercept)
    characteristicsT = getCharacteristics(x, y, aT_, bT_, alpha)
    textBrowser.append("\n|---Лінійна регресія---|\n "
                       "\n|---Метод Тейла---|\n"
                       "\t\t\t|---Точкові оцінки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristicsT['point']))
    textBrowser.append("\t\t\t|---Інтервальні оцінки---|\n")
    textBrowser.append(getIntervalCharacteristicsTable(characteristicsT['interval']))
    textBrowser.append("\t\t\t|---Залежність двовимірної вибірки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristicsT['tests']))




def generateTable(headers: list, rows: list):
    return """
        <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
        }
        </style>

        <table border="1" width="100%">
            <tr>{% for header in headers%}<th>{{header}}</th>{% endfor %}</tr>
            {% for row in rows %}<tr>
                {% for element in row %}<td>
                    {{element}}
                </td>{% endfor %}
            </tr>{% endfor %}
        </table>
        """
