# -*- coding:UTF-8 -*-
'''
Created on 10 sept. 2014

@author: michael
'''
from tkinter import Tk
import hmi.MainGui as MainGui
import hmi.GuiController as GuiController
import db.DBUtils as DBUtils
import Inittools as Inittools
import os
    
if __name__ == '__main__':
    ini = Inittools.Inittools("tt.ini")
    db = DBUtils.DBUtils(ini.props["dbname"])
    controller = GuiController.GuiController(db)
    mainWnd = Tk()
    mainWnd.resizable(True, True)
    mainWnd.title("Time Tracker")
    mainWnd.wm_attributes("-topmost", 1)
    mainWnd.geometry(ini.props["width"] + "x" + ini.props["height"] + "+" + ini.props["positionX"] + "+" + ini.props["positionY"])
    gui = MainGui.MainGui(mainWnd, controller, ini)
    controller.setMainGui(gui)
    gui.mainloop()
    

