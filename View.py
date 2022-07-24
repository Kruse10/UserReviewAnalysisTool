from PyQt5.QtCore import QObject
from abc import ABC, abstractmethod, ABCMeta
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import *

import sys

def window(self, c):
    app = qtw.QApplication(sys.argv)
        
    win = MainWindow(c)
    c.set_view(win)
    win.show()
    
    sys.exit(app.exec_())

class abcView_Meta(type(QMainWindow), type(ABCMeta)): pass

class ab_View(QMainWindow):
    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def initUI(self): pass

class ColWindow(ab_View):
    def __init__(self, controller ,col_title, row1):
        super().__init__()
        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle("column select")
     #labels of current column titles and dropdowns of expected values  
    def initUI(self):
        pass
    
    def assign_cols(new_collist):
        pass
        
class VisWindow(ab_View):
    __metaclass__ = abcView_Meta
    def __init__(self):
        super(ab_View, self).__init__()

    def initUI(self):
        pass

class ASWindow(ab_View):
    __metaclass__ = abcView_Meta
    def __init__(self, c, p):
        super(ab_View, self).__init__()
        self.parentwindow = p
        self.controller = c
        self.movielist = []
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
        self.e4.setPlaceholderText("Cast\crew")

        self.b1 = qtw.QPushButton(self)
        self.b1.move(100,0)
        self.b1.setText("-->")
        self.b1.clicked.connect(self.clicked)


    def clicked(self):
        
        newmovielist = self.controller.get_adv_search(self.e1.text(), self.e2.text(), self.e3.text(), self.e4.text())
        for mov in newmovielist:
            if mov in self.movielist:
                newmovielist.remove(mov)

        lw_list = []
        if len(newmovielist) > 0:
            for x in range(len(self.movielist)):
                lw_list.append(self.parentwindow.lb1.item(x).text())
            
            for item in newmovielist:
                if item.get_str() not in lw_list:
                    self.parentwindow.lb1.addItem(item.get_str())
       


class MainWindow(ab_View): 
    __metaclass__ = abcView_Meta
    def __init__(self, c):
        super(ab_View, self).__init__()
        self.setGeometry(100, 100, 350, 400)
        self.setWindowTitle("Dataset Entry")
        self.controller = c
        self.initUI()
        self.movielist= []

    def initUI(self): 
        self.b1 = qtw.QPushButton(self)
        self.b1.move(180,10)
        self.b1.resize(150, 30)
        self.b1.setText("-->")
        self.b1.clicked.connect(self.clicked)
        
        self.b2 = qtw.QPushButton(self)
        self.b2.move(10 , 85)
        self.b2.resize(150,30)
        self.b2.setText("import dataset")
        self.b2.clicked.connect(self.openFile)

        self.b3 = qtw.QPushButton(self)
        self.b3.move(10, 50)
        self.b3.resize(150, 30)
        self.b3.setText("Advanced search")
        self.b3.clicked.connect(self.advanced_search)

        self.e1 = qtw.QLineEdit(self)
        self.e1.move(10, 10)
        self.e1.resize(150,30)
        self.e1.setMaxLength(20)
        self.e1.setPlaceholderText("Query")

        self.lb1 = qtw.QListWidget(self)
        self.lb1.resize(328, 280)
        self.lb1.move(10,120)

        self.b4 = qtw.QPushButton(self)
        self.b4.resize(150, 30)
        self.b4.move(180, 45)
        self.b4.setText("analyze datasets")
        self.b4.clicked.connect(self.analyze_dataset)

        self.dd1 = qtw.QComboBox(self)
        self.dd1.addItems(['vis1', 'vis2', 'vis3'])
        self.dd1.resize(150, 30)
        self.dd1.move(180, 80)

    def clicked(self):
        newmovielist = self.controller.request_search(self.e1.text())
        for mov in newmovielist:
            if mov in self.movielist:
                newmovielist.remove(mov)

        lw_list = []
        if len(newmovielist) > 0:
            for x in range(len(self.movielist)):
                lw_list.append(self.lb1.item(x).text())
            
            for item in newmovielist:
                if item.get_str() not in lw_list:
                    self.lb1.addItem(item.get_str())
        

    def analyze_dataset():
        lw_list = []
        for x in range(self.lb1.count()):
            lw_list.append(self.lb1.item(x).url)
        df = self.controller.gather_data(lw_list)

        create_new_plot()


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
        self.w = ASWindow(self.controller, self)
        self.w.show()
        pass
        

    