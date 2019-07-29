import json
import pathlib
import os

# mod definitions
namespace_defs = {}
tile_defs = {
    "U": {
        "img": "unknown.png"
    }
}

def is_mod(folder_path):
    folder_path = pathlib.Path(folder_path)
    if (folder_path/"mod.json").exists():
        if "soph_namespace" in json.load(open(folder_path / "mod.json")):
            return True, "valid-mod"
        else:
            return False, "no-namespace"
    else:
        return False, "no-mod.json"

def load_mod(folder_path):
    if not is_mod(folder_path)[0]:
        raise ValueError(f"{folder_path} is not a valid mod for Sophistication because {is_mod(folder_path)[1]}")
    # no error? let's continue
    mod_def = pathlib.Path(folder_path) / "mod.json"
    mod = json.load(open(mod_def))
    namespace_defs[mod["soph_namespace"]] = folder_path
    mod_tile_defs = mod["tile_defs"]
    # TODO(adoria298): Put this bit into some functions
    # creates full path to each image under the types named in images
    images = ["struct", "traders"]
    for tile_sym in mod_tile_defs:
        tile_def = mod_tile_defs[tile_sym]
        for image in images:
            if tile_def.get(image, False):
                for el in tile_def[image]: #short for element
                    if el != None:
                        el["img"] = os.path.abspath(f"{folder_path}/{el['img']}")
    tile_defs.update(mod_tile_defs)
    
    

