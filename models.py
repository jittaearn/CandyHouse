import arcade.key


DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
MOVEMENT_SPEED = 3
 
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
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
 
    def update(self, delta):
        self.move(self.direction)

class Hanzel:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
 
    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
 
    def update(self, delta):
        self.move(self.direction)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gretel = Gretel(self, width // 2, height // 2)
        self.hanzel = Hanzel(self, width // 2, height // 2)
        self.breadwall = BreadWall(self)
 
    def update(self, delta):
        self.gretel.update(delta)
        self.hanzel.update(delta)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.gretel.direction = DIR_UP
        if key == arcade.key.LEFT:
            self.gretel.direction = DIR_LEFT
        if key == arcade.key.RIGHT:
            self.gretel.direction = DIR_RIGHT
        if key == arcade.key.DOWN:
            self.gretel.direction = DIR_DOWN

        if key == arcade.key.W:
            self.hanzel.direction = DIR_UP
        if key == arcade.key.A:
            self.hanzel.direction = DIR_LEFT
        if key == arcade.key.D:
            self.hanzel.direction = DIR_RIGHT
        if key == arcade.key.S:
            self.hanzel.direction = DIR_DOWN

    def on_key_release(self, key, key_modifers):
        self.gretel.direction = DIR_STILL
        self.hanzel.direction = DIR_STILL

class BreadWall:
    def __init__(self, world):
        self.map = [ '#########################',
                     '#lllllllllllllllllllllll#',
                     '# clw clw  clw  clw     #',
                     '#                       #',
                     '#                       #',
                     '#                       #',
                     '#                       #',
                     '#                       #',
                     '#                       #',
                     '#                       #',
                     '#                       #',
                     '#---------------  ------#',
                     '#                       #',
                     '#                       #',
                     '#--  -------------------#',
                     '#                       #',
                     '#                       #',
                     '#----------  -----------#',
                     '#                       #',
                     '#########################',]
        self.height = len(self.map)
        self.width = len(self.map[0])

    def has_breadwall_at(self, r, c):
        return self.map[r][c] == '#'

    def has_candywall_at(self, r, c):
        return self.map[r][c] == '-'

    def has_chocolava_at(self, r, c):
        return self.map[r][c] == 'l'

    def has_chocolavacurve_at(self, r, c):
        return self.map[r][c] == 'c'

    def has_chocolavacountercurve_at(self, r, c):
        return self.map[r][c] == 'w'
