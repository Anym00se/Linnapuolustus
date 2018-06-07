'''
Created on 20.4.2017

@author: Mattias
'''
import sys
from io import *

def file_reader(settings_file, gui_class):
    try:
        file = open(settings_file, "r")
        line = file.readline()
        
        while (line != "end_of_file"):
        
            line = line.strip()
            
            if (line == "initial_money"):
                line = file.readline().strip()
                gui_class.initial_money = int(line)
                print("initial_money = " + line)
                
            if (line == "difficulty"):
                line = file.readline().strip()
                gui_class.difficulty = int(line)
                print("difficulty = " + line)
            
            if (line == "small_tower_price"):
                line = file.readline().strip()
                gui_class.small_tower_price = int(line)
                print("small_tower_price = " + line)
            
            if (line == "medium_tower_price"):
                line = file.readline().strip()
                gui_class.medium_tower_price = int(line)
                print("medium_tower_price = " + line)
            
            if (line == "large_tower_price"):
                line = file.readline().strip()
                gui_class.large_tower_price = int(line)
                print("large_tower_price = " + line)
                
            if (line == "splash_tower_price"):
                line = file.readline().strip()
                gui_class.splash_tower_price = int(line)
                print("splash_tower_price = " + line)
            
            if (line == "tower_range"):
                line = file.readline().strip()
                gui_class.tower_range = int(line)
                print("tower_range = " + line)
                
            if (line == "splash_radius"):
                line = file.readline().strip()
                gui_class.splash_radius = int(line)
                print("splash_radius = " + line)
                
            if (line == "splash_modifier"):
                line = file.readline().strip()
                gui_class.splash_modifier = int(line)
                print("splash_modifier = " + line)
            
            if (line == "enemy_range"):
                line = file.readline().strip()
                gui_class.enemy_range = int(line)
                print("enemy_range = " + line)
                
            if (line == "enemy_speed_modifier"):
                line = file.readline().strip()
                gui_class.enemy_speed_modifier = int(line)
                print("enemy_speed_modifier = " + line)
                
            if (line == "enemy_damage_modifier"):
                line = file.readline().strip()
                gui_class.enemy_damage_modifier = int(line)
                print("enemy_damage_modifier = " + line)    
                
            if (line == "enemy_hp_modifier"):
                line = file.readline().strip()
                gui_class.enemy_hp_modifier = int(line)
                print("enemy_hp_modifier = " + line)  
            
            if (line == "castle_coordinates"):
                line = file.readline().strip()
                coordinates = line.split(",")
                int_coordinates = []
                int_coordinates.append(int(coordinates[0]))
                int_coordinates.append(int(coordinates[1]))
                gui_class.castle_class.coordinates = int_coordinates
                print("castle_coordinates = " + line)
            
            if (line == "enemy_route_begin"):
                route = []
                line = file.readline().strip()
                while (line != "enemy_route_end"):
                    coordinates = line.split(",")
                    int_coordinates = []
                    
                    int_coordinates.append(int(coordinates[0]))
                    int_coordinates.append(int(coordinates[1]))
                    
                    route.append(int_coordinates)
                    line = file.readline().strip()
                    
                gui_class.enemy_route = route
                print("Enemy route: " + str(route))
                
            if (line == "tower_spots_begin"):
                spots = []
                line = file.readline().strip()
                while (line != "tower_spots_end"):
                    coordinates = line.split(",")
                    int_coordinates = []
                    
                    int_coordinates.append(int(coordinates[0]))
                    int_coordinates.append(int(coordinates[1]))
                    
                    spots.append(int_coordinates)
                    line = file.readline().strip()
                    
                gui_class.tower_spots = spots
                print("Tower spots: " + str(spots))
                
            line = file.readline().strip()   
                
        file.close()
    except IOError:
        print("\nError reading file.\n")        # default values will be used