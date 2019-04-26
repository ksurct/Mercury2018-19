import tkinter as tk
import requests
from time import sleep
import random

"""
    Sensor list for base tests:
        1 quad encoder on each wheel (front left, front right, back left, back right) NOT USING QUAD ENCODERS
        1 distance sensor on each side of robot (front, back, left, right)
"""

class SensorGUI(tk.Frame):
    def __init__(self, master=None, sensorLock=None, controlDataLock=None):
        self.sensorLock = sensorLock
        self.controlDataLock = controlDataLock
        self.hlOn = False
        self.limVal = 50
        tk.Frame.__init__(self, master)
        self.grid()

        # Front left quad encoder
        self.t_qfl = "Front Left Wheel"# "Quad Front Left: "
        self.tv_qfl = tk.StringVar()
        self.tv_qfl.set(self.t_qfl)# + str(-1))
        self.lbl_qfl = tk.Label(self, textvariable=self.tv_qfl)
        self.lbl_qfl.grid(column=0, row=1, padx=5, pady=5)

        #Front right quad encoder
        self.t_qfr = "Front Right Wheel" #"Quad Front Right: "
        self.tv_qfr = tk.StringVar()
        self.tv_qfr.set(self.t_qfr)# + str(-1))
        self.lbl_qfr = tk.Label(self, textvariable=self.tv_qfr)
        self.lbl_qfr.grid(column=4, row=1, padx=5, pady=5)

        #Back left quad encoder
        self.t_qbl = "Back Left Wheel" #"Quad Back Left: "
        self.tv_qbl = tk.StringVar()
        self.tv_qbl.set(self.t_qbl)# + str(-1))
        self.lbl_qbl = tk.Label(self, textvariable=self.tv_qbl)
        self.lbl_qbl.grid(column=0, row=5, padx=5, pady=5)

        #Back right quad encoder
        self.t_qbr = "Back Right Wheel" #"Quad Back Right: "
        self.tv_qbr = tk.StringVar()
        self.tv_qbr.set(self.t_qbr)# + str(-1))
        self.lbl_qbr = tk.Label(self, textvariable=self.tv_qbr)
        self.lbl_qbr.grid(column=4, row=5, padx=5, pady=5)

        #Front left distance sensor
        self.t_dfl = "Front left: "
        self.tv_dfl = tk.StringVar()
        self.tv_dfl.set(self.t_dfl)# + str(-1))
        self.lbl_dfl = tk.Label(self, textvariable=self.tv_dfl)
        self.lbl_dfl.grid(column=1, row=1, padx=5, pady=5)

        #Left side distance sensor
        self.t_dsl = "Left Side: "
        self.tv_dsl = tk.StringVar()
        self.tv_dsl.set(self.t_dsl + str(-1))
        self.lbl_dsl = tk.Label(self, textvariable=self.tv_dsl)
        self.lbl_dsl.grid(column=0, row=2, padx=5, pady=5)

        #Front right distance sensor
        self.t_dfr = "Front Right: "
        self.tv_dfr = tk.StringVar()
        self.tv_dfr.set(self.t_dfr + str(-1))
        self.lbl_dfr = tk.Label(self, textvariable=self.tv_dfr)
        self.lbl_dfr.grid(column=3, row=1, padx=5, pady=5)

        #Right side distance sensor
        self.t_dsr = "Right Side: "
        self.tv_dsr = tk.StringVar()
        self.tv_dsr.set(self.t_dsr + str(-1))
        self.lbl_dsr = tk.Label(self, textvariable=self.tv_dsr)
        self.lbl_dsr.grid(column=4, row=2, padx=5, pady=5)

        #Arm distance sensor
        self.t_da = "Arm"
        self.tv_da = tk.StringVar()
        self.tv_da.set(self.t_da)# + str(-1))
        self.lbl_da = tk.Label(self, textvariable=self.tv_da)
        self.lbl_da.grid(column=0, row=0, padx=5, pady=5)

        #Headlights button
        self.tv_hl = tk.StringVar()
        self.tv_hl.set("Turn headlights on")
        self.btn_hl = tk.Button(master, command=self.updateHL, textvariable=self.tv_hl)
        self.btn_hl.grid(column=0, row=6, padx=5, pady=5)

        #Entry box for limiter
        self.e_lim = tk.Entry(master)
        self.e_lim.insert(0, "50")
        self.e_lim.grid(column=1, row=7, padx=5, pady=5)

        #Button to update limiter
        self.btn_lim = tk.Button(master, command=self.updateLim, text="Update Motor Limiter")
        self.btn_lim.grid(column=0, row=7, padx=5, pady=5)
    
    def updateSensorValues(self, valueDict):
        if (valueDict['dfl'] < 52):
            self.lbl_dfl.config(foreground='red')
        else:
            self.lbl_dfl.config(foreground='black')
        self.tv_dfl.set(self.t_dfl + str(valueDict['dfl']))
        if (valueDict['dfr'] < 52):
            self.lbl_dfr.config(foreground='red')
        else:
            self.lbl_dfr.config(foreground='black')
        self.tv_dfr.set(self.t_dfr + str(valueDict['dfr']))
        if (valueDict['dsl'] < 52):
            self.lbl_dsl.config(foreground='red')
        else:
            self.lbl_dsl.config(foreground='black')
        self.tv_dsl.set(self.t_dsl + str(valueDict['dsl']))
        if (valueDict['dsr'] < 52):
            self.lbl_dsr.config(foreground='red')
        else:
            self.lbl_dsr.config(foreground='black')
        self.tv_dsr.set(self.t_dsr + str(valueDict['dsr']))
        #self.tv_da.set(self.t_da + str(valueDict['da']))
        #self.tv_qbl.set(self.t_qbl + str(valueDict['qbl']))
        #self.tv_qbr.set(self.t_qbr + str(valueDict['qbr']))
        #self.tv_qfl.set(self.t_qfl + str(valueDict['qfl']))
        #self.tv_qfr.set(self.t_qfr + str(valueDict['qfr']))

    def testUpdate(self):
        valueDict = {
            'dfl': random.randint(0, 100),
            'dfr': random.randint(0, 100),
            'dsl': random.randint(0, 100),
            'dsr': random.randint(0, 100),
            'da': random.randint(0, 100),
            'qbl': random.randint(0, 100),
            'qbr': random.randint(0, 100),
            'qfl': random.randint(0, 100),
            'qfr': random.randint(0, 100)
        }
        self.updateSensorValues(valueDict)
        self.after(1000, self.testUpdate)

    def getSensorValues(self):
        values = self.sensorLock.requestData()
        self.updateSensorValues(values)
        self.after(100, self.getSensorValues)

    def updateControlDataLock(self, HL):
        self.controlDataLock.updateGUIParams({'hl': HL, 'lim': self.limVal})

    def updateHL(self):
        if (self.hlOn == False):
            self.hlOn = True
            self.tv_hl.set("Turn headlights off")
            self.updateControlDataLock(1)
        else:
            self.hlOn = False
            self.tv_hl.set("Turn headlights on")
            self.updateControlDataLock(0)

    def updateLim(self):
        tempLim = self.e_lim.get()
        try:
            int(tempLim)
        except:
            self.e_lim.delete(0, len(tempLim) + 1)
            self.e_lim.insert(0, 50)
        self.limVal = self.e_lim.get()
        if (self.hlOn == False):
            self.updateControlDataLock(0)
        else:
            self.updateControlDataLock(1)

        

if __name__ == '__main__':
    gui = SensorGUI()
    gui.master.title('Sensors')
    gui.after(1000, gui.testUpdate) #Used to make sure everything updates
    gui.mainloop()