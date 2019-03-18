import sys
from PyQt5 import QtWidgets, QtCore


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.label1 = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.label3 = QtWidgets.QLabel(self)

        self.image_label1 = QtWidgets.QLabel(self)
        self.image_label2 = QtWidgets.QLabel(self)
        self.image_label3 = QtWidgets.QLabel(self)

        self.desc_image_label1 = QtWidgets.QLabel(self)
        self.desc_image_label2 = QtWidgets.QLabel(self)
        self.desc_image_label3 = QtWidgets.QLabel(self)

        self.s1 = QtWidgets.QSlider(QtCore.Qt.Horizontal,self)
        self.s1.setMinimum(5)
        self.s1.setMaximum(360)
        self.s1.setValue(15)
        #self.sl.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.s1.setTickInterval(5)
        self.s1.setGeometry(30, 500, 300, 50)

        self.window = QtWidgets.QMainWindow()
        self.setGeometry(200, 200, 1000, 750)
        self.setWindowTitle("Tomograph")
        self.home()

    def home(self):

        btn = QtWidgets.QPushButton("Quit", self)
        btn.setGeometry(0, 0, 100, 100)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.label1.setGeometry(150, 600, 220, 100)
        self.label2.setGeometry(400, 600, 220, 100)
        self.label3.setGeometry(650, 600, 220, 100)

        self.label1.setText("Krok (∆α)")
        self.label2.setText("Liczba detektorów (n)")
        self.label3.setText("Rozpiętość układu emiter/detektor (l)")

        self.desc_image_label1.setGeometry(30, 415, 300, 50)
        self.desc_image_label2.setGeometry(350, 415, 300, 50)
        self.desc_image_label3.setGeometry(670, 415, 300, 50)

        self.desc_image_label1.setText("Obraz wejściowy")
        self.desc_image_label1.setAlignment(QtCore.Qt.AlignCenter)
        self.desc_image_label2.setText("Sinogram")
        self.desc_image_label2.setAlignment(QtCore.Qt.AlignCenter)
        self.desc_image_label3.setText("Obraz wyjściowy")
        self.desc_image_label3.setAlignment(QtCore.Qt.AlignCenter)

        self.image_label1.setGeometry(30, 100, 300, 300)
        self.image_label1.setStyleSheet("border: 1px solid #000000;")

        self.image_label2.setGeometry(350, 100, 300, 300)
        self.image_label2.setStyleSheet("border: 1px solid #000000;")

        self.image_label3.setGeometry(670, 100, 300, 300)
        self.image_label3.setStyleSheet("border: 1px solid #000000;")

        self.show()


def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    app.exec_()


run()
