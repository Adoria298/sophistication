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
from constants import *

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
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, fullscreen=False, resizable=False)

        arcade.set_background_color(arcade.color.BANANA_MANIA) # when the map runs out

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
        self.player = Player(PLAYER_SCALING)

        #for scrolling
        self.view_bottom = 0
        self.view_left = 0

        # for trade
        self.trade_graph = self.gen_trade_graph()
        self.traders = arcade.SpriteList()

    def gen_trade_graph(self):
        """
        Populates self.trade_graph with lists of coords attached to other coords.
        Randomised.

        Assumes the map is a square
        """
        max_coord = len(self.map) * 64 -1
        graph = {}
        for tile in self.tile_list:
            routes = []
            for j in range(random.randint(1, 10)): # never empty
                routes.append((random.randint(0, max_coord), random.randint(0, max_coord)))
            graph[(tile.center_x, tile.center_y)] = routes
        return graph
        
    def gen_trader(self):
        """
        Generates a trader, tells it the tile it starts at, where it ends, its speed and its form.
        Adds it to a list of traders.

        Returns True if trader successfully generated
        """
        #TODO: COMPLETE! (trade in general)
        start = random.choice(list(self.trade_graph.keys()))
        end = random.choice(self.trade_graph[start])

        ps = arcade.Sprite() # placeholder sprite
        ps.center_x, ps.center_y = start
        closest_tile = arcade.get_closest_sprite(ps, self.tile_list)
        ps.kill() # not needed anymore

        tdef = self.tile_defs[closest_tile[0].symbol] # tile def for the closest tile
        if "traders" in tdef: # in case traders aren't defined
            trader_info = tdef["traders"][closest_tile[0].struct_level]
            trader = Trader(trader_info["img"], start, end, trader_info["speed"])
            self.traders.append(trader)
            print(start, end)
            return True
        else:
            return False

    def prepare_tile_list(self):
        """
        Adds every tile to self.tile_list as a Tile instance.
        Makes a grid of 8x8 tiles, each at 64 pixels.
        """
        for row_index, row in enumerate(self.map):
            for symbol_index, symbol in enumerate(row):
                tile = Tile(symbol, self.tile_defs)               
                tile.right = (1 + symbol_index) * 64
                tile.top = (8 - row_index) * 64 
                
                self.tile_list.append(tile)
                
    def gen_slow_events(self):
        """
        Generates score and traders.
        """
        # scores only updated every now and then.
        if int(sum(self.delta_times)) > int(sum(self.delta_times[:-1])):
            for tile in self.tile_list:
                if tile.mode == "regressed":
                    self.score += tile.score_mod  
                    # only update the score if the tile has just regressed, 
                    # because the score updates itself upon development.
            #also used to generate traders
            if random.randint(0, 10) > 5:
                print(self.gen_trader())

    def on_draw(self):
        """
        Draws everything to the screen.
        """
        arcade.start_render()

        # draw map and player, as well as any traders
        self.tile_list.draw()
        self.traders.draw()
        self.player.draw()


        # display score
        score_text = f"Score: {int(self.score)}" # remove decimal place from score.
        arcade.draw_text(score_text, self.view_left+400, self.view_bottom+480, arcade.color.BLACK, 14) # addition in position keeps the score stable, stops it drifting

        #display player position
        pos_text = f"x: {int(self.player.center_x)}, y: {int(self.player.center_y)}"
        arcade.draw_text(pos_text, self.view_left+10, self.view_bottom+480, arcade.color.BLACK, 14)

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
        self.traders.update()

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
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_bndry:
            self.view_left += self.player.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
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
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

        self.on_draw()

    def on_key_press(self, key, modifiers):
        """
        Called upon key press.
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
            # on enter develop the structure
            closest_tile = arcade.get_closest_sprite(self.player, self.tile_list)[0] # second element is its distance to the player
            if closest_tile.develop(self.score): # if tile developed, apply the immediate score
                self.score += closest_tile.score_mod
        
        #TODO(adoria298): add save logic


if __name__ == "__main__":
    game = Sophistication("map.csv", "csv", "./default")
    arcade.run()
