import arcade, random#, time

class Main_Character:
    def __init__(self, world, pos_x, pos_y):
        self.world = world
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
        self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2
        self.limit_x = len(self.world.plan_map[0])
        self.limit_y = len(self.world.plan_map)
        print("limit is %i and %i"%(self.limit_x,self.limit_y))
        self.status = 1
        self.round = 0
# assign status 1 is alive 2 is winner 3 is die

    def update(self, movement_x , movement_y):
        self.check_zombie_on_map(2)
        self.check_black_hole() 
        print("move is %i and %i"%(movement_x,movement_y))
        if self.pos_x + movement_x > -1 and self.pos_x + movement_x < self.limit_x and movement_x != 0 and self.check_wall(movement_x, movement_y) and self.status == 1:
            self.pos_x += movement_x
            self.check_map()
            self.check_zombie_on_map(1)
            self.world.update_zombie() 
            self.check_zombie_on_map(2) 
            self.world.check_only_black_hole()
            self.round += 1
            print("----------finish round {:>3.0f}----------".format(self.round))
        elif self.pos_y + movement_y > -1 and self.pos_y + movement_y < self.limit_y and movement_y != 0 and self.check_wall(movement_x, movement_y) and self.status == 1:
            self.pos_y += movement_y
            self.check_map() 
            self.check_zombie_on_map(1) 
            self.world.update_zombie() 
            self.check_zombie_on_map(2) 
            self.world.check_only_black_hole()
            self.round += 1
            print("----------finish round {:>3.0f}----------".format(self.round))
#        if self.round == 30:
#            self.world.board.event_data("***************************************")
#            self.world.board.event_data("***************************************")
#            self.world.board.event_data("***Next turn Zombie will see you***")
#            self.world.board.event_data("***************************************")
#            self.world.board.event_data("***************************************")
        self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
        self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2

    def check_wall(self, movement_x, movement_y):
        if movement_x == -1 and self.world.wall_map[self.pos_y][self.pos_x][0] == 1:
            return False
        elif movement_x == 1 and self.world.wall_map[self.pos_y][self.pos_x][3] == 1:
            return False
        if movement_y == -1 and self.world.wall_map[self.pos_y][self.pos_x][2] == 1:
            return False
        if movement_y == 1 and self.world.wall_map[self.pos_y][self.pos_x][1] == 1:
            return False
        return True            

    def check_map(self):
        print("Welcome to check_map in Main_Character")
# Check about switch
        if self.world.plan_map[self.pos_y][self.pos_x] > 10:
            print("That is switch")
            self.world.open_or_close(self.world.plan_map[self.pos_y][self.pos_x],"hero",self.pos_x,self.pos_y)
# Check about target
        elif self.world.plan_map[self.pos_y][self.pos_x] == 2:
            print("You win")
            self.status = 2

    def check_black_hole(self):
        for test_key in self.world.trap_keys.keys():
            if self.world.trap_keys[test_key][0] == self.pos_y and self.world.trap_keys[test_key][1] == self.pos_x:
                print("this position have black hole")
                if self.world.trap_keys[test_key][2] == 1:
                    print("you are dead")
                    self.status = 3
                else:
                    None
                break

    def check_zombie_on_map(self,situation): 
        for count_zombie in range(len(self.world.zombie)):
            if self.world.zombie[count_zombie].status == 1:
                if self.pos_x == self.world.zombie[count_zombie].pos_x and self.pos_y == self.world.zombie[count_zombie].pos_y:
                    if situation == 1:
                        self.world.zombie[count_zombie].status = 0
                        self.world.board.event_data("Oh! You kill zombie ")    
                    elif situation == 2:
                        print("you were biten by zombie")
                        self.status = 4
                    

class Zombie_Character:
    def __init__(self, world, pos_x, pos_y, code, NUM_ZOMBIE):
        self.world = world
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
        self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2
        self.limit_x = len(self.world.plan_map[0])
        self.limit_y = len(self.world.plan_map)
        self.seeing = 0
        self.picture = arcade.Sprite("images/Zombie_01.png")
        self.picture.set_position(self.real_x,self.real_y)
        self.id = code
        self.num_zombie = NUM_ZOMBIE
#        print("limit is %i and %i"%(self.limit_x,self.limit_y))
        self.status = 1

    def draw(self):
        self.picture.draw()

    def update(self):
        self.world.check_only_black_hole()
        if self.seeing == 1:
#            print("Zombie follow you")
            None
        elif self.find_main_character():
            print("line 119")
#            print("Zombie see you before move")
            self.seeing = 1
            self.picture = arcade.Sprite("images/Zombie_02.png")
        else:
            self.seeing = 0
            self.picture = arcade.Sprite("images/Zombie_01.png")
        if self.status == 0:
            None
        elif self.seeing == 0:
            count = 0
            while count < 6:
                count += 1
                movement_x = 0
                movement_y = 0
                rand_move = random.randint(1,100)
                if rand_move < 26:
                    movement_x = -1
                elif rand_move < 51:
                    movement_y = -1
                elif rand_move < 76:
                    movement_x = 1
                else:
                    movement_y = 1
