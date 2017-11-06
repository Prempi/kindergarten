import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class Text_Window(arcade.Window):
    def __init__(self,width,height):
        super().__init__(width,height)
        arcade.set_background_color(arcade.color.WHITE)
        self.width_screen = width
        self.height_screen = height
        
    def on_draw(self):
        arcade.start_render()
        output = "test"
        size = 60
        arcade.draw_rectangle_filled(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,60*len(output),60,arcade.color.GREEN)
        arcade.draw_text(output,SCREEN_WIDTH//2-size/4*len(output),SCREEN_HEIGHT//2-size/2,arcade.color.BRICK_RED,60)
        arcade.draw_line(0,0,60,60,arcade.color.BRICK_RED,2)

if __name__ == '__main__':
    window = Text_Window(SCREEN_WIDTH,SCREEN_HEIGHT)
    arcade.run()
