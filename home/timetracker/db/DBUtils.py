# -*- coding:UTF-8 -*-
'''
Created on 10 sept. 2014

@author: michael
'''
import os
import sys
from datetime import datetime, timedelta
import sqlite3
import Task
import Tracker


class DBUtils:
    def __init__(self, dbName):
        self.formatDateTime = "%Y-%m-%d %H:%M:%S"
        self.dbName = dbName
        if not os.path.isfile(self.dbName):
            self.connection = sqlite3.connect(self.dbName)
            cursor = self.connection.cursor()
            cursor.execute("CREATE TABLE TASKS (ID INTEGER PRIMARY KEY, NAME TEXT UNIQUE, PRIORITY INTEGER, CATEGORY TEXT)")
            cursor.execute("CREATE TABLE TRACKER (ID INTEGER PRIMARY KEY, TASK_ID INTEGER NOT NULL, "
                            + "BEGIN_TIMESTAMP TEXT, END_TIMESTAMP TEXT, DURATION_MIN INTEGER, FOREIGN KEY(TASK_ID) REFERENCES TASKS(ID))")
            self.connection.commit()
            cursor.close()
        else:
            self.connection = sqlite3.connect(self.dbName)
                
    def disconnect(self):
        self.connection.close()
        
    def addTask(self, name, priority, category):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO TASKS(NAME, PRIORITY, CATEGORY) VALUES(?, ?, ?)", (name, priority, category))
            taskId = cursor.lastrowid
            self.connection.commit()
            return taskId
        except:
            print("Error inserting new task")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def updateTask(self):
        pass
    
    def deleteTask(self, taskId):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM TASKS WHERE ID = ?", (taskId,))
        self.connection.commit()
        cursor.close()
        
    def selectAllTasks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM TASKS ORDER BY PRIORITY, NAME, CATEGORY")
        tasks = []
        for line in cursor:
            task = Task.Task(line[0], line[1], line[2], line[3])
            tasks.append(task)
        self.connection.commit()
        cursor.close()
        return tasks
        
    def selectCurrentTask(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT ID, TASK_ID, BEGIN_TIMESTAMP, END_TIMESTAMP, DURATION_MIN FROM TRACKER WHERE END_TIMESTAMP IS NULL")
            line = cursor.fetchone()
            tracker = Tracker.Tracker(line[0], line[1], line[2], line[3], line[4])
            return (tracker,self.getTaskById(line[1]))
        except:
            return None
        finally:
            cursor.close()
        
    def getTaskById(self, taskId):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM TASKS WHERE ID = ?", (taskId, ))
        line = cursor.fetchone()
        task = Task.Task(line[0], line[1], line[2], line[3])
        self.connection.commit()
        cursor.close()
        return task
    
    def getTrackerById(self, trackerId):
        cursor = self.connection.cursor()
        cursor.execute("SELECT ID, TASK_ID, BEGIN_TIMESTAMP, END_TIMESTAMP, DURATION_MIN FROM TRACKER WHERE ID = ?", (trackerId, ))
        line = cursor.fetchone()
        tracker = Tracker.Tracker(line[0], line[1], line[2], line[3], line[4])
        self.connection.commit()
        cursor.close()
        return tracker
    
    def startTask(self, taskId):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO TRACKER(TASK_ID, BEGIN_TIMESTAMP) VALUES(?, ?)", (taskId, datetime.now().strftime(self.formatDateTime)))
            trackerId = cursor.lastrowid
            self.connection.commit()
            return trackerId
        except:
            print("Error inserting new tracker : {0}".format(sys.exc_info()[0]))
            print("====> {0}".format(sys.exc_info()[1]))
            self.connection.rollback()
        finally:
            cursor.close()
        
    def stopTask(self, trackerId=0):
        # Si taskId = 0 alors on prend la tâche courante
        if trackerId == 0:
            tracker = self.selectCurrentTask()[0]
            trackerId = tracker.trackerId
        else:
            tracker = self.getTrackerById(trackerId)
            
        currentDate = datetime.now()
        duration = ((currentDate - datetime.strptime(tracker.begin_timestamp, self.formatDateTime)).total_seconds())/60
        cursor = self.connection.cursor()
        cursor.execute("UPDATE TRACKER SET END_TIMESTAMP = ?, DURATION_MIN = ? WHERE ID = ?", (currentDate, duration, trackerId))
        self.connection.commit()
        cursor.close()
        
        
    def selectAllTrackers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM TRACKER ORDER BY BEGIN_TIMESTAMP")
        trackers = []
        for line in cursor:
            tracker = Tracker.Tracker(line[0], self.getTaskById(line[1]), line[2], line[3], line[4])
            trackers.append(tracker)
        self.connection.commit()
        cursor.close()
        return trackers
    
    def deleteAllTrackers(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM TRACKER")
        self.connection.commit()
        cursor.close()
        
    def getWeekReport(self, week):
        lundi = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=datetime.now().weekday()) + timedelta(days=0, weeks=week)
        dimanche = datetime.now().replace(hour=23, minute=59, second=59) - timedelta(days=datetime.now().weekday()) + timedelta(days=6, weeks=week)

        cursor = self.connection.cursor()
        cursor.execute("SELECT TASK_ID, SUM(DURATION_MIN/60) FROM TRACKER WHERE BEGIN_TIMESTAMP >= ? AND END_TIMESTAMP <= ? GROUP BY TASK_ID", 
                            (lundi.strftime(self.formatDateTime), dimanche.strftime(self.formatDateTime)))
        report = []
        for line in cursor:
            report.append((self.getTaskById(line[0]), line[1]))
        self.connection.commit()
        cursor.close()
        return report

