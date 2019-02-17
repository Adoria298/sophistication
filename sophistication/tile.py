import arcade

from constants import TILE_SCALING

class Tile(arcade.Sprite):
    """ 
    A single tile, ready to be drawn and placed.
    """

    def __init__(self, symbol, scaling, tile_defs):
        """
        Creates this tile.

        Params: 
            - symbol - for looking up in mod definitions
            - scaling - the scale the tile should be rendered at
        """
        self.symbol = symbol
        self.tile_def = tile_defs.get(self.symbol, tile_defs.get("U"))
        super().__init__(self.tile_def.get("img", "unknown.png"),
                            scaling)


if __name__ == "__main__":
    tile = Tile("U", 0.5)
