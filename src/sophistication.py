# python standard libraries
import json
import csv 
import os
import random

# external libraries
import arcade

# homemade libraries
import mods
from player import Player 
from tile import Tile
from trader import Trader
from constants import (SCREEN_LEN, GAME_TITLE, VIEWPORT_MARGIN, TILE_LEN,
                         MOVEMENT_SPEED)

# sets the working directory to the same directory as where this code is saved.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Sophistication(arcade.Window):
    """
    A game of Sophistication. No glamour.
    """
    def __init__(self, map_file, map_type="csv", *mods_to_load):
        """
        Initialises a game.

        Params:        
            - map_file: the map to be used
            - map_type: what format the map is in. default = "csv". Options:
                - "csv": CSV file, with each element being a tile to be referenced from *mods_to_load
            - *mods_to_load : valid mods that should be loaded. Game will crash if
         a mod is not valid.
        """
        super().__init__(width=SCREEN_LEN, height=SCREEN_LEN,
                            title=GAME_TITLE, fullscreen=False, resizable=False)

        arcade.set_background_color(arcade.color.BANANA_MANIA) # for when the map runs out

        # mod loading
        for mod in mods_to_load:
            mods.load_mod(mod)
        self.tile_defs = mods.tile_defs
        self.namespaces = mods.namespace_defs

        # map loading
        #TODO(adoria298): allow map state to be saved (pickle?)
        if (map_file.endswith(".csv")
            or map_type=="csv"):
            self.map = list(csv.reader(open(map_file)))
        else: 
            raise TypeError("Invalid map.")

        self.tile_list = arcade.SpriteList()
        self.prepare_tile_list()

        # initialises score functionality
        self.delta_times = []
        self.score = 0
        self.game_over = False

        # initialises the player
        self.player = Player()
        ## how the player interacts with the world
        self.mode = "default"
        self.new_trade_route = arcade.SpriteList()
        
        #for scrolling
        self.view_bottom = 0
        self.view_left = 0

    def prepare_tile_list(self):
        """
        Adds every tile to self.tile_list as a Tile instance.
        Makes a grid of 8x8 tiles, each at 64 pixels.
        """
        for row_index, row in enumerate(self.map):
            for symbol_index, symbol in enumerate(row):
                tile = Tile(symbol, self.tile_defs)               
                tile.right = (1 + symbol_index) * TILE_LEN
                tile.top = (8 - row_index) * TILE_LEN 
                
                self.tile_list.append(tile)
                
    def gen_slow_events(self):
        """
        Generates score and traders.
        """
        # for occasional occurings
        if int(sum(self.delta_times)) > int(sum(self.delta_times[:-1])):
            random.choice(self.tile_list).gen_trader()
        for tile in self.tile_list:
                if tile.mode == "regressed":
                    self.score += tile.score_mod  
                    # only update the score if the tile has just regressed, 
                    # because the score updates itself upon development.

    def on_draw(self):
        """
        Draws everything to the screen.
        """
        arcade.start_render()

        # draw map and player
        self.tile_list.draw()
        self.player.draw()

        # draws traders
        for tile in self.tile_list:
            tile.traders.draw()

        # display score
        score_text = f"Score: {int(self.score)}" # remove decimal place from score.
        arcade.draw_text(score_text, self.view_left+400, 
                        self.view_bottom+480, arcade.color.BLACK, 14) 
                        # addition in position keeps the score stable, stops it drifting
                        # drawn in the upper right

        #display player position
        pos_text = f"x: {int(self.player.center_x)}, y: {int(self.player.center_y)}"
        arcade.draw_text(pos_text, self.view_left+10, self.view_bottom+480, 
                            arcade.color.BLACK, 14) # drawn in the upper left

        # indicate player mode
        mode_text = f"Mode: {self.mode}"
        arcade.draw_text(mode_text, self.view_left+195, self.view_bottom+480,
                            arcade.color.BLACK, 14) # drawn in the middle

        # game over mechanics
        if self.game_over:
            out_text = "Game Over! Thank You For Playing!"
            arcade.draw_text(out_text, 60, 250, arcade.color.BLACK, 20)
        

    def update(self, delta_time):
        """
        game logic.
        """
        # for time based scoring
        self.delta_times.append(delta_time)
        self.gen_slow_events()
        # all after here stay at the end of the function
        
        # if negative score - empire collapse
        if self.score < 0:
            self.game_over = True

        self.player.update(self.map)
        self.tile_list.update()

        for tile in self.tile_list:
            tile.traders.update()

        # scrolling
        #TODO(adoria298): Allow the 16th column to be seen.
        #TODO(adoria298): stop bounce back on the far right

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_bndry:
            self.view_left -= left_bndry - self.player.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_LEN - VIEWPORT_MARGIN
        if self.player.right > right_bndry:
            self.view_left += self.player.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_LEN - VIEWPORT_MARGIN
        if self.player.top > top_bndry:
            self.view_bottom += self.player.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_LEN + self.view_left,
                                self.view_bottom,
                                SCREEN_LEN + self.view_bottom)

        self.on_draw()

    def on_key_press(self, key, modifiers):
        """
        Called upon key press. 

        Listens for:
         - UP/DOWN/LEFT/RIGHT: player movement
         - ENTER: development/trade network creation
         - T: toggle "trade" mode
        """
        # player movement
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.ENTER:
            closest_tile = arcade.get_closest_sprite(self.player, self.tile_list)[0] # second element is its distance to the player
            if self.mode=="default":
                # on enter develop the structure
                if closest_tile.develop(self.score): # if tile developed, apply the immediate score
                    self.score += closest_tile.score_mod
            elif self.mode=="trade":
                # on enter create a trade route
                if len(self.new_trade_route) == 1:
                    print("Ending trade route")
                    start = self.new_trade_route[0]
                    start.trade_routes.append(closest_tile.position)
                    self.new_trade_route = arcade.SpriteList()
                elif len(self.new_trade_route) == 0:
                    print("Starting trade route")
                    self.new_trade_route.append(closest_tile) # start of the trade route
                else:
                    print(f"len of self.new_trade_route: {len(self.new_trade_route)}!")  
            else:
                print("Unrecognised action: ", self.mode)
        elif key == arcade.key.T:
            # toggle trade mode
            if self.mode == "trade":
                self.mode = "default"
            else: # in case of other modes
                self.mode = "trade"
                self.new_trade_route = arcade.SpriteList()
        
        #TODO(adoria298): add save logic


if __name__ == "__main__":
    game = Sophistication("map16.csv", "csv", "./default")
    arcade.run()
