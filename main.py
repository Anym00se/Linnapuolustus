'''
Created on 21.3.2017

@author: Mattias
'''
import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui import *
from castle import *
from towers import *
from enemies import *
from time import *
from file_reader import *


#-------------------- Main --------------------

def main():
    app = QApplication(sys.argv)
    gui_class = GUI()
    
    
    sys.exit(app.exec_())
    
def print_debugger(gui_class):      # calls all classes debug data
    print("------------------------------Linnapuolustus Debugger------------------------------\n")
    print("\nPlayer money: " + str(gui_class.money) + "\n")
    print("Input text: " + str(gui_class.line_edit.displayText()) + "\n\n")
    print_tower_data(gui_class)
    print_enemy_data(gui_class)
    print_castle_data(gui_class)
    print_functions_data(gui_class)

    
def print_tower_data(gui_class):    # towers debug data
    print("-----Towers data-----\n")
    for i in range (0, len(gui_class.towers_class.towers)):
        print("Tower " + str(i) + " [ID:" + str(id(gui_class.towers_class.towers[i])) + "] Coordinates: "+ str(gui_class.towers_class.towers[i].coordinates) + " Type: " + str(gui_class.towers_class.towers[i].tower_type) + " Alive: " + str(gui_class.towers_class.towers[i].alive))
        print("    Nearest enemy: " + str(gui_class.towers_class.towers[i].nearest_enemy))
    print("\nTower spots: " + str(gui_class.tower_spots))
    print("\nTowers list: " + str(gui_class.towers_class.towers)+ "\n\n")


def print_enemy_data(gui_class):    # enemies debug data
    print("-----Enemies data-----\n")
    for i in range (0, len(gui_class.enemies_class.enemies)):
        print("Enemy " + str(i) + " [ID:" + str(id(gui_class.enemies_class.enemies[i])) + "] Coordinates: " + str(gui_class.enemies_class.enemies[i].coordinates) + " Type: " + str(gui_class.enemies_class.enemies[i].enemy_type) + " Alive: " + str(gui_class.enemies_class.enemies[i].alive))
        print("    HP: " + str(gui_class.enemies_class.enemies[i].current_hitpoints*(gui_class.enemy_hp_modifier * max(1, (gui_class.step_count*gui_class.difficulty)/20000 ))/10) + "/" + str(gui_class.enemies_class.enemies[i].max_hitpoints*(gui_class.enemy_hp_modifier * max(1, (gui_class.step_count*gui_class.difficulty)/20000 ))/10))
        print("    Speed: " + str(gui_class.enemies_class.enemies[i].movement_speed))
        print("    Target coordinates: " + str(gui_class.enemies_class.enemies[i].target_coordinates) + " Index: " + str(gui_class.enemies_class.enemies[i].target_cdn_index))
    print("\nEnemies list: " + str(gui_class.enemies_class.enemies))
    print("\nEnemy route: " + str(gui_class.enemy_route) + "\n\n")

    
def print_castle_data(gui_class):   # castle debug data
    print("-----Castle data-----\n")
    print("Castle coordinates: " + str(gui_class.castle_class.coordinates))
    print("Castle HP: " + str(gui_class.castle_class.current_hitpoints) + "/" + str(gui_class.castle_class.max_hitpoints) + "\n\n")
    
def print_functions_data(gui_class):
    print("-----Functions data-----\n")
    
    #distance
    x0, y0, x1, y1 = 0, 0, 150, 150
    print("def distance(self, x0, y0, x1, y1):")
    print("    x0 = " + str(x0) + ", y0 = " + str(y0) + ", x1 = " + str(x1) + ", y1 = " + str(y1))
    print("    Returned distance: " + str(gui_class.distance(x0,y0,x1,y1)) + "\n")
    
    #enemies near castle
    print("def enemies_near_castle(self):")
    print("    Returned count: " + str(gui_class.enemies_near_castle()) + "\n")
    
    

if __name__ == '__main__':
    main()