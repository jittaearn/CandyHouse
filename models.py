import arcade.key


DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }


class Gretel:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
 
    def move(self, direction):
        self.x += DIR_OFFSETS[direction][0]
        self.y += DIR_OFFSETS[direction][1]
 
    def update(self, delta):
        self.move(self.direction)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
 
        self.gretel = Gretel(self, width // 2, height // 2)
 
    def update(self, delta):
        self.gretel.update(delta)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.gretel.direction = DIR_UP
        if key == arcade.key.LEFT:
            self.gretel.direction = DIR_LEFT
        if key == arcade.key.RIGHT:
            self.gretel.direction = DIR_RIGHT