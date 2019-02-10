import arcade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Player(arcade.Sprite):
    def __init__(self, scaling):
        """
        Initialises player code. 
        Creates a sprite and centers it on (160, 160).
        """
        super().__init__("player.png", scaling)
        self.center_x = 160
        self.center_y = 160

        self.change_x = 0
        self.change_y = 0

    def update(self):
        """
        Moves this class by self.change_x and self.change_y.
        Attempts to prevent players being outside the visible window.
        """
        if (self.center_x + self.change_x) >= SCREEN_WIDTH:
            self.change_x = 0
        if (self.center_y + self.change_y) >= SCREEN_HEIGHT:
            self.change_y = 0 
        if (self.center_x + self.change_x)<= -SCREEN_WIDTH:
            self.change_x = 0
        if (self.center_y + self.change_y) <= -SCREEN_HEIGHT:
            self.change_y = 0

        self.center_x += self.change_x
        self.center_y += self.change_y    
        self.change_x = 0
        self.change_y = 0


