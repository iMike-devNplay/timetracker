'''
Created on 12 sept. 2014

@author: michael
'''

class Tracker(object):
    def __init__(self, trackerId, task, begin_timestamp, end_timestamp, duration_min):
        self.trackerId = trackerId
        self.task = task
        self.begin_timestamp = begin_timestamp
        self.end_timestamp = end_timestamp
        self.duration_min = duration_min
        
        