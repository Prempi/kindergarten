import arcade, arcade.key, time

from detail_of_map import Map
from detail_of_board import Board

from vs_map import VS_Map

NUM_ROW = 12
NUM_COLUMN = 16

WIDTH = 51
HIGHT = 51
SCREEN_BOARD = 400
SCREEN_WIDTH = NUM_COLUMN * WIDTH +1 +SCREEN_BOARD 
SCREEN_HIGHT = NUM_ROW * HIGHT +1
SCREEN_MAP = NUM_COLUMN * WIDTH + 1

if NUM_COLUMN*NUM_ROW >=50:
    NUM_TRAP = NUM_ROW*NUM_COLUMN*20//100
    NUM_TRAP += NUM_TRAP%6
else:
    NUM_TRAP = NUM_ROW*NUM_COLUMN*5//100

NUM_WALL = NUM_ROW*NUM_COLUMN*25//100

NUM_ZOMBIE = NUM_ROW*NUM_COLUMN*17//100
#NUM_ZOMBIE = 6
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
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.current_state = "interface"
        self.point = 1
#        self.setup_map= []
#        for row in range(NUM_ROW):
#            self.setup_map.append([])
#            for column in range(NUM_COLUMN):
#                self.setup_map[row].append(0)

#        self.map = Map(SCREEN_WIDTH,SCREEN_HIGHT,WIDTH,HIGHT,self.setup_map,NUM_TRAP,NUM_ZOMBIE,NUM_WALL,SCREEN_MAP+10)
#        self.knight_sprite = Game_Character('images/Knight.png',knight=self.map.knight)
                        
            
    def update(self, data):
#        print("Update_in_Game_Window")
        if self.current_state == "setting_game":
            print("Seting_Game")
            self.setup_map= []
            for row in range(NUM_ROW):
                self.setup_map.append([])
                for column in range(NUM_COLUMN):
                    self.setup_map[row].append(0)
            self.map = Map(SCREEN_WIDTH,SCREEN_HIGHT,WIDTH,HIGHT,self.setup_map,NUM_TRAP,NUM_ZOMBIE,NUM_WALL,SCREEN_MAP+10)
            self.knight_sprite = Game_Character('images/Knight.png',knight=self.map.knight)
            self.current_state = "game_running"
            
        elif self.current_state == "game_running":
            if self.map.knight.status == 2:
                self.current_state = "you_win"
            elif self.map.knight.status == 3 :
                print("Dead by Black Hole")
                self.current_state = "you_lose"
            elif self.map.knight.status == 4 :
                print("Dead by Zombie")
                self.current_state = "you_lose"

        elif self.current_state == "set_vs_game":
            print("set_vs_Game")
            self.setup_map= []
            for row in range(NUM_ROW):
                self.setup_map.append([])
                for column in range(NUM_COLUMN):
                    self.setup_map[row].append(0)
            self.map = VS_Map(SCREEN_WIDTH,SCREEN_HIGHT,WIDTH,HIGHT,self.setup_map,(NUM_TRAP*2)//3,NUM_ZOMBIE,NUM_WALL,SCREEN_MAP+10)
#            print("Set map finish")
            self.knight_01_sprite = Game_Character('images/Knight_02.png',knight=self.map.knight_01)
            self.knight_02_sprite = Game_Character('images/Knight.png',knight=self.map.knight_02)
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
#            print("finish set_vs_game")

        elif self.current_state == "vs_game":
            self.current_time = time.time() 
            if self.current_time - self.start_time > 31:
                self.current_state = "time_out"
            self.map.knight_01.check_zombie_on_map(2)
            self.map.knight_01.check_black_hole()
            self.map.knight_02.check_zombie_on_map(2)
            self.map.knight_02.check_black_hole()
#            print("first time of in run out of Zombie")
#            print("vs_game")
            if self.map.knight_01.status == 2 or self.map.knight_02.status == 2:
                self.current_state = "vs_win"
            elif self.map.knight_01.status in [3,4,5] and self.map.knight_02.status in [3,4,5] :
                self.current_state = "vs_lose"
#            if self.current_time - self.set_time >= 0.0001:
# detail about update zombie 1 zombie per time
            self.map.zombie[self.num_zombie_update].update()
            if self.map.zombie[self.num_zombie_update].seeing in [1,2]:
                self.zombie_sprite[self.num_zombie_update] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update])
            else:
                self.zombie_sprite[self.num_zombie_update] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update])
            self.num_zombie_update += 1
            if self.num_zombie_update == NUM_ZOMBIE:
                self.num_zombie_update = 0
