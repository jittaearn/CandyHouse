import arcade
from models import World, Player, Witch

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
        arcade.set_background_color(arcade.color.CREAM)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gretel_sprite = ModelSprite('images/gretel.png',
                                         model=self.world.gretel)
        self.hanzel_sprite = ModelSprite('images/hanzel.png',
                                         model=self.world.hanzel)
        self.witch_sprite = ModelSprite('images/witch.png',
                                         model=self.world.witch)                            

    def update(self, delta):
        self.world.update(delta)
 
    def on_draw(self):
        arcade.start_render()

        gretel_score = f"Gretel's Donut: {self.world.gretel_score}"
        arcade.draw_text(gretel_score, self.width - 200, self.height - 48,
                         arcade.color.BROWN, 14)
    
        hanzel_score = f"Hanzel's Donut: {self.world.hanzel_score}"
        arcade.draw_text(hanzel_score, 60, self.height - 48,
                         arcade.color.SKY_MAGENTA, 14)

        gretel_lives = f"Gretel's lives: {self.world.gretel_lives}"
        arcade.draw_text(gretel_lives, self.width - 200, self.height - 25,
                         arcade.color.BROWN, 14)

        hanzel_lives = f"Hanzel's lives: {self.world.hanzel_lives}"
        arcade.draw_text(hanzel_lives, 60, self.height - 25,
                         arcade.color.SKY_MAGENTA, 14)

        self.draw_door()
        self.draw_donut()
        self.draw_lava()
        self.draw_wall()
        self.gretel_sprite.draw()
        self.hanzel_sprite.draw()
        self.witch_sprite.draw()
        

    def on_key_press(self, key, key_modifiers):
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
            elif self.world.breadwall.has_candywall_at(y, x):
                pp = ModelSprite('images/candywall.png', model=p)
                pp.draw()
            elif self.world.breadwall.has_candywall2_at(y, x):
                pp = ModelSprite('images/candywall2.png', model=p)
                pp.draw()
            elif self.world.breadwall.has_candywall3_at(y, x):
                pp = ModelSprite('images/candywall3.png', model=p)
                pp.draw()

    def draw_door(self):
        for d in self.world.door_list:
            x = (d.x-1)//40
            y = (d.y)//40
            if self.world.breadwall.has_greteldoor_at(y, x):
                pp = ModelSprite('images/greteldoor.png', model=d)
                pp.draw()
            elif self.world.breadwall.has_hanzeldoor_at(y, x):
                pp = ModelSprite('images/hanzeldoor.png', model=d)
                pp.draw()

    def draw_lava(self):
        for l in self.world.chocolava_list:
            x = (l.x-1)//40
            y = (l.y)//40
            if self.world.breadwall.has_chocolava_at(y, x):
                pp = ModelSprite('images/chocolava.png', model=l)
                pp.draw()
            elif self.world.breadwall.has_chocolavacurve_at(y, x):
                pp = ModelSprite('images/chocolavacurve.png', model=l)
                pp.draw() 
            elif self.world.breadwall.has_chocolavacountercurve_at(y, x):
                pp = ModelSprite('images/chocolavacountercurve.png', model=l)
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


    def draw_menu_screen(self):
        if self.world.state == World.FROZEN:
            arcade.draw_text("Press space to enter", 400, 500,
                         arcade.color.BLACK, 30)
        if self.world.state == World.DEAD:
            arcade.draw_text("GAME OVER", 400, 500,
                         arcade.color.BLACK, 30)
                

def main():
    window = BreadWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()