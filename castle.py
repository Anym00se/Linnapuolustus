'''
Created on 16.3.2017

@author: Mattias
'''

#-------------------- Castle-class --------------------

class Castle():
    def __init__(self):
        self.max_hitpoints = 100
        self.current_hitpoints = self.max_hitpoints
        self.coordinates = [55, 300]