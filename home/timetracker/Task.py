'''
Created on 10 sept. 2014

@author: michael
'''

class Task:

    def __init__(self, taskId, name, priority, category):
        self.taskId = taskId
        self.name = name
        self.priority = priority
        self.category = category
        
    def __str__(self):
        return str(self.taskId) + "-" + self.name

    def __repr__(self):
        return self.__str__()