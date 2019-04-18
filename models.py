import arcade.key


DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
MOVEMENT_SPEED = 4
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }

class Gretel:
    GRAVITY = 1
    STARTING_VELOCITY = 10
    JUMPING_VELOCITY = 10

    def __init__(self, world, x, y, breadwall, block_size):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.breadwall = breadwall
        self.block_size = block_size
        self.vy = Gretel.STARTING_VELOCITY
 
    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def jump(self):
        self.vy = Gretel.JUMPING_VELOCITY
 
    def update(self, delta):
        self.move(self.direction)
        self.y += self.vy
        self.vy -= Gretel.GRAVITY
        self.check_dots()
        
    def check_walls(self, direction):
        new_r = self.get_row() + DIR_OFFSETS[direction][1]
        new_c = self.get_col() + DIR_OFFSETS[direction][0]
        return not self.breadwall.has_breadwall_at(new_r, new_c)
 
    def check_dots(self):
        pass

    def get_row(self):
        return (self.y - self.block_size) // self.block_size
 
    def get_col(self):
        return self.x // self.block_size

class Hanzel:
    GRAVITY = 1
    STARTING_VELOCITY = 0
    JUMPING_VELOCITY = 10

    def __init__(self, world, x, y, breadwall, block_size):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.vy = Hanzel.STARTING_VELOCITY
        self.breadwall = breadwall
        self.block_size = block_size
 
    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def jump(self):
        self.vy = Hanzel.JUMPING_VELOCITY
 
    def update(self, delta):
        self.move(self.direction)
        self.y += self.vy
        self.vy -= Hanzel.GRAVITY
        self.check_dots()

    def check_walls(self, direction):
        new_r = self.get_row() + DIR_OFFSETS[direction][1]
        new_c = self.get_col() + DIR_OFFSETS[direction][0]
        return not self.breadwall.has_breadwall_at(new_r, new_c)
 
    def check_dots(self):
        pass
    
    def get_row(self):
        return (self.y - self.block_size) // self.block_size
 
    def get_col(self):
        return self.x // self.block_size

class World:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.breadwall = BreadWall(self)
        self.block_size = block_size
        self.gretel = Gretel(self, 60, 100,
                             self.breadwall,
                             self.block_size)
        self.hanzel = Hanzel(self, 60, 100,
                             self.breadwall,
                             self.block_size)
 
    def update(self, delta):
        self.gretel.update(delta)
        self.hanzel.update(delta)

    def on_key_press_gretel(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.gretel.jump()
        if key == arcade.key.LEFT:
            self.gretel.direction = DIR_LEFT
        if key == arcade.key.RIGHT:
            self.gretel.direction = DIR_RIGHT
        if key == arcade.key.DOWN:
            self.gretel.direction = DIR_DOWN

    def on_key_press_hanzel(self, key, key_modifiers):
        if key == arcade.key.W:
            self.hanzel.jump()
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
        self.map = [ '                         ',
                     '#########################',
                     '#lllllllllllllllllllllll#',
                     '#cwcllwcwcllwcwcwcllwcwc#',
                     '#                 ======#',
                     '#               ==      #',
                     '#                       #',
                     '#                       #',
                     '#__  ___________________#',
                     '#                       #',
                     '#                       #',
                     '#-----------------  ----#',
                     '#                       #',
                     '#                       #',
                     '#____  _________________#',
                     '#                       #',
                     '#                       #',
                     '#                       #',
                     '#########################',
                     '                         ',]
        self.height = len(self.map)
        self.width = len(self.map[0])

    def has_breadwall_at(self, r, c):
        return self.map[r][c] == '#'

    def has_candywall_at(self, r, c):
        return self.map[r][c] == '-'
    
    def has_candywall2_at(self, r, c):
        return self.map[r][c] == '='

    def has_candywall3_at(self, r, c):
        return self.map[r][c] == '_'

    def has_chocolava_at(self, r, c):
        return self.map[r][c] == 'l'

    def has_chocolavacurve_at(self, r, c):
        return self.map[r][c] == 'c'

    def has_chocolavacountercurve_at(self, r, c):
        return self.map[r][c] == 'w'

