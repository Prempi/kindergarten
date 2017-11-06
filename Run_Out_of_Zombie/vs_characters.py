import arcade, random, time

class VS_Main_Character:
    def __init__(self, world, pos_x, pos_y, target, id_code):
        self.world = world
        self.id = id_code
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
        self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2
        self.limit_x = len(self.world.plan_map[0])
        self.limit_y = len(self.world.plan_map)
        self.target = target
        print("limit is %i and %i"%(self.limit_x,self.limit_y))
        self.status = 1
        self.kill = 0
        self.time = 0
# assign status 1 is alive 2 is winner 3 and 4 is die last is five die from hero

    def update(self, movement_x , movement_y):
        self.check_zombie_on_map(2)
        self.check_black_hole() 
        print("move is %i and %i"%(movement_x,movement_y))
        if self.pos_x + movement_x > -1 and self.pos_x + movement_x < self.limit_x and movement_x != 0 and self.check_wall(movement_x, movement_y) and self.status == 1:
            self.pos_x += movement_x
            self.check_map()
            self.check_zombie_on_map(1)
            self.world.check_only_black_hole()
            self.check_hero()
#            self.round += 1
#            print("----------finish round {:>3.0f}----------".format(self.round))
        elif self.pos_y + movement_y > -1 and self.pos_y + movement_y < self.limit_y and movement_y != 0 and self.check_wall(movement_x, movement_y) and self.status == 1:
            self.pos_y += movement_y
            self.check_map() 
            self.check_zombie_on_map(1) 
            self.world.check_only_black_hole()
            self.check_hero()
#            self.round += 1
#            print("----------finish round {:>3.0f}----------".format(self.round))
        self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
        self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2

    def check_hero(self):
        if self.id == 1 and self.pos_x == self.world.knight_02.pos_x and self.pos_y == self.world.knight_02.pos_y:
            self.world.knight_02.status = 5
            self.world.board.event_data("-----------------------------------------")    
            self.world.board.event_data("     Player 01 Kill Player 02     ")    
            self.world.board.event_data("-----------------------------------------")    
        elif self.id == 2 and self.pos_x == self.world.knight_01.pos_x and self.pos_y == self.world.knight_01.pos_y:
            self.world.knight_01.status = 5
            self.world.board.event_data("-----------------------------------------")    
            self.world.board.event_data("     Player 02 Kill Player 01     ")    
            self.world.board.event_data("-----------------------------------------")    

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
        elif self.world.plan_map[self.pos_y][self.pos_x] == self.target:
            print("You win")
            self.status = 2
            self.time = time.time()
            print("time = {} of {}".format(self.time,self.id))

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
                        self.kill += 1
                        self.world.board.event_data("Player "+str(self.id)+" kill zombie ")    
                    elif situation == 2:
                        print("you were biten by zombie")
                        self.status = 4
                    

class VS_Zombie_Character:
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
        if self.find_main_character(1) and self.find_main_character(2):
            self.seeing = (random.randint(1,100)%2)+1
            self.picture = arcade.Sprite("images/Zombie_02.png")
        elif self.find_main_character(1):
#            print("Zombie see you before move")
            self.seeing = 1
            self.picture = arcade.Sprite("images/Zombie_02.png")
        elif self.find_main_character(2):
#            print("Zombie see you before move")
            self.seeing = 2
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
        elif self.seeing == 1:
#            print("Zombie move mode find you")
            distance_x = self.world.knight_01.pos_x - self.pos_x
            distance_y = self.world.knight_01.pos_y - self.pos_y
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
            self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2
            self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
        elif self.seeing == 2:
#            print("Zombie move mode find you")
            distance_x = self.world.knight_02.pos_x - self.pos_x
            distance_y = self.world.knight_02.pos_y - self.pos_y
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
            self.real_y = 1 + self.pos_y*self.world.hight + self.world.hight/2
            self.real_x = 1 + self.pos_x*self.world.width + self.world.width/2
        if self.find_main_character(1):
#            print("Zombie see you before move")
            self.seeing = 1
            self.picture = arcade.Sprite("images/Zombie_02.png")
        elif self.find_main_character(2):
#            print("Zombie see you before move")
            self.seeing = 2
            self.picture = arcade.Sprite("images/Zombie_02.png")
#            print("Zombie see you after move")
        else:
            self.seeing = 0
            self.picture = arcade.Sprite("images/Zombie_01.png")
        self.picture.set_position(self.real_x,self.real_y)

    def find_main_character(self,id_knight):
#        print("Zombie will find you!!")
        if id_knight == 1:
            if self.world.knight_01.status != 1:
                return False
            distance_pos_x = self.world.knight_01.pos_x - self.pos_x
            distance_pos_y = self.world.knight_01.pos_y - self.pos_y
        elif id_knight == 2:
            if self.world.knight_02.status != 1:
                return False
            distance_pos_x = self.world.knight_02.pos_x - self.pos_x
            distance_pos_y = self.world.knight_02.pos_y - self.pos_y
#        print("{} {} {}   {} {} {}".format(distance_pos_x , self.world.knight.pos_x , self.pos_x ,distance_pos_y , self.world.knight.pos_y , self.pos_y))
        if distance_pos_x == 0 and distance_pos_y == 0:
            return True
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