# detail about update zombie 2 zombie per time
            self.map.zombie[self.num_zombie_update_02].update()
            if self.map.zombie[self.num_zombie_update_02].seeing in [1,2]:
                self.zombie_sprite[self.num_zombie_update_02] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_02])
            else:
                self.zombie_sprite[self.num_zombie_update_02] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_02])
            self.num_zombie_update_02 += 1
            if self.num_zombie_update_02 == NUM_ZOMBIE:
                self.num_zombie_update_02 = 0
# detail about update zombie 3 zombie per time
            self.map.zombie[self.num_zombie_update_03].update()
            if self.map.zombie[self.num_zombie_update_03].seeing in [1,2]:
                self.zombie_sprite[self.num_zombie_update_03] = Game_Character('images/Zombie_02.png',zombie=self.map.zombie[self.num_zombie_update_03])
            else:
                self.zombie_sprite[self.num_zombie_update_03] = Game_Character('images/Zombie_01.png',zombie=self.map.zombie[self.num_zombie_update_03])
            self.num_zombie_update_03 += 1
            if self.num_zombie_update_03 == NUM_ZOMBIE:
                self.num_zombie_update_03 = 0

    def time_out(self):
        output = "Do you have brain?"
        size = 40
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length +20, SCREEN_HIGHT/2+60, arcade.color.RED, size)

        size = 25
        output = "{:0>2.0f}:{:0>2.0f}".format(self.map.knight_01.kill,self.map.knight_02.kill)
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length - 33, SCREEN_HIGHT/2 -50, arcade.color.RED, size)
        size = 20 
        output = "Player01:Player02"
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length - 20, SCREEN_HIGHT/2, arcade.color.RED, size)
        output = "Please enter to try again"
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH - 4*delete_length, (2*size), arcade.color.RED, size)

    def vs_lose(self):
        output = "You all Lose"
        size = 50
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length  , SCREEN_HIGHT/2+60, arcade.color.RED, size)

        size = 25
        output = "{:0>2.0f}:{:0>2.0f}".format(self.map.knight_01.kill,self.map.knight_02.kill)
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length - 33, SCREEN_HIGHT/2 -50, arcade.color.RED, size)
        size = 20 
        output = "Player01:Player02"
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length - 20, SCREEN_HIGHT/2, arcade.color.RED, size)
        output = "Please enter to try again"
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH - 4*delete_length, (2*size), arcade.color.RED, size)

    def vs_win(self): 
        if self.map.knight_01.status == 2 and self.map.knight_02.status == 2:
            if self.map.knight_01.kill > self.map.knight_02.kill:
                output = "Player 1 is winner"
            elif self.map.knight_02.kill > self.map.knight_01.kill:
                output = "Player 2 is winner"
            else:
                output = "Draw"
        elif self.map.knight_01.status == 2:
            output = "Player 1 is winner"
        else:
            output = "Player 2 is winner"
        if output == "Draw":
            size = 60
        else:
            size = 40
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length + 30 , SCREEN_HIGHT/2+60, arcade.color.RED, size)

        size = 25
        output = "{:0>2.0f}:{:0>2.0f}".format(self.map.knight_01.kill,self.map.knight_02.kill)
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length - 33, SCREEN_HIGHT/2 -50, arcade.color.RED, size)
        size = 20 
        output = "Player01:Player02"
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length - 20, SCREEN_HIGHT/2, arcade.color.RED, size)
        output = "Please enter to try again"
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH - 4*delete_length, (2*size), arcade.color.RED, size)

    def draw_win_game(self):
        output = "Congraturation!!!"
        size = 60
        delete_length = len(output)//2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - 300, SCREEN_HIGHT/2, arcade.color.RED, size)
        output = "You Win"
        delete_length = len(output)//2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - 200, SCREEN_HIGHT/2- (3*size/2), arcade.color.RED, 60)
        output = "Please enter to try again"
        size = 20
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH - 4*delete_length, (2*size), arcade.color.RED, 20)

    def draw_lose_game(self):
        output = "Game Over!!!"
        size = 60
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length, SCREEN_HIGHT/2 + 40, arcade.color.RED, size)
        output = "You Lose"
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length, SCREEN_HIGHT/2-(1.5*size) + 30, arcade.color.RED, 60)
        output = "Please enter to try again"
        size = 20
        delete_length = len(output)/2.5*size
        arcade.draw_text(output, SCREEN_WIDTH - 2*delete_length, (2*size), arcade.color.RED, 20)
        if self.map.knight.status == 3:
            output = "Dead by Black Hole "
            size = 40
            delete_length = len(output)/2.5*size
            arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length + 55, SCREEN_HIGHT/2 - (3.5*size) + 10, arcade.color.RED, size)
        elif self.map.knight.status == 4:
            output = "Dead by Zombie "
            size = 40
            delete_length = len(output)//2.5*size
            arcade.draw_text(output, SCREEN_WIDTH/2 - delete_length + 10 , SCREEN_HIGHT/2 - (3.5*size), arcade.color.RED, size)

    def interface(self):
        arcade.draw_text("Classic Mode", SCREEN_WIDTH/2 -175,500,arcade.color.FLAME,30)
        arcade.draw_text("VS Mode", SCREEN_WIDTH/2 -140,200,arcade.color.ANTIQUE_FUCHSIA,30)
        if self.point == 1:
            arcade.draw_line(SCREEN_WIDTH/2 - 180,500,SCREEN_WIDTH/2 + 70,500,arcade.color.CORAL_RED)
        else:
            arcade.draw_line(SCREEN_WIDTH/2 - 140,200,SCREEN_WIDTH/2+30,200,arcade.color.CORAL_RED)

    def on_draw(self):
        arcade.start_render()
