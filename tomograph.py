import sys
from PyQt5 import QtWidgets, QtCore


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.label1 = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.label3 = QtWidgets.QLabel(self)
        self.window = QtWidgets.QMainWindow()
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("Tomograph")
        self.home()

    def home(self):

        btn = QtWidgets.QPushButton("Quit", self)
        btn.setGeometry(0, 200, 100, 100)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.label1.setGeometry(150, 0, 200, 100)
        self.label2.setGeometry(400, 0, 200, 100)
        self.label3.setGeometry(650, 0, 200, 100)

        self.label1.setText("Krok ∆α")
        self.label2.setText("Liczba detektorów (n)")
        self.label3.setText("Rozpiętość układu emiter/detektor (l)")

        self.show()


def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    app.exec_()


run()
