import tkinter as tk
import requests
from time import sleep

class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.timevar = tk.StringVar()
        self.timevar.set('test')
        self.grid()
        self.label = tk.Label(self, textvariable=self.timevar)
        self.label.grid(column=0, row=0)
        #self.button = tk.Button(self, text='Start', comman=self.startGet)
        #self.button.grid()

    def updateTime(self):
        self.timevar.set(self.getTime())
        self.label.grid(column=0, row=0)
        self.after(2000, self.updateTime)
        

    def getTime(self):
        r = requests.get('http://worldclockapi.com/api/json/est/now')
        return r.text

    def startGet(self):
        self.updateTime()

gui = GUI()
gui.master.title('Sample time')
gui.after(10, gui.updateTime)
gui.mainloop()