import tkinter as tk
import requests
from time import sleep
import random

"""
    Sensor list for base tests:
        1 quad encoder on each wheel (front left, front right, back left, back right)
        1 distance sensor on each side of robot (front, back, left, right)
"""

class SensorGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        # Front left quad encoder
        self.t_qfl = "Quad Front Left: "
        self.tv_qfl = tk.StringVar()
        self.tv_qfl.set(self.t_qfl + str(-1))
        self.lbl_qfl = tk.Label(self, textvariable=self.tv_qfl)
        self.lbl_qfl.grid(column=0, row=0)

        #Front right quad encoder
        self.t_qfr = "Quad Front Right: "
        self.tv_qfr = tk.StringVar()
        self.tv_qfr.set(self.t_qfr + str(-1))
        self.lbl_qfr = tk.Label(self, textvariable=self.tv_qfr)
        self.lbl_qfr.grid(column=2, row=0)

        #Back left quad encoder
        self.t_qbl = "Quad Back Left: "
        self.tv_qbl = tk.StringVar()
        self.tv_qbl.set(self.t_qbl + str(-1))
        self.lbl_qbl = tk.Label(self, textvariable=self.tv_qbl)
        self.lbl_qbl.grid(column=0, row=3)

        #Back right quad encoder
        self.t_qbr = "Quad Back Right: "
        self.tv_qbr = tk.StringVar()
        self.tv_qbr.set(self.t_qbr + str(-1))
        self.lbl_qbr = tk.Label(self, textvariable=self.tv_qbr)
        self.lbl_qbr.grid(column=2, row=3)

        #Front distance sensor
        self.t_df = "Distance Front: "
        self.tv_df = tk.StringVar()
        self.tv_df.set(self.t_df + str(-1))
        self.lbl_df = tk.Label(self, textvariable=self.tv_df)
        self.lbl_df.grid(column=1, row=0)

        #Back distance sensor
        self.t_db = "Distance Back: "
        self.tv_db = tk.StringVar()
        self.tv_db.set(self.t_db + str(-1))
        self.lbl_db = tk.Label(self, textvariable=self.tv_db)
        self.lbl_db.grid(column=1, row=3)

        #Left distance sensor
        self.t_dl = "Distance Left: "
        self.tv_dl = tk.StringVar()
        self.tv_dl.set(self.t_dl + str(-1))
        self.lbl_dl = tk.Label(self, textvariable=self.tv_dl)
        self.lbl_dl.grid(column=0, row=1)

        #Right distance sensor
        self.t_dr = "Distance Right: "
        self.tv_dr = tk.StringVar()
        self.tv_dr.set(self.t_dr + str(-1))
        self.lbl_dr = tk.Label(self, textvariable=self.tv_dr)
        self.lbl_dr.grid(column=2, row=1)
    
    def updateSensorValues(self, valueDict):
        self.tv_db.set(self.t_db + str(valueDict['db']))
        self.tv_df.set(self.t_df + str(valueDict['df']))
        self.tv_dl.set(self.t_dl + str(valueDict['dl']))
        self.tv_dr.set(self.t_dr + str(valueDict['dr']))
        self.tv_qbl.set(self.t_qbl + str(valueDict['qbl']))
        self.tv_qbr.set(self.t_qbr + str(valueDict['qbr']))
        self.tv_qfl.set(self.t_qfl + str(valueDict['qfl']))
        self.tv_qfr.set(self.t_qfr + str(valueDict['qfr']))

    def testUpdate(self):
        valueDict = {
            'db': random.randint(0, 100),
            'df': random.randint(0, 100),
            'dl': random.randint(0, 100),
            'dr': random.randint(0, 100),
            'qbl': random.randint(0, 100),
            'qbr': random.randint(0, 100),
            'qfl': random.randint(0, 100),
            'qfr': random.randint(0, 100)
        }
        self.updateSensorValues(valueDict)
        self.after(1000, self.testUpdate)
        

if __name__ == '__main__':
    gui = SensorGUI()
    gui.master.title('Sensors!!')
    gui.after(1000, gui.testUpdate) #Used to make sure everything updates
    gui.mainloop()