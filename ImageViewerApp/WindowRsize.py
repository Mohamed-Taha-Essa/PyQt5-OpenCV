
from Header import *

class Window_resize(QtWidgets.QMainWindow):
    def __init__(self,image):
        super(Window_resize, self).__init__()
        uic.loadUi('wind_resize.ui', self)
        self.new_width = None
        self.new_height = None
        self.image = image

        self.label_width.setText(str(self.image.shape[1]))
        self.label_height.setText(str(self.image.shape[0]))

        self.lineEdit.setValidator(QIntValidator())
        self.lineEdit_2.setValidator(QIntValidator())
        self.Button_apply.clicked.connect(self.apply)


    def apply(self):
        self.new_width =int(self.lineEdit.text())
        self.new_height =int(self.lineEdit_2.text())
        self.newimage=cv2.resize(self.image ,(self.new_width,self.new_height),interpolation=cv2.INTER_AREA )
        fname, _ = QFileDialog.getSaveFileName(self, "save file", QDir.homePath(), "Images (*.jpg);; (*.png);;(*.jpeg)")
        if fname:
            cv2.imwrite(fname,self.newimage)
        else:
            print("Error")
        print(self.lineEdit.text())
        print(self.lineEdit_2.text())



