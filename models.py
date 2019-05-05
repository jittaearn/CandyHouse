import arcade.key


GRAVITY = -1
JUMP_VY = 10
MAX_VX = 6
ACCX = 2
PLAYER_RADIUS = 60
WITCH_RADIUS = 60
PLATFORM_MARGIN = 5

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 6
MOVEMENT_SPEED = 4
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }

class Model:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

class Gretel(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.vx = 0
        self.vy = 0
        self.is_jump = False
        self.is_die = False
        self.platform = None
        self.direction = DIR_STILL
        self.breadwall = BreadWall(world)
 
    def move(self, direction):
        if self.not_in_wall():
            self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
            if self.x >= 920:
                self.x = 919
            elif self.x <= 60:
                self.x = 62
        if self.not_in_wall():
            self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
            if self.y >= 718:
                self.y = 717

    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY

    def set_platform(self, platform):
        self.is_jump = False
        self.platform = platform
        self.y = platform.y + (PLAYER_RADIUS // 2)

    def is_on_platform(self, platform, margin=PLATFORM_MARGIN):
        if not platform.in_top_range(self.x):
            return False
        
        if abs(platform.y - self.bottom_y()) <= PLATFORM_MARGIN:
            return True

        return False

    def is_falling_on_platform(self, platform):
        if not platform.in_top_range(self.x):
            return False
        
        if self.bottom_y() - self.vy > platform.y > self.bottom_y():
            return True
        
        return False

    def find_touching_platform(self):
        gen_wall = self.world.wall
        for g in gen_wall:
            if self.is_falling_on_platform(g):
                return g
        return None    
    
    def update(self, delta):
        self.move(self.direction)
        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY
        
            new_p = self.find_touching_platform()
            if new_p:
                self.vy = 0
                self.set_platform(new_p)
        else:
            if (self.platform) and not self.is_on_platform(self.platform):
                self.platform = None
                self.is_jump = True
                self.vy = 0

    def bottom_y(self):
        return self.y - (PLAYER_RADIUS // 2)


    def not_in_wall(self):
        x = 60 <= self.x <= 920
        y = self.y <= 718 
        return x and y

class Hanzel(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.vx = 0
        self.vy = 0
        self.is_jump = False
        self.is_die = False
        self.platform = None
        self.direction = DIR_STILL
        self.breadwall = BreadWall(world)
 
    def move(self, direction):
        if self.not_in_wall():
            self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
            if self.x >= 920:
                self.x = 919
            elif self.x <= 60:
                self.x = 62
        if self.not_in_wall():
            self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
            if self.y >= 718:
                self.y = 717
            elif self.y <= 201:
                self.y = 202

    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY

    def set_platform(self, platform):
        self.is_jump = False
        self.platform = platform
        self.y = platform.y + 60

    def is_on_platform(self, platform, margin=PLATFORM_MARGIN):
        if not platform.in_top_range(self.x):
            return False
        
        if abs(platform.y - self.bottom_y()) <= PLATFORM_MARGIN:
            return True

        return False

    def is_falling_on_platform(self, platform):
        if not platform.in_top_range(self.x):
            return False
        
        if self.bottom_y() - self.vy > platform.y > self.bottom_y():
            return True
        
        return False

    def find_touching_platform(self):
        gen_wall = self.world.wall
        for g in gen_wall:
            if self.is_falling_on_platform(g):
                return g
        return None    
    
    def update(self, delta):
        self.move(self.direction)
        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY
        
            new_p = self.find_touching_platform()
            if new_p:
                self.vy = 0
                self.set_platform(new_p)
        else:
            if (self.platform) and not self.is_on_platform(self.platform):
                self.platform = None
                self.is_jump = True
                self.vy = 0

    def bottom_y(self):
        return self.y - (PLAYER_RADIUS // 2)


    def not_in_wall(self):
        x = 60 <= self.x <= 920
        y = 202 <= self.y <= 718 
        return x and y

class Witch(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.vx = 0
        self.direction = DIR_STILL

    def move(self, direction):
        if self.vx < MAX_VX:
            self.vx += ACCX
        if self.not_in_wall():
            self.x += self.vx
            if self.x >= 920:
                self.x = 62
            elif self.x <= 60:
                self.x = 919

    def update(self, delta):
        self.move(self.direction)

    def not_in_wall(self):
        x = 60 <= self.x <= 920
        return x


class Platform:
    def __init__(self, world, x, y, width, height, is_bluedonut, is_pinkdonut):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_blue_donut = is_bluedonut
        self.is_pink_dont = is_pinkdonut

    def in_top_range(self, x):
        return self.x <= x <= self.x + self.width

    def top(self):
        return self.y + 20

class Donut:
    def __init__(self, world, x, y, is_blue):
        self.world = world
        self.x = x
        self.y = y
        self.is_pick = False
        self.is_blue = is_blue
    
    def pick(self, player):
        return abs(self.x - player.x) < 40 and abs(self.y - player.y) < 40


class World:
    START = 0
    DEAD = 1
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.breadwall = BreadWall(self)
        self.gretel = Gretel(self, self.width - 150, 210)
        self.hanzel = Hanzel(self, 150, self.height-195)
        self.witch = Witch(self, 500, 380)
        self.wall, self.donut_list = self.gen_wall()
        self.state = World.START
        self.score = 0 

    def gen_wall(self):
        breadwall_lst = []
        donut_list =[]
        for r in range(len(self.breadwall.map)):
            for c in range(len(self.breadwall.map[0])):
                if self.breadwall.map[r][c] != ' ' and self.breadwall.map[r][c] != 'o' and self.breadwall.map[r][c] != '.':
                    p = Platform(self, (c+1) * 40, r * 40, 40, 40, False, False)
                    breadwall_lst.append(p)
                elif self.breadwall.map[r][c] == 'o':
                    d = Donut(self, (c+1) * 40, r * 40, False)
                    donut_list.append(d)
                elif self.breadwall.map[r][c] == '.':
                    d = Donut(self, (c+1) * 40, r * 40, True)
                    donut_list.append(d)
        return breadwall_lst, donut_list

    def update(self, delta):
        self.is_dead()
        if self.state == World.START:
            self.gretel.update(delta)
            self.hanzel.update(delta)
            self.witch.update(delta)
        
        for d in self.donut_list:
            if d.pick(self.gretel):
                d.is_pick = True

    def is_dead(self):
        if self.gretel.bottom_y() < 0:
            self.state = World.DEAD

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
        self.map = [ '                        ',
                     '########################',
                     '#llllllllllllllllllllll#',
                     '#cwcllwcwclwcwcwcllwcwc#',
                     '#==== == == == ========#',
                     '#        o             #',
                     '#                      #',
                     '#                      #',
                     '#___  _________________#',
                     '# o                  . #',
                     '#                      #',
                     '#----------------  ----#',
                     '# .                  o #',
                     '#                      #',
                     '#____  ________________#',
                     '#                      #',
                     '#                   .  #',
                     '#                      #',
                     '########################',
                     '                        ',]
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

    def has_pinkdonut_at(self, r, c):
        return self.map[r][c] == '.'

    def has_bluedonut_at(self, r, c):
        return self.map[r][c] == 'o'


