import arcade, time

def find_time(time_01,time_02):
#    print("time_01: {} \t time_02: {}".format(time_01,time_02))
    diff = time_02 - time_01
#    print("diff: {}".format(diff))
    diff -= diff%1
    diff = int(diff)
#    print("diff: {}".format(diff))
    minute = diff//60
#    print("minute: {}".format(minute))
    second = diff%60
#    print("second: {}".format(second))
    return "{:0>2.0f}:{:0>2.0f}".format(minute,second)

class Board:
    def __init__(self, SCREEN_BOARD,SCREEN_HIGHT, Map):
        self.width = SCREEN_BOARD
        self.hight = SCREEN_HIGHT
        self.map = Map
        self.data = []
        self.limit_data = 20
        self.standard_hight = 0
        self.event_hight = 0
        self.start_time = time.time()

#Draw original detail    
    def standard_draw(self):
        output = "Round : {:>3.0f}".format(self.map.knight.round)
        size = 16
        arcade.draw_text(output,self.width,self.hight - (size*2), arcade.color.BLACK, size)
        self.standard_hight = size*2
        output = "Zombie remaining : "+str(self.zombie_alive())
        size = 14
        arcade.draw_text(output,self.width,self.hight - (size*2) - self.standard_hight, arcade.color.BLACK, size)
        self.standard_hight += size*2

#Draw vs mode detail
    def vs_standard_draw(self):
        output = "Time : "+find_time(self.start_time,time.time())
        size = 16
        arcade.draw_text(output,self.width,self.hight - (size*2), arcade.color.BLACK, size)
        self.standard_hight = size*2
        output = "Zombie remaining : "+str(self.zombie_alive())
        size = 14
        arcade.draw_text(output,self.width,self.hight - (size*2) - self.standard_hight, arcade.color.BLACK, size)
        self.standard_hight += size*2

#input data to event Board
    def event_data(self, event):
#        print("event draw")
        if event == None:
            None
        elif len(self.data) <= self.limit_data:
            self.data.append(event)
        else:
            move = 1
            while move < len(self.data):
                self.data[move-1] = self.data[move]
                move += 1
            self.data[len(self.data)-1] = event 

#Draw event Board
    def event_draw(self):
        size = 12
        arcade.draw_text("-----------------------------------------------------------------------",self.width, self.hight - self.standard_hight - size*2, arcade.color.BRICK_RED, size)
        self.event_hight = size*2
        size = 12
        for count in range(len(self.data)):
            arcade.draw_text(self.data[count],self.width,self.hight - self.standard_hight - self.event_hight  - size*2, arcade.color.BLACK, size)
            self.event_hight += size*2 
            

#Count Zombie Alive    
    def zombie_alive(self):
        count = 0
#        print(len(self.map.zombie))
        for check in range(len(self.map.zombie)):
            if self.map.zombie[check].status == 1:
                count += 1
        return count
