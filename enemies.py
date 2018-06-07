'''
Created on 16.3.2017

@author: Mattias
'''

#-------------------- Enemies-class --------------------

class Enemies():
    def __init__(self):     # basic stuff for all enemies
        self.coordinates = []
        self.enemies = []   # list for all enemiy instances
        self.alive = 1
        self.target_coordinates = []
        self.target_cdn_index = 0

    def set_coordinates(self, enemy, x, y):
        enemy.coordinates = [x,y]
            
    def get_x_coordinate(self, enemy):
        return enemy.coordinates[0]
        
    def get_y_coordinate(self, enemy):
        return enemy.coordinates[1]
        
    def add_enemy(self, enemy, x, y):
        self.enemies.append(enemy)
        self.set_coordinates(enemy, x, y)
        
    def get_enemy(self, index):
        return self.enemies[index]


class Small_Enemy(Enemies):
    def __init__(self):
        super().__init__()
        self.enemy_type = 0     # small enemy
        self.max_hitpoints = 10
        self.current_hitpoints = self.max_hitpoints
        self.movement_speed = 4 # bigger = better
        
class Medium_Enemy(Enemies):
    def __init__(self):
        super().__init__()
        self.enemy_type = 1     # medium enemy
        self.max_hitpoints = 30
        self.current_hitpoints = self.max_hitpoints
        self.movement_speed = 2
        
        
class Large_Enemy(Enemies):
    def __init__(self):
        super().__init__()
        self.enemy_type = 2     # large enemy
        self.max_hitpoints = 100
        self.current_hitpoints = self.max_hitpoints
        self.movement_speed = 1