import arcade.key
class Ship:
    DIR_HORIZONTAL = 0
    DIR_VERTICAL = 1

    def __init__(self,world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = Ship.DIR_VERTICAL

    def switch_direction(self):
        if self.direction == Ship.DIR_HORIZONTAL:
            self.direction = Ship.DIR_VERTICAL
        else:
            self.direction = Ship.DIR_HORIZONTAL

    def update(self, delta):
        if self.direction == Ship.DIR_VERTICAL:
            if self.y > self.world.height:
                self.y = 0
            self.y += delta
        else:
            if self.x > self.world.width:
                self.x = 0
            self.x += delta

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.ship = Ship(self,100,100)

    def update(self, delta):
        self.ship.update(delta)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.switch_direction()
