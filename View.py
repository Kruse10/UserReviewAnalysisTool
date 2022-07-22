from PyQt5.QtCore import QObject
from abc import ABC, abstractmethod, ABCMeta
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import *

import sys

def window(self, c):
    app = qtw.QApplication(sys.argv)
        
    win = MainView(c)
    c.set_view(win)
    win.show()
    
    sys.exit(app.exec_())

class abcView_Meta(type(QMainWindow), type(ABCMeta)): pass

class abcView(QMainWindow):
    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def initUI(self): pass

class ColWindow(abcView):
    def __init__(self, col_title, row1):
        super().__init__()
        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle("column select")
       
    def initUI(self):
        pass
        #labels of current column titles and dropdowns of expected values

class ASWindow(abcView):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 200, 120)
        self.setWindowTitle("AdvancedSearch")
        self.initUI()
    

    def initUI(self):
        self.e1 = qtw.QLineEdit(self)
        self.e1.setMaxLength(20)
        self.e1.setPlaceholderText("Query")

        self.e2 = qtw.QLineEdit(self)
        self.e2.setMaxLength(20)
        self.e2.move(0, 30)
        self.e2.setPlaceholderText("Director")

        self.e3 = qtw.QLineEdit(self)
        self.e3.setMaxLength(20)
        self.e3.move(0, 60)
        self.e3.setPlaceholderText("Year")

        self.e4 = qtw.QLineEdit(self)
        self.e4.setMaxLength(20)
        self.e4.move(0, 90)
        self.e4.setPlaceholderText("Actor")

        self.b1 = qtw.QPushButton(self)
        self.b1.move(100,0)
        self.b1.setText("-->")
        self.b1.clicked.connect(self.clicked)


    def clicked(self):
        
        #links = self.controller.get_adv_search(e1.get(), e2.get(), e3.get())
        pass


class MainView(abcView): 
    __metaclass__ = abcView_Meta
    def __init__(self, c):
        super(abcView, self).__init__()
        self.setGeometry(100, 100, 500, 570)
        self.setWindowTitle("Main Window")
        self.controller = c
        self.initUI()

    def initUI(self): 
        #actual layout is still a little jank at the moment 
        self.label = qtw.QLabel(self)
        self.label.setText("search")
        self.label.move(0,0)

        self.b1 = qtw.QPushButton(self)
        self.b1.move(130,0)
        self.b1.setText("-->")
        self.b1.clicked.connect(self.clicked)

        
        self.b2 = qtw.QPushButton(self)
        self.b2.move(130, 75)
        self.b2.setText("import dataset")
        self.b2.clicked.connect(self.openFile)

        self.b3 = qtw.QPushButton(self)
        self.b3.move(130, 50)
        self.b3.setText("Advanced search")
        self.b3.clicked.connect(self.advanced_search)

        self.e1 = qtw.QLineEdit(self)
        self.e1.setMaxLength(20)
        self.e1.setPlaceholderText("Query")

        self.lb1 = qtw.QListWidget(self)
        self.lb1.resize(200, 500)
        self.lb1.move(250, 25)

        self.b4 = qtw.QPushButton(self)
        self.b4.move(250, 530)
        self.b4.setText("analyze datasets")
        self.b4.clicked.connect(self.analyze_dataset)

    def clicked(self):
       
        links =  self.controller.request_search(self.e1.text())

        #next 6 lines prevent duplicate additions
        lw_list = []
        for x in range(self.lb1.count()):
            lw_list.append(self.lb1.item(x).text())
            
        for item in links:
            if item not in lw_list:
                self.lb1.addItem(item)
        
        initialsearch = None
        

    def analyze_dataset():
        #call method in controller and pass contents of lb1
        pass

    def openFile(self):
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",".csv (*.csv)", options=options)
        
        #next 6 lines prevent duplicate additions
        lw_list = []
        for x in range(self.lb1.count()):
            lw_list.append(self.lb1.item(x).text())
        if fileName not in lw_list:
            self.lb1.addItem(fileName)
            
   
    def advanced_search(self):
        self.w = ASWindow()
        self.w.show()
        
    def select_link(self, l):
        #get titles from all lists
        selecttitle=SelectTitle()
        win = SelectWindow(selecttitle.get_title(l))
        win.show()

        
        

        selecttitle = None
        '''self.w = SelectWindow(titles)
        self.w.show()
        return w.getlink()'''
        pass
        

    