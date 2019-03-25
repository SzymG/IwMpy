import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from math import *
from skimage.draw import line
import numpy as np
import cv2
from PIL import Image
from scipy.misc import toimage
from PIL.ImageQt import ImageQt
from matplotlib import pyplot as plt
from skimage.io import imread


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label2 = QtWidgets.QLabel(self)
        self.label3 = QtWidgets.QLabel(self)
        self.label4 = QtWidgets.QLabel(self)
        self.progress_label = QtWidgets.QLabel(self)

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
        self.setGeometry(0, 0, 1000, 735)
        self.setWindowTitle("Tomograph")
        self.initGUI()

        self.imgAs2DArray = 0
        self.array = []

        self.sinogram = 0

        self.rrs = []
        self.ccs = []

    def initGUI(self):

        self.btn_start = QtWidgets.QPushButton("Start", self)
        self.btn_start.setGeometry(400, 660, 210, 50)
        self.btn_start.setStyleSheet("font-size: 18px;")
        self.btn_start.clicked.connect(self.start)
        self.btn_start.setEnabled(False)

        self.btn_choose = QtWidgets.QPushButton("Wybierz obraz wejściowy", self)
        self.btn_choose.setGeometry(30, 25, 300, 50)
        self.btn_choose.setStyleSheet("font-size: 18px;")
        self.btn_choose.clicked.connect(self.choose_file)

        self.btn_filter = QtWidgets.QPushButton("Filtruj", self)
        self.btn_filter.setGeometry(670, 25, 300, 50)
        self.btn_filter.setStyleSheet("font-size: 18px;")
        self.btn_filter.clicked.connect(self.filter_output)

        self.b2.setGeometry(600, 25, 320, 50)

        self.progress_label.setGeometry(120, 660, 210, 50)
        self.progress_label.setStyleSheet("font-size: 18px;")

        self.label4.setGeometry(390, 25, 200, 50)
        self.label4.setText("Pokazywanie iteracyjne")
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
        self.s1.setValue(1)
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
        self.s3.setValue(100)
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

    def filter_output(self):
        print("filtruje")

    def valuechange(self):
        angle = self.s1.value()
        self.slider_label1.setText(angle.__str__()+"°")

    def valuechange_2(self):
        angle = self.s2.value()
        self.slider_label2.setText(angle.__str__())

    def valuechange_3(self):
        angle = self.s3.value()
        self.slider_label3.setText(angle.__str__()+"°")

    def normalizeArray(self,arr):
        arrMax = np.amax(arr)
        arr = arr / arrMax
        return arr

    def inverseRadonTransform(self, radon_image):

        output = np.zeros((self.imgAs2DArray.shape[0], self.imgAs2DArray.shape[1], 3))

        i = 0
        j = 0

        for rr,cc in zip(self.rrs, self.ccs):
            for x,y in zip(rr, cc):
                point = (x, y)
                if (point[0] >= 0 and point[0] < output.shape[0] and
                        point[1] >= 0 and point[1] < output.shape[1]):
                        try:
                            pixel = self.sinogram[i][j]
                            output[x][y] += pixel
                        except:
                            print('exeption')


            j += 1
            if j > self.sinogram.shape[1] - 1:
                j = 0
                i += 1


        newOut = self.normalizeArray(output)
        o_img = toimage(newOut)
        o_img.save("output.jpg")

        qim = ImageQt(o_img)
        pixMap = QtGui.QPixmap.fromImage(qim)
        pixMap = pixMap.scaled(self.image_label3.width(), self.image_label3.height())
        self.image_label3.setPixmap(pixMap)

    def generateSinogram(self):

        #self.imgAs2DArray = cv2.imread("Kwadraty2.jpg")

        imgSize = (len(self.imgAs2DArray), len(self.imgAs2DArray[0]), len(self.imgAs2DArray[0][0]))

        step = self.s1.value()
        detectorNumber = self.s2.value()
        l = self.s3.value()
        r = sqrt((imgSize[0] / 2)**2 + (imgSize[1] / 2)**2)

        steps = int(180 / step)
        self.sinogram = np.zeros((steps, detectorNumber, 3))

        show_progress = not self.b2.isChecked()


        for i in range(steps):

            if show_progress:
                QtGui.QGuiApplication.processEvents()
                self.progress_label.setText("Progres: "+(round(100*((i+1)*step)/180)).__str__()+"%")
            print(((i+1)*step).__str__())

            angle = i * step
            emiterX = int((r * cos(radians(angle))) + (imgSize[0] / 2))
            emiterY = int((r * sin(radians(angle))) + (imgSize[1] / 2))

            for x in range(detectorNumber):
                detectorX = int(r * cos(
                    radians(angle) + pi - (radians(l) / 2) + x * (radians(l) / (detectorNumber - 1))) + (imgSize[0] / 2))
                detectorY = int(r * sin(
                    radians(angle) + pi - (radians(l) / 2) + x * (radians(l) / (detectorNumber - 1))) + (imgSize[1] / 2))

                rr, cc = line(emiterX, emiterY, detectorX, detectorY)

                self.rrs.append(rr)
                self.ccs.append(cc)

                pixelsSum = 0

                for z in range(len(rr)):
                    point = (rr[z], cc[z])
                    if (point[0] >= 0 and point[0] < imgSize[1] and
                            point[1] >= 0 and point[1] < imgSize[0]):
                        pixelsSum += self.imgAs2DArray[point[1]][point[0]][0]

                self.sinogram[i][x] += [pixelsSum, pixelsSum, pixelsSum]

            if not show_progress:
                QtGui.QGuiApplication.processEvents()
                self.set_sinogram_on_label(self.sinogram)

        self.set_sinogram_on_label(self.sinogram)

        sinImg = toimage(self.sinogram)
        sinImg.save("sin.jpg")
        radon_image = cv2.imread('sin.jpg')
        self.inverseRadonTransform(radon_image)

        self.progress_label.setText("")

        print('DONE')
        self.array = []


    def set_sinogram_on_label(self, sin):

        sinogram = sin
        sinogram = self.normalizeArray(sinogram)

        sinogram = toimage(sinogram)
        qim = ImageQt(sinogram)

        pixMap = QtGui.QPixmap.fromImage(qim)
        pixMap = pixMap.scaled(self.image_label1.width(), self.image_label1.height())
        pixMap = pixMap.transformed(QtGui.QTransform().rotate(270))

        self.image_label2.setPixmap(pixMap)

        return sinogram


    def generateOutput(self):
        print("generuje output")

    def start(self):
        self.btn_start.setEnabled(False)
        self.b2.setEnabled(False)
        self.generateSinogram()
        #self.inverseRadonTransform(sinogram)
        self.btn_start.setEnabled(True)
        self.b2.setEnabled(True)

    def choose_file(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        pixmap = QtGui.QPixmap(name[0])
        pixmap = pixmap.scaled(self.image_label1.width(),
                               self.image_label1.height())
        self.image_label1.setPixmap(pixmap)
        self.imgAs2DArray = cv2.imread(name[0])
        #resized = cv2.resize(self.imgAs2DArray, (300, 300), interpolation=cv2.INTER_AREA)
        #self.imgAs2DArray = resized
        self.btn_start.setEnabled(True)

def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    app.exec_()


run()
