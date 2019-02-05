import tkinter as tk
import requests
from time import sleep

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
        self.v_qfl = -1
        self.tv_qfl = tk.StringVar()
        self.tv_qfl.set(self.t_qfl + str(self.v_qfl))
        self.lbl_qfl = tk.Label(self, textvariable=self.tv_qfl)
        self.lbl_qfl.grid(column=0, row=0)

        #Front right quad encoder
        self.t_qfr = "Quad Front Right: "
        self.v_qfr = -1
        self.tv_qfr = tk.StringVar()
        self.tv_qfr.set(self.t_qfr + str(self.v_qfr))
        self.lbl_qfr = tk.Label(self, textvariable=self.tv_qfr)
        self.lbl_qfr.grid(column=2, row=0)

        #Back left quad encoder
        self.t_qbl = "Quad Back Left: "
        self.v_qbl = -1
        self.tv_qbl = tk.StringVar()
        self.tv_qbl.set(self.t_qbl + str(self.v_qbl))
        self.lbl_qbl = tk.Label(self, textvariable=self.tv_qbl)
        self.lbl_qbl.grid(column=0, row=3)

        #Back right quad encoder
        self.t_qbr = "Quad Back Right: "
        self.v_qbr = -1
        self.tv_qbr = tk.StringVar()
        self.tv_qbr.set(self.t_qbr + str(self.v_qbr))
        self.lbl_qbr = tk.Label(self, textvariable=self.tv_qbr)
        self.lbl_qbr.grid(column=2, row=3)

        #Front distance sensor
        self.t_df = "Distance Front: "
        self.v_df = -1
        self.tv_df = tk.StringVar()
        self.tv_df.set(self.t_df + str(self.v_df))
        self.lbl_df = tk.Label(self, textvariable=self.tv_df)
        self.lbl_df.grid(column=1, row=0)

        #Back distance sensor
        self.t_db = "Distance Back: "
        self.v_db = -1
        self.tv_db = tk.StringVar()
        self.tv_db.set(self.t_db + str(self.v_db))
        self.lbl_db = tk.Label(self, textvariable=self.tv_db)
        self.lbl_db.grid(column=1, row=3)

        #Left distance sensor
        self.t_dl = "Distance Left: "
        self.v_dl = -1
        self.tv_dl = tk.StringVar()
        self.tv_dl.set(self.t_dl + str(self.v_dl))
        self.lbl_dl = tk.Label(self, textvariable=self.tv_dl)
        self.lbl_dl.grid(column=0, row=1)

        #Right distance sensor
        self.t_dr = "Distance Right: "
        self.v_dr = -1
        self.tv_dr = tk.StringVar()
        self.tv_dr.set(self.t_dr + str(self.v_dr))
        self.lbl_dr = tk.Label(self, textvariable=self.tv_dr)
        self.lbl_dr.grid(column=2, row=1)
    
    def updateSensorValues(self, valueDict):
        self.v_db = valueDict['db']
        self.v_df = valueDict['df']
        self.v_dl = valueDict['dl']
        self.v_dr = valueDict['dr']
        self.v_qbl = valueDict['qbl']
        self.v_qbr = valueDict['qbr']
        self.v_qfl = valueDict['qfl']
        self.v_qfr = valueDict['qfr']
        

if __name__ == '__main__':
    gui = SensorGUI()
    gui.master.title('Sensors!!')
    gui.mainloop()
        