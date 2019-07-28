import math
import random

import arcade

from constants import TRADER_SCALING

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
        super().__init__(filename=figure, scale=TRADER_SCALING)

        self.center_x, self.center_y = start
        self.end = end
        self.speed = speed
    
    def update(self):
        """
        Moves the sprite.
        INCOMPLETE.
        """
        # self.angle=0 is NorthEast (where North is the top)
        # therefore, North is the now the top right corner.
        # the bearing between two points can be found from atan2(x2-x1, y2-y1)
        # https://stackoverflow.com/questions/3932502/calculate-angle-between-two-latitude-longitude-points
        # added some randomness for effect
        END_ACCURACY = 20
        b = math.atan2(self.end[0]-self.center_x, self.end[1]-self.center_y)
        #self.angle += (b + random.randint(0,360)) % 360 # modulo'd so it's <360
        if ((self.center_x != self.end[0] and self.center_y != self.end[1])
            or (self.center_x <= self.end[0]-END_ACCURACY and self.center_x <= self.end[0]+END_ACCURACY)
            or (self.center_y <= self.end[1]-END_ACCURACY and self.center_y <= self.end[1]+END_ACCURACY)):
            self.center_x += self.speed * b
            self.center_y += self.speed * b
        else:
            self.kill()
        self.center_x += self.change_x
        self.center_y += self.change_y