#                print("move is %i and %i"%(movement_x,movement_y))
                if self.looking_black_hole(self.pos_x + movement_x,self.pos_y + movement_y):
                    if self.pos_x + movement_x > -1 and self.pos_x + movement_x < self.limit_x and movement_x != 0 and not(self.pos_x + movement_x == 0 and self.pos_y == 0) and not(self.pos_x + movement_x == len(self.world.plan_map[0])-1 and self.pos_y == len(self.world.plan_map)-1) and self.check_wall(movement_x,movement_y) and self.check_zombie_team(movement_x,0):
                        self.pos_x += movement_x
                        self.check_switch()
#                        self.world.check_only_black_hole()
                    elif self.pos_y + movement_y > -1 and self.pos_y + movement_y < self.limit_y and movement_y != 0 and not(self.pos_y + movement_y == 0 and self.pos_x == 0) and not(self.pos_y + movement_y == len(self.world.plan_map)-1 and self.pos_x == len(self.world.plan_map[0])-1) and self.check_wall(movement_x,movement_y) and self.check_zombie_team(0,movement_y):
                        self.pos_y += movement_y
                        self.check_switch()
#                        self.world.check_only_black_hole()
                    else:
#                        print("Random again in out table")
                        continue
                else:
                    continue
#                print("before move pos_x:{} pos_y:{} movement_x:{} movement_y:{}".format(self.pos_x,self.pos_y,movement_x,movement_y))   
                self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
                self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2
#                print("after move pos_x:{} pos_y:{} real_x:{} real_y:{}".format(self.pos_x,self.pos_y,self.real_x,self.real_y))   
#                print("Zombie Move")
                break
#            print("Finish Move")
        else:
#            print("Zombie move mode find you")
            distance_x = self.world.knight.pos_x - self.pos_x
            distance_y = self.world.knight.pos_y - self.pos_y
#            print("{} {} {}   {} {} {}".format(distance_x , self.world.knight.pos_x , self.pos_x ,distance_y , self.world.knight.pos_y , self.pos_y))
            if distance_x != 0 and distance_y != 0:
                random_way = random.randint(1,100)%2
                if random_way == 0:
#                    print("random_way is {}".format(random_way))
                    if distance_x < 0 and self.check_wall(-1,0) and self.check_zombie_team(-1,0):  
                        self.pos_x -= 1
                    elif distance_x > 0 and self.check_wall(1,0) and self.check_zombie_team(1,0):
                        self.pos_x += 1
                    elif distance_y < 0 and self.check_wall(0,-1) and self.check_zombie_team(0,-1):
                        self.pos_y -= 1
                    elif distance_y > 0 and self.check_wall(0,1) and self.check_zombie_team(0,1):
                        self.pos_y += 1   
                elif random_way == 1:
                    if distance_y < 0 and self.check_wall(0,-1) and self.check_zombie_team(0,-1):
                        self.pos_y -= 1
                    elif distance_y > 0 and self.check_wall(0,1) and self.check_zombie_team(0,1):
                        self.pos_y += 1   
                    elif distance_x < 0 and self.check_wall(-1,0) and self.check_zombie_team(-1,0):  
                        self.pos_x -= 1
                    elif distance_x > 0 and self.check_wall(1,0) and self.check_zombie_team(1,0):
                        self.pos_x += 1
                else:
#                    print("don't move")
                    None
            elif distance_x == 0:
                if distance_y < 0 and self.check_wall(0,-1) and self.check_zombie_team(0,-1):
                     self.pos_y -= 1
                elif distance_y > 0 and self.check_wall(0,1) and self.check_zombie_team(0,1):
                    self.pos_y += 1
                else:
#                    print("don't move")
                    None
            elif distance_y == 0:
                if distance_x < 0 and self.check_wall(-1,0) and self.check_zombie_team(-1,0):
                     self.pos_x -= 1
                elif distance_x > 0 and self.check_wall(1,0) and self.check_zombie_team(1,0):
                    self.pos_x += 1
                else:
#                    print("don't move")
                    None
            self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
            self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2
        if self.find_main_character():
#            print("Zombie see you after move")
            self.seeing = 1
            self.picture = arcade.Sprite("images/Zombie_02.png")
        else:
            self.seeing = 0
            self.picture = arcade.Sprite("images/Zombie_01.png")
        self.picture.set_position(self.real_x,self.real_y)

    def find_main_character(self):
#        print("Zombie will find you!!")
        distance_pos_x = self.world.knight.pos_x - self.pos_x
        distance_pos_y = self.world.knight.pos_y - self.pos_y
