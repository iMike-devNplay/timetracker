'''
Created on 17 sept. 2014

@author: michael
'''

class GuiController():

    def __init__(self, dbUtils):
        self.dbUtils = dbUtils 
        
    def setMainGui(self,mainGui):
        self.mainGui = mainGui
        
    def getTasksList(self):
        return self.dbUtils.selectAllTasks()
    
    def addTask(self, taskName, taskPriority, taskCategory):
        return self.dbUtils.addTask(taskName, taskPriority, taskCategory)
    
    def getCurrentTask(self):
        return self.dbUtils.selectCurrentTask()
    
    def getTrackersList(self):
        return self.dbUtils.selectAllTrackers()

    def startTask(self, taskId):
        return self.dbUtils.startTask(taskId)
        
    def stopTask(self, trackerId):
        return self.dbUtils.stopTask(trackerId)
    
    def deleteAllTrackers(self):
        self.dbUtils.deleteAllTrackers()
        
    def getWeekReport(self, week):
        return self.dbUtils.getWeekReport(week)