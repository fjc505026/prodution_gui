import tkinter as tk
from view import View
from controller import Controller
from model import Model

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Definium Prodution Test Tool")
        self.geometry('1200x1000+50+50')
        # create a model
        self.model = Model('')
        # create a view and place it on the root window
        self.view = View(self)
        # create a controller
        self.controller = Controller(self.model,self.view)

        # set the controller to view
        self.view.set_controller(self.controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()