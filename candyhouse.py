import arcade
from models import World, Player, Witch, Door

music = arcade.sound.load_sound('sound/backgroundmusic.wav')
arcade.sound.play_sound(music)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None) 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()
         

class BreadWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gretel_sprite = ModelSprite('images/gretel.png',
                                         model=self.world.gretel)
        self.hanzel_sprite = ModelSprite('images/hanzel.png',
                                         model=self.world.hanzel)
        self.witch_sprite = ModelSprite('images/witch.png',
                                         model=self.world.witch)     
        self.exitdoor_sprite = ModelSprite('images/exitdoor.png',
                                         model=self.world.exitdoor)                                                          

    def update(self, delta):
        self.world.update(delta)
    
    def restart(self):
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gretel_sprite = ModelSprite('images/gretel.png',
                                         model=self.world.gretel)
        self.hanzel_sprite = ModelSprite('images/hanzel.png',
                                         model=self.world.hanzel)
        self.witch_sprite = ModelSprite('images/witch.png',
                                         model=self.world.witch)     
        self.exitdoor_sprite = ModelSprite('images/exitdoor.png',
                                         model=self.world.exitdoor)

    def draw_menu_screen(self):
        if self.world.state == World.FROZEN:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        texture=arcade.load_texture('images/frozenbackground.jpg'))
            arcade.draw_texture_rectangle(500, 712, 300, 60,
                                        texture=arcade.load_texture('images/screen.png'))
            arcade.draw_texture_rectangle(500, 80, 300, 60,
                                        texture=arcade.load_texture('images/space.png'))
            arcade.draw_text("Press (esc) to EXIT", 790, 765,
                         arcade.color.VIOLET_BLUE, 15)

        elif self.world.state == World.INSTRUCTION:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        texture=arcade.load_texture('images/instructionbackground.png'))
            arcade.draw_text("Press (esc) to EXIT", 790, 765,
                         arcade.color.VIOLET_BLUE, 15)

        elif self.world.state == World.CHARACTER:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        texture=arcade.load_texture('images/characterbackground.png'))
            arcade.draw_text("Press (esc) to EXIT", 790, 765,
                         arcade.color.VIOLET_BLUE, 15)
                                        
        elif self.world.state == World.DEAD:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        texture=arcade.load_texture('images/gameoverbackground.png'))
            arcade.draw_text("Press (esc) to EXIT", 790, 765,
                         arcade.color.VIOLET_BLUE, 15)

        elif self.world.state == World.WINNER:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        texture=arcade.load_texture('images/winnerbackground.png'))
            arcade.draw_text("Press (esc) to EXIT", 790, 765,
                         arcade.color.VIOLET_BLUE, 15)    
 
    def on_draw(self):
        arcade.start_render()
        self.draw_menu_screen()
        if self.world.state == World.START:
            self.state_start()

    def background(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        texture=arcade.load_texture('images/background.png'))
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                        SCREEN_WIDTH - 50, SCREEN_HEIGHT-125,
                                        texture=arcade.load_texture('images/creambackground.jpg'))
        arcade.draw_texture_rectangle(700, 770, 380, 55,
                                        texture=arcade.load_texture('images/scorebar_gretel.png'))
        arcade.draw_texture_rectangle(300, 770, 380, 55,
                                        texture=arcade.load_texture('images/scorebar_hanzel.png'))

    def state_start(self):
        self.background()
        hanzel_lives = f"{self.world.hanzel_lives}"
        arcade.draw_text(hanzel_lives, 215, self.height - 40,
                         arcade.color.FLUORESCENT_ORANGE, 14)
            
        hanzel_score = f"{self.world.hanzel_score}"
        arcade.draw_text(hanzel_score, 370, self.height - 40,
                         arcade.color.FLUORESCENT_ORANGE, 14)

        gretel_score = f"{self.world.gretel_score}"
        arcade.draw_text(gretel_score, 620, self.height - 40,
                         arcade.color.FLUORESCENT_ORANGE, 14)

        gretel_lives = f"{self.world.gretel_lives}"
        arcade.draw_text(gretel_lives, 770, self.height - 40,
                         arcade.color.FLUORESCENT_ORANGE, 14)

        
        arcade.draw_text("Press (esc) to EXIT", 750, 30,
                         arcade.color.VIOLET_BLUE, 15)

        self.draw_donut()
        self.draw_lava()
        self.draw_wall()
        self.exitdoor_sprite.draw()
        self.gretel_sprite.draw()
        self.hanzel_sprite.draw()
        self.witch_sprite.draw()
        
    def on_key_press(self, key, key_modifiers):
        if self.world.state < 3:
            if key == arcade.key.SPACE:
                self.world.state += 1   
        if self.world.state == 4 and self.world.state == 5:
            if key == arcade.key.SPACE:
                self.world.state = World.START
        if key == arcade.key.ESCAPE:
            exit()

        self.world.on_key_press_gretel(key, key_modifiers)
        self.world.on_key_press_hanzel(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
         self.world.on_key_release(key, key_modifiers)

    def draw_wall(self):
        for p in self.world.wall:
            x = (p.x-1)//40
            y = (p.y)//40

            if self.world.breadwall.has_breadwall_at(y, x):
                pp = ModelSprite('images/breadwall.png', model=p)
                pp.draw()
            elif self.world.breadwall.has_whitecandy_at(y, x):
                pp = ModelSprite('images/whitecandy.png', model=p)
                pp.draw()
            elif self.world.breadwall.has_pinkcandy_at(y, x):
                pp = ModelSprite('images/pinkcandy.png', model=p)
                pp.draw()
        arcade.draw_texture_rectangle(150, 627, 170, 128,
                                texture=arcade.load_texture('images/enterdoor.png'))

    def draw_lava(self):
        for l in self.world.chocolava_list:
            x = (l.x-1)//40
            y = (l.y)//40
            if self.world.breadwall.has_chocolava_at(y, x):
                pp = ModelSprite('images/chocolava.png', model=l)
                pp.draw()

    def draw_donut(self):
        for d in self.world.pink_donut_list:
            x = (d.x-1)//40
            y = (d.y-1)//40
            if not d.is_pink_pick:
                if not d.is_blue:
                    pp = ModelSprite('images/pinkdonut.png', model=d)
                    pp.draw()
        for d in self.world.blue_donut_list:
            x = (d.x-1)//40
            y = (d.y-1)//40
            if not d.is_blue_pick:
                if not d.is_pink:
                    pp = ModelSprite('images/bluedonut.png', model=d)
                    pp.draw()
                
def main():
    window = BreadWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()
