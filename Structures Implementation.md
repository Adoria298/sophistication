# Structures Implementation

## Description

A structure is a visual graphic that can be placed upon a tile, and which improves the score of the player. A structure is placed when a player navigates to a tile and presses enter. Different tiles have a different structure that will be placed upon enter. A structure will grant the player an immediate score, and a countdown will begin. When the countdown is less than zero, the structure will be removed from the player's view, but will still affect the player's score.

A player can develop a structure by pressing enter upon the structure. This may change the structure's graphic, but will grant the player an immediate score increas. A structure will not disappear if its time is less then zero, but instead will regress a level, until the structure disappears. A regression decreases the player's score by half of the structure's immediate score.

Some structures may require a minimum score before they can be developed.

## Representation by Mods

A structure should be represented as an array named `struct` in a tile definition. Each element of the array will be a level of structure. Every tile starts out with no structure, and returns to no structure.

### Example

```json
"P": {
    "struct": [
        {
            "img": "plains.png",    // image representing the structure
            "imm_score": 0,         // the score the structure adds to the game when first created
            "time": 0,              // the starting value for how long until the structure regresses (countdown)
            "decrease": 0           // how much this value ^ decreases each loop
        },
        {
            "img": "struct1.png",
            "imm_score": 100,
            "time": 99,
            "decrease": 1
        },
        {
            "img": "struct2.png",
            "imm_score": 200,
            "time": 198,
            "decrease": 2,
            "min_score": 150        // the minimum score required for this structure to be built.
        }
    ]
}
```

This creates a structure with 2 levels, each with their own image (the first level is the default). The immediate score added of level 1 is 100, and this structure will countdown from 99 before it disappears. The third level grants 200 points and counts down from 198. The third level requires a score of at least 150 points to be developed.

## Internal Code Representation

Structures are core information about the tile. They are what the tile looks like. They are effectively levels for tiles. As such, they should be stored in the tile class, and graphically represented as textures of the tile. Values undefined in mod.json are to be assumed as 0.
