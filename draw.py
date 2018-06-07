'''
Created on 19.4.2017

@author: Mattias
'''
import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import * #QPainter, QBrush, QPixmap
from main import *


#-------------------- Draw-class --------------------

class Draw(QGraphicsItem):
    
    def __init__(self, scene, towers_class, castle_class, enemies_class, gui_class):
        super().__init__()
        painter = QPainter()
        self.brush = QBrush()
        self.scene = scene
        self.towers_class = towers_class
        self.castle_class = castle_class
        self.enemies_class = enemies_class
        self.gui_class = gui_class
        
        
    def boundingRect(self):
        return QRectF(0,0,800,600)
    
    def paint(self, painter, option, widget):   # draws everything in the game world
        self.draw_towers(painter, self.brush)
        self.draw_lasers(painter, self.brush)
        self.draw_splash(painter, self.brush)
        self.draw_tower_range(painter, self.brush)
        
        self.draw_castle(painter, self.brush)
        self.draw_castle_health(painter, self.brush)
        
        self.draw_enemies(painter, self.brush)
        self.draw_enemy_health(painter, self.brush)
        self.draw_enemy_route(painter, self.brush)
        
        self.draw_tower_spots(painter, self.brush)
        #self.draw_debug(painter, self.brush)
        self.draw_world_boundaries(painter, self.brush)
        
        
    
    def draw_world_boundaries(self, painter, brush):
        painter.setPen(Qt.black)
        painter.drawRect(0, 0, 800, 600)
        
    def draw_tower_spots(self, painter, brush):
        painter.setPen(Qt.black)
        for i in range(0, len(self.gui_class.tower_spots)):
            if (self.gui_class.tower_spot_free(self.gui_class.tower_spots[i][0], self.gui_class.tower_spots[i][1]) == 1):
                painter.drawText(self.gui_class.tower_spots[i][0]-4, self.gui_class.tower_spots[i][1]+4, (str(i)))
                painter.drawLine(self.gui_class.tower_spots[i][0]-8, self.gui_class.tower_spots[i][1]-8, self.gui_class.tower_spots[i][0]+8, self.gui_class.tower_spots[i][1]-8)
                painter.drawLine(self.gui_class.tower_spots[i][0]-8, self.gui_class.tower_spots[i][1]+8, self.gui_class.tower_spots[i][0]+8, self.gui_class.tower_spots[i][1]+8)
                painter.drawLine(self.gui_class.tower_spots[i][0]-8, self.gui_class.tower_spots[i][1]-8, self.gui_class.tower_spots[i][0]-8, self.gui_class.tower_spots[i][1]+8)
                painter.drawLine(self.gui_class.tower_spots[i][0]+8, self.gui_class.tower_spots[i][1]-8, self.gui_class.tower_spots[i][0]+8, self.gui_class.tower_spots[i][1]+8)
            else:
                painter.drawText(self.gui_class.tower_spots[i][0]+15, self.gui_class.tower_spots[i][1]-15, (str(i)))
        
    #    '''Draw Towers'''
    def draw_towers(self, painter, brush):                          # loop for drawing each tower
        painter.setPen(Qt.green)
        for i in range (0, len(self.towers_class.towers)):
            self.draw_current_tower(painter, self.brush, self.towers_class.towers[i])
           
    def draw_current_tower(self, painter, brush, current_tower):    # draws tower in current index in the loop
        if (current_tower.alive == 1):
            self.draw_tower_circle(painter, self.brush, current_tower)
            if (current_tower.tower_type == 1 or current_tower.tower_type == 2):
                self.draw_tower_medium(painter, self.brush, current_tower)
            if (current_tower.tower_type == 2):
                    self.draw_tower_large(painter, self.brush, current_tower)
            if (current_tower.tower_type == 3):
                    self.draw_tower_splash(painter, self.brush, current_tower)    
    
    def draw_tower_circle(self, painter, brush, current_tower):     # small tower
        painter.drawEllipse(self.towers_class.get_x_coordinate(current_tower)-15, self.towers_class.get_y_coordinate(current_tower)-15, 30, 30)
    
    def draw_tower_medium(self, painter, brush, current_tower):      # small and medium tower
        painter.drawEllipse(self.towers_class.get_x_coordinate(current_tower)-10, self.towers_class.get_y_coordinate(current_tower)-10, 20, 20)
        
    def draw_tower_large(self, painter, brush, current_tower):        # small, medium and large tower
        painter.drawEllipse(self.towers_class.get_x_coordinate(current_tower)-5, self.towers_class.get_y_coordinate(current_tower)-5, 10, 10)
        
    def draw_tower_splash(self, painter, brush, current_tower):     # splash towe
        painter.drawLine(self.towers_class.get_x_coordinate(current_tower)-15, self.towers_class.get_y_coordinate(current_tower), self.towers_class.get_x_coordinate(current_tower)+15, self.towers_class.get_y_coordinate(current_tower))
        painter.drawLine(self.towers_class.get_x_coordinate(current_tower), self.towers_class.get_y_coordinate(current_tower)-15, self.towers_class.get_x_coordinate(current_tower), self.towers_class.get_y_coordinate(current_tower)+15)
        
    def draw_lasers(self, painter, brush):      # draw lasers when tower shoots
        painter.setPen(Qt.red)
        for i in range(0, len(self.gui_class.lasers_list)):
            x0 = self.gui_class.lasers_list[i][0][0]
            y0 = self.gui_class.lasers_list[i][0][1]
            x1 = self.gui_class.lasers_list[i][1][0]
            y1 = self.gui_class.lasers_list[i][1][1]
            painter.drawLine(x0,y0,x1,y1)
            
    def draw_splash(self, painter, brush):      # draw splash circle
        painter.setPen(Qt.gray)
        for i in range(0, len(self.gui_class.splash_list)):
            x0 = self.gui_class.splash_list[i][0]
            y0 = self.gui_class.splash_list[i][1]
            painter.drawEllipse(x0 - self.gui_class.splash_radius, y0 - self.gui_class.splash_radius, self.gui_class.splash_radius*2, self.gui_class.splash_radius*2)
            
    def draw_tower_range(self, painter, brush): # draw circle indicating tower range
        painter.setPen(Qt.yellow)
        for i in range(0, len(self.towers_class.towers)):
            painter.drawEllipse(self.towers_class.towers[i].coordinates[0] - self.gui_class.tower_range, self.towers_class.towers[i].coordinates[1] - self.gui_class.tower_range, self.gui_class.tower_range*2, self.gui_class.tower_range*2)
    
    
    
    #    '''Draw Castle'''
    def draw_castle(self, painter, brush):
        painter.setPen(Qt.blue)
        painter.drawRect(self.castle_class.coordinates[0]-50, self.castle_class.coordinates[1]-50, 100, 100)
    
    def draw_castle_health(self, painter, brush):       # health bar
        painter.setPen(Qt.red)
        painter.drawLine(self.gui_class.castle_class.coordinates[0]-40, self.gui_class.castle_class.coordinates[1]-70, self.gui_class.castle_class.coordinates[0]+40, self.gui_class.castle_class.coordinates[1]-70) 
        painter.setPen(Qt.green)
        painter.drawLine(self.gui_class.castle_class.coordinates[0]-40, self.gui_class.castle_class.coordinates[1]-70, self.gui_class.castle_class.coordinates[0]-40 + max(0,(self.gui_class.castle_class.current_hitpoints / self.gui_class.castle_class.max_hitpoints) * 80), self.gui_class.castle_class.coordinates[1]-70)
        
        
        
    #    '''Draw Enemies'''
    def draw_enemies(self, painter, brush):                         # loop for drawing each enemy
        painter.setPen(Qt.red)
        for i in range (0, len(self.enemies_class.enemies)):
            self.draw_current_enemy(painter, self.brush, self.enemies_class.enemies[i])
    
    def draw_current_enemy(self, painter, brush, current_enemy):    # draws enemy in current index in the loop
        self.draw_enemy_triangle(painter, brush, current_enemy)
        if (current_enemy.enemy_type >= 1):
            self.draw_enemy_medium(painter, brush, current_enemy)
        if (current_enemy.enemy_type >= 2):
            self.draw_enemy_large(painter, brush, current_enemy)
    
    def draw_enemy_triangle(self, painter, brush, current_enemy):   # small enemy
        painter.drawLine(self.enemies_class.get_x_coordinate(current_enemy), self.enemies_class.get_y_coordinate(current_enemy)-6, self.enemies_class.get_x_coordinate(current_enemy)-10, self.enemies_class.get_y_coordinate(current_enemy)+10)
        painter.drawLine(self.enemies_class.get_x_coordinate(current_enemy), self.enemies_class.get_y_coordinate(current_enemy)-6, self.enemies_class.get_x_coordinate(current_enemy)+10, self.enemies_class.get_y_coordinate(current_enemy)+10)
        painter.drawLine(self.enemies_class.get_x_coordinate(current_enemy)-10, self.enemies_class.get_y_coordinate(current_enemy)+10, self.enemies_class.get_x_coordinate(current_enemy)+10, self.enemies_class.get_y_coordinate(current_enemy)+10)
        
    def draw_enemy_medium(self, painter, brush, current_enemy):     # small and medium enemy
        painter.drawLine(self.enemies_class.get_x_coordinate(current_enemy), self.enemies_class.get_y_coordinate(current_enemy)-12, self.enemies_class.get_x_coordinate(current_enemy)-10, self.enemies_class.get_y_coordinate(current_enemy)+4)
        painter.drawLine(self.enemies_class.get_x_coordinate(current_enemy), self.enemies_class.get_y_coordinate(current_enemy)-12, self.enemies_class.get_x_coordinate(current_enemy)+10, self.enemies_class.get_y_coordinate(current_enemy)+4)
        
    def draw_enemy_large(self, painter, brush, current_enemy):      # small, medium and large enemy
        painter.drawLine(self.enemies_class.get_x_coordinate(current_enemy), self.enemies_class.get_y_coordinate(current_enemy)-18, self.enemies_class.get_x_coordinate(current_enemy)-10, self.enemies_class.get_y_coordinate(current_enemy)-2)
        painter.drawLine(self.enemies_class.get_x_coordinate(current_enemy), self.enemies_class.get_y_coordinate(current_enemy)-18, self.enemies_class.get_x_coordinate(current_enemy)+10, self.enemies_class.get_y_coordinate(current_enemy)-2)
    
    def draw_enemy_route(self, painter, brush):                     # draw lines connecting enemy route points
        painter.setPen(Qt.gray)  
        for i in range(0, len(self.gui_class.enemy_route)-1):
            painter.drawLine(self.gui_class.enemy_route[i][0], self.gui_class.enemy_route[i][1], self.gui_class.enemy_route[i+1][0], self.gui_class.enemy_route[i+1][1])
    
    def draw_enemy_health(self, painter, brush):                    # # health bar
        for i in range(0, len(self.gui_class.enemies_class.enemies)):   
            if (self.gui_class.enemies_class.enemies[i].alive == 1):
                painter.setPen(Qt.red)
                painter.drawLine(self.gui_class.enemies_class.enemies[i].coordinates[0]-20, self.gui_class.enemies_class.enemies[i].coordinates[1]-25, self.gui_class.enemies_class.enemies[i].coordinates[0]+20, self.gui_class.enemies_class.enemies[i].coordinates[1]-25)
                painter.setPen(Qt.green)
                painter.drawLine(self.gui_class.enemies_class.enemies[i].coordinates[0]-20, self.gui_class.enemies_class.enemies[i].coordinates[1]-25, self.gui_class.enemies_class.enemies[i].coordinates[0]-20 + max(0, (self.gui_class.enemies_class.enemies[i].current_hitpoints / self.gui_class.enemies_class.enemies[i].max_hitpoints) * 40), self.gui_class.enemies_class.enemies[i].coordinates[1]-25)
                
        
    #    '''Draw Debug'''
    def draw_debug(self, painter, brush):
        painter.setPen(Qt.black)
        #draw debug square large
        painter.drawLine(10, 10, 10, 590)
        painter.drawLine(10, 10, 790, 10)
        painter.drawLine(10, 590, 790, 590)
        painter.drawLine(790, 10, 790, 590)
        #draw debug square small
        painter.drawLine(100, 100, 100, 500)
        painter.drawLine(100, 100, 700, 100)
        painter.drawLine(700, 100, 700, 500)
        painter.drawLine(100, 500, 700, 500)