from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import *
import sys

def window(self, c):
    app = qtw.QApplication(sys.argv)
        
    win = MainView(c)
    c.set_view(win)
    win.show()
    
    sys.exit(app.exec_())

class SelectWindow(QMainWindow):
    def __init__(self, titles):
        super().__init__()
        self.setGeometry(100, 100, 200, 120)
        self.setWindowTitle("select")
        initUI(titles)

    def initUI(self, titles):
        self.dd1 = QComboBox()
        self.dd1.move(0,0)
        self.list_items = List()
        for title in titles:
            self.dd1.addItem(title)


class ColWindow(QMainWindow):
    def __init__(self, col_title, row1):
        super().__init__()
        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle("column select")
       
    def initUI(self):
        pass
        #labels of current column titles and dropdowns of expected values

class ASWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 200, 120)
        self.setWindowTitle("AdvancedSearch")
        self.initUI()
    

    def initUI(self):
        self.e1 = qtw.QLineEdit(self)
        self.e1.setMaxLength(20)
        self.e1.setPlaceholderText("Query")
        self.e1.textEdited.connect(self.text_edited)

        self.e2 = qtw.QLineEdit(self)
        self.e2.setMaxLength(20)
        self.e2.move(0, 30)
        self.e2.setPlaceholderText("Director")
        self.e2.textEdited.connect(self.text_edited)

        self.e3 = qtw.QLineEdit(self)
        self.e3.setMaxLength(20)
        self.e3.move(0, 60)
        self.e3.setPlaceholderText("Year")
        self.e3.textEdited.connect(self.text_edited)

        self.e4 = qtw.QLineEdit(self)
        self.e4.setMaxLength(20)
        self.e4.move(0, 90)
        self.e4.setPlaceholderText("Actor")
        self.e4.textEdited.connect(self.text_edited)

        self.b1 = qtw.QPushButton(self)
        self.b1.move(100,0)
        self.b1.setText("-->")
        self.b1.clicked.connect(self.clicked)


    def clicked(self):
        
        #links = self.controller.get_adv_search(e1.get(), e2.get(), e3.get())
        pass


class MainView(QMainWindow): 

    def __init__(self, c):
        super(MainView, self).__init__()
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
        initialsearch = InitialSearch()
        links = self.initialsearch.get_search(self.e1.text())
        print(links)


        #self.lb1.addItems(self.links)
        #call method to remove duplicate items from lb1

        initialsearch = None
        pass

    def analyze_dataset():
        #call method in controller and pass contents of lb1
        pass

    def openFile(self):
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",".csv (*.csv)", options=options)
        if fileName:
            controller.open_file()
            print(fileName)
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
        

    