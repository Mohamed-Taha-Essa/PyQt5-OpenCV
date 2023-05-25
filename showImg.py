from PyQt5.QtCore import QDir
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
import sys
import urllib.request


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('main.ui', self)
        self.width = self.label.width()
        self.height =self.label.height()

        # creating a push button
        self.button = self.findChild(QPushButton, "pushButton")
        self.label = self.findChild(QLabel, "label")
        # what will happen if i click on button i will call func HandlerButton
        self.button.clicked.connect(self.Handle_button)

    ####################################################################

    def Handle_ui(self):
        self.resize(512,512)
        # self.label.adjustSize()


    def Handle_button(self):
        fname, _ = QFileDialog.getOpenFileName(self, "open file", QDir.homePath(),
                                                "Images (*)")
        # fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
        #                                          QDir.homePath(), "Images (*.png *.xpm *.jpg *.bmp *.pdf)")
        print(fname)
        # open the Image
        self.pixmap = QPixmap(fname)
        self.width =self.pixmap.width()
        self.height =self.pixmap.height()
        print(self.width)
        # add image to label
        self.label.setPixmap(self.pixmap)
        w = self.label.width();
        h = self.label.height();




# from PyQt5.QtGui import QImageReader
#
# for image_formats in QImageReader.supportedImageFormats():
#     print(image_formats.data().decode())

app = QtWidgets.QApplication(sys.argv)
window = UI()
window.show()
app.exec_()
