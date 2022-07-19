
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import *
import sys


def window(self, c):
    app = qtw.QApplication(sys.argv)
        
    win = MainView(c)
    c.set_view(win)
    win.show()
    
    sys.exit(app.exec_())


class MainView(QMainWindow): #might just switch this back to the PYQt5 version i tried before
  
    def __init__(self, c):
        super(MainView, self).__init__()
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle("Main Window")
        self.controller = c
        self.initUI()

    def initUI(self):
        pass

       


   
        
        

    def start(self):
        pass