#        print("In on draw is {}".format(self.current_state))
        if self.current_state == "game_running":
            self.map.draw_grid()
            self.map.draw_wall()
            self.knight_sprite.draw()
            self.map.draw_trap()
            self.map.draw_zombie()
#            for count in range(NUM_ZOMBIE):
#                self.map.zombie[count].draw()
#            self.map.set_up = 0
            self.map.board.standard_draw()
            self.map.board.event_draw()
        elif self.current_state == "you_win":
            self.draw_win_game()
        elif self.current_state == "you_lose":
            self.draw_lose_game()
        elif self.current_state == "interface":
            self.interface()
        elif self.current_state == "time_out":
            self.time_out()
        elif self.current_state == "vs_lose":
            self.vs_lose()
        elif self.current_state == "vs_win":
            self.vs_win()
        elif self.current_state == "vs_game":
            self.map.draw_grid()
            self.map.draw_wall()
            if self.map.knight_01.status == 1:
                self.knight_01_sprite.draw()
            if self.map.knight_02.status == 1:
                self.knight_02_sprite.draw()
            self.map.draw_trap()
#            self.map.draw_zombie()
            count = 0
            while count < NUM_ZOMBIE:
                if self.map.zombie[count].status == 1:
                    self.zombie_sprite[count].draw()
                count += 1
            self.map.set_up = 0
            self.map.board.vs_standard_draw()
            self.map.board.event_draw()            

    def on_key_press(self, key, key_modifiers):
        print(key)
        if key == 65307 and self.current_state == "interface":
            exit(0)            
            arcade.close_window()
        elif key == 65307:
            self.current_state = "interface"
        elif self.current_state == "game_running":
            self.map.on_key_press(key, key_modifiers)
        elif self.current_state == "vs_game":
            self.map.on_key_press(key, key_modifiers)
        elif self.current_state in ["you_lose","you_win","time_out","vs_lose","vs_win"] and key == arcade.key.ENTER:
            self.current_state = "interface"
            self.point = 1
        elif self.current_state == "interface" and key == arcade.key.UP:
            self.point = 1
        elif self.current_state == "interface" and key == arcade.key.DOWN:
            self.point = 2
        elif self.current_state == "interface" and key == arcade.key.ENTER and self.point == 1:
            self.current_state = "setting_game"
        elif self.current_state == "interface" and key == arcade.key.ENTER and self.point == 2:
            self.current_state = "set_vs_game"

if __name__ == '__main__':
    window = Game_Window(SCREEN_WIDTH, SCREEN_HIGHT)
    arcade.run()
