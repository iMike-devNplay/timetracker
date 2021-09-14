# -*- coding:UTF-8 -*-
'''
Created on 16 sept. 2014

@author: michael
'''

class Inittools():

    def initFile(self):
        f = open(self.initFileName, "r", newline=None)
        mapProperties = {}
        for line in f.readlines():
            tbl = line.replace("\n", "").split("=")
            mapProperties[tbl[0]]=tbl[1]
        f.close()
        return mapProperties
        
    def saveInitFile(self):
        f = open(self.initFileName, "w", newline=None)
        for key in self.props.keys():
            f.write(str(key) + "=" + str(self.props[key]) + "\n")
        f.close()

    def updateValue(self, key, newValue):
        self.props[key]=newValue
        
    def __init__(self, initFileName):
        self.initFileName = initFileName
        self.props = self.initFile()