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
        self.symbol = symbol
        self.tile_def = tile_defs.get(self.symbol, tile_defs.get("U"))
        super().__init__(self.tile_def.get("img", "unknown.png"),
                            TILE_SCALING)

        # all code past this point is about structures.
        # TODO(adoria298): make structures work as outlined!
        self.struct_level = 0

        self.struct = arcade.Sprite()
        self.struct.center_x = self.center_x
        self.struct.center_y = self.center_y
        self.struct.scale = TILE_SCALING
        self.struct.draw()


    def develop(self):
        if self.tile_def.get("structs", False):
            print("Developing structure.")
        else:
            print("No structure found for this tile.")
            return None
        
        self.struct_level += 1
        if self.struct_level > len(self.tile_def["structs"])-1:
            self.struct_level -= 1
            return None

        self.struct_def = self.tile_def["structs"][self.struct_level]
        self.struct_img = self.struct_def.get("img", None)
        if self.struct_img == None:
            return None
        
        self.struct = arcade.Sprite(self.struct_img, TILE_SCALING)

    def update(self):
        super().update()
        if self.struct:
            self.struct.update()

    def draw(self):
        super().draw()
        if self.struct:
            self.struct.draw()

if __name__ == "__main__":
    tile = Tile("U", 0.5)
