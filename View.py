
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
        self.label = qtw.QLabel(self)
        self.label.setText("search")
        self.label.move(0,0)

        self.b1 = qtw.QPushButton(self)
        self.b1.move(150,25)
        self.b1.setText("-->")
        self.b1.clicked.connect(self.clicked)

        self.e1 = qtw.QLineEdit(self)
        self.e1.setMaxLength(20)
        self.e1.setPlaceholderText("Query")
        self.e1.textEdited.connect(self.text_edited)

    def clicked(self):
        #links = self.controller.get_search(e1.get())
        pass

    def text_edited(self, s):
        print(self.e1.text())

       


   
        
        

    def start(self):
        pass