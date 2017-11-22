import arcade, arcade.key, time

from detail_of_board import Board
from vs_map import VS_Map

NUM_ROW = 13
NUM_COLUMN = 17

WIDTH = 51
HIGHT = 51
SCREEN_BOARD = 350
SCREEN_WIDTH = NUM_COLUMN * WIDTH +1 +SCREEN_BOARD 
SCREEN_HIGHT = NUM_ROW * HIGHT +1
SCREEN_MAP = NUM_COLUMN * WIDTH + 1

if NUM_COLUMN*NUM_ROW >=50:
    NUM_TRAP = NUM_ROW*NUM_COLUMN*50//100
    NUM_TRAP += NUM_TRAP%6
else:
    NUM_TRAP = NUM_ROW*NUM_COLUMN*5//100

NUM_WALL = NUM_ROW*NUM_COLUMN*38//100

NUM_ZOMBIE = NUM_ROW*NUM_COLUMN*20//100
#NUM_ZOMBIE = 5
class Game_Character(arcade.Sprite):
    def __init__(self, *location_of_picture, **character):
        self.knight = character.pop('knight', None)
        self.zombie = character.pop('zombie',None)
        super().__init__(*location_of_picture, **character)

    def sync_with_model(self):
        if self.knight:
            self.set_position(self.knight.real_x, self.knight.real_y)
        elif self.zombie:
            self.set_position(self.zombie.real_x, self.zombie.real_y)

    def draw(self):
        self.sync_with_model()
        super().draw()

class Game_Window(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height,"Run Out of ZOMBIES")
        arcade.set_background_color(arcade.color.WHITE)
        self.current_state = "welcome"
        self.point = 1
        self.time = 1
        self.background = arcade.load_texture("images/welcome_background.png")
        self.select_classic = arcade.load_texture("images/select_1.png")
        self.select_survival = arcade.load_texture("images/select_2.png")
        self.select_team = arcade.load_texture("images/select_3.png")
        self.num_of_player = []
        self.classic_tab = 0
        self.p1_tab = 0
        self.p2_tab = 0
        self.p3_tab = 0
        self.p4_tab = 0
        self.classic_setting1 = arcade.load_texture("images/classic_setting1.png")
        self.classic_setting2 = arcade.load_texture("images/classic_setting2.png")
        self.gg = arcade.load_texture("images/gameover_background.png")
#  set about key
        self.all_key = [119,97,100,115,116,102,103,104,65362,65361,65364,65363,106,105,107,108]
        self.all_up = [119, 65362, 116, 105]
        self.all_down = [115, 65364, 103, 107]
        self.all_right = [100, 65363, 108, 104]
        self.all_left = [97, 102, 65361, 106]
        self.key_01 = [97,119,115,100]
        self.key_02 = [65361, 65362, 65364, 65363]
        self.key_03 = [102, 116, 103, 104]
        self.key_04 = [106, 105, 107, 108]
# set picture
        self.tns_setting = arcade.load_texture("images/team_n_survival_setting.png")
        self.k1_sprite = arcade.Sprite('images/knightsp_01.png')
        self.k1_sprite.set_position(150,150)
        self.k2_sprite = arcade.Sprite('images/knightsp_02.png')
        self.k2_sprite.set_position(SCREEN_WIDTH/4+160,160)
        self.k3_sprite = arcade.Sprite('images/knightsp_03.png')
        self.k3_sprite.set_position(SCREEN_WIDTH/2+160,160)
        self.k4_sprite = arcade.Sprite('images/knightsp_04.png')
        self.k4_sprite.set_position(3/4*SCREEN_WIDTH+170,170)
  
    def update(self, data):
