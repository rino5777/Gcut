import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import ImageGrab
import numpy as np
import cv2
import glob
import os
from PIL import Image
import time
import datetime
import uuid


class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    writer=[]
    
    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowOpacity(0.5)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 2

        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        print(self.start_point, self.end_point)
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
#         print(self.end_point)
        self.update()
         




   
    def mouseReleaseEvent(self, QMouseEvent):
        r = QtCore.QRect(self.start_point, self.end_point).normalized()
        img = ImageGrab.grab(bbox=r.getCoords())

        c = 0.0
        now = datetime.datetime.now()
        while now.second + 5 != datetime.datetime.now().second:
            for i in range(5):
                img = ImageGrab.grab(bbox=(r.left(), r.top(), r.right(), r.bottom())) #x, y, w, h
                img_np = np.array(img)
                frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    #             cv2.imshow("frame", frame)
                
                writer = img_np
                img = Image.fromarray(writer, 'RGB')
                c+=0.1
                img.save('forgif/my{}.png'.format(c))
                cv2.destroyAllWindows()
        else:
            w = MainWindow()
            w.resize(400, 300)
            w.show()

#         cv2.destroyAllWindows()
        self.hide()
        frames = [Image.open(image) for image in glob.glob(f"forgif/*.png")]
        frame_one = frames[0]
        frame_one.save("my_{}.gif".format(uuid.uuid4().hex), format="GIF", append_images=frames,
               save_all=True, duration=60, loop=0)
        cwd = os.getcwd()
        os.chdir("/".join(cwd.split("\\"))+'/forgif')
        files=glob.glob('*.png')
        for i in files:
            os.unlink(i)

    def paintEvent(self, event):
        trans = QtGui.QColor('6ECCAF')
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(
            QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness)
        )
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)
#         print(r)
       

class MainWindow(QtWidgets.QMainWindow): #главное окно 
    writer=[]

    def __init__(self):
        super().__init__()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setStyleSheet("background-color: #05445E;")
        self.setWindowTitle('Gcut')
        self.setWindowIcon(QtGui.QIcon('logo.png'))
       
        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.button = QtWidgets.QPushButton('Make gif')
        self.button.setStyleSheet("background-color : #B1D4E0")
        self.button.clicked.connect(self.activateSnipping)
        
        

        layout = QtWidgets.QVBoxLayout(self.centralWidget) #добавление кнопок в окно
        layout.addWidget(self.label, 1)
        layout.addWidget(self.button, 0)
        self.snipper = SnippingWidget()
        
        
    

    def activateSnipping(self):
        self.snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.hide()
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)        
    w = MainWindow()
    w.resize(400, 300)
    w.show()
    sys.exit(app.exec_())