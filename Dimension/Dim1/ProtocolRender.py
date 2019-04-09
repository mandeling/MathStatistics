from jinja2 import Template
from PyQt5.QtWidgets import QTextBrowser


def showProtocol(characteristics: dict, textBrowser: QTextBrowser):
    textBrowser.clear()
    textBrowser.append("АНАЛІЗ ОДНОВИМІРНОГО ОБ'ЄКТУ\n \t\t\t\t\t|---Точкові статистичні оцінки---|\n")
    textBrowser.append(getPointCharacteristicsTable(characteristics['point']))
    textBrowser.append("\t\t\t\t\t|---Інтервальні статистичні оцінки---|\n")
    textBrowser.append(getIntervalCharacteristicsTable(characteristics['interval']))


def getPointCharacteristicsTable(pointCharacteristics: dict):
    headers = ['Характеристика', 'Значення']
    rows = [[key, pointCharacteristics[key]] for key in pointCharacteristics.keys()]
    table = generateTable(headers, rows)

    return Template(table).render(headers=headers, rows=rows)


def getIntervalCharacteristicsTable(intervalCharacteristics: dict):
    headers = ['Характеристика', 'INF', 'Значення', 'SUP', 'SKV']
    rows = []
    for key in intervalCharacteristics.keys():
        tmpList = list()
        tmpList.append(key)
        for value in intervalCharacteristics[key]:
            tmpList.append(value)
        rows.append(tmpList)

    table = generateTable(headers, rows)

    return Template(table).render(headers=headers, rows=rows)


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
