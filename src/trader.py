import arcade

from constants import TILE_SCALING

class Trader(arcade.Sprite):
    """
    Trader sprite class.
    Manages movement and death.
    """

    def __init__(self, figure, start, end, speed):
        """
        Initialises a trader.
        
        Params: 
            - figure: path to an image for the trader to use.
            - start: coords to start at.
            - end: coords to end at.
            - speed: pixels/frame
        """
        super().__init__(filename=figure, scale=TILE_SCALING)

        self.center_x, self.center_y = start
        self.end = end
        self.speed = speed
    
    def update(self):
        """
        Moves the sprite.
        INCOMPLETE.
        """
        super().update()
        if self.center_x != self.end[0] and self.center_y != self.end[1]:
            self.center_x += self.speed / 2
            self.center_y += self.speed / 2
        else:
            self.kill()
        self.center_x += self.change_x
        self.center_y += self.change_y