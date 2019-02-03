import arcade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Player(arcade.Sprite):
    def __init__(self, scaling):
        super().__init__("player.png", scaling)
        self.center_x = 160
        self.center_y = 160

        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.center_x >= SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH-128
        if self.center_y >= SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT-128



