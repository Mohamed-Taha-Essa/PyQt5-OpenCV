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
        uic.loadUi('design.ui', self)


        self.pix =None
        self.image =None
        self.temp =None
        self.canny = None
        self.fname=None
        self.h = 420
        self.w =600
        self.disply_width = 640
        self.display_height = 480


        # creating a push button
        self.button_show = self.findChild(QPushButton, "B_show_img")
        self.button_save = self.findChild(QPushButton, "B_save_img")
        self.button_canny = self.findChild(QPushButton, "B_canny")

        #find label
        self.label = self.findChild(QLabel, "label")
        self.label_2 = self.findChild(QLabel, "label_2")

    # what will happen if i click on button i will call func HandlerButton
        self.button_show.clicked.connect(self.Img_read)
        self.button_save.clicked.connect(self.Img_save)
        self.button_canny.clicked.connect(self.Img_canny)
        #file main window
        self.actionshow.triggered.connect(self.Img_read)
        self.actionImage.triggered.connect(self.Img_save)
        self.actioncanny.triggered.connect(self.Img_canny)
        self.actionCannySave.triggered.connect(self.Img_canny_save)

        # slider
        self.CannySlider.valueChanged.connect(self.Img_canny)
        self.H_min.valueChanged.connect(self.Img_hsv)
        self.H_max.valueChanged.connect(self.Img_hsv)
        self.S_min.valueChanged.connect(self.Img_hsv)
        self.S_max.valueChanged.connect(self.Img_hsv)
        self.V_min.valueChanged.connect(self.Img_hsv)
        self.V_max.valueChanged.connect(self.Img_hsv)
    ####################################################################
    def Img_hsv(self):
        self.image =self.temp
        lower = np.array([self.H_min.value(),self.S_min.value(), self.V_min.value()])
        upper = np.array([self.H_max.value(),self.S_max.value(), self.V_max.value()])
        print(self.H_min.value(),self.S_min.value(), self.V_min.value())

        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask= cv2.inRange(hsv, lower, upper)

        masked_image = np.copy(self.temp)
        masked_image[mask != 0] = [0, 0, 0]
        self.image =masked_image
        self.Img_show(2)

    def Handle_ui(self):
        # self.setCentralWidget(self.widget)
        # self.show()
        print(self.label_2.size())
    def Img_canny(self):
        self.image =self.temp
        gray =cv2.cvtColor(self.image ,cv2.COLOR_BGR2GRAY) if(len(self.image.shape)>=3)else self.image
        self.image = cv2.Canny(gray,self.CannySlider.value()  ,self.CannySlider.value()*3)
        self.canny =self.image
        self.Img_show(2)
    def Img_canny_save(self):
        self.image=self.canny
        fname, _ = QFileDialog.getSaveFileName(self, "save file", QDir.homePath(), "Images (*.jpg)")
        if fname:
            cv2.imwrite(fname, self.image)
        else:
            print("Error")
    def Img_save(self):
        self.image=self.temp
        fname, _ = QFileDialog.getSaveFileName(self, "save file", QDir.homePath(), "Images (*.jpg);;png(*.png)")
        if fname:
            cv2.imwrite(fname,self.image)
        else:
            print("Error")

    def Img_read(self):
        fname, _ = QFileDialog.getOpenFileName(self, "open file", QDir.homePath(), "Images (*)")
        self.Handle_ui
        self.image = cv2.imread(fname)
        self.temp =self.image
        self.Img_show(1)

    def Img_show(self,window =1):
        #self.Img_resize()
        p =self.convert_cv_qt()

        if window ==1:
            self.label.setPixmap(p)
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        if window ==2:
            self.label_2.setPixmap(p)
            self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

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
window = TUI()
window.show()
app.exec_()
