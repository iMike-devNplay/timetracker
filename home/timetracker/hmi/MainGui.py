# -*- coding:UTF-8 -*-
'''
Created on 16 sept. 2014

@author: michael
'''
from tkinter import *
from tkinter import messagebox, ttk

class MainGui(Frame):

    def geoliste(self, g):
        r=[i for i in range(0,len(g)) if not g[i].isdigit()]
        return [int(g[0:r[0]]),int(g[r[0]+1:r[1]]),int(g[r[1]+1:r[2]]),int(g[r[2]+1:])]

    def createWindow(self, title):
        wnd = Toplevel()
        wnd.resizable(True, True)
        wnd.title(title)
        screenWidth = wnd.winfo_screenwidth()
        #screenHeight = wndDisplayTask.winfo_screenheight()
        wnd.geometry("350x350+%d+%d" % (screenWidth-350, 125))
        return wnd

    def __init__(self, wnd, controller, ini, ** kwargs):
        self.ini = ini
        self.mainWnd = wnd
        self.mainWnd.protocol('WM_DELETE_WINDOW', self.actionBtnQuit)
        self.version = self.ini.props["version"]
        Frame.__init__(self, self.mainWnd, **kwargs)
        self.controller = controller
        #Menu de l'application
        #self.mnuMain = Menu(self)
        #self.mnuMain.add_command(label="?", command=self.actionBtnAbout)
        #self.mnuManageTask = Menu(self.mnuMain, tearoff=0)
        #self.mnuManageTask.add_command(label="Create a task", command=self.actionBtnManageTaskCreate)
        #self.mnuManageTask.add_command(label="Update a task", command=self.actionBtnManageTaskUpdate)
        #self.mnuManageTask.add_command(label="Remove a task", command=self.actionBtnManageTaskRemove)
        #self.mnuManageTask.add_command(label="Display tasks", command=self.actionBtnManageTaskDisplay)
        #self.mnuMain.add_cascade(label="Manage tasks", menu=self.mnuManageTask)
        #self.mnuTracker = Menu(self.mnuMain, tearoff=0)
        #self.mnuTracker.add_command(label="Add a tracker", command=self.actionBtnTrackerAdd)
        #self.mnuMain.add_cascade(label="Manage tracker", menu=self.mnuTracker)
        #self.mnuReport = Menu(self.mnuMain, tearoff=0)
        #self.mnuReport.add_command(label="Week-2", command=self.actionBtnReportWeekMinus2)
        #self.mnuReport.add_command(label="Last week", command=self.actionBtnReportLastWeek)
        #self.mnuReport.add_command(label="Current week", command=self.actionBtnReportCurrentWeek)
        #self.mnuReport.add_command(label="Display All", command=self.actionBtnReportDisplayAll)
        #self.mnuReport.add_command(label="Reset", command=self.controller.deleteAllTrackers)
        #self.mnuMain.add_cascade(label="Reports", menu=self.mnuReport)
        #self.mnuMain.add_command(label="Quit!", command=self.actionBtnQuit)
        #self.mainWnd.config(menu=self.mnuMain)

        self.info = PhotoImage(file='./img/info.' + self.ini.props["imgExt"])
        self.btnAbout = Button(self.mainWnd, image=self.info, command=self.actionBtnAbout)
        self.btnAbout.grid(row=0, column=0)
        #
        self.addTask = PhotoImage(file='./img/addTask.' + self.ini.props["imgExt"])
        self.btnCreateTask = Button(self.mainWnd, image=self.addTask, command=self.actionBtnManageTaskCreate)
        self.btnCreateTask.grid(row=0, column=1)
        #
        self.displayTask = PhotoImage(file='./img/displayTask.' + self.ini.props["imgExt"])
        self.btnDisplayTask = Button(self.mainWnd, image=self.displayTask, command=self.actionBtnManageTaskDisplay)
        self.btnDisplayTask.grid(row=0, column=2)
        #
        self.reportMinus2 = PhotoImage(file='./img/reportMinus2.' + self.ini.props["imgExt"])
        self.btnReportMinus2 = Button(self.mainWnd, image=self.reportMinus2, command=self.actionBtnReportWeekMinus2)
        self.btnReportMinus2.grid(row=0, column=3)
        #
        self.reportLastWeek = PhotoImage(file='./img/reportLastWeek.' + self.ini.props["imgExt"])
        self.btnReportLastWeek = Button(self.mainWnd, image=self.reportLastWeek, command=self.actionBtnReportLastWeek)
        self.btnReportLastWeek.grid(row=0, column=4)
        #
        self.reportCurrentWeek = PhotoImage(file='./img/reportCurrentWeek.' + self.ini.props["imgExt"])
        self.btnReportCurrentWeek = Button(self.mainWnd, image=self.reportCurrentWeek, command=self.actionBtnReportCurrentWeek)
        self.btnReportCurrentWeek.grid(row=0, column=5)
        #        
        self.displayAll = PhotoImage(file='./img/displayAll.' + self.ini.props["imgExt"])
        self.btnReportAll = Button(self.mainWnd, image=self.displayAll, command=self.actionBtnReportDisplayAll)
        self.btnReportAll.grid(row=0, column=6)
        #
        self.currentAction = StringVar()
        self.btnStartStopTask = Button(self.mainWnd, textvariable=self.currentAction, command=self.actionBtnStartStopTask)
        self.btnStartStopTask.grid(row=0, column=7)

        #Affichage de la tâche en cours
        self.currentTaskName = StringVar()
        self.lblCurrentTaskName = Label(self.mainWnd, textvariable=self.currentTaskName)
        
        self.startTask = PhotoImage(file='./img/startTask.' + self.ini.props["imgExt"])
        self.stopTask = PhotoImage(file='./img/stopTask.' + self.ini.props["imgExt"])
        
        self.taskStarted = self.updateCurrentTaskName()
        
        
    def updateCurrentTaskName(self):
        self.current = self.controller.getCurrentTask()
        if self.current is None:
            self.mainWnd.title("No current Task !!!")
            #self.currentTaskName.set("No current Task !!!")
            self.currentAction.set("Start")
            self.btnStartStopTask.configure(image=self.startTask)
            return False
        else:
            currentTracker = self.current[0]
            currentTask = self.current[1]
            self.mainWnd.title(currentTask.name + " (Begin=" + currentTracker.begin_timestamp + ")")
            #self.currentTaskName.set(currentTask.name + " (Begin=" + currentTracker.begin_timestamp + ")")
            self.currentAction.set("Stop")
            self.btnStartStopTask.configure(image=self.stopTask)
            return True
        
    def actionBtnStartTask(self):
        messagebox.showinfo("Start Task", "Bientôt dans la nouvelle version")
        #

    def createTask(self, wndCreateTask, taskName, taskPriority, taskCategory):
        taskId = self.controller.addTask(taskName, taskPriority, taskCategory)
        messagebox.showinfo("Create a task", "Task added : id=(" + str(taskId) + ")")
        wndCreateTask.destroy()
    
    def actionBtnManageTaskCreate(self):
        # Window preparation
        wndCreateTask = self.createWindow("Create task...")
        # Input task name
        lblTaskName = Label(wndCreateTask, text="Input task name : ")
        lblTaskName.grid(row=0, column=0)
        taskName = StringVar()
        entTaskName = Entry(wndCreateTask, textvariable=taskName)
        entTaskName.focus_set()
        entTaskName.grid(row=0, column=1)
        # Input priority
        lblTaskPriority = Label(wndCreateTask, text="Input task priority : ")
        lblTaskPriority.grid(row=1, column=0)
        taskPriority = IntVar()
        entTaskPriority = Entry(wndCreateTask, textvariable=taskPriority)
        entTaskPriority.grid(row=1, column=1)
        # Input category
        lblTaskCategory = Label(wndCreateTask, text="Input task category : ")
        lblTaskCategory.grid(row=2, column=0)
        taskCategory = StringVar()
        entTaskCategory = Entry(wndCreateTask, textvariable=taskCategory)
        entTaskCategory.grid(row=2, column=1)
        # OK button
        btnOK = Button(wndCreateTask, text="OK", default=ACTIVE, command=lambda:self.createTask(wndCreateTask, taskName.get(), taskPriority.get(), taskCategory.get()) )
        btnOK.grid(row=3, column=0)
        # Quit button
        btnCancel = Button(wndCreateTask, text="Cancel", command=wndCreateTask.destroy)
        btnCancel.grid(row=3, column=1)

    def actionBtnManageTaskUpdate(self):
        messagebox.showinfo("Manage Task", "UPDATE")
        
    def actionBtnManageTaskRemove(self):
        messagebox.showinfo("Manage Task", "REMOVE")

    def actionBtnManageTaskDisplay(self):
        # Window Preparation
        wndDisplayTask = self.createWindow("Display tasks...")
        # List with scrollbar
        scrollbar = Scrollbar(wndDisplayTask, orient=VERTICAL)
        lstTasksList = Listbox(wndDisplayTask, yscrollcommand=scrollbar.set)
        scrollbar.config(command=lstTasksList.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        lstTasksList.pack(side=TOP, fill=BOTH, expand=1)
        # Quit button
        btnQuit = Button(wndDisplayTask, text="OK", command=wndDisplayTask.destroy)
        btnQuit.pack(side=BOTTOM, fill=X)

        # Data input
        tasksList =  self.controller.getTasksList()
        for task in tasksList:
            lstTasksList.insert(END, "(" + str(task.taskId) + ")=>" + task.name + "(" + task.category + ")")

    def actionBtnReportWeekMinus2(self):
        self.weekReport("Week-2 report...", -2)

    def actionBtnReportLastWeek(self):
        self.weekReport("Last week report...", -1)

    def actionBtnReportCurrentWeek(self):
        self.weekReport("Current week report...", 0)
    
    def weekReport(self, title, week):
        # Window preparation
        wndWeekReport = self.createWindow(title)
        # List with scrollbars
        scrollbarV = Scrollbar(wndWeekReport, orient=VERTICAL)
        scrollbarH = Scrollbar(wndWeekReport, orient=HORIZONTAL)
        lstWeekReport = Listbox(wndWeekReport, yscrollcommand=scrollbarV.set, xscrollcommand=scrollbarH.set)
        scrollbarV.config(command=lstWeekReport.yview)
        scrollbarH.config(command=lstWeekReport.xview)
        scrollbarV.pack(side=RIGHT, fill=Y)
        scrollbarH.pack(side=BOTTOM, fill=X)
        lstWeekReport.pack(side=TOP, fill=BOTH, expand=1)
        # Quit button
        btnQuit = Button(wndWeekReport, text="OK", command=wndWeekReport.destroy)
        btnQuit.pack(side=BOTTOM, fill=X)

        # Data input    
        reportList =  self.controller.getWeekReport(week)
        for report in reportList:
            lstWeekReport.insert(END, report[0].name + "(" + report[0].category + ") = " + str(round(report[1],2))  + " heure(s).")
    
    def actionBtnReportDisplayAll(self):
        # Window preparation
        wndDisplayAll = self.createWindow("All records ...")
        # List with scrollbars
        scrollbarV = Scrollbar(wndDisplayAll, orient=VERTICAL)
        scrollbarH = Scrollbar(wndDisplayAll, orient=HORIZONTAL)
        lstAll = Listbox(wndDisplayAll, yscrollcommand=scrollbarV.set, xscrollcommand=scrollbarH.set)
        scrollbarV.config(command=lstAll.yview)
        scrollbarH.config(command=lstAll.xview)
        scrollbarV.pack(side=RIGHT, fill=Y)
        scrollbarH.pack(side=BOTTOM, fill=X)
        lstAll.pack(side=TOP, fill=BOTH, expand=1)
        # Quit button
        btnQuit = Button(wndDisplayAll, text="OK", command=wndDisplayAll.destroy)
        btnQuit.pack(side=BOTTOM, fill=X)

        # Data input    
        trackersList =  self.controller.getTrackersList()
        for tracker in trackersList:
            lstAll.insert(END, tracker.task.name + "(" + tracker.task.category + ") ; " + tracker.begin_timestamp + " ; " + str(tracker.end_timestamp) + " ; " + str(tracker.duration_min))

    def actionBtnStartStopTask(self):
        if self.taskStarted == True:
            self.controller.stopTask(self.current[0].trackerId)
            self.taskStarted = self.updateCurrentTaskName()
        else:
            # Window Preparation
            wndDisplayTask = self.createWindow("Select Task...")
            # List with scrollbar
            scrollbar = Scrollbar(wndDisplayTask, orient=VERTICAL)
            lstTasksList = Listbox(wndDisplayTask, yscrollcommand=scrollbar.set)
            scrollbar.config(command=lstTasksList.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            lstTasksList.pack(side=TOP, fill=BOTH, expand=1)
            # Quit button
            btnQuit = Button(wndDisplayTask, text="OK", command=lambda:self.actionBtnStartSelectedTask(wndDisplayTask, lstTasksList))
            btnQuit.pack(side=BOTTOM, fill=X)
    
            # Data input
            tasksList =  self.controller.getTasksList()
            for task in tasksList:
                lstTasksList.insert(END, str(task.taskId) + "-" + task.name + "(" + task.category + ")")
    
    def actionBtnStartSelectedTask(self, wnd, lstTasks):
        if lstTasks.curselection() != ():
            selectedTask = lstTasks.selection_get()
            extractedID = selectedTask.split("-", 1)
            self.controller.startTask(int(extractedID[0]))
        self.taskStarted = self.updateCurrentTaskName()
        wnd.destroy()
    
    def actionBtnTrackerAdd(self):
        wndAddTracker = self.createWindow("Add tracker manually")
        # Choose task
        #sbTasklist = Spinbox(wndAddTracker, values=(1, 2, 4, 8))
        box_value = StringVar()
        self.sbTasklist = ttk.Combobox(wndAddTracker, textvariable=box_value)
        self.sbTasklist.bind("<<ComboboxSelected>>", self.newselection)
        self.sbTasklist['values'] = ('X', 'Y', 'Z')
        self.sbTasklist.pack()
        # Choose begin date/time
        
        # Choose end date/time
        
        # Buttons (OK/Cancel)
        btnQuit = Button(wndAddTracker, text="OK", command=wndAddTracker.destroy)
        btnQuit.pack(side=BOTTOM, fill=X)
    
    def newselection(self, event):
        value_of_combo = self.sbTasklist.get()
        print(value_of_combo)
    
    def actionBtnAbout(self):
        messagebox.showinfo("About TimeTracker", "Version: " + self.version + "\nDev: MS")
    
    def actionBtnQuit(self):
        width,height,positionX,positionY = self.geoliste(self.mainWnd.geometry())
        self.updateSize(self.ini.props, width, height)
        self.updatePosition(self.ini.props, positionX, positionY)
        self.ini.saveInitFile()
        self.quit()
        
    def updateSize(self, map, width, height):
        map["width"] = str(width)
        map["height"] = str(height)
        
    def updatePosition(self, map, positionX, positionY):
        map["positionX"] = str(positionX)
        map["positionY"] = str(positionY)