#        print("Update_in_Game_Window")
        if self.current_state == "setting_game":
            print("Seting_Game")
            self.setup_map= []
            self.zombie_sprite = []
            for row in range(NUM_ROW):
                self.setup_map.append([])
                for column in range(NUM_COLUMN):
                    self.setup_map[row].append(0)
            self.map = VS_Map(SCREEN_WIDTH,SCREEN_HIGHT,WIDTH,HIGHT,self.setup_map,NUM_TRAP,NUM_ZOMBIE,NUM_WALL,SCREEN_MAP+10,self)
            self.num_of_player = [1] # set number of player
            self.map.create_knight(self.num_of_player)
            self.knight_01_sprite = Game_Character('images/Knight_02.png',knight=self.map.knight_01)
            self.knight_02_sprite = Game_Character('images/Knight.png',knight=self.map.knight_02)
            self.knight_04_sprite = Game_Character('images/Knight_04.png',knight=self.map.knight_04)
            self.knight_03_sprite = Game_Character('images/Knight_03.png',knight=self.map.knight_03)
            self.current_state = "game_running"
            for count in range(NUM_ZOMBIE):
                self.zombie_sprite.append(Game_Character('images/Zombie_01.png',zombie=self.map.zombie[count]))
            self.current_state = "game_running"
            
        elif self.current_state == "game_running":
            if 1 == self.num_of_player[0]:
                if self.map.knight_01.status == 2:
                    self.current_state = "you_win"
                elif self.map.knight_01.status in [3,4] :
                    self.current_state = "you_lose"
            elif 2 == self.num_of_player[0]:
                if self.map.knight_02.status == 2:
                    self.current_state = "you_win"
                elif self.map.knight_02.status in [3,4] :
                    self.current_state = "you_lose"
            elif 3 == self.num_of_player[0]:
                if self.map.knight_03.status == 2:
                    self.current_state = "you_win"
                elif self.map.knight_03.status == [3,4] :
                    self.current_state = "you_lose"
            elif 4 == self.num_of_player[0]:
                if self.map.knight_04.status == 2:
                    self.current_state = "you_win"
                elif self.map.knight_04.status == [3,4] :
                    self.current_state = "you_lose"
            for count in range(len(self.zombie_sprite)):
                if self.map.zombie[count].seeing in [1,2]:
                    self.zombie_sprite[count] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[count])
                else:
                    self.zombie_sprite[count] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[count])

        elif self.current_state == "set_vs_game":
            print("set_vs_Game")
            self.setup_map= []
            for row in range(NUM_ROW):
                self.setup_map.append([])
                for column in range(NUM_COLUMN):
                    self.setup_map[row].append(0)
            self.map = VS_Map(SCREEN_WIDTH,SCREEN_HIGHT,WIDTH,HIGHT,self.setup_map,(NUM_TRAP*2)//3,NUM_ZOMBIE,NUM_WALL,SCREEN_MAP+10,self)
#            print("Set map finish")
#            self.num_of_player = [1,2,3,4] # set number of player
            self.map.create_knight(self.num_of_player)
            self.knight_01_sprite = Game_Character('images/Knight_02.png',knight=self.map.knight_01)
            self.knight_02_sprite = Game_Character('images/Knight.png',knight=self.map.knight_02)
            self.knight_03_sprite = Game_Character('images/Knight_03.png',knight=self.map.knight_03)
            self.knight_04_sprite = Game_Character('images/Knight_04.png',knight=self.map.knight_04)
            self.zombie_sprite = []
            for count in range(NUM_ZOMBIE):
                self.zombie_sprite.append(Game_Character('images/Zombie_01.png',zombie=self.map.zombie[count]))
#            print("Have all Zombie")
            self.current_state = "vs_game"
            self.start_time = time.time()
            self.set_time = self.start_time
            self.num_zombie_update = 0
            self.num_zombie_update_02 = (NUM_ZOMBIE)//2
            self.num_zombie_update_03 = (NUM_ZOMBIE)//3
            self.num_zombie_update_04 = (NUM_ZOMBIE)//4
            self.num_zombie_update_05 = (NUM_ZOMBIE)//5
#            print("finish set_vs_game")

        elif self.current_state == "vs_game":
            self.current_time = time.time() 
            if self.current_time - self.start_time > 31:
                self.current_state = "time_out"
            self.map.knight_01.check_zombie_on_map(2)
            self.map.knight_01.check_black_hole()
            self.map.knight_02.check_zombie_on_map(2)
            self.map.knight_02.check_black_hole()
            self.map.knight_03.check_zombie_on_map(2)
            self.map.knight_03.check_black_hole()
            self.map.knight_04.check_zombie_on_map(2)
            self.map.knight_04.check_black_hole()
#            print("first time of in run out of Zombie")
#            print("vs_game")
            if self.map.knight_01.status == 2 or self.map.knight_02.status == 2 or self.map.knight_03.status == 2 or self.map.knight_04.status == 2:
                self.current_state = "vs_win"
            elif self.map.knight_01.status in [0,3,4,5] and self.map.knight_02.status in [0,3,4,5] and self.map.knight_03.status in [0,3,4,5] and self.map.knight_04.status in [0,3,4,5] and self.map.knight_04.status in [0,3,4,5] :
                self.current_state = "vs_lose"
#            if self.current_time - self.set_time >= 0.0001:
# detail about update zombie 1 zombie per time
            self.map.zombie[self.num_zombie_update].update()
            if self.map.zombie[self.num_zombie_update].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update])
            else:
                self.zombie_sprite[self.num_zombie_update] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update])
            self.num_zombie_update += 1
            if self.num_zombie_update == NUM_ZOMBIE:
                self.num_zombie_update = 0
