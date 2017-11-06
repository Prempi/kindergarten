import arcade, arcade.key, random #, time

from detail_of_characters import Main_Character, Zombie_Character
from detail_of_board import Board

# random trap and key of trap
def random_position_trap(array_map):
    limit_y = len(array_map) - 1
    limit_x = len(array_map[0]) -1 
#    print("limit_x : {} limit_y : {}".format(limit_x,limit_y))
    while True:
        switch_x = random.randint(0,limit_x)
        switch_y = random.randint(0,limit_y)
#        print("switch_x : {} switch_y : {}".format(switch_x,switch_y))
        if(array_map[switch_y][switch_x] == 0):
            None
        else:
            continue
        trap_x = random.randint(0,limit_x)
        trap_y = random.randint(0,limit_y)
#        print("trap_x : {} trap_y : {}".format(trap_x,trap_y))
        if (trap_x < 3 and trap_y <3):
            continue
        if(array_map[trap_y][trap_x] != 1 and array_map[trap_y][trap_x] != 2):
            None
        else:
            continue
        return switch_x, switch_y, trap_x, trap_y

# random postion of zombie when start
def random_start_position_of_zombie(zombie_map):
    while True:
        random_x = random.randint(0,len(zombie_map[0])-1)
        random_y = random.randint(0,len(zombie_map)-1)
        if (random_x < 4 and random_y < 4) or (random_x == len(zombie_map[0])-1 and random_y == len(zombie_map)-1):
            continue
        if zombie_map[random_y][random_x] == 0:
            return random_x, random_y

# random the wall
def random_position_of_wall(wall_map):
    while True:
        random_x = random.randint(0,len(wall_map[0])-1)
        random_y = random.randint(0,len(wall_map)-1)
        if (random_x == 0 and random_y == 0) or (random_x > len(wall_map[0])-2 and random_y > len(wall_map)-1) or(random_x < 3 and random_y < 3):
            continue
        count = 0
        for wall in wall_map[random_y][random_x]:
            count += wall
        if count > 2:
            continue
        random_wall = random.randint(1,100)%4
        if wall_map[random_y][random_x][random_wall] == 1:
            continue
        if random_wall == 0 and random_x != 0:
            count = 0
            for wall in wall_map[random_y][random_x-1]:
                count += wall
            if count > 2:
                continue
        elif random_wall == 3 and random_x != len(wall_map[0])-1:
            count = 0
            for wall in wall_map[random_y][random_x+1]:
                count += wall
            if count > 2:
                continue
        elif random_wall == 1 and random_y != len(wall_map)-1:
            count = 0
            for wall in wall_map[random_y+1][random_x]:
                count += wall
            if count > 2:
                continue
        elif random_wall == 2 and random_y != 0:
            count = 0
            for wall in wall_map[random_y-1][random_x]:
                count += wall
            if count > 2:
                continue
        return random_x, random_y, random_wall
        
def print_map(text,array_map):
    print(text)
    row = len(array_map) - 1
    while row > -1:
        for column in range(len(array_map[row])):
            print("{:>5.0f}".format(array_map[row][column]), end = " ")
        print()
        row -= 1

def print_map_array(text,array_map):
    print(text)
    row = len(array_map) - 1
    while row > -1:
        for column in range(len(array_map[row])):
            for count in range(len(array_map[row][column])):
                if count == len(array_map[row][column])-1:
                    print(array_map[row][column][count], end ="")
                else:
                    print(array_map[row][column][count], end =":")
            print("  ", end = "")
        print()
        row -= 1

def print_key(text,dictionary):
    print(text)
    limit_per_line = 6
    count = 0
    for test_key in dictionary.keys():
        print("{:>5.0f} : ".format(test_key),dictionary[test_key], end = "\t")
        count +=1
        if count == limit_per_line:
            count = 0
            print("")

#value in map have 1:start  2:target 3:zombie 4:black_hole >10:switch
class Map:
    def __init__(self, SCREEN_WIDTH, SCREEN_HIGHT, WIDTH, HIGHT, array_map , NUM_TRAP, NUM_ZOMBIE, NUM_WALL,SCREEN_BOARD):
