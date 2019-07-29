# Trade Implementation

## Description

Trade is a connection between structures that creates a random visual image representing a trader, which goes between predefined structures. A trade network is represented by coloured lines over tiles that these "traders" move along, in either direction. After implementing traders, I(adoria298) feel that traders are made better by their randomness, so they have not been implemented as of 2019-07-29. Upon a structure upgrade, the traders may also upgrade, for example plains/nomads -> villages/merchants -> towns/trains in the default mod. The speed a trader moves at may also change, generally increasing, upon a trader upgrade.

## Representation by Mods

Much like structures, trade networks are represented under the `trade` object in a tile definition. Any values not given are assumed to be zero.

### Example

```json
"P": {
    "struct": [...], // unimportant here, but necessary
    "trade": {
        "traders": [ // elements correspong to structure levels
            { // both values required for trader to work
                "img": "nomad.png", // image representing the trader
                "speed": 8 // speed the trader moves at
            },
            {
                "img": "merchants.png",
                "speed": 16
            },
            {
                "img": "train.png",
                "speed": 32 // half player speed
            }
        ],
        "colour": "#F60678" // a nice pinky-purple
    }
}
```

## Internal Code Representation

Tiles will need to know which tiles they can trade with. This is done with a dictionary representing a graph of coordinates.
