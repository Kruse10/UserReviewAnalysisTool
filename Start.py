from PyQt5.QtWidgets import QApplication, QWidget as qa
import Model
import View
import Controller
import sys

class App():
    def __init__(self):
        super().__init__()
        

        #create model
        model = Model.DataModel()

        #create view
       
        controller = Controller.MainController(model)
        
        view = View.window(self, controller)  
       
if __name__ == '__main__':
      
    a = App()