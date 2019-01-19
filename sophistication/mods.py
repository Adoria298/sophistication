import json
import pathlib

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
            return True, "is-mod"
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
    # creates full path to each tile image
    for tile_def in mod_tile_defs:
        mod_tile_defs[tile_def]["img"] = folder_path + "/" + mod_tile_defs[tile_def]["img"]
    tile_defs.update(mod_tile_defs)
    
    
#TODO(adoria298): continue with mod work until game works.
