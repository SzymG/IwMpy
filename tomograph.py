import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog


def window():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setWindowTitle("Tomograph")
    window.setGeometry(200, 200, 800, 600)
    window.show()
    app.exec_()

window()
