import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from MainWindow import MainWindow


def setPalette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 15, 15))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    palette.setColor(QPalette.Disabled, QPalette.Light, Qt.black)
    palette.setColor(QPalette.Disabled, QPalette.Text, Qt.gray)

    return palette


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(setPalette())

    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