#        print("{} {} {}   {} {} {}".format(distance_pos_x , self.world.knight.pos_x , self.pos_x ,distance_pos_y , self.world.knight.pos_y , self.pos_y))
#        if self.world.knight.round >= 30:
#            return True
        if distance_pos_x == 1 and distance_pos_y == 1:
            if (self.world.wall_map[self.pos_y+distance_pos_y][self.pos_x][3]==0 and self.world.wall_map[self.pos_y][self.pos_x][1]==0) or (self.world.wall_map[self.pos_y][self.pos_x+distance_pos_x][1]==0 and self.world.wall_map[self.pos_y][self.pos_x][3]==0): 
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
        elif distance_pos_x == -1 and distance_pos_y == -1:
            if (self.world.wall_map[self.pos_y+distance_pos_y][self.pos_x][0]==0 and self.world.wall_map[self.pos_y][self.pos_x][2]==0) or (self.world.wall_map[self.pos_y][self.pos_x+distance_pos_x][2]==0 and self.world.wall_map[self.pos_y][self.pos_x][0]==0): 
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
        elif distance_pos_x == 1 and distance_pos_y == -1:
            if (self.world.wall_map[self.pos_y+distance_pos_y][self.pos_x][3]==0 and self.world.wall_map[self.pos_y][self.pos_x][2]==0) or (self.world.wall_map[self.pos_y][self.pos_x+distance_pos_x][2]==0 and self.world.wall_map[self.pos_y][self.pos_x][3]==0): 
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
        elif distance_pos_x == -1 and distance_pos_y == 1:
            if (self.world.wall_map[self.pos_y+distance_pos_y][self.pos_x][0]==0 and self.world.wall_map[self.pos_y][self.pos_x][1]==0) or (self.world.wall_map[self.pos_y][self.pos_x+distance_pos_x][1]==0 and self.world.wall_map[self.pos_y][self.pos_x][0]==0): 
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
        elif distance_pos_x in [-2,-1,1,2] and distance_pos_y == 0:
            if distance_pos_x == -2 and self.world.wall_map[self.pos_y][self.pos_x-1][0] == 0 and self.world.wall_map[self.pos_y][self.pos_x-1][3] ==0:
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
            elif distance_pos_x == -1 and self.world.wall_map[self.pos_y][self.pos_x][0] == 0:
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
            elif distance_pos_x == 2 and self.world.wall_map[self.pos_y][self.pos_x+1][0] == 0 and self.world.wall_map[self.pos_y][self.pos_x+1][3] ==0:
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
            elif distance_pos_x == 1 and self.world.wall_map[self.pos_y][self.pos_x][3] == 0:
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
        elif distance_pos_y in [-2,-1,1,2] and distance_pos_x == 0:
            if distance_pos_y == -2 and self.world.wall_map[self.pos_y-1][self.pos_x][2] == 0 and self.world.wall_map[self.pos_y-1][self.pos_x][1] ==0:
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
            elif distance_pos_y == -1 and self.world.wall_map[self.pos_y][self.pos_x][2] == 0:
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
            elif distance_pos_y == 2 and self.world.wall_map[self.pos_y+1][self.pos_x][2] == 0 and self.world.wall_map[self.pos_y+1][self.pos_x][1] ==0:
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
            elif distance_pos_y == 1 and self.world.wall_map[self.pos_y][self.pos_x][1] == 0:
                if self.seeing == 0:
                    self.world.board.event_data("Warning! Zombie see you")
                return True
#        print("Can't find")
        if self.seeing==1:
            self.world.board.event_data("Success! One Zombie can't find you")
        return False

    def check_zombie_team(self, movement_x, movement_y):
#        print("Check team")
        for count in range(self.num_zombie):
            if count != self.id and self.world.zombie[count].pos_x == (self.pos_x + movement_x) and self.world.zombie[count].pos_y == (self.pos_y + movement_y):
#                print("I don't move this way because have my team")
                if self.world.zombie[count].status == 1:
                    return False
        return True

    def check_wall(self, movement_x, movement_y):
        if movement_x == -1 and self.world.wall_map[self.pos_y][self.pos_x][0] == 1:
            return False
        elif movement_x == 1 and self.world.wall_map[self.pos_y][self.pos_x][3] == 1:
            return False
        if movement_y == -1 and self.world.wall_map[self.pos_y][self.pos_x][2] == 1:
            return False
        if movement_y == 1 and self.world.wall_map[self.pos_y][self.pos_x][1] == 1:
            return False
        return True            
 
    def looking_black_hole(self, check_x, check_y):
        for test_key in self.world.trap_keys.keys():
            if self.world.trap_keys[test_key][0] == check_y and self.world.trap_keys[test_key][1] == check_x:
                if self.world.trap_keys[test_key][2] == 1:
                    return False               
                else:
                    return True
        return True  

    def check_black_hole(self):
        for test_key in self.world.trap_keys.keys():
            if self.world.trap_keys[test_key][0] == self.pos_y and self.world.trap_keys[test_key][1] == self.pos_x:
#                print("this position have black hole")
                if self.world.trap_keys[test_key][2] == 1:
                    print("zombie dead")
                    self.world.board.event_data("One zombie dead :D")
                    self.status = 0
                else:
                    None
                break 

    def check_switch(self):
        if self.world.plan_map[self.pos_y][self.pos_x] > 10:
            self.world.open_or_close(self.world.plan_map[self.pos_y][self.pos_x],"zombie",self.pos_x,self.pos_y)
