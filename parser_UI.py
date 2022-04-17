from Parser_tree_vis import *
import pyqt5_tools
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, qApp
import sys
from PyQt5.QtGui import QIcon
import cv2
from numpy import *

'''
:parameters:
click_x : record the previous x about clicking
click_y : record the previous y about clicking
label   : use to paint the graphic
size_x : use to define the width of picture
size_y : use to define the height of picture
img_path : use to find the loc of img
scene_x : use to define the scroll area size
scene_y : use to define the scroll area size
scale_coe : use to record the scale condition
'''
FIXED_WIDTH = 1500
FIXED_HEIGHT = 1000
FACTOR = 500

class MyParserTree(Ui_ParserTree,QMainWindow):
    def __init__(self, img_path, parent=None):
        super(MyParserTree, self).__init__(parent)
        self.setupUi(self)
        self.click_x = 0
        self.click_y = 0
        self.label = QLabel()

        self.img_path = img_path
        try:
            file = cv2.imread(img_path)
        except:
            QMessageBox.critical(self, "Wrong", "The figure is too large, please check in " + self.img_path)
            return
        self.size_x = file.shape[1]          # obtain the width of the generating figure
        self.size_y = file.shape[0]          # obtain the height of the generating figure
        self.scene_x = self.size_x if self.size_x <= FIXED_WIDTH else FIXED_WIDTH
        self.scene_y = self.size_y if self.size_y <= FIXED_HEIGHT else FIXED_HEIGHT
        self.scrollArea.resize(self.scene_x, self.scene_y)
        self.resize(self.scene_x, self.scene_y)
        self.setFixedSize(self.scene_x, self.scene_y)
        self.scale_coe = 1
        self.paint_graphic()

    '''
    function: finish the process of painting and show it onto the scroll area
    '''
    def paint_graphic(self):
        pixmap = QPixmap(self.size_x, self.size_y)
        paint = QPainter()
        paint.begin(pixmap)
        paint.drawPixmap(0, 0, self.size_x, self.size_y, QPixmap(self.img_path))
        paint.end()
        self.scrollArea.setWidget(self.label)
        self.label.setPixmap(pixmap)

    '''
    function: redefine the process of mousemove
    '''
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        mouse_x = a0.x()
        mouse_y = a0.y()
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() + self.click_y - mouse_y)
        self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() - mouse_x + self.click_x)
        self.click_x = mouse_x
        self.click_y = mouse_y

    '''
    function: redefine the process of mousepress
    '''
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        mouse_x = a0.x()
        mouse_y = a0.y()
        self.click_x = mouse_x
        self.click_y = mouse_y

    '''
    function: redefine the process of wheel event, in order to scale the image when the mouse outside the scroll area
    '''
    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if 0 <= a0.x() <= 1500 and 0 <= a0.y() <= 1000:
            return
        if a0.angleDelta().y() > 0 and self.scale_coe <= 3:
            self.size_x += 500
            self.size_y += 500
            self.scale_coe += 1
            self.paint_graphic()
        elif a0.angleDelta().y() < 0 and self.scale_coe > 0:
            if self.size_x < FACTOR + self.scene_x or self.size_y < FACTOR + self.scene_y:
                return
            self.size_x -= 500
            self.size_y -= 500
            self.scale_coe -= 1
            self.paint_graphic()

