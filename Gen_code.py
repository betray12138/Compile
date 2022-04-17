from inter_code import *
from Parser_tree_vis import *
import pyqt5_tools
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, qApp
import sys
from PyQt5.QtGui import QIcon
from numpy import *

HEIGHT = 800
WIDTH = 600

class Myinter_Code(Ui_Form, QMainWindow):
    def __init__(self, inter_code_list, parent = None):
        super(Myinter_Code, self).__init__(parent)
        self.setupUi(self)
        self.resize(WIDTH, HEIGHT)
        self.setFixedSize(WIDTH, HEIGHT)
        self.textBrowser.resize(WIDTH, HEIGHT)
        self.textBrowser.setFixedSize(WIDTH, HEIGHT)
        self.inter_code_list = inter_code_list
        self.textBrowser.setStyleSheet('background-image:url(' + 'bg.jpg' + ')')
        self.print()

    def print(self):
        for i in range(len(self.inter_code_list)):
            self.textBrowser.append(self.inter_code_list[i])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mycode = Myinter_Code(['123', '24'])
    mycode.show()
    sys.exit(app.exec_())