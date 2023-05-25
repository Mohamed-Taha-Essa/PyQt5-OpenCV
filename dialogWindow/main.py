
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox,QPushButton,QLabel,QFileDialog
from PyQt5.QtGui import QPixmap
import sys
import urllib.request

class ImgEdit(QtWidgets.QMainWindow):
    def __init__(self,flag=0):
        super(ImgEdit, self).__init__()
        uic.loadUi('main.ui', self)
        self.Handle_ui()
        self.Handle_button()
        # creating a push button
        self.button=self.findChild(QPushButton,"pushButton")
        self.label=self.findChild(QLabel,"label")
        #what will happen if i click on button i will call func HandlerButton
        self.button.clicked.connect(self.Handle_button)

    ####################################################################
    def Handle_ui(self):
        self.setWindowTitle("Taha Downloader")
        #self.setFixedSize(544,310)

    def Handle_button(self):
        #self.label.setText("you clicked on butoon")
        # if button is checked
        #print(self.pushButton.isChecked())

        fname =QFileDialog.getOpenFileNames(self ,"open File " ,"""starting directory""" ,\
                                                            "All files(*);;imag files(*.png)")
        if fname :
            # open the Image
            self.pixmap = QPixmap(fname[0])
            # add image to label
            self.label.setPixmap(self.pixmap)


app = QtWidgets.QApplication(sys.argv)
window = ImgEdit()
window.show()
app.exec_()