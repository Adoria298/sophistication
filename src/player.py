import arcade
from constants import SCREEN_LEN, PLAYER_SCALING, TILE_LEN

class Player(arcade.Sprite):
    def __init__(self):
        """
        Initialises player code. 
        Creates a sprite and centers it on (160, 160).
        """
        super().__init__("player.png", PLAYER_SCALING)
        self.center_x = 160
        self.center_y = 160

        self.change_x = 0
        self.change_y = 0

    def update(self, game_map):
        """
        Moves this class by self.change_x and self.change_y.
        Attempts to prevent players from being outside the visible window
        (bouncing).
        """

        x = self.center_x // TILE_LEN
        y = self.center_y // TILE_LEN
      
        self.center_x += self.change_x
        self.center_y += self.change_y   

        if (x == 0 
            or y == 0
            or x == len(game_map)-1
            or y == len(game_map)-1): # prevent bouncing on edge of map 

            # prevents x-axis bouncing
            if self.left < 0:
                self.left = 0
            
            if self.right > SCREEN_LEN - 1:
                self.right = SCREEN_LEN

            
            # prevents y-axis bouncing
            # removed to allow movement/prevent blackouts
            """ 
            if self.bottom < 0:
                self.bottom = 0
            """
            if self.top > SCREEN_LEN - 1:
                self.top = SCREEN_LEN
       
        self.change_x = 0
        self.change_y = 0


