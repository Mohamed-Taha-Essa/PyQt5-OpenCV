from Header import *
from WindowRsize import Window_resize
from PyQt5 import QtCore, QtGui, QtWidgets

class View(QtWidgets.QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        uic.loadUi('design.ui', self)




        self.window_resize =None
        self.image=None
        self.temp =None
        self.w = None
        # what will happen if i click on button i will call func HandlerButton
        self.Show_button_2.clicked.connect(self.Img_read)
        self.Rotate_button_2.clicked.connect(self.Img_rotate)
        # setting icon to the button
        self.Rotate_button_2.setIcon(QIcon('icons-rotate2.png'))
        # self.pushButton.clicked.connect(self.printe)
        #
        # # file main window
        self.actionresize.triggered.connect(self.window2_resize)



    ####################################################################
    def resizeEvent(self, event):
        print("Window has been resized")
        self.Img_resize
        QtWidgets.QMainWindow.resizeEvent(self, event)
        print(type(self.label_2.height()) ,self.label_2.width())

    def Img_resize(self):
        self.image=cv2.resize(self.image,(int(self.label_2.width())),int(self.label_2.height()))
        print(self.image.shape)
        self.Img_show(1)

    def window2_resize(self):  # <===
        self.window_resize = Window_resize(self.image)
        self.window_resize.show()

    def Img_rotate(self):
        #self.image =self.temp
        self.image =cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        self.Img_show(1)
    def Handle_Viewer(self):
        pass

    def Img_read(self):
        fname, _ = QFileDialog.getOpenFileName(self, "open file", QDir.homePath(), "Images (*);;img(*.png)")

        self.image = cv2.imread(fname)
        self.temp = self.image

        title = fname.split('/')[-1]
        self.setWindowTitle(title)

        self.Img_show(1)

    def Img_show(self, window=1):
        # self.Img_resize()
        p = self.convert_cv_qt()

        if window == 1:
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
            high, width, ch = rgb_image.shape
            bytes_per_line = ch * width
            convert_to_Qt_format = QtGui.QImage(rgb_image.data, width, high, bytes_per_line, qformat)
            p = convert_to_Qt_format.scaled(width, high, QtCore.Qt.KeepAspectRatio)
        else:
            img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
            p = img.rgbSwapped()

        return QPixmap.fromImage(p)


app = QtWidgets.QApplication(sys.argv)
window = View()
window.show()
app.exec_()
