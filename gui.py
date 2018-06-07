'''
Created on 16.3.2017

@author: Mattias
'''
import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from math import *
from towers import *
from enemies import *
from castle import *
from draw import *
from main import *
from file_reader import *
from random import *
 

#-------------------- GUI-class --------------------
    
class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Linnapuolustus Buttons"
        self.left = 200     # buttonwindow x-location in screen
        self.top = 758      # buttonwindow y-location in screen
        self.width = 820    # buttonwindow width
        self.height = 200   # buttonwindow height
        self.file = "castle_defense_settings.txt"
        self.step_count = 0
        self.enemies_defeated = 0
            
        # values
        self.initial_money = 10000
        self.money = self.initial_money     # player money
        self.difficulty = 1                 # from external file
        self.small_tower_price = 1          # from external file
        self.medium_tower_price = 1         # from external file
        self.large_tower_price = 1          # from external file
        self.splash_tower_price = 1         # from external file
        self.splash_radius = 1              # from external file
        self.splash_modifier = 1            # from external file
        self.tower_range = 1                # from external file
        self.enemy_range = 1                # from external file
        self.enemy_speed_modifier = 1       # from external file
        self.enemy_damage_modifier = 1      # from external file
        self.enemy_hp_modifier = 1          # from external file
        self.lasers_list = []           # for Draw class to help draw lasers
        self.splash_list = []           # for Draw class to help draw splashes
        self.play = 1                       # if play == 1 the game plays

        # Castle
        self.castle_class = Castle()
        self.castle_class.coordinates = [0,0]
        
        self.enemy_route = [[0,0]]               # from external file     
        self.tower_spots = [[0,0]]               # from external file

        file_reader(self.file ,self)        # replace initial settings values with correct ones from a file

        
        # Towers
        self.towers_class = Towers()
            # Following creates testing instances when game starts, removed when restarted
        self.towers_class.add_tower(Small_Tower(), 150, 150)
        self.towers_class.add_tower(Small_Tower(), 64, 64)
        self.towers_class.add_tower(Medium_Tower(), 250, 300)
        self.towers_class.add_tower(Medium_Tower(), 700, 500)
        self.towers_class.add_tower(Medium_Tower(), 720, 80)
        self.towers_class.add_tower(Large_Tower(), 400, 250)
        self.towers_class.add_tower(Splash_Tower(), 400, 350)
        
        
        # Enemies
        self.enemies_class = Enemies()
            # Following creates testing instances when game starts, removed when restarted
        self.enemies_class.add_enemy(Small_Enemy(), 180, 170)
        self.enemies_class.add_enemy(Small_Enemy(), 380, 370)
        self.enemies_class.add_enemy(Small_Enemy(), 520, 200)
        self.enemies_class.add_enemy(Small_Enemy(), 100, 350)
        self.enemies_class.add_enemy(Medium_Enemy(), 680, 270)
        self.enemies_class.add_enemy(Medium_Enemy(), 690, 350)
        self.enemies_class.add_enemy(Large_Enemy(), 400, 480)
        self.enemies_class.add_enemy(Large_Enemy(), 110, 300)

        for i in range(0, len(self.enemies_class.enemies)):     # set first target coordinate
            self.enemies_class.enemies[i].target_coordinates = self.enemy_route[0]
    
        # Scene
        self.scene = Scene(self.towers_class, self.castle_class, self.enemies_class, self)
        self.init_buttons()
        self.init_window()
        
        self.statusBar = QStatusBar()   # status bar shows information about player's actions
        self.setStatusBar(self.statusBar)

        # Graphics Update Loop
        self.step = QTimer()
        self.step.timeout.connect(self.step_timer)
        self.step.start(100) # ms
        
        self.reset_game()
        
  
    def init_window(self):      # setting geometry for buttonwindow
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.show()
        
    # buttons and texts
    def init_buttons(self):
        '''# print debug
        print_debug_btn = QPushButton("Print debug data", self)
        print_debug_btn.move(0,150)
        print_debug_btn.clicked.connect(self.debugger_function)
        
        # spawn enemy
        spawn_enemy_btn = QPushButton("Spawn Enemy",self)
        spawn_enemy_btn.move(100,150)
        spawn_enemy_btn.clicked.connect(self.spawn_enemy_clicked)'''
        
        # play
        self.play_btn = QPushButton("Play / Pause", self)
        self.play_btn.move(40,20)
        self.play_btn.clicked.connect(self.toggle_play)
        
        # restart
        reset_btn = QPushButton("Restart", self)
        reset_btn.move(40,55)
        reset_btn.clicked.connect(self.reset_game)
        
        # exit
        exit_btn = QPushButton("Exit",self)
        exit_btn.move(40,115)
        exit_btn.clicked.connect(self.close)
        exit_btn.clicked.connect(Scene.close)
        
        
        # small tower
        buy_small_tower_btn = QPushButton("Buy Small Tower\n" + str(self.small_tower_price),self)
        buy_small_tower_btn.move(350,20)
        buy_small_tower_btn.clicked.connect(self.buy_small_clicked)
        
        # medium tower
        buy_medium_tower_btn = QPushButton("Buy Medium Tower\n" + str(self.medium_tower_price),self)
        buy_medium_tower_btn.move(350,50)
        buy_medium_tower_btn.clicked.connect(self.buy_medium_clicked)
        
        # large tower
        buy_large_tower_btn = QPushButton("Buy Large Tower\n" + str(self.large_tower_price),self)
        buy_large_tower_btn.move(450,20)
        buy_large_tower_btn.clicked.connect(self.buy_large_clicked)
        
        # splash tower
        buy_splash_tower_btn = QPushButton("Buy Splash Tower\n" + str(self.splash_tower_price),self)
        buy_splash_tower_btn.move(450,50)
        buy_splash_tower_btn.clicked.connect(self.buy_splash_clicked)
        
        # delete tower
        delete_tower_btn = QPushButton("Delete",self)
        delete_tower_btn.move(400,150)
        delete_tower_btn.clicked.connect(self.delete_clicked)
        
        # line edit
        self.line_edit = QLineEdit(self)
        self.line_edit.move(400,100)
        self.line_edit.setText("0")
        self.input_text = self.line_edit.displayText()
        
        # money text
        self.qLabel_money = QLabel(self)
        self.qLabel_money.move(190, 60)
        self.qLabel_money.setText("Money\n" + str(self.money))
        
        # castle hitpoints text
        self.qLabel_castleHP_text = QLabel(self)
        self.qLabel_castleHP_text.move(190, 20)
        self.qLabel_castleHP_text.setText("Castle Hitpoints\n" + str("{:3.0f}".format(max(0,self.castle_class.current_hitpoints))) + "/" + str(self.castle_class.max_hitpoints))
        
        # step_count text
        self.qLabel_step_count = QLabel(self)
        self.qLabel_step_count.move(190, 100)
        self.qLabel_step_count.setText("Time\n" + str("{:6}".format(self.step_count/10)))
        
        # enemies_defeated text
        self.qLabel_enemies_defeated = QLabel(self)
        self.qLabel_enemies_defeated.move(190, 140)
        self.qLabel_enemies_defeated.setText("Enemies Defeated\n" + str(self.enemies_defeated))
                
        self.show()
    
    def toggle_play(self):          # toggles game state between pause and play
        if (self.play == 0):
            self.play = 1
            self.statusBar.showMessage("Game resumed.",1500) 
        else:
            self.play = 0
            self.statusBar.showMessage("Game paused.",1500) 
        
    def debugger_function(self):    # only for debugging purposes
        print_debugger(self)
        self.update_all()
        
    def add_instance(self, instance, x, y):         # add tower depending on which button is clicked
        if (self.play == 1):
            if (self.tower_spot_free(x, y) == 1):
        
                if (instance == "small_tower"):
                    self.money -= self.small_tower_price
                    self.towers_class.add_tower(Small_Tower(), x, y)
                    self.statusBar.showMessage("Small Tower added.",1500) 
                if (instance == "medium_tower"):
                    self.money -= self.medium_tower_price
                    self.towers_class.add_tower(Medium_Tower(), x, y)
                    self.statusBar.showMessage("Medium Tower added.",1500) 
                if (instance == "large_tower"):
                    self.money -= self.large_tower_price
                    self.towers_class.add_tower(Large_Tower(), x, y)
                    self.statusBar.showMessage("Large Tower added.",1500) 
                if (instance == "splash_tower"):
                    self.money -= self.splash_tower_price
                    self.towers_class.add_tower(Splash_Tower(), x, y)
                    self.statusBar.showMessage("Splash Tower added.",1500) 
            self.update_all()
    
    def delete_tower(self, x, y):                   # remove tower from world, doesn't delete it, clean_lists() deletes tower permanently
        if (self.play == 1):
            if (self.tower_spot_free(x, y) == 0):
                for i in range(0, len(self.towers_class.towers)):
                    if (self.towers_class.towers[i].coordinates == [x,y]):
                        self.towers_class.towers[i].alive = 0
                        self.statusBar.showMessage("Tower deleted.",1500)
            self.update_all()
        
    def tower_spot_free(self, x, y):                # check if tower spot is free or not
        for i in range(0, len(self.towers_class.towers)):
            if (self.towers_class.towers[i].coordinates == [x,y]):
                if (self.towers_class.towers[i].alive == 1):
                    return 0
        return 1
    
    def update_all(self):                           # update graphics and texts
        self.update_text()
        self.scene.draw_gfx.update()
        
    def step_timer(self):                           # step: happens every 100ms
        self.clean_lists()
        self.update_all()
        if (self.play == 1):
            self.move_enemies()
            self.damage_castle()
            self.attack_enemies() 
            if (self.step_count % (5 + randint(-2,2)) == 0):
                self.enemy_spawner_function()
            self.step_count += 1
      
               
    def update_text(self):                          # updates buttonwindow's texts
        self.qLabel_money.setText("Money\n" + str(self.money))
        self.qLabel_castleHP_text.setText("Castle Hitpoints\n" + str("{:3.0f}".format(max(0,self.castle_class.current_hitpoints))) + "/" + str(self.castle_class.max_hitpoints))
        self.qLabel_step_count.setText("Time\n" + str("{:6}".format(self.step_count/10)))
        self.qLabel_enemies_defeated.setText("Enemies Defeated\n" + str(self.enemies_defeated))
        if (self.play == 1):
            self.play_btn.setText("Pause")
        else:
            self.play_btn.setText("Play")
        
        
    def move_enemies(self):                         # move all enemies towards their next target coordinate
        for i in range(0, len(self.enemies_class.enemies)):
            if (self.enemies_class.enemies[i].current_hitpoints <= 0):
                self.enemies_class.enemies[i].alive = 0
            x_speed = cos(self.calculate_angle(self.enemies_class.enemies[i].coordinates[0], self.enemies_class.enemies[i].coordinates[1], self.enemies_class.enemies[i].target_coordinates[0], self.enemies_class.enemies[i].target_coordinates[1]))*(0.1 * self.enemy_speed_modifier * self.enemies_class.enemies[i].movement_speed)
            y_speed = -sin(self.calculate_angle(self.enemies_class.enemies[i].coordinates[0], self.enemies_class.enemies[i].coordinates[1], self.enemies_class.enemies[i].target_coordinates[0], self.enemies_class.enemies[i].target_coordinates[1]))*(0.1 * self.enemy_speed_modifier * self.enemies_class.enemies[i].movement_speed)
            if (fabs(self.enemies_class.enemies[i].target_coordinates[0] - self.enemies_class.enemies[i].coordinates[0]) < 5 and fabs(self.enemies_class.enemies[i].target_coordinates[1] - self.enemies_class.enemies[i].coordinates[1]) < 5):
                if (self.enemies_class.enemies[i].target_cdn_index != len(self.enemy_route)-1):
                    self.set_next_target_coordinate(i)
                else:
                    x_speed = 0
                    y_speed = 0
                
            self.enemies_class.enemies[i].coordinates[0] += x_speed     # x_speed means how many pixels enemy's x-coordinate changes in one step
            self.enemies_class.enemies[i].coordinates[1] += y_speed     # y_speed means how many pixels enemy's y-coordinate changes in one step
                
                   
    def calculate_angle(self, x0, y0, x1, y1):      # angle between two coordinates
        return (-atan2( y1-y0, x1-x0 ))
    
    def distance(self, x0, y0, x1, y1):             # distance between two coordinates
        return sqrt(  fabs(y0 - y1)**2 + fabs(x0 - x1)**2  )
       
    def set_next_target_coordinate(self, enemy_index):  # update enemy's target coordinate to next in the list
        self.enemies_class.enemies[enemy_index].target_cdn_index += 1
        self.enemies_class.enemies[enemy_index].target_coordinates = self.enemy_route[self.enemies_class.enemies[enemy_index].target_cdn_index]
    
    
    # buttons clicked
    def buy_small_clicked(self):    # triggered by button
        try:
            if (self.play == 1):
                if (self.money >= self.small_tower_price):
                    if (int(self.line_edit.displayText()) >= 0 and int(self.line_edit.displayText()) < len(self.tower_spots)):
                        self.add_instance("small_tower", self.tower_spots[int(self.line_edit.displayText())][0], self.tower_spots[int(self.line_edit.displayText())][1])
                    else:
                        self.value_error()
                else:
                    self.statusBar.showMessage("Not enough money!",1500)
        except ValueError:
            self.value_error()
                            
    def buy_medium_clicked(self):   # triggered by button
        try:
            if (self.play == 1):
                if (self.money >= self.medium_tower_price):
                    if (int(self.line_edit.displayText()) >= 0 and int(self.line_edit.displayText()) < len(self.tower_spots)):
                        self.add_instance("medium_tower", self.tower_spots[int(self.line_edit.displayText())][0], self.tower_spots[int(self.line_edit.displayText())][1])
                    else:
                        self.value_error()
                else:
                    self.statusBar.showMessage("Not enough money!",1500)
        except ValueError:
            self.value_error()
                
    def buy_large_clicked(self):    # triggered by button
        try:
            if (self.play == 1):
                if (self.money >= self.large_tower_price):
                    if (int(self.line_edit.displayText()) >= 0 and int(self.line_edit.displayText()) < len(self.tower_spots)):
                        self.add_instance("large_tower", self.tower_spots[int(self.line_edit.displayText())][0], self.tower_spots[int(self.line_edit.displayText())][1])
                    else:
                        self.value_error()
                else:
                    self.statusBar.showMessage("Not enough money!",1500)
        except ValueError:
            self.value_error()
                
    def buy_splash_clicked(self):   # triggered by button
        try:
            if (self.play == 1):
                if (self.money >= self.splash_tower_price):
                    if (int(self.line_edit.displayText()) >= 0 and int(self.line_edit.displayText()) < len(self.tower_spots)):
                        self.add_instance("splash_tower", self.tower_spots[int(self.line_edit.displayText())][0], self.tower_spots[int(self.line_edit.displayText())][1])
                    else:
                        self.value_error()
                else:
                    self.statusBar.showMessage("Not enough money!",1500)
        except ValueError:
            self.value_error()
    
    def delete_clicked(self):   # triggered by button
        try:
            if (self.play == 1):
                if (int(self.line_edit.displayText()) >= 0 and int(self.line_edit.displayText()) < len(self.tower_spots)):
                    self.delete_tower(self.tower_spots[int(self.line_edit.displayText())][0], self.tower_spots[int(self.line_edit.displayText())][1])
                else:
                    self.value_error()
        except ValueError:
            self.value_error()
            
    def value_error(self):
        #print("-Invalid input-")
        self.statusBar.showMessage("Invalid input.",1000)
                 
    
    def nearest_enemy(self, tower):         # check and set nearest enemy for the tower
        smallest_distance = self.tower_range
        nearest_enemy_instance = None
        for i in range(0, len(self.enemies_class.enemies)):
            if (self.distance(self.towers_class.get_x_coordinate(tower), self.towers_class.get_y_coordinate(tower), self.enemies_class.get_x_coordinate(self.enemies_class.enemies[i]), self.enemies_class.get_y_coordinate(self.enemies_class.enemies[i])) < smallest_distance):
                if (self.enemies_class.enemies[i].alive == 1):
                    smallest_distance = self.distance(self.towers_class.get_x_coordinate(tower), self.towers_class.get_y_coordinate(tower), self.enemies_class.get_x_coordinate(self.enemies_class.enemies[i]), self.enemies_class.get_y_coordinate(self.enemies_class.enemies[i]))
                    nearest_enemy_instance = self.enemies_class.enemies[i]
        tower.nearest_enemy = nearest_enemy_instance
    
    def enemies_near_castle(self):          # returns number of enemies
        count = 0
        for i in range(0, len(self.enemies_class.enemies)):
            if (self.distance(self.castle_class.coordinates[0], self.castle_class.coordinates[1], self.enemies_class.get_x_coordinate(self.enemies_class.enemies[i]), self.enemies_class.get_y_coordinate(self.enemies_class.enemies[i])) <= self.enemy_range):
                count += 1
        return count
    
    def spawn_enemy(self, enemy):           # spawn enemy in first target coordinate depending on line edit text, activated by "spawn_enemy_clicked" which is activated by button
        if (enemy == "small_enemy"):
            self.enemies_class.add_enemy(Small_Enemy(), self.enemy_route[0][0], self.enemy_route[0][1])
        if (enemy == "medium_enemy"):
            self.enemies_class.add_enemy(Medium_Enemy(), self.enemy_route[0][0], self.enemy_route[0][1])
        if (enemy == "large_enemy"):
            self.enemies_class.add_enemy(Large_Enemy(), self.enemy_route[0][0], self.enemy_route[0][1])
        self.enemies_class.enemies[len(self.enemies_class.enemies)-1].target_coordinates = self.enemy_route[0]
        self.update_all()
            
    def spawn_enemy_clicked(self):          # activated by button
        try:
            enemy = "small_enemy"
            if (int(self.line_edit.displayText()) == 1):
                enemy = "medium_enemy"
            if (int(self.line_edit.displayText()) > 1):
                enemy = "large_enemy"
            self.spawn_enemy(enemy)
        except ValueError:
            self.value_error()
        
    def clean_lists(self):                  # delete useless instances from game world and memory
        deletables_towers = []
        deletables_enemies = []
        if (self.step_count % 5 == 0):
            self.lasers_list = []
            self.splash_list = []
        
        for i in range(0, len(self.towers_class.towers)):               # towers
            if (self.towers_class.towers[i].alive == 0):
                deletables_towers.append(self.towers_class.towers[i])
        for i in range(0, len(deletables_towers)):
            self.towers_class.towers.remove(deletables_towers[i])
        deletables_towers = []
        
        for i in range(0, len(self.enemies_class.enemies)):             # enemies
            if (self.enemies_class.enemies[i].alive == 0):
                deletables_enemies.append(self.enemies_class.enemies[i])
                if (self.enemies_class.enemies[i].enemy_type == 0):
                    self.money += 30
                    self.enemies_defeated += 1
                if (self.enemies_class.enemies[i].enemy_type == 1):
                    self.money += 60
                    self.enemies_defeated += 1
                if (self.enemies_class.enemies[i].enemy_type == 2):
                    self.money += 120
                    self.enemies_defeated += 1
        for i in range(0, len(deletables_enemies)):
            self.enemies_class.enemies.remove(deletables_enemies[i])
        deletables_enemies = []
                
        
    def damage_castle(self):        # happens every step, castle loses 0 hp / step if no enemies near
        self.castle_class.current_hitpoints -= 0.01 * self.enemy_damage_modifier * self.enemies_near_castle()
        if (self.castle_class.current_hitpoints <= 0):
            self.play = 0
            self.play_btn.move(-100,-100)
            self.statusBar.showMessage("---------- Game Over ----------",60000)
            
        
    def attack_enemies(self):       # damages enemies depending on tower damage, modified by modifiers
        for i in range(0, len(self.towers_class.towers)):
            self.nearest_enemy(self.towers_class.towers[i])
            if (self.step_count % (10 * self.towers_class.towers[i].firerate) == 0):
                if (self.towers_class.towers[i].nearest_enemy != None):
                    if (self.towers_class.towers[i].tower_type != 3):
                        self.towers_class.towers[i].nearest_enemy.current_hitpoints -= 10 * self.towers_class.towers[i].damage / (self.enemy_hp_modifier * max(1, (self.step_count*self.difficulty)/20000 ))  # modifiers basically change enemy hp by changing tower damage
                        self.lasers_list.append([self.towers_class.towers[i].coordinates, self.towers_class.towers[i].nearest_enemy.coordinates])
                    if (self.towers_class.towers[i].tower_type == 3):
                        self.splash_list.append(self.towers_class.towers[i].nearest_enemy.coordinates)
                        self.lasers_list.append([self.towers_class.towers[i].coordinates, self.towers_class.towers[i].nearest_enemy.coordinates])
                        for j in range(0, len(self.enemies_class.enemies)):
                            if (self.distance( self.towers_class.towers[i].nearest_enemy.coordinates[0], self.towers_class.towers[i].nearest_enemy.coordinates[1], self.enemies_class.enemies[j].coordinates[0], self.enemies_class.enemies[j].coordinates[1] ) <= self.splash_radius):
                                self.enemies_class.enemies[j].movement_speed *= 0.7*(10/self.splash_modifier)
                        
    def enemy_spawner_function(self):   # changes which enemy to spawn (if any at all) depending on difficulty
        enemy = "small_enemy"
        if (randint(0,100) > (100 - (self.difficulty) * (1 + 2*self.step_count/1000))):
            if (randint(0,100) > 70):
                enemy = "medium_enemy"
                if (randint(0,100) > 70):
                    enemy = "large_enemy"
            if (self.difficulty >= 150):
                enemy = "large_enemy"
            self.spawn_enemy(enemy)
    
    def reset_game(self):               # reset all lists (clear towers and enemies)
        self.statusBar.showMessage("Game restarted.",1500) 
        self.towers_class.towers = []
        self.enemies_class.enemies = []
        self.castle_class.current_hitpoints = self.castle_class.max_hitpoints
        self.money = self.initial_money
        self.step_count = 0
        self.enemies_defeated = 0
        self.line_edit.setText("0")
        self.play = 1
        self.play_btn.move(40,20)
        self.update_all()
        
        
#-------------------- Scene-class --------------------

class Scene(QGraphicsView):
    def __init__(self, towers_class, castle_class, enemies_class, gui_class):
        super().__init__()
        self.title = "Linnapuolustus Scene"
        self.left = 200     # graphicswindow x-location in screen
        self.top = 100      # graphicswindow y-location in screen
        self.width = 820    # graphicswindow width
        self.height = 620   # graphicswindow height
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # setting scene
        self.scene = QGraphicsScene(self)
        self.draw_gfx = Draw(self.scene, towers_class, castle_class, enemies_class, gui_class)
        self.scene.addItem(self.draw_gfx)
        self.setWindowTitle(self.title)
        self.scene.setSceneRect(0,0,800, 600)
        self.setScene(self.scene)
        self.show()