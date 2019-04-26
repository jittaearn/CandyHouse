import arcade.key

GRAVITY = -1
JUMP_VY = 15
GRETEL_RADIUS = 40
HANZEL_RADIUS = 40
GROUND_THICKNESS = 100
PLATFORM_MARGIN = 5

DIR_STILL = 0
DIR_RIGHT = 2
DIR_LEFT = 4
MOVEMENT_SPEED = 4
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_RIGHT: (1,0),
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
 
    def move(self, direction):
        if self.not_in_wall():
            self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
            if self.x >= 920:
                self.x = 919
            elif self.x <= 60:
                self.x = 62
        if self.not_in_wall():
            self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
            if self.y >= 800:
                self.y = 799
            elif self.y < 80:
                self.y = 100

    def jump(self):
        if not self.platform:
            return
        
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY

    def update(self, delta):
        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY

            new_platform = self.find_touching_platform()
            if new_platform:
                self.vy = 0
                self.set_platform(new_platform)
        else:
            if (self.platform) and (not self.is_on_platform(self.platform)):
                self.platform = None
                self.is_jump = True
                self.vy = 0
        self.move(self.direction)

    def bottom_y(self):
        return self.y - (GRETEL_RADIUS // 2)

    def set_platform(self, platform):
        self.is_jump = False
        self.platform = platform
        self.y = platform.y + (GRETEL_RADIUS // 2)

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

    def not_in_wall(self):
        x = 60 <= self.x <= 920
        y = 80<= self.y <=700
        print(x, y)
        return x and y

class Hanzel(Model):
    pass
    # def __init__(self, world, x, y):
    #     super().__init__(world, x, y)
    #     self.vx = 0
    #     self.vy = 0
    #     self.is_jump = False
    #     self.current_direction = DIR_RIGHT
    #     self.direction = DIR_STILL
 
    # def move(self, direction):
    #     self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
    #     self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    # def jump(self):
    #     self.is_jump = True
    #     self.vy = JUMP_VY

    # # def closest_wall(self):
    # #     dx, dy = self.world.width, self.world.height
    # #     platform = Platform(self.world, self.world.width, self.world.height)
    # #     for p in self.world.gen_wall:
    # #         if self.y >= p.y and self.y - p.y <= dy:
    # #             if min(abs(self.x - p.x)):
    # #                 abs(self.x - p.)

    # def check_boarder(self, player_boarder, platforms):
    #     if platforms.x <= player_boarder <= platforms.x + self.width
 
    # def update(self, delta):
    #     self.move(self.direction)
    #     self.y += self.vy
    #     if self.vy >= 0:
            # self.vy += Hanzel.GRAVITY

class Platform:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def in_top_range(self, x):
        return self.x <= x <= self.x + self.width

    def right_most_x(self):
        return self.x + self.width

    def top(self):
        return self.y + 40

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.breadwall = BreadWall(self)
        self.gretel = Gretel(self, self.width - 150, 250)
        self.hanzel = Hanzel(self, 150, self.height-100)
        self.wall = self.gen_wall()

    def gen_wall(self):
        breadwall_lst = []
        for r in range(len(self.breadwall.map)):
            for c in range(len(self.breadwall.map[0])):
                if c != ' ':
                    p = Platform(self, (c+1) * 40, r * 40, 40, 40)
                    breadwall_lst.append(p)
        return breadwall_lst

    def update(self, delta):
        self.gretel.update(delta)
        # self.hanzel.update(delta)

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
                     '#                ======#',
                     '#              ==      #',
                     '#                      #',
                     '#                      #',
                     '#__  __________________#',
                     '#                      #',
                     '#                      #',
                     '#----------------  ----#',
                     '#                      #',
                     '#                      #',
                     '#____  ________________#',
                     '#                      #',
                     '#                      #',
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

