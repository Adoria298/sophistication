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
            - scaling - the scale the tile should be rendered at
        """
        super().__init__(scale=TILE_SCALING)

        self.symbol = symbol
        self.tile_def = tile_defs[symbol]
        self.struct_def = self.tile_def["struct"]
        self.struct_level = 0 # texture level as well

        for struct in self.struct_def:
            struct_img = arcade.draw_commands.load_texture(struct["img"])
            self.append_texture(struct_img)


    def develop(self):        
        self.struct_level += 1
        if self.struct_level > len(self.tile_def["structs"])-1:
            print("No structure found for this tile.")
            self.struct_level -= 1
            return None
        else:
            print("Developing structure.")

        self.set_texture(self.struct_level)

        
        

if __name__ == "__main__":
    tile = Tile("U", 0.5)
