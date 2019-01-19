import json
import pathlib

# mod definitions
namespace_defs = {}
tile_defs = {}

def is_mod(folder_path):
    folder_path = pathlib.Path(folder_path)
    if "mod.json" in folder_path.iterdir():
        if "soph_namespace" in json.load(open(folder_path / "mod.json")):
            return True
    else:
        return False

def get_mod(folder_path):
    if not is_mod(folder_path):
        raise ValueError(f"{folder_path} is not a valid mod for Sophistication.")
    # no error? let's continue
    mod_def = pathlib.Path(folder_path) / "mod.json"
    mod = json.load(open(mod_def))
    namespace_defs[mod["soph_namespace"]] = folder_path
    mod_tile_defs_json = pathlib.Path(mod["tile_defs"])
    mod_tile_defs = json.load(open(mod_tile_defs_json))
    tile_defs.update(mod_tile_defs)
    
    
#TODO(adoria298): continue with mod work until game works.
