import arcade
from models import World, Gretel

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BLOCK_SIZE = 60

class BreadWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.CREAM)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)
        self.gretel_sprite = ModelSprite('images/gretel.png',
                                         model=self.world.gretel)
        self.hanzel_sprite = ModelSprite('images/hanzel.png',
                                         model=self.world.hanzel)
        self.breadwall_drawer = BreadWallDrawer(self.world.breadwall)

    def update(self, delta):
        self.world.update(delta)
 
    def on_draw(self):
        arcade.start_render()
        self.breadwall_drawer.draw()
        self.gretel_sprite.draw()
        self.hanzel_sprite.draw()

    def on_key_press(self, key, key_modifiers):
         self.world.on_key_press_gretel(key, key_modifiers)
         self.world.on_key_press_hanzel(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
         self.world.on_key_release(key, key_modifiers)

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

class BreadWallDrawer():
    def __init__(self, breadwall):
        self.breadwall = breadwall
        self.width = self.breadwall.width
        self.height = self.breadwall.height
        self.breadwall_sprite = arcade.Sprite('images/breadwall.png')
        self.candywall_sprite = arcade.Sprite('images/candywall.png')
        self.candywall2_sprite = arcade.Sprite('images/candywall2.png')
        self.candywall3_sprite = arcade.Sprite('images/candywall3.png')
        self.chocolava_sprite = arcade.Sprite('images/chocolava.png')
        self.chocolavacurve_sprite = arcade.Sprite('images/chocolavacurve.png')
        self.chocolavacountercurve_sprite = arcade.Sprite('images/chocolavacountercurve.png')

    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                x = c * 40 + 20;
                y = r * 40 + 25;
 
                if self.breadwall.has_breadwall_at(r,c):
                    self.breadwall_sprite.set_position(x,y)
                    self.breadwall_sprite.draw()
                elif self.breadwall.has_candywall_at(r,c):
                    self.candywall_sprite.set_position(x,y)
                    self.candywall_sprite.draw()
                elif self.breadwall.has_candywall2_at(r,c):
                    self.candywall2_sprite.set_position(x,y)
                    self.candywall2_sprite.draw()
                elif self.breadwall.has_candywall3_at(r,c):
                    self.candywall3_sprite.set_position(x,y)
                    self.candywall3_sprite.draw()
                elif self.breadwall.has_chocolava_at(r,c):
                    self.chocolava_sprite.set_position(x,y)
                    self.chocolava_sprite.draw()
                elif self.breadwall.has_chocolavacurve_at(r,c):
                    self.chocolavacurve_sprite.set_position(x,y)
                    self.chocolavacurve_sprite.draw()
                elif self.breadwall.has_chocolavacountercurve_at(r,c):
                    self.chocolavacountercurve_sprite.set_position(x,y)
                    self.chocolavacountercurve_sprite.draw()

def main():
    window = BreadWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()