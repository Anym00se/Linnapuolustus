'''
Created on 16.3.2017

@author: Mattias
'''

#-------------------- Towers-class --------------------

class Towers():
    def __init__(self):     # basic stuff for all towers
        self.coordinates = []
        self.towers = []    # list for all tower instances
        self.alive = 1
        self.nearest_enemy = None
    
    def set_coordinates(self, tower, x, y):
        tower.coordinates = [x,y]
        
    def get_x_coordinate(self, tower):
        return tower.coordinates[0]
    
    def get_y_coordinate(self, tower):
        return tower.coordinates[1]
    
    def add_tower(self, tower, x, y):
        self.towers.append(tower)
        self.set_coordinates(tower, x, y)
    
    def get_tower(self, index):
        return self.towers[index]




class Small_Tower(Towers):
    def __init__(self):
        super().__init__()
        self.tower_type = 0     # small tower
        self.damage = 1
        self.firerate = 1       # smaller = faster
        
        
class Medium_Tower(Towers):
    def __init__(self):
        super().__init__()
        self.tower_type = 1     # medium tower
        self.damage = 8
        self.firerate = 3
                
class Large_Tower(Towers):
    def __init__(self):
        super().__init__()
        self.tower_type = 2     # large tower
        self.damage = 80
        self.firerate = 6

class Splash_Tower(Towers):
    def __init__(self):
        super().__init__()
        self.tower_type = 3     # splash tower
        self.damage = 0
        self.firerate = 6