#preparing variable
        self.plan_map = array_map
        self.width = WIDTH
        self.hight = HIGHT
        self.widths = SCREEN_WIDTH
        self.hights = SCREEN_HIGHT
        self.knight = Main_Character(self, 0, 0)
        self.zombie = []
        self.num_trap = NUM_TRAP
        self.num_zombie = NUM_ZOMBIE
        self.num_wall = NUM_WALL
        self.set_up = 1
        self.board = Board(SCREEN_BOARD,SCREEN_HIGHT,self)
        print("len(self.plan_map) is %i"%(len(self.plan_map)))
        print("len(self.plan_map[0]) is %i"%(len(self.plan_map[0])))

#Set original Map
        self.plan_map[0][0] = 1
        self.plan_map[len(self.plan_map)-1][len(self.plan_map[0])-1] = 2
        print_map("Print set up map",self.plan_map) # check map

#Set trap
        self.trap_keys = {}
        self.trap = []
        for count in range(self.num_trap):
#            print("count is {}".format(count))
            data = random_position_trap(self.plan_map)
            self.plan_map[data[1]][data[0]] = count+11
            self.trap_keys[count+11] = [data[3],data[2],0]
            self.trap.append(arcade.Sprite("images/Black_Hole.png"))
            self.trap[count].set_position(data[2]*self.width+1+self.width/2,data[3]*self.hight+1+self.hight/2)

#Set Zombie
        self.zombie_map = []
        for row in range(len(self.plan_map)):
            self.zombie_map.append([])
            for column in range(len(self.plan_map[row])):
                self.zombie_map[row].append(0)
        print_map("Print set up map of zombie",self.zombie_map) # check zombie map
        for count in range(self.num_zombie):
            print("For count in Zombie is {}".format(count),end = "\t")
            data = random_start_position_of_zombie(self.zombie_map)
            print("Data is ", end = " ")
            print(data)
            self.zombie.append(Zombie_Character(self, data[0], data[1], count, self.num_zombie))
            self.zombie_map[data[1]][data[0]] = 1

#Set Wall postiton 1 is right position 2 is up position 3 is down position 4 is left
        self.wall_map = []
        for row in range(len(self.plan_map)):
            self.wall_map.append([])
            for column in range(len(self.plan_map[row])):
                self.wall_map[row].append([0,0,0,0])
                if row == 0:
                    self.wall_map[row][column][2] = 1
                elif row == len(self.plan_map)-1:
                    self.wall_map[row][column][1] = 1
                if column == 0:
                    self.wall_map[row][column][0] = 1
                elif column == len(self.plan_map[row])-1:
                    self.wall_map[row][column][3] = 1
        print_map_array("Print set up wall map",self.wall_map) # check wall map
        for count in range(self.num_wall):
            data = random_position_of_wall(self.wall_map)
            print(data)
            self.wall_map[data[1]][data[0]][data[2]] = 1
            if data[2] == 0 and data[0] != 0:
                self.wall_map[data[1]][data[0]-1][3] = 1    
            elif data[2] == 3 and data[0] != len(self.wall_map[0])-1 :
                self.wall_map[data[1]][data[0]+1][0] = 1
            elif data[2] == 1 and data[1] != len(self.wall_map)-1:
                self.wall_map[data[1]+1][data[0]][2] = 1
            elif data[2] == 2 and data[1] != 0:
                self.wall_map[data[1]-1][data[0]][1] = 1 

        print_map("Print set up map after add trap",self.plan_map) # check map
        print_key("Print key of trap",self.trap_keys) # 0 is row 1 is column 3 has two value 0 close 1 open
        print_map("Print set up map of zombie after add zombie",self.zombie_map) # check zombie map
        print_map_array("Print set up wall map after add wall",self.wall_map) # check wall map

