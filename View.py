import tkinter
from tkinter import ttk


class MainView(ttk.Frame):
    def __init__(self, parent):
        super().__init__()
        
        self.label = ttk.Label(self, text="MainWindow1")
        self.label.grid(row= 1, column= 0)

        self.controller = None

    
        


    def set_controller(self, controller):
        self.controller = controller