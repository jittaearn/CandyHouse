import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class BreadWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.CREAM)

    def on_draw(self):
        arcade.start_render()

def main():
    window = BreadWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()