# detail about update zombie 2 zombie per time
            self.map.zombie[self.num_zombie_update_02].update()
            if self.map.zombie[self.num_zombie_update_02].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update_02] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_02])
            else:
                self.zombie_sprite[self.num_zombie_update_02] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_02])
            self.num_zombie_update_02 += 1
            if self.num_zombie_update_02 == NUM_ZOMBIE:
                self.num_zombie_update_02 = 0
# detail about update zombie 3 zombie per time
            self.map.zombie[self.num_zombie_update_03].update()
            if self.map.zombie[self.num_zombie_update_03].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update_03] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_03])
            else:
                self.zombie_sprite[self.num_zombie_update_03] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_03])
            self.num_zombie_update_03 += 1
            if self.num_zombie_update_03 == NUM_ZOMBIE:
                self.num_zombie_update_03 = 0
# detail about update zombie 4 zombie per time
            self.map.zombie[self.num_zombie_update_04].update()
            if self.map.zombie[self.num_zombie_update_04].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update_04] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_04])
            else:
                self.zombie_sprite[self.num_zombie_update_04] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_04])
            self.num_zombie_update_04 += 1
            if self.num_zombie_update_04 == NUM_ZOMBIE:
                self.num_zombie_update_04 = 0
# detail about update zombie 5 zombie per time
            self.map.zombie[self.num_zombie_update_05].update()
            if self.map.zombie[self.num_zombie_update_05].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update_05] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_05])
            else:
                self.zombie_sprite[self.num_zombie_update_05] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_05])
            self.num_zombie_update_05 += 1
            if self.num_zombie_update_05 == NUM_ZOMBIE:
                self.num_zombie_update_05 = 0

        elif self.current_state == "set_team_game":
            print("set_vs_Game")
            self.setup_map= []
            for row in range(NUM_ROW):
                self.setup_map.append([])
                for column in range(NUM_COLUMN):
                    self.setup_map[row].append(0)
            self.map = VS_Map(SCREEN_WIDTH,SCREEN_HIGHT,WIDTH,HIGHT,self.setup_map,(NUM_TRAP*2)//3,NUM_ZOMBIE,NUM_WALL,SCREEN_MAP+10,self)
#            print("Set map finish")
#            self.num_of_player = [1,2,3,4] # set number of player
            self.map.create_knight(self.num_of_player)
            self.knight_01_sprite = Game_Character('images/Knight_02.png',knight=self.map.knight_01)
            self.knight_02_sprite = Game_Character('images/Knight.png',knight=self.map.knight_02)
            self.knight_03_sprite = Game_Character('images/Knight_03.png',knight=self.map.knight_03)
            self.knight_04_sprite = Game_Character('images/Knight_04.png',knight=self.map.knight_04)
            self.zombie_sprite = []
            for count in range(NUM_ZOMBIE):
                self.zombie_sprite.append(Game_Character('images/Zombie_01.png',zombie=self.map.zombie[count]))
#            print("Have all Zombie")
            self.current_state = "team_game"
            self.start_time = time.time()
            self.set_time = self.start_time
            self.num_zombie_update = 0
            self.num_zombie_update_02 = (NUM_ZOMBIE)//2
            self.num_zombie_update_03 = (NUM_ZOMBIE)//3
            self.num_zombie_update_04 = (NUM_ZOMBIE)//4
            self.num_zombie_update_05 = (NUM_ZOMBIE)//5
#            print("finish set_vs_game")

        elif self.current_state == "team_game":
            self.current_time = time.time() 
            if self.current_time - self.start_time > 31:
                self.current_state = "time_out"
            self.map.knight_01.check_zombie_on_map(2)
            self.map.knight_01.check_black_hole()
            self.map.knight_02.check_zombie_on_map(2)
            self.map.knight_02.check_black_hole()
            self.map.knight_03.check_zombie_on_map(2)
            self.map.knight_03.check_black_hole()
            self.map.knight_04.check_zombie_on_map(2)
            self.map.knight_04.check_black_hole()
#            print("first time of in run out of Zombie")
#            print("vs_game")
            if self.map.knight_01.status == 2 or self.map.knight_02.status == 2 or self.map.knight_03.status == 2 or self.map.knight_04.status == 2:
                self.current_state = "team_win"
            elif self.map.knight_01.status in [0,3,4,5] and self.map.knight_02.status in [0,3,4,5] and self.map.knight_03.status in [0,3,4,5] and self.map.knight_04.status in [0,3,4,5] and self.map.knight_04.status in [0,3,4,5] :
                self.current_state = "team_lose"
#            if self.current_time - self.set_time >= 0.0001:
# detail about update zombie 1 zombie per time
            self.map.zombie[self.num_zombie_update].update()
            if self.map.zombie[self.num_zombie_update].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update])
            else:
                self.zombie_sprite[self.num_zombie_update] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update])
            self.num_zombie_update += 1
            if self.num_zombie_update == NUM_ZOMBIE:
                self.num_zombie_update = 0
