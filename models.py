import arcade.key


GRAVITY = -1
JUMP_VY = 10
MAX_VX = 2
ACCX = 2
PLAYER_RADIUS = 50
WITCH_RADIUS = 60
PLATFORM_MARGIN = 5

DIR_STILL = 0
DIR_RIGHT = 2
DIR_LEFT = 6
MOVEMENT_SPEED = 4
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_RIGHT: (1,0),
                DIR_LEFT: (-1,0) }

class Model:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

class Player(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.vx = 0
        self.vy = 0
        self.is_jump = False
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
        if not platform.in_block_range(self.x):
            return False
        
        if abs(platform.y - self.bottom_y()) <= PLATFORM_MARGIN:
            return True

        return False

    def is_falling_on_platform(self, platform):
        if not platform.in_block_range(self.x):
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

    def bottom_y(self):
        return self.y - (PLAYER_RADIUS // 2)
    
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

    def not_in_wall(self):
        x = 60 <= self.x <= 920
        y = self.y <= 718 
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
            if self.x >= 520:
                self.x = 62

    def update(self, delta):
        self.move(self.direction)

    def not_in_wall(self):
        x = 60 <= self.x <= 520
        return x

    def incontact_witch(self, player):
        return abs(self.x - player.x) < 40 and abs(self.y - player.y) < 40

class Chocolatelava():
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def incontact_lava(self, player):
        return abs(self.x - player.x) < 20 and abs(self.y - player.y) < 20

class Donut:
    def __init__(self, world, x, y, is_blue, is_pink):
        self.world = world
        self.x = x
        self.y = y
        self.is_pink_pick = False
        self.is_blue_pick = False
        self.is_blue = is_blue
        self.is_pink = is_pink
    
    def pick(self, player):
        return abs(self.x - player.x) < 40 and abs(self.y - player.y) < 40

class Door:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def incontact_door(self, player):
        return abs(self.x - player.x) < 40 and abs(self.y - player.y) < 40

class Platform:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def in_block_range(self, x):
        return self.x - self.width//2 <= x <= self.x + self.width//2

class World:
    START = 0
    DEAD = 1
    FROZEN = 2
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.breadwall = BreadWall(self)
        self.gretel = Player(self, self.width - 150, 210)
        self.hanzel = Player(self, 150, self.height-195)
        self.witch = Witch(self, 500, 380)
        self.wall, self.pink_donut_list , self.blue_donut_list, self.chocolava_list, self.door_list = self.gen_wall()
        self.state = World.START
        self.gretel_score = 0 
        self.hanzel_score = 0 
        self.gretel_lives = 3 
        self.hanzel_lives = 3 

    def gen_wall(self):
        breadwall_lst = []
        pink_donut_list =[]
        blue_donut_list =[]
        chocolava_list =[]
        door_list = []
        for r in range(len(self.breadwall.map)):
            for c in range(len(self.breadwall.map[0])):
                if self.breadwall.map[r][c] != ' ' and self.breadwall.map[r][c] != 'o' and \
                    self.breadwall.map[r][c] != '.' and self.breadwall.map[r][c] != 'c' and \
                        self.breadwall.map[r][c] != 'w' and self.breadwall.map[r][c] != 'l' and \
                            self.breadwall.map[r][c] != 'g' and self.breadwall.map[r][c] != 'h':
                    p = Platform(self, (c+1) * 40, r * 40, 40, 60)
                    breadwall_lst.append(p)
                elif self.breadwall.map[r][c] == 'o':
                    d = Donut(self, (c+1) * 40, r * 40, False, True)
                    pink_donut_list.append(d)
                elif self.breadwall.map[r][c] == '.':
                    d = Donut(self, (c+1) * 40, r * 40, True, False)
                    blue_donut_list.append(d)
                elif self.breadwall.map[r][c] == 'l':
                    l = Chocolatelava(self, (c+1) * 40, r * 40, 40, 40)
                    chocolava_list.append(l)
                elif self.breadwall.map[r][c] == 'c' :
                    l = Chocolatelava(self, (c+1) * 40, r * 40, 40, 40)
                    chocolava_list.append(l)
                elif self.breadwall.map[r][c] == 'w':
                    l = Chocolatelava(self, (c+1) * 40, r * 40, 40, 40)
                    chocolava_list.append(l)
                elif self.breadwall.map[r][c] == 'h':
                    h = Door(self, (c+1) * 40, r * 40, 40, 40)
                    door_list.append(h)
                elif self.breadwall.map[r][c] == 'g':
                    g = Door(self, (c+1) * 40, r * 40, 40, 40)
                    door_list.append(g)

        return breadwall_lst, pink_donut_list, blue_donut_list, chocolava_list, door_list

    def update(self, delta):
        self.is_dead()
        if self.state == World.START:
            self.gretel.update(delta)
            self.hanzel.update(delta)
            self.witch.update(delta)
            self.check_lives()
            self.check_donut_collection()
            self.check_chocolava()
            self.check_door()

    def is_dead(self):
        if self.gretel_lives == 0 or self.hanzel_lives == 0:
                self.state = World.DEAD
        else:
            self.state = World.START

    def check_lives(self):
        if self.gretel_lives >= 1 and self.hanzel_lives >= 1:
            if self.witch.incontact_witch(self.gretel):
                self.gretel_lives -= 1
                self.gretel.x = self.width - 150
                self.gretel.y = 210
            if self.witch.incontact_witch(self.hanzel):
                self.hanzel_lives -= 1
                self.hanzel.x = 150 
                self.hanzel.y = self.height - 195

    def check_donut_collection(self):
        for d in self.pink_donut_list:
            if d.pick(self.gretel):
                d.is_pink_pick = True
                self.gretel_score += 1
                self.pink_donut_list.remove(d)
        for d in self.blue_donut_list:
            if d.pick(self.hanzel):
                d.is_blue_pick = True
                self.hanzel_score += 1
                self.blue_donut_list.remove(d)

    def check_chocolava(self):
        for l in self.chocolava_list:
            if l.incontact_lava(self.gretel):
                self.gretel_lives -= 1
                self.gretel.x = self.width - 150
                self.gretel.y = 210
            if l.incontact_lava(self.hanzel):
                self.hanzel_lives -= 1
                self.hanzel.x = 150
                self.hanzel.y = self.height - 195

    def check_door(self):
        if self.door_list[0].incontact_door(self.gretel) and self.gretel_score == 4:
            self.state = World.DEAD
        if self.door_list[1].incontact_door(self.hanzel) and self.hanzel_score == 4:
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
                     '#        o  .          #',
                     '#                    h #',
                     '#                      #',
                     '#____  ________________#',
                     '# o                  . #',
                     '#                      #',
                     '#--------------  ------#',
                     '# .                  o #',
                     '#                      #',
                     '#_____  _______________#',
                     '#                 o .  #',
                     '# g                    #',
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

    def has_greteldoor_at(self, r, c):
        return self.map[r][c] == 'g'

    def has_hanzeldoor_at(self, r, c):
        return self.map[r][c] == 'h'

    def has_pinkdonut_at(self, r, c):
        return self.map[r][c] == '.'

    def has_bluedonut_at(self, r, c):
        return self.map[r][c] == 'o'