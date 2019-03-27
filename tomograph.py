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
import pydicom
from pydicom.dataset import Dataset, FileDataset
import random
import math


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self, pixMap = None, output = None):
        super().__init__()

        self.info_label = QtWidgets.QLabel(self)
        self.forename_label = QtWidgets.QLabel(self)
        self.surname_label = QtWidgets.QLabel(self)
        self.id_label = QtWidgets.QLabel(self)
        self.date_label = QtWidgets.QLabel(self)
        self.image_label = QtWidgets.QLabel(self)
        self.comments_label = QtWidgets.QLabel(self)

        self.forename_text = QtWidgets.QTextEdit(self)
        self.surname_text = QtWidgets.QTextEdit(self)

        self.comments_text = QtWidgets.QTextEdit(self)

        self.calendar = QtWidgets.QCalendarWidget(self)

        self.submitButton = QtWidgets.QPushButton(self)

        self.PatientID = random.randint(1, 1000)

        self.setModal(True)
        self.initGui(pixMap)


    def initGui(self,pixMap):

        self.info_label.setGeometry(10, 10, 200, 50)
        self.info_label.setText("Dane pacjenta")
        self.info_label.setStyleSheet("font-size: 25px;")

        self.id_label.setGeometry(10, 60, 200, 50)
        id = "Id: " + str(self.PatientID)
        self.id_label.setText(id)
        self.id_label.setStyleSheet("font-size: 18px;")

        self.forename_label.setGeometry(10, 100, 200, 50)
        self.forename_label.setText("Imię:")
        self.forename_label.setStyleSheet("font-size: 18px;")

        self.forename_text.setGeometry(95, 112, 100, 25)

        self.surname_label.setGeometry(10, 140, 200, 50)
        self.surname_label.setText("Nazwisko:")
        self.surname_label.setStyleSheet("font-size: 18px;")

        self.surname_text.setGeometry(95, 152, 100, 25)

        self.date_label.setGeometry(10,180,200,50)
        self.date_label.setText("Data badania: ")
        self.date_label.setStyleSheet("font-size: 18px;")

        self.calendar.setGeometry(10, 225, 350 ,350)
        self.calendar.clicked.connect(self.calendarClicked)

        self.comments_label.setGeometry(10, 585, 100, 25)
        self.comments_label.setText("Komentarze")
        self.comments_label.setStyleSheet("font-size: 18px;")

        self.comments_text.setGeometry(10, 615, 350 ,75)


        self.image_label.setGeometry(400, 10, 300, 300)
        self.image_label.setStyleSheet("border: 1px solid #000000;")

        self.submitButton.setGeometry(400,640,300,50)
        self.submitButton.setText("Zapisz")
        self.submitButton.setStyleSheet("font-size: 18px;")
        self.submitButton.clicked.connect(self.saveImageAsDicom)

        qim = ImageQt(pixMap)
        pixM = QtGui.QPixmap.fromImage(qim)
        pixM = pixM.scaled(self.image_label.width(), self.image_label.height())
        self.image_label.setPixmap(pixM)

    def calendarClicked(self):
        self.date_label.setText("Data badania: " + self.calendar.selectedDate().toString("dd/MM/yy"))

    def to2DArray(self,img):
        tab = []
        for a in range(3):
            row = []
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    tab.append(math.floor(img[i][j][0]))
        return tab

    def saveImageAsDicom(self):

        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]

        x = name.split('.')

        if len(x) == 1:
            name = name + ".dcm"

        if name is not "":

            output = cv2.imread("output.jpg")

            file_meta = Dataset()
            file_meta.ImplementationClassUID = "1.2.3.4"
            file_meta.MediaStorageSOPInstanceUID = "1.2.3"
            file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
            ds = FileDataset(name, {}, file_meta=file_meta, preamble=b"\0" * 128)

            ds.is_little_endian = True
            ds.is_implicit_VR = True


            ds.PatientID = str(self.PatientID)
            ds.PatientName = self.forename_text.toPlainText() + ' ' + self.surname_text.toPlainText()
            ds.ContentDate = self.calendar.selectedDate().toString("yyyyMMdd")
            ds.ContentTime = '666666'
            ds.ImageComments = self.comments_text.toPlainText()

            ds.PhotometricInterpretation = "RGB"
            ds.SamplesPerPixel = 3
            ds.PlanarConfiguration = 1
            ds.Columns = output.shape[0]
            ds.Rows = output.shape[1]


            result = self.to2DArray(output)
            print(result)
            ds.PixelData = np.array(result, np.int8).tostring()

            ds.save_as(name, False)


            print('Load file {} ...')
            ds = pydicom.dcmread(name)
            print(ds)


            self.destroy()


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
        self.initGUI()#

        self.imgAs2DArray = 0
        self.array = []

        self.sinogramPixMap = 0
        self.output = 0

        self.rrs = []
        self.ccs = []

    def initGUI(self):

        self.btn_start = QtWidgets.QPushButton("Start", self)
        self.btn_start.setGeometry(400, 660, 210, 50)
        self.btn_start.setStyleSheet("font-size: 18px;")
        self.btn_start.clicked.connect(self.start)
        self.btn_start.setEnabled(False)

        self.btn_save = QtWidgets.QPushButton("Zapisz wynik", self)
        self.btn_save.setGeometry(720, 660, 210, 50)
        self.btn_save.setStyleSheet("font-size: 18px;")
        self.btn_save.clicked.connect(self.saveResult)
        self.btn_save.setEnabled(False)


        self.btn_choose = QtWidgets.QPushButton("Wybierz obraz wejściowy", self)
        self.btn_choose.setGeometry(30, 25, 300, 50)
        self.btn_choose.setStyleSheet("font-size: 18px;")
        self.btn_choose.clicked.connect(self.choose_file)

        self.btn_filter = QtWidgets.QPushButton("Filtruj", self)
        self.btn_filter.setGeometry(670, 25, 300, 50)
        self.btn_filter.setStyleSheet("font-size: 18px;")
        self.btn_filter.clicked.connect(self.filter_output)
        self.btn_filter.setEnabled(False)

        self.b2.setGeometry(600, 25, 320, 50)

        self.progress_label.setGeometry(30, 670, 325, 50)
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
        self.s1.setMaximum(40)
        self.s1.setValue(20)
        self.s1.setTickInterval(1)
        self.s1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.s1.setGeometry(30, 490, 300, 50)
        self.s1.valueChanged.connect(self.valuechange)

        self.s2.setMinimum(90)
        self.s2.setMaximum(1000)
        self.s2.setValue(180)
        self.s2.setTickInterval(100)
        self.s2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.s2.setGeometry(350, 490, 300, 50)
        self.s2.valueChanged.connect(self.valuechange_2)

        self.s3.setMinimum(1)
        self.s3.setMaximum(360)
        self.s3.setValue(180)
        self.s3.setTickInterval(10)
        self.s3.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.s3.setGeometry(670, 490, 300, 50)
        self.s3.valueChanged.connect(self.valuechange_3)

        self.slider_label1.setGeometry(210, 570, 50, 50)
        self.slider_label1.setStyleSheet("border: 1px solid #000000;")
        self.slider_label1.setText((self.s1.value()/10).__str__()+"°")
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

    def check_err(self):
        img_in = self.imgAs2DArray
        img_out = self.filt_arr
        sum = 0
        if (img_in.shape[0] != img_out.shape[0]) or (img_in.shape[1] != img_out.shape[1]):
            print("Measures of input and output image are not the same")
        else:
            for i in range(img_in.shape[0]):
                for j in range(img_in.shape[1]):
                    sum += (img_in[i][j][0]/255 - img_out[i][j][0])**2

            blad = sum/(img_in.shape[0]*img_out.shape[1])
            blad = round(blad*10000)/10000
            print(sum)
            print(blad)

            self.progress_label.setText("Błąd średniokwadratowy: "+blad.__str__())

    def filter_output(self):

        print("filtruje")

        self.btn_filter.setEnabled(False)

        mask = [[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]]

        arr = self.filt_arr

        for i in range(1, arr.shape[0] - 1):
            for j in range(1, arr.shape[1] - 1):
                sum = 0
                for m in range(-1, 1, 1):
                    for n in range(-1, 1, 1):
                        sum += mask[m][n] * arr[i - m][j - n][0]
                arr[i][j] = [sum, sum, sum]

        self.filt_arr = arr
        self.set_output_image(arr, True)
        self.check_err()
        self.btn_filter.setEnabled(True)


    def saveResult(self):
        dialog = QtWidgets.QDialog()
        self.dialog = Ui_Dialog(pixMap=self.sinogramPixMap, output=self.output)
        self.dialog.show()

    def valuechange(self):
        angle = self.s1.value()/10
        self.slider_label1.setText(angle.__str__()+"°")

    def valuechange_2(self):
        angle = self.s2.value()
        self.slider_label2.setText(angle.__str__())

    def valuechange_3(self):
        angle = self.s3.value()
        self.slider_label3.setText(angle.__str__()+"°")

    def normalizeArray(self, arr):
        arrMax = np.amax(arr)
        arr = arr / arrMax
        return arr

    def normalize_2nd(self, arr):
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                x = arr[i][j][0]
                wart = min(1.8*(x**3), 1)
                arr[i][j] += [wart, wart, wart]

        return arr

    def inverseRadonTransform(self, radon_image):

        output = np.zeros((self.imgAs2DArray.shape[0], self.imgAs2DArray.shape[1], 3))

        i = 0
        j = 0

        step = self.s1.value()/10
        show_progress = not self.b2.isChecked()

        o = 0

        for rr,cc in zip(self.rrs, self.ccs):
            o += 1
            for x,y in zip(rr, cc):
                point = (x, y)
                if (0 <= point[0] < output.shape[0] and
                        0 <= point[1] < output.shape[1]):
                        try:
                            pixel = self.sinogram[i][j]
                            output[y][x] += pixel
                        except:
                            print('exeption')

            j += 1
            if j > self.sinogram.shape[1] - 1:

                QtGui.QGuiApplication.processEvents()
                a = round(100*o/len(self.rrs))
                self.progress_label.setText("Progres: " + (a.__str__()) + "%")

                print((100*(i/180)).__str__())
                j = 0
                i += 1
                if not show_progress:
                    self.set_output_image(output, False)

        self.set_output_image(output, True)
        self.progress_label.setText("")

    def set_output_image(self, output, save):

        QtGui.QGuiApplication.processEvents()

        new_out = self.normalizeArray(output)
        new_out_filt = self.normalize_2nd(new_out)
        o_img = toimage(new_out_filt)
        if save:
            self.filt_arr = new_out_filt
            o_img.save("output.jpg")

        qim = ImageQt(o_img)
        pixMap = QtGui.QPixmap.fromImage(qim)
        pixMap = pixMap.scaled(self.image_label3.width(), self.image_label3.height())
        self.image_label3.setPixmap(pixMap)

    def set_output_image(self, output):

        QtGui.QGuiApplication.processEvents()

        new_out = self.normalizeArray(output)
        new_out_filt = self.normalize_2nd(new_out)
        o_img = toimage(new_out_filt)

        qim = ImageQt(o_img)
        pixMap = QtGui.QPixmap.fromImage(qim)
        pixMap = pixMap.scaled(self.image_label3.width(), self.image_label3.height())
        self.image_label3.setPixmap(pixMap)

    def generateSinogram(self):

        imgSize = (len(self.imgAs2DArray), len(self.imgAs2DArray[0]), len(self.imgAs2DArray[0][0]))

        step = self.s1.value()/10
        detectorNumber = self.s2.value()
        l = self.s3.value()
        r = sqrt((imgSize[0] / 2)**2 + (imgSize[1] / 2)**2)

        steps = int(360 / step)
        self.sinogram = np.zeros((steps, detectorNumber, 3))

        show_progress = not self.b2.isChecked()

        for i in range(steps):

            QtGui.QGuiApplication.processEvents()
            self.progress_label.setText("Progres: "+round(100*i/steps).__str__()+"%")
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
                    if (0 <= point[0] < imgSize[1] and
                            0 <= point[1] < imgSize[0]):
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
        self.btn_save.setEnabled(False)
        self.btn_start.setEnabled(False)
        self.b2.setEnabled(False)
        sinogram = self.generateSinogram()
        self.inverseRadonTransform(sinogram)
        self.check_err()
        self.btn_filter.setEnabled(True)
        self.btn_start.setEnabled(True)
        self.b2.setEnabled(True)
        self.btn_save.setEnabled(True)

    def choose_file(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')

        names = name[0].split('.')
        print(names)

        if names[1] == "dcm" or names[1] == "DCM":
            #print("dmc file!")

            ds = pydicom.dcmread(name[0])
            print(ds.pixel_array)

        else:
            pixmap = QtGui.QPixmap(name[0])
            pixmap = pixmap.scaled(self.image_label1.width(),
                                   self.image_label1.height())
            self.image_label1.setPixmap(pixmap)
            self.imgAs2DArray = cv2.imread(name[0])

        self.btn_start.setEnabled(True)

def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    app.exec_()


run()
