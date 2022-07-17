import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import StringVar
from tkinter.messagebox import showinfo

class GUI:
    def fileselect():
        filetype = (('text files', '*.txt'),('.csv files', '*.csv'),('all files', '*.*'))
        filename = fd.askopenfilename(
            title = 'open file',
            initialdir= '/',
            filetypes = filetype
            )
        
        showinfo(
            title = 'selected file',
            message = filename
            )



class MainView(GUI):
    
    
    def __init__(self):
        
        def fileselect():
            filetype = (('text files', '*.txt'),('.csv files', '*.csv'),('all files', '*.*'))
            filename = fd.askopenfilename(
                title = 'open file',
                initialdir= '/',
                filetypes = filetype
                )
        
            showinfo(
                title = 'selected file',
                message = filename
                )

        def adv_search():
            _adv_search = tk.Tk()
            _adv_search.geometry("100x100")
            _adv_search_frame = ttk.Frame(_adv_search, padding = 10)
            _adv_search_frame.grid()
            en2 = ttk.Entry(_adv_search_frame).grid(row= 1, column= 0)
            _adv_search.mainloop()


        try: main_window
        except NameError: main_window = tk.Tk()
        main_window.geometry("500x200")

        self.label = ttk.Label(main_window, text="MainWindow1")
        self.label.grid(row= 1, column= 0)
        
        en1 = tk.Entry(main_window)
        en1.grid(row= 1, column= 0)

        btn1 = tk.Button(main_window, text= "-->").grid(row=1, column=1, padx=10)
        btn2 = tk.Button(main_window, text= "Advanced Search"
                         ,command= adv_search) 
        btn2.grid(row=2, column = 0)
        btn3 = tk.Button(main_window, text ="Import dataset"
                         ,command= fileselect)  
        btn3.grid(column= 0, pady= 5)

        ttk.Label(main_window, text= "datasets").grid(row=0, column=3)
        self.cntr = None
        main_window.mainloop()

    def search(controller):
        self.cntr.getResponse()

    
    
    
    
    

    def set_controller(self, controller):
        self.controller = controller