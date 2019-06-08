import arcade

from constants import TILE_SCALING


class Tile(arcade.Sprite):
    """ 
    A single tile, ready to be drawn and placed.
    """

    def __init__(self, symbol, tile_defs):
        """
        Creates this tile.

        Params: 
            - symbol - for looking up in mod definitions
            - tile_defs - where to find information about this tile.
        """
        super().__init__(scale=TILE_SCALING)

        self.symbol = symbol
        self.tile_def = tile_defs[symbol].copy()
        self.struct_def = self.tile_def["struct"]
        self.struct_level = 0 # texture level as well

        for struct in self.struct_def:
            struct_img = arcade.draw_commands.load_texture(struct["img"])
            self.append_texture(struct_img)

        self._update_struct(
            self.struct_def[self.struct_level].get("imm_score", 0), apply_imm_score=True)

    def develop(self, curr_score):
        """
        Develops this tile's structure. The current score is required to check if the tile has the minimum amount of score.
        """
        # updates the current level of structure        
        self.struct_level += 1
        # checks if that level of structure is possible
        if self.struct_level > len(self.tile_def["struct"])-1:
            print("No structure found for this tile.")
            self.struct_level -= 1
            return False
        # checks if the minimum score is less than the current score
        else:
            if curr_score >= self.struct_def[self.struct_level].get("min_score", 0):
                print("Developing structure.")
            else:
                print("Score must be higher to develop this tile.")
                return False

        # if all the tests are passed, develop the structure
        self._update_struct(self.struct_def[self.struct_level].get("imm_score", 0), apply_imm_score=True)
        return True

    # TODO(adoria298): structure regression
    def regress(self):
        """ 
        Checks if this structure can be regressed. 
        If so, regresses it.
        """
        if self.struct_level <= 0:
            return None # can't be regressed further
        elif self.time < 0:
            self.struct_level -= 1
            imm_score = self.struct_def[self.struct_level+1].get("imm_score", 0)
            self._update_struct(imm_score, 
                                apply_imm_score=False, 
                                negate_imm_score=True)
    # TODO(adoria298): multiple default structures - ports etc - trade?
    # TODO(adoria298): decrease default structures' score mods?

    def _update_struct(self, imm_score, apply_imm_score, negate_imm_score=False):
        """
        Changes this tile's texture to the struct_level of textures. 
        If apply_imm_score is truey, sets self.score_mod to the structure's imm_score (default 0).
        If negate_imm_score is truey, sets self.score_mod to -1/2 of the structure's immediate score. This doesn't happen if apply_imm_score is truey.
        """
        self.set_texture(self.struct_level)
        if apply_imm_score:
            self.score_mod = imm_score
        elif negate_imm_score:
            self.score_mod = -1/2 * imm_score
        self.time = self.struct_def[self.struct_level].get("time", 0)
        
    def get_time(self):
        """
        Updates and returns the countdown.
        """
        curr_struct = self.struct_def[self.struct_level]
        self.time -= curr_struct.get("decrease", 0)
        print(self.time)
        return self.time

    def update(self):
        super().update()

        if self.score_mod != 0:
            self.score_mod = 0

        self.get_time()
        self.regress() # if necessary

        
        

if __name__ == "__main__":
    tile = Tile("U")