# detail about update zombie 2 zombie per time
            self.map.zombie[self.num_zombie_update_02].update()
            if self.map.zombie[self.num_zombie_update_02].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update_02] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_02])
            else:
                self.zombie_sprite[self.num_zombie_update_02] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_02])
            self.num_zombie_update_02 += 1
            if self.num_zombie_update_02 == NUM_ZOMBIE:
                self.num_zombie_update_02 = 0
# detail about update zombie 3 zombie per time
            self.map.zombie[self.num_zombie_update_03].update()
            if self.map.zombie[self.num_zombie_update_03].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update_03] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_03])
            else:
                self.zombie_sprite[self.num_zombie_update_03] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_03])
            self.num_zombie_update_03 += 1
            if self.num_zombie_update_03 == NUM_ZOMBIE:
                self.num_zombie_update_03 = 0
# detail about update zombie 4 zombie per time
            self.map.zombie[self.num_zombie_update_04].update()
            if self.map.zombie[self.num_zombie_update_04].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update_04] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_04])
            else:
                self.zombie_sprite[self.num_zombie_update_04] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_04])
            self.num_zombie_update_04 += 1
            if self.num_zombie_update_04 == NUM_ZOMBIE:
                self.num_zombie_update_04 = 0
# detail about update zombie 5 zombie per time
            self.map.zombie[self.num_zombie_update_05].update()
            if self.map.zombie[self.num_zombie_update_05].seeing in [1,2,3,4]:
                self.zombie_sprite[self.num_zombie_update_05] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_05])
            else:
                self.zombie_sprite[self.num_zombie_update_05] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_05])
            self.num_zombie_update_05 += 1
            if self.num_zombie_update_05 == NUM_ZOMBIE:
                self.num_zombie_update_05 = 0

    def time_out(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.gg)
        output = "Do you have brain?"
        size = 40
        delete_length = len(output)/2.5*size
        arcade.draw_text(output,SCREEN_WIDTH/2,500,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 25
        if 1 in self.num_of_player :
            output = "{:0>2.0f}".format(self.map.knight_01.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 2 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_02.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 3 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_03.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 4 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_04.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 20
        output = "Player01"
        arcade.draw_text(output,SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player02"
        arcade.draw_text(output,SCREEN_WIDTH/4+200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player03"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4-200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player04"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Press any key to try again"
        arcade.draw_text(output,SCREEN_WIDTH/2,100,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")

    def vs_lose(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.gg)
        output = "You all Lose"
        size = 50
        delete_length = len(output)/2.5*size
        arcade.draw_text(output,SCREEN_WIDTH/2,500,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 25
        if 1 in self.num_of_player :
            output = "{:0>2.0f}".format(self.map.knight_01.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 2 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_02.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 3 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_03.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 4 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_04.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 20
        output = "Player01"
        arcade.draw_text(output,SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player02"
        arcade.draw_text(output,SCREEN_WIDTH/4+200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player03"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4-200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player04"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Press any key to continue"
        arcade.draw_text(output,SCREEN_WIDTH/2,100,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")

    def vs_win(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.gg)
        if self.map.knight_01.status == 2 and self.map.knight_02.status == 2 and self.map.knight_03.status == 2 and self.map.knight_04.status == 2:
            if self.map.knight_01.kill > self.map.knight_02.kill and self.map.knight_01.kill > self.map.knight_03.kill and self.map.knight_01.kill > self.map.knight_04.kill:
                output = "Player 1 is winner"
            elif self.map.knight_02.kill > self.map.knight_01.kill and self.map.knight_02.kill > self.map.knight_03.kill and self.map.knight_02.kill > self.map.knight_04.kill:
                output = "Player 2 is winner"
            elif self.map.knight_03.kill > self.map.knight_01.kill and self.map.knight_03.kill > self.map.knight_02.kill and self.map.knight_03.kill > self.map.knight_04.kill:
                output = "Player 3 is winner"
            elif self.map.knight_04.kill > self.map.knight_01.kill and self.map.knight_04.kill > self.map.knight_02.kill and self.map.knight_04.kill > self.map.knight_03.kill:
                output = "Player 4 is winner"
            else:
                output = "draw"
        elif self.map.knight_01.status == 2:
            output = "Player 1 is winner"
        elif self.map.knight_02.status == 2:
            output = "Player 2 is winner"
        elif self.map.knight_03.status == 2:
            output = "Player 3 is winner"
        elif self.map.knight_04.status == 2:
            output = "Player 4 is winner"
        if output == "draw":
            size = 60
        else:
            size = 40
        #delete_length = len(output)/2.5*size
        arcade.draw_text(output,SCREEN_WIDTH/2,500,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 25
        if 1 in self.num_of_player :
            output = "{:0>2.0f}".format(self.map.knight_01.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 2 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_02.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 3 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_03.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 4 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_04.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 20
        output = "Player01"
        arcade.draw_text(output,SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player02"
        arcade.draw_text(output,SCREEN_WIDTH/4+200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player03"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4-200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player04"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Press any key to continue"
        arcade.draw_text(output,SCREEN_WIDTH/2,100,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")


    def team_win(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.gg)
        if (self.map.knight_01.status == 2 or self.map.knight_03.status == 2) and (self.map.knight_02.status == 2 or self.map.knight_04.status == 2 ):
            if self.map.knight_01.kill + self.map.knight_03.kill > self.map.knight_02.kill + self.map.knight_04.kill:
                output = "Team 1 is winner"
            elif self.map.knight_01.kill + self.map.knight_03.kill < self.map.knight_02.kill + self.map.knight_04.kill:
                output = "Team 2 is winner"
            else:
                output = "draw"
        elif self.map.knight_01.status == 2 or self.map.knight_03.status == 2:
            output = "Team 1 is winner"
        elif self.map.knight_02.status == 2 or self.map.knight_04.status == 2:
            output = "Team 2 is winner"
        if output == "draw":
            size = 60
        else:
            size = 40
        #delete_length = len(output)/2.5*size
        arcade.draw_text(output,SCREEN_WIDTH/2,500,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 25
        if 1 in self.num_of_player :
            output = "{:0>2.0f}".format(self.map.knight_01.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 3 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_03.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 2 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_02.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 4 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_04.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 20
        output = "Player01"
        arcade.draw_text(output,SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player03"
        arcade.draw_text(output,SCREEN_WIDTH/4+200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player02"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4-200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player04"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Press any key to continue"
        arcade.draw_text(output,SCREEN_WIDTH/2,100,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        

    def team_lose(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.gg)
        output = "You all Lose"
        size = 50
        delete_length = len(output)/2.5*size
        arcade.draw_text(output,SCREEN_WIDTH/2,500,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 25
        if 1 in self.num_of_player :
            output = "{:0>2.0f}".format(self.map.knight_01.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 3 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_03.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4+200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 2 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_02.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3 - 200,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        if 4 in self.num_of_player:
            output = "{:0>2.0f}".format(self.map.knight_04.kill)
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        else:
            output = "--"
            arcade.draw_text(output,SCREEN_WIDTH/4*3,275,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        size = 20
        output = "Player01"
        arcade.draw_text(output,SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player03"
        arcade.draw_text(output,SCREEN_WIDTH/4+200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player02"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4-200,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Player04"
        arcade.draw_text(output,SCREEN_WIDTH-SCREEN_WIDTH/4,375,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")
        output = "Press any key to continue"
        arcade.draw_text(output,SCREEN_WIDTH/2,100,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")


    def draw_win_game(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.gg)
        output = "Congraturation!!!"
        size = 60
        delete_length = len(output)//2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - 300, SCREEN_HIGHT/2, arcade.color.RED, size, anchor_x = "center" ,  anchor_y = "center", align = "center")
        output = "You Win"
        delete_length = len(output)//2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - 200, SCREEN_HIGHT/2- (3*size/2), arcade.color.RED, 60 , anchor_x = "center" ,anchor_y="center", align="center")
        output = "Press any key to continue"
        size = 20
        delete_length = len(output)/2.5*size
        arcade.draw_text(output,SCREEN_WIDTH/2,100,arcade.color.RED, size, width=500, align="center",anchor_x="center", anchor_y="center")


    def draw_lose_game(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.gg)
        arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HIGHT/2 + 100, arcade.color.RED, 60, anchor_x = "center", anchor_y = "center", align = "center")
        arcade.draw_text("You Lose", SCREEN_WIDTH/2, SCREEN_HIGHT/2, arcade.color.RED, 60, anchor_x="center", anchor_y="center", align="center")
        arcade.draw_text("Press any key to continue", SCREEN_WIDTH/2, SCREEN_HIGHT/2 - 80, arcade.color.RED, 20, anchor_x="center", anchor_y="center", align="center")

    def interface(self):
        if self.point == 1:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.select_classic)
        elif self.point == 2:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.select_survival)
        else:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.select_team)

    def welcome(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.background)
        if self.time<=30:
            arcade.draw_text("Press any key to Start", SCREEN_WIDTH/2,100,arcade.color.RED_DEVIL,30, anchor_x = "center", anchor_y = "center", align = "center")
        if self.time>60:
            self.time=1
        self.time+=1

    def set_classic(self):
        if self.classic_tab%2!=0:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.classic_setting2)
        else:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.classic_setting1)

    def set_survival(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2,SCREEN_WIDTH, SCREEN_HIGHT, self.tns_setting)
        if self.p1_tab%2!=0:
            '''
            arcade.draw_text("P1", 100,100,arcade.color.RED_DEVIL,30)
            '''
            self.k1_sprite.draw()
        if self.p2_tab%2!=0:
            '''
            arcade.draw_text("P2", 400,100,arcade.color.RED_DEVIL,30)
            '''
            self.k2_sprite.draw()
        if self.p3_tab%2!=0:
            '''
            arcade.draw_text("P3", 700,100,arcade.color.RED_DEVIL,30)
            '''
            self.k3_sprite.draw()
        if self.p4_tab%2!=0:
            '''
            arcade.draw_text("P3", 1100,100,arcade.color.RED_DEVIL,30)
            '''
            self.k4_sprite.draw()

#        if self.p1_tab%2!=0:
#            arcade.draw_text("P1", 100,100,arcade.color.RED_DEVIL,30)
#        if self.p2_tab%2!=0:
#            arcade.draw_text("P2", 400,100,arcade.color.RED_DEVIL,30)
#        if self.p3_tab%2!=0:
#            arcade.draw_text("P3", 700,100,arcade.color.RED_DEVIL,30)
#        if self.p4_tab%2!=0:
#            arcade.draw_text("P4", 1000,100,arcade.color.RED_DEVIL,30)

    def on_draw(self):
        arcade.start_render()
#        print("In on draw is {}".format(self.current_state))
        if self.current_state == "game_running":
            self.map.draw_grid()
            self.map.draw_wall()
#            if self.map.knight_01.status == 1:
#                self.knight_01_sprite.draw()
            self.draw_knight()
            self.map.draw_trap()
            for count in range(NUM_ZOMBIE):
                if self.map.zombie[count].status == 1:
                    self.zombie_sprite[count].draw()
            self.map.set_up = 0
            self.map.board.standard_draw()
            self.map.board.event_draw()
        elif self.current_state == "you_win":
            self.draw_win_game()
        elif self.current_state == "you_lose":
            self.draw_lose_game()
        elif self.current_state == "interface":
            self.interface()
        elif self.current_state == "welcome":
            arcade.set_background_color(arcade.color.BLACK)
            self.welcome()
        elif self.current_state == "set_classic":
            self.set_classic()
        elif self.current_state == "set_survival":
            self.set_survival()
        elif self.current_state == "set_team":
            self.set_survival()
        elif self.current_state == "time_out":
            self.time_out()
        elif self.current_state == "team_lose":
            self.team_lose()
        elif self.current_state == "vs_lose":
            self.vs_lose()
        elif self.current_state == "vs_win":
            self.vs_win()
        elif self.current_state == "team_win":
            self.team_win()
        elif self.current_state == "vs_game":
            self.map.draw_grid()
            self.map.draw_wall()
            self.draw_knight()
            self.map.draw_trap()
            count = 0
            while count < NUM_ZOMBIE:
                if self.map.zombie[count].status == 1:
                    self.zombie_sprite[count].draw()
                count += 1
            self.map.set_up = 0
            self.map.board.vs_standard_draw()
            self.map.board.event_draw()            
        elif self.current_state == "team_game":
            self.map.draw_grid()
            self.map.draw_wall()
            self.draw_knight()
            self.map.draw_trap()
            count = 0
            while count < NUM_ZOMBIE:
                if self.map.zombie[count].status == 1:
                    self.zombie_sprite[count].draw()
                count += 1
            self.map.set_up = 0
            self.map.board.vs_standard_draw()
            self.map.board.event_draw()            

    def draw_knight(self):
        if self.map.knight_01.status == 1:
            self.knight_01_sprite.draw()
        if self.map.knight_02.status == 1:
            self.knight_02_sprite.draw()
        if self.map.knight_03.status == 1:
            self.knight_03_sprite.draw()
        if self.map.knight_04.status == 1:
            self.knight_04_sprite.draw()

    def on_key_press(self, key, key_modifiers):
        print(key)
        if key == 65307:
            self.current_state = "interface"
        elif key in self.all_left and self.current_state == "welcome":
            exit(0)
            arcade.close_window()
        elif key in self.all_key and self.current_state == "welcome":
            arcade.set_background_color(arcade.color.WHITE)
            self.point = 1
            self.current_state = "interface"
        elif self.current_state == "game_running":
            self.map.on_key_press(key, key_modifiers)
        elif self.current_state == "vs_game":
            self.map.on_key_press(key, key_modifiers)
        elif self.current_state == "team_game":
            self.map.on_key_press(key, key_modifiers)
        elif self.current_state in ["you_lose","you_win","time_out","vs_lose","vs_win","team_win","team_lose"] and key in self.all_key:
            self.current_state = "interface"
            self.point = 1
        elif self.current_state == "interface" and key in self.all_up:
            if self.point == 1:
                self.point = 1
            else:
                self.point -= 1
        elif self.current_state == "interface" and key in self.all_down:
            if self.point==3:
                self.point = 3
            else:
                self.point+=1
        elif self.current_state == "interface" and key in self.all_left:
            self.current_state = "welcome"
        elif self.current_state in ["set_classic","set_survival","set_team"] and key in self.all_left:
            self.current_state = "interface"
            self.point = 1
#Classic Mode
        elif self.current_state == "interface" and key in [100, 65363, 104, 108] and self.point == 1:
            self.classic_tab=0
            self.current_state = "set_classic"
        elif self.current_state == "set_classic" and key == 119:
            self.classic_tab+=1
        elif self.current_state == "set_classic" and key in [100, 65363, 104, 108] and self.classic_tab%2!=0:
            self.current_state = "setting_game"
#Survival Mode
        elif self.current_state == "interface" and key in [100, 65363, 104, 108] and self.point == 2:
            self.num_of_player = []
            self.p1_tab=0
            self.p2_tab=0
            self.p3_tab=0
            self.p4_tab=0
            self.current_state = "set_survival"
#set number of player for survival mode
        elif self.current_state == "set_survival" and key == 119:
            self.p1_tab+=1
            if self.p1_tab%2!=0:
                self.num_of_player.append(1)
            elif self.p1_tab%2==0 and self.p1_tab!=0:
                self.num_of_player.remove(1)
        elif self.current_state == "set_survival" and key == 65362:
            self.p2_tab+=1
            if self.p2_tab%2!=0:
                self.num_of_player.append(2)
            elif self.p2_tab%2==0 and self.p2_tab!=0:
                self.num_of_player.remove(2)
        elif self.current_state == "set_survival" and key == 116:
            self.p3_tab+=1
            if self.p3_tab%2!=0:
                self.num_of_player.append(3)
            elif self.p3_tab%2==0 and self.p3_tab!=0:
                self.num_of_player.remove(3)
        elif self.current_state == "set_survival" and key == 105:
            self.p4_tab+=1
            if self.p4_tab%2!=0:
                self.num_of_player.append(4)
            elif self.p4_tab%2==0 and self.p4_tab!=0:
                self.num_of_player.remove(4)
        elif self.current_state=="set_survival" and len(self.num_of_player) >= 2 and key in [100, 65363, 104, 108]:
            print(self.num_of_player)
            print(len(self.num_of_player))
            self.current_state = "set_vs_game"
#Team Mode
        elif self.current_state == "interface" and key in [100, 65363, 104, 108] and self.point == 3:
            self.num_of_player = []
            self.p1_tab=0
            self.p2_tab=0
            self.p3_tab=0
            self.p4_tab=0
            self.current_state = "set_team"
#set number of player for team mode
        elif self.current_state == "set_team" and key == 119:
            self.p1_tab+=1
            if self.p1_tab%2!=0:
                self.num_of_player.append(1)
            elif self.p1_tab%2==0 and self.p1_tab!=0:
                self.num_of_player.remove(1)
        elif self.current_state == "set_team" and key == 65362:
            self.p2_tab+=1
            if self.p2_tab%2!=0:
                self.num_of_player.append(2)
            elif self.p2_tab%2==0 and self.p2_tab!=0:
                self.num_of_player.remove(2)
        elif self.current_state == "set_team" and key == 116:
            self.p3_tab+=1
            if self.p3_tab%2!=0:
                self.num_of_player.append(3)
            elif self.p3_tab%2==0 and self.p3_tab!=0:
                self.num_of_player.remove(3)
        elif self.current_state == "set_team" and key == 105:
            self.p4_tab+=1
            if self.p4_tab%2!=0:
                self.num_of_player.append(4)
            elif self.p4_tab%2==0 and self.p4_tab!=0:
                self.num_of_player.remove(4)
        elif self.current_state=="set_team" and len(self.num_of_player)==4 and key in self.all_right:
            self.current_state = "set_team_game"

if __name__ == '__main__':
    window = Game_Window(SCREEN_WIDTH, SCREEN_HIGHT)
    arcade.run()
