import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from math import *
from skimage.draw import line
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.label3 = QtWidgets.QLabel(self)
        self.label4 = QtWidgets.QLabel(self)

        self.b2 = QtWidgets.QCheckBox(self)

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

        self.imgAs2DArray = []
        self.array = []

    def initGUI(self):

        btn_start = QtWidgets.QPushButton("Start", self)
        btn_start.setGeometry(400, 660, 210, 50)
        btn_start.setStyleSheet("font-size: 18px;")
        btn_start.clicked.connect(self.start)

        btn_choose = QtWidgets.QPushButton("Wybierz obraz wejściowy", self)
        btn_choose.setGeometry(30, 25, 350, 50)
        btn_choose.setStyleSheet("font-size: 18px;")
        btn_choose.clicked.connect(self.choose_file)

        self.b2.setGeometry(920, 25, 320, 50)

        self.label4.setGeometry(800, 25, 100, 50)
        self.label4.setText("Filtrowanie")
        self.label4.setStyleSheet("font-size: 18px;")

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

        self.s2.setMinimum(100)
        self.s2.setMaximum(1000)
        self.s2.setValue(200)
        self.s2.setTickInterval(100)
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

    def normalizeArray(self,arr, max):
        for x in range(0, len(arr)):
            try:
                arr[x] = arr[x] / max
                if isnan(arr[x]):
                    arr[x] = 0
            except:
                arr[x] = 0

        return arr

    def start(self):
        step = self.s1.value()
        detectorNumber = self.s2.value()
        l = self.s3.value()
        r = 300
        a = 0

        for i in range(0, 360, step):

            emiterX = (r * cos(radians(i))) + 150
            emiterY = (r * sin(radians(i))) + 150

            #print("Alfa: " + str(i))
            #print("Emiter X: " + str(emiterX))
            #print("Emiter Y: " + str(emiterY))

            max = 0
            pixelSumList = []

            for x in range(0, detectorNumber):
                detectorX = r * cos(radians(i) + pi - (radians(l) / 2) + x * (radians(l) / (detectorNumber - 1))) + 150
                detectorY = r * sin(radians(i) + pi - (radians(l) / 2) + x * (radians(l) / (detectorNumber - 1))) + 150

                rr,cc = line(int(emiterX), int(emiterY), int(detectorX), int(detectorY))

                pixelsSum = 0

                for i in range(0,len(rr)):
                    try:
                        pixel = self.imgAs2DArray[rr[i]][cc[i]]
                        pixelsSum = pixelsSum + pixel
                    except:
                        pixelsSum = pixelsSum + 0

                if pixelsSum > max:
                    max = pixelsSum

                pixelSumList.append(pixelsSum)


            pixelSumList = self.normalizeArray(pixelSumList,max)

            #print(pixelSumList)

            #Przenoszenie wynikow na Sinogram
            self.array.append(pixelSumList)

        a += 1
        print(self.array)
        print(len(self.array))
        self.array = np.array(self.array)
        img = Image.fromarray(self.array * 255)

        img = img.convert("L")

        img.save('test.png')

    def choose_file(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        pixmap = QtGui.QPixmap(name[0])
        pixmap = pixmap.scaled(self.image_label1.width(),
                               self.image_label1.height())
        self.image_label1.setPixmap(pixmap)
        self.imgAs2DArray = cv2.imread(name[0], 0)
        resized = cv2.resize(self.imgAs2DArray, (300,300), interpolation=cv2.INTER_AREA)
        self.imgAs2DArray = resized






def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    app.exec_()


run()