#Draw wall
    def draw_wall(self):
        for row in range(len(self.wall_map)):
            for column in range(len(self.wall_map[row])):
                for count in range(len(self.wall_map[row][column])):
                    if(self.wall_map[row][column][count] == 1 and count == 0):
                        arcade.draw_line(column*self.width+1,row*self.hight+1,column*self.width+1,(row+1)*self.hight+1,arcade.color.BRICK_RED,2)  
                    if(self.wall_map[row][column][count] == 1 and count == 3):
                        arcade.draw_line((column+1)*self.width,row*self.hight+1,(column+1)*self.width,(row+1)*self.hight+1,arcade.color.BRICK_RED,2)  
                    if(self.wall_map[row][column][count] == 1 and count == 1):
                        arcade.draw_line(column*self.width+1,(row+1)*self.hight+1,(column+1)*self.width+1,(row+1)*self.hight+1,arcade.color.BRICK_RED,2)  
                    if(self.wall_map[row][column][count] == 1 and count == 2):
                        arcade.draw_line(column*self.width+1,row*self.hight+1,(column+1)*self.width+1,row*self.hight+1,arcade.color.BRICK_RED,2)  
        
# Open or Close Trap
    def open_or_close(self, import_key, who,pos_x,pos_y):
        data_of_key = self.trap_keys[import_key]
        same_target = []
        for test_key in self.trap_keys.keys():
#            print("Test Key is {} and data is {}".format(test_key,self.trap_keys[test_key]))
            if data_of_key[0] == self.trap_keys[test_key][0] and data_of_key[1] == self.trap_keys[test_key][1]:
                same_target.append(test_key)
#                print("Collect key is {}".format(test_key))
        sum_score = 1 
        for collect_key in same_target:
            sum_score += self.trap_keys[collect_key][2]
            self.trap_keys[collect_key][2] = 0
        sum_score = sum_score % 2
        self.trap_keys[same_target[0]][2] = sum_score
        if sum_score == 0: 
            self.board.event_data("Trap at ({},{}) close by ".format(data_of_key[0]+1,data_of_key[1]+1) + who + " at ({},{})".format(pos_x+1,pos_y+1))
        if sum_score == 1: 
            self.board.event_data("Trap at ({},{}) open by ".format(data_of_key[0]+1,data_of_key[1]+1) + who + " at ({},{})".format(pos_x+1,pos_y+1))

# Update all zombie
    def update_zombie(self):
        for count in range(len(self.zombie)):
            print("Update Zombie {}".format(count))
            self.zombie[count].update()
#            self.zombie[count].draw()
#            time.sleep(0.01)   
            self.knight.check_black_hole()

# Draw all zombie
    def draw_zombie(self):
        for count in range(len(self.zombie)):
            if self.zombie[count].status == 1:
                self.zombie[count].draw()

# Check all black hole for Zombie
    def check_only_black_hole(self):
        for count in range(len(self.zombie)):
            if self.zombie[count].status == 1:
                self.zombie[count].check_black_hole()

    def draw_trap(self):
#        print("This is in draw_trap len(self.trap) is {}".format(self.trap))
        number_of_trap = len(self.trap_keys)
#        print(number_of_trap)
        count = 0
        while count < number_of_trap:
            if self.trap_keys[count+11][2] == 1:
                self.trap[count].draw()
            count += 1
        
    def draw_grid(self):
        for row in range(len(self.plan_map)):
            for column in range(len(self.plan_map[row])):
                arcade.draw_rectangle_filled(column*self.width+self.width/2+1,row*self.hight+self.hight/2,self.width-1,self.hight-1,arcade.color.BLACK)
                if row == len(self.plan_map)-1 and column == len(self.plan_map[row])-1:
                    arcade.draw_rectangle_filled(column*self.width+self.width/2+1,row*self.hight+self.hight/2,self.width-1,self.hight-1,arcade.color.GREEN)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.MOTION_DOWN:
            self.knight.update(0,-1)
        elif key == arcade.key.MOTION_UP:
            self.knight.update(0,1)
        elif key == arcade.key.MOTION_LEFT:
            self.knight.update(-1,0)
        elif key == arcade.key.MOTION_RIGHT:
            self.knight.update(1,0)                
