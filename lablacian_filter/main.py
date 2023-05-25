import cv2
import PyQt5
import numpy as np

from PyQt5.QtCore import QDir
from PyQt5 import QtWidgets, uic,QtGui,QtCore
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog,QHBoxLayout,QFrame
from PyQt5.QtGui import QPixmap ,QImage
import sys
import urllib.request
class TUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(TUI, self).__init__()
        uic.loadUi('design1.ui', self)


        self.pix =None
        self.image =None
        self.temp =None
        self.canny = None
        self.fname=None
        self.h = 420
        self.w =600
        self.disply_width = 640
        self.display_height = 480
        self.pushButton.clicked.connect(self.Img_read)
        self.sobel.clicked.connect(self.Img_sobel)

        self.lablacian.valueChanged.connect(self.Img_lablacian)

    def Img_sobel(self):
        self.image = self.temp
        dy = 1
        if(dy):
            sobely_img =cv2.Sobel(self.image  ,cv2.CV_64F,dy = dy , dx = 1)
            sobely_img = np.uint8(np.absolute(sobely_img))
        else :
            sobely_img =cv2.Sobel(self.image  ,cv2.CV_64F,dy = dy , dx = 1)
            sobely_img = np.uint8(np.absolute(sobely_img))
        self.image = sobely_img
        self.Img_show(1)
    def Img_lablacian(self):
        print(self.lablacian.value())
        self.image = self.temp
        if(self.lablacian.value()% 2 != 0):
            lablace =cv2.Laplacian(self.image ,cv2.CV_64F ,self.lablacian.value())
        else :
            lablace =cv2.Laplacian(self.image ,cv2.CV_64F ,self.lablacian.value()+1)

        self.image = cv2.convertScaleAbs(lablace)
        self.Img_show(1)
    def Img_read(self):
        fname, _ = QFileDialog.getOpenFileName(self, "open file", QDir.homePath(), "Images (*)")

        self.image = cv2.imread(fname)
        self.temp =self.image
        self.Img_show(1)
    def Img_show(self,window =1):
        # self.Img_resize()
        p =self.convert_cv_qt()

        if window ==1:
            self.label.setPixmap(p)
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if window ==2:
            self.label_2.setPixmap(p)
            self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
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
        if (len(self.image.shape) == 3):
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
window = TUI()
window.show()
app.exec_()
