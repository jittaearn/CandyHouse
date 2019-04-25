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
    GRAVITY = -1
    MAX_HEIGHT = 10
    JUMPING_VELOCITY = 10

    def __init__(self, world, x, y, breadwall):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.vy = Gretel.MAX_HEIGHT
        self.breadwall = breadwall

 
    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def jump(self):
        self.vy = Gretel.JUMPING_VELOCITY
 
    def update(self, delta):
        self.move(self.direction)
        self.y += self.vy
        if self.vy >= 0:
            self.vy += Gretel.GRAVITY

class Hanzel:
    GRAVITY = -1
    MAX_HEIGHT = 10
    JUMPING_VELOCITY = 10

    def __init__(self, world, x, y, breadwall):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.vy = Hanzel.MAX_HEIGHT
        self.breadwall = breadwall
 
    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def jump(self):
        self.vy = Hanzel.JUMPING_VELOCITY
 
    def update(self, delta):
        self.move(self.direction)
        self.y += self.vy
        if self.vy >= 0:
            self.vy += Hanzel.GRAVITY

class Platform:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
    
    def top(self):
        return self.y + 40

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.breadwall = BreadWall(self)
        self.gretel = Gretel(self, 60, 100,
                             self.breadwall)
        self.hanzel = Hanzel(self, 60, 100,
                             self.breadwall)
        self.wall = self.gen_wall()

    def gen_wall(self):
        breadwall_lst = []
        for r in range(len(self.breadwall.map)):
            for c in range(len(self.breadwall.map[0])):
                if c != ' ':
                    p = Platform(self, r, c)
                    breadwall_lst.append(p)
        return breadwall_lst

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

    def on_key_press_hanzel(self, key, key_modifiers):
        if key == arcade.key.W:
            self.hanzel.jump()
        if key == arcade.key.A:
            self.hanzel.direction = DIR_LEFT
        if key == arcade.key.D:
            self.hanzel.direction = DIR_RIGHT

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

