import arcade

HEIGHT_SCREEN = 100
WIDTH_SCREEN = 100

class testwindow(arcade.Window):
    def __init__(self, HEIGHT_SCREEN, WIDTH_SCREEN):
        super().__init__(HEIGHT_SCREEN, WIDTH_SCREEN)
        arcade.set_background_color(arcade.color.WHITE)
        self.width = WIDTH_SCREEN
        self.height = HEIGHT_SCREEN
        
    def on_draw(self):
        arcade.start_render()

        arcade.draw_rectangle_filled(0,50,10,20, arcade.color.BLACK)
        arcade.draw_rectangle_filled(50,50,10,10, arcade.color.BLACK)
        

if __name__=="__main__":
    start = testwindow(HEIGHT_SCREEN, WIDTH_SCREEN)
    arcade.run()
