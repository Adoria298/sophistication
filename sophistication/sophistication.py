# python standard libraries
import json 
import os

# external libraries
import arcade

# homemade libraries
import mods
from player import Player 
from constants import *

# sets the working directory to the same directory as where this code is saved.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Sophistication(arcade.Window):
    """
    A game of Sophistication. No glamour.
    """
    def __init__(self, *mods_to_load):
        """
        Initialises a game.
        
        *mods_to_load : valid mods that should be loaded. Game will crash if
         a mod is not valid.
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, False)

        # mod loading
        for mod in mods_to_load:
            mods.load_mod(mod)
        self.tile_defs = mods.tile_defs
        self.namespaces = mods.namespace_defs

        # map loading
        #TODO(adoria298): Allow csv files/choosing maps
        #TODO(adoria298): allow map state to be saved
        self.map = [
            ["M", "M", "M", "M", "M", "D", "D", "D"],
            ["P", "M", "M", "M", "D", "D", "D", "D"],
            ["P", "P", "M", "D", "D", "D", "D", "D"],
            ["W", "W", "W", "W", "D", "D", "D", "D"],
            ["P", "P", "P", "W", "W", "D", "D", "D"],
            ["P", "P", "P", "P", "W", "W", "D", "W"],
            ["P", "P", "P", "W", "W", "W", "W", "W"],
            ["P", "P", "W", "W", "W", "W", "W", "W"]
        ]
        self.tile_list = arcade.SpriteList()
        self.prepare_tile_list()

        # initialises score functionality
        self.delta_times = []
        self.score = 0
        self.game_over = False

        # initialises the player
        self.player = Player(PLAYER_SCALING)

    def prepare_tile_list(self):
        """
        Adds every tile to self.tile_list as a sprite image.
        Makes a grid of 8x8 tiles, each at 64 pixels.
        """
        #TODO(adoria298): make each tile into a Tile object
        for row_index, row in enumerate(self.map):
            for symbol_index, symbol in enumerate(row):
                tile = arcade.Sprite(
                    self.tile_defs.get(symbol, "U").get("img", "unknown.png"), 
                    TILE_SCALING)                
                tile.right = (1 + symbol_index) * 64
                tile.top = (8 - row_index) * 64
                
                self.tile_list.append(tile)
                
    def gen_score(self):
        # time based scoring
        if int(sum(self.delta_times)) > int(sum(self.delta_times[:-1])):
            self.score += int(sum(self.delta_times) / 7)
        

    def on_draw(self):
        """
        Draws everything to the screen.
        """
        arcade.start_render()

        # draw map and player
        self.tile_list.draw()
        self.player.draw()


        # display score
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 400, 480, arcade.color.BLACK, 14)

        # game over mechanics
        if self.game_over:
            out_text = "Game Over! Thank You For Playing!"
            arcade.draw_text(out_text, 60, 250, arcade.color.BLACK, 20)
        

    def update(self, delta_time):
        """
        game logic.
        """
        # for time based scoring
        #self.delta_times.append(delta_time)
        #print(f"Total time: {sum(self.delta_times)}")
        # all after here stay at the end of the function self.gen_score()
        
        # if negative score - empire collapse
        if self.score < 0:
            self.game_over = True

        #TODO(adoria298): add structures
        #TODO(adoria298): add decay logic

        self.player.update()

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
        
        #TODO(adoria298): add develop logic
        #TODO(adoria298): add save logic


if __name__ == "__main__":
    game = Sophistication('./default')
    arcade.run()
