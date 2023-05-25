
import cv2
import PyQt5
import numpy as np

from PyQt5.QtCore import QDir
from PyQt5 import QtWidgets, uic,QtGui,QtCore
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog,QHBoxLayout,QFrame
from PyQt5.QtGui import QPixmap ,QImage
import sys
import urllib.request

class UI(QtWidgets.QMainWindow):
    def __init__(self,flag=0):
        super(UI, self).__init__()
        uic.loadUi('design1.ui', self)

        self.pix = None
        self.image = None
        self.temp = None
        self.canny = None
        self.fname = None
        self.h = 420
        self.w = 600
        self.disply_width = 640
        self.display_height = 480

        self.pushButton.clicked.connect(self.Img_read)
        self.blure.valueChanged.connect(self.Img_blure)
    ####################################################################
    def Img_blure(self):
        print(self.blure.value())
        self.image = self.temp
        self.image =cv2.blur(self.image,(self.blure.value(),self.blure.value())) #mean for pixels
        self.Img_show(1)
    def Img_read(self):
        fname, _ = QFileDialog.getOpenFileName(self, "open file", QDir.homePath(), "Images (*);;img(*.png)")

        self.image = cv2.imread(fname)
        self.temp = self.image
        self.Img_show(1)

    def Img_show(self, window=1):
        # self.Img_resize()
        p = self.convert_cv_qt()

        if window == 1:
            self.label.setPixmap(p)
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # if window == 2:
        #     self.label_2.setPixmap(p)
        #     self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def Img_resize(self):
        ww = self.label.width()
        hh = self.label.height()
        self.image = cv2.resize(self.image, (ww, hh))

    def convert_cv_qt(self):
        # from PyQt5.QtGui import QImageReader
        # for image_formats in QImageReader.supportedImageFormats():
        # print(image_formats.data().decode())
        qformat = QImage.Format_Indexed8
        if (len(self.image.shape) == 3):
            if (self.image.shape[2] == 4):
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        """Convert from an opencv image to QPixmap"""
        if(len(self.image.shape)==3):
            rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.h, self.w, ch = rgb_image.shape
            bytes_per_line = ch * self.w
            convert_to_Qt_format = QtGui.QImage(rgb_image.data, self.w, self.h, bytes_per_line, qformat)
            p = convert_to_Qt_format.scaled(self.w, self.h, QtCore.Qt.KeepAspectRatio)
        else:
            img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
            p = img.rgbSwapped()

        return QPixmap.fromImage(p)

app = QtWidgets.QApplication(sys.argv)
window = UI()
window.show()
app.exec_()