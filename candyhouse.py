import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

class CandyHouse:
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.CREAM)

def main():
    window = CandyHouse(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
 
if __name__ == '__main__':
    main()