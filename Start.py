import tkinter as tk
import re
import Model
import View
import Controller


class App():
    def __init__(self):
        super().__init__()
        

        #create model
        model = Model.DataModel()

        #create view
        view = View.MainView()
        
        controller = Controller.MainController(model, view)
        
        view.set_controller(controller)

if __name__ == '__main__':
    a = App()
    
