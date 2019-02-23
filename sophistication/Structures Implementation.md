# Structures Implementation

## Description

A structure is visual graphic that can be placed upon a tile, which improves the score of the player. A structure is placed when a player navigates to a tile and presses enter. Different tiles have a different structure that will be placed upon enter. A structure will grant the player an immediate score, and an over time score, which will decrease unless the player develops the structure. If the score added is less than zero, the structure will be removed from the player's view, but will still affect the player's score.

A player can develop a structure by pressing enter upon the structure. This may change the structure's graphic, but will grant the player an immediate score increase, and an over time score increase, which will act the same as before the development. A structure will not disappear if the over time score is less then zero, but instead will regress a level, until the structure disappears. As before, the over time score will still affect the player, and will continue to decrease.

## Representation by Mods

A structure should be represented as an array named `struct` in a tile definition. Each element of the array will be a level of structure. Every tile starts out with no structure, and returns to no structure.

Example:

```json
"P": {
    "struct": [
        {
            "img": "struct1.png",
            "imm_score": 100,
            "over_time_score": 99,
            "decrease": 1
        },
        {
            "img": "struct2.png",
            "imm_score": 200,
            "over_time_score": 198,
            "decrease": 2
        }
    ]
}
```

This creates a structure with 2 levels, each with their own overlay image. The immediate score added of level 1 is 100, which decreases to 99 on the next turn, then 98, 97, 96, etc. The second level grants 200 points, which decreases by 2 each go from the `over_time_score`, which starts at 198.

## Internal Code Representation

Structures should be stored in a Tile class, as part of the information about the Tile.