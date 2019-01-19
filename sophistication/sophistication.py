import json
import arcade

import mods

SCREEN_WIDTH, SCREEN_HEIGHT = 512, 512
GAME_TITLE = "Sophistication"
TILE_SCALING = 0.5
PLAYER_SCALING = 1


class Sophistication(arcade.Window):
    """
Main game class.
"""
    def __init__(self, *mods_to_load):
        """
Starts the game setup processes.
"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, False)

        for mod in mods_to_load:
            mods.load_mod(mod)
        self.tile_defs = mods.tile_defs
        self.namespaces = mods.namespace_defs

        #TODO(adoria298): Allow csv files/choosing maps
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

        self.delta_times = []
        self.score = 0
        self.game_over = False

        #self.player = arcade.Sprite("images/player.png", PLAYER_SCALING, 0, 0, center_x=256, center_y=256)

        self.prepare_tile_list()

    def prepare_tile_list(self):
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
        #self.player.draw()


        # display score
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 400, 480, arcade.color.BLACK, 14)

        # game over mechanics
        if self.game_over:
            out_text = "Game Over! Thank You For Playing!"
            arcade.draw_text(out_text, 60, 250, arcade.color.BLACK, 20)
        
        arcade.finish_render()

    def update(self, delta_time):
        """
game logic.
"""
        # for time based scoring
        self.delta_times.append(delta_time)
        print(f"Total time: {sum(self.delta_times)}")


        # all after here stay at the end of the function
        self.gen_score()
        
        # if negative score - empire collapse
        if self.score < 0:
            self.game_over = True


if __name__ == "__main__":
    game = Sophistication('./sophistication/default')
    arcade.run()
