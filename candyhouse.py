import arcade
from models import World, Gretel

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class BreadWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.CREAM)
 
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.gretel_sprite = ModelSprite('images/gretel.png',
                                         model=self.world.gretel)

        self.hanzel_sprite = ModelSprite('images/hanzel.png',
                                         model=self.world.hanzel)

        self.breadwall_drawer = BreadWallDrawer(self.world.breadwall)

        # self.witch_sprite = ModelSprite('images/witch.png',
        #                                  model=self.world.witch)

    def update(self, delta):
        self.world.update(delta)
 
    def on_draw(self):
        arcade.start_render()
        self.breadwall_drawer.draw()
        self.gretel_sprite.draw()
        self.hanzel_sprite.draw()


    def on_key_press(self, key, key_modifiers):
         self.world.on_key_press(key, key_modifiers)

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

    def draw(self):
        for r in range(self.height):
            for c in range(self.width):
                x = c * 40 + 20;
                y = r * 40 + 60;
 
                if self.breadwall.has_wall_at(r,c):
                    self.breadwall_sprite.set_position(x,y)
                    self.breadwall_sprite.draw()

def main():
    window = BreadWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()