import arcade
from models import World, Gretel, Hanzel

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

    def update(self, delta):
        self.world.update(delta)
 
    def on_draw(self):
        arcade.start_render()
        self.draw()

        self.gretel_sprite.draw()
        self.hanzel_sprite.draw()
        

    def on_key_press(self, key, key_modifiers):
         self.world.on_key_press_gretel(key, key_modifiers)
         self.world.on_key_press_hanzel(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
         self.world.on_key_release(key, key_modifiers)

    def draw(self):
        for p in self.world.wall:ใ
                x = p.y + 20
                y = p.x + 20

                # if self.world.breadwall.has_breadwall_at(p.x, p.y):
                #     pp = ModelSprite('images/breadwall.png', model=p)
                #     pp.draw()
                if self.world.breadwall.has_candywall_at(p.x, p.y):
                    pp = ModelSprite('images/candywall.png', model=p)
                    pp.draw()
                elif self.world.breadwall.has_candywall2_at(p.x, p.y):
                    pp = ModelSprite('images/candywall2.png', model=p)
                    pp.draw()
                elif self.world.breadwall.has_candywall3_at(p.x, p.y):
                    pp = ModelSprite('images/candywall3.png', model=p)
                    pp.draw()
                elif self.world.breadwall.has_chocolava_at(p.x, p.y):
                    pp = ModelSprite('images/chocolava.png', model=p)
                    pp.draw()
                elif self.world.breadwall.has_chocolavacurve_at(p.x, p.y):
                    pp = ModelSprite('images/chocolavacurve.png', model=p)
                    pp.draw()
                elif self.world.breadwall.has_chocolavacountercurve_at(p.x, p.y):
                    pp = ModelSprite('images/chocolavacountercurve.png', model=p)
                    pp.draw()

def main():
    window = BreadWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()