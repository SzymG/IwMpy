import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.label3 = QtWidgets.QLabel(self)

        self.slider_label1 = QtWidgets.QLabel(self)
        self.slider_label2 = QtWidgets.QLabel(self)
        self.slider_label3 = QtWidgets.QLabel(self)

        self.image_label1 = QtWidgets.QLabel(self)
        self.image_label2 = QtWidgets.QLabel(self)
        self.image_label3 = QtWidgets.QLabel(self)

        self.desc_image_label1 = QtWidgets.QLabel(self)
        self.desc_image_label2 = QtWidgets.QLabel(self)
        self.desc_image_label3 = QtWidgets.QLabel(self)

        self.s1 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.s2 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.s3 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)

        self.window = QtWidgets.QMainWindow()
        self.setGeometry(200, 200, 1000, 735)
        self.setWindowTitle("Tomograph")
        self.initGUI()

    def initGUI(self):

        btn_start = QtWidgets.QPushButton("Start", self)
        btn_start.setGeometry(400, 660, 210, 50)
        btn_start.setStyleSheet("font-size: 18px;")
        btn_start.clicked.connect(self.start)

        btn_choose = QtWidgets.QPushButton("Wybierz obraz wejściowy", self)
        btn_choose.setGeometry(30, 25, 350, 50)
        btn_choose.setStyleSheet("font-size: 18px;")
        btn_choose.clicked.connect(self.choose)

        self.label1.setGeometry(120, 545, 220, 100)
        self.label2.setGeometry(400, 545, 220, 100)
        self.label3.setGeometry(680, 545, 220, 100)

        self.label1.setText("Krok (∆α)")
        self.label2.setText("Liczba detektorów (n)")
        self.label3.setText("Rozpiętość układu emiter/detektor (l)")

        self.desc_image_label1.setGeometry(30, 415, 300, 50)
        self.desc_image_label2.setGeometry(350, 415, 300, 50)
        self.desc_image_label3.setGeometry(670, 415, 300, 50)

        self.desc_image_label1.setText("Obraz wejściowy")
        self.desc_image_label1.setStyleSheet("font-size: 18px;")
        self.desc_image_label1.setAlignment(QtCore.Qt.AlignCenter)
        self.desc_image_label2.setText("Sinogram")
        self.desc_image_label2.setStyleSheet("font-size: 18px;")
        self.desc_image_label2.setAlignment(QtCore.Qt.AlignCenter)
        self.desc_image_label3.setText("Obraz wyjściowy")
        self.desc_image_label3.setStyleSheet("font-size: 18px;")
        self.desc_image_label3.setAlignment(QtCore.Qt.AlignCenter)

        self.image_label1.setGeometry(30, 100, 300, 300)
        self.image_label1.setStyleSheet("border: 1px solid #000000;")

        self.image_label2.setGeometry(350, 100, 300, 300)
        self.image_label2.setStyleSheet("border: 1px solid #000000;")

        self.image_label3.setGeometry(670, 100, 300, 300)
        self.image_label3.setStyleSheet("border: 1px solid #000000;")

        self.s1.setMinimum(1)
        self.s1.setMaximum(360)
        self.s1.setValue(20)
        self.s1.setTickInterval(10)
        self.s1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.s1.setGeometry(30, 490, 300, 50)
        self.s1.valueChanged.connect(self.valuechange)

        self.s2.setMinimum(1)
        self.s2.setMaximum(10)
        self.s2.setValue(1)
        self.s2.setTickInterval(1)
        self.s2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.s2.setGeometry(350, 490, 300, 50)
        self.s2.valueChanged.connect(self.valuechange_2)

        self.s3.setMinimum(1)
        self.s3.setMaximum(360)
        self.s3.setValue(20)
        self.s3.setTickInterval(10)
        self.s3.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.s3.setGeometry(670, 490, 300, 50)
        self.s3.valueChanged.connect(self.valuechange_3)

        self.slider_label1.setGeometry(210, 570, 50, 50)
        self.slider_label1.setStyleSheet("border: 1px solid #000000;")
        self.slider_label1.setText(self.s1.value().__str__()+"°")
        self.slider_label1.setAlignment(QtCore.Qt.AlignCenter)

        self.slider_label2.setGeometry(560, 570, 50, 50)
        self.slider_label2.setStyleSheet("border: 1px solid #000000;")
        self.slider_label2.setText(self.s2.value().__str__())
        self.slider_label2.setAlignment(QtCore.Qt.AlignCenter)

        self.slider_label3.setGeometry(920, 570, 50, 50)
        self.slider_label3.setStyleSheet("border: 1px solid #000000;")
        self.slider_label3.setText(self.s3.value().__str__()+"°")
        self.slider_label3.setAlignment(QtCore.Qt.AlignCenter)

        self.show()

    def valuechange(self):
        angle = self.s1.value()
        self.slider_label1.setText(angle.__str__()+"°")

    def valuechange_2(self):
        angle = self.s2.value()
        self.slider_label2.setText(angle.__str__())

    def valuechange_3(self):
        angle = self.s3.value()
        self.slider_label3.setText(angle.__str__()+"°")

    def start(self):
        #TODO co się dzieje po naciśnięciu Start
        print("Start")

    def choose(self):
        print("Choosed")

def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    app.exec_()


run()
