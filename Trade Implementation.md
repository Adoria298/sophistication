# Trade Implementation

## Description

Trade is a connection between structures that creates a random visual image representing a trader, which goes between predefined structures. A trade network is represented by coloured lines over tiles that these "traders" move along, in either direction. Upon a structure upgrade, the traders may also upgrade, for example plains/nomads -> villages/merchants -> towns/trains in the default mod. The speed a trader moves at may also change, generally increasing, upon a trader upgrade.

The player decides between which tiles traders move by pressing `T` and navigating normally. Upon pressing enter, instead of tile development, the starting node of a trade path is created, and the second enter ends that particular path. Each tile has a limited number of traders that can leave it, which should increase with tile development. Upon a trader's generation, the tile's `time` counter will be increased, delaying that structures regression.

## Representation by Mods

Much like structures, trade networks are represented under the `trade` object in a tile definition. Any values not given are assumed to be zero.

### Example

```json
"P": {
    "struct": [
        {
            ..., // unimportant here
            "max_traders": 5 // 5 traders all going somewhere at once
        },
        {
            ...,
            "max_traders": 10
        },
        {
            ...,
            "max_traders": 20
        }
    ], 
    "trade": {
        "traders": [ // elements correspong to structure levels
            { // both values required for trader to work
                "img": "nomad.png", // image representing the trader
                "speed": 8, // speed the trader moves at
                 // no regression at first structure
            },
            {
                "img": "merchants.png",
                "speed": 16,
                "regress_delay": 1 
            },
            {
                "img": "train.png",
                "speed": 32, // half player speed
                "regress_delay": 2
            }
        ],
        "colour": "#F60678" // a nice pinky-purple line
    }
}
```

## Internal Code Representation

Traders will be managed by their origin tile, which will have a list of other tiles they can send traders to.
