# Suikoden 1 Remaster Save Editing

Source: https://github.com/asilverthorn/suikoden_ref

- [Suikoden 1 Remaster Save Editing](#suikoden-1-remaster-save-editing)
  - [Overview](#overview)
  - [JSON Breakdown](#json-breakdown)
    - [party\_data](#party_data)
    - [shiro\_data](#shiro_data)
    - [player\_base](#player_base)
      - [MP](#mp)
      - [Stats](#stats)
      - [Items](#items)
      - [Weapons](#weapons)
      - [Runes](#runes)
    - [member\_flag](#member_flag)
  - [Data Tables](#data-tables)
    - [Characters](#characters)
    - [Items](#items-1)
    - [Equipment Slots](#equipment-slots)
    - [Runes](#runes-1)

## Overview
This document captures the results of reverse engineering Suikoden 1 HD Remaster decrypted save files using the EditSave option in d3xMachina's excellent https://github.com/d3xMachina/Suikoden-Fix.

It is also applicable to modding the g1mem_000 - g1mem_003 base data (extracted via https://github.com/nesrak1/UABEANext)

## JSON Breakdown

This section breaks down individual items within the decrypted JSON. In the examples below, inline comments (`//`) are included -- when editing your save, do not include those as they're not proper JSON.

### party_data

The `"chara_code"` array is for the characters in the current party by slot number (shown on the Formation screen). Ref: [Characters Data Table](#characters)

`8` (Tir) must always be present, otherwise you'll get a black screen on load.

You can also include non-battle characters (ex: `27` for Mathiu), but those will also cause an infinite "Loading..." screen with "IndexOutOfRangeExceptions" in the BepInEx log.

```
    "chara_code": [
      35, //slot 1 (Viktor)
      17, //slot 2 (Flik)
      2, //slot 3 (Gremio)
      8, //slot 4 (Tir)
      6, //slot 5 (Pahn)
      91 //slot 6 (Kai)
    ],
```

`"mochi_kin"` is the party Potch.

`"party_item_kazu"` is the number of items to be used from the `"party_item"` array. Ref: [Items Data Table](#items-1)

```
    "party_item_kazu": 4, // # of party items
    "party_item": [
      85, //Earring
      82, //Suiko Map
      81, //Blinking Mirror
      90, //Mathiu's Letter
      0,
      0,
      0,
      0
    ],
```

### shiro_data

This section appears to be HQ data

### player_base

This section stores the stats, equipment, weapons, and Runes for every character, recruited and unrecruited.

`"chara_no"` indicates the character for that object. Ref: [Characters Data Table](#characters)

####  MP

The `"magic_point"` array is the current (not max) MP remaining per spell level.

```
      "magic_point": [
        0,
        5, //lvl1 MP
        3, //lvl2 MP
        1, //lvl3 MP
        0
      ],
```

#### Stats
The `"noryoku"` array is the characters stats (before equipment modifiers) in the order shown on the Stats screen

```
      "noryoku": [
        92, //STR
        115, //DEX
        90, // PROT
        103, //SPD
        89, //MAG
        98 //LCK
      ],
```

#### Items

`"item_kazu"` is the number of items to be used from the `"item"` array. For Item IDs, ref the [Items Data Table](#items-1)

For an item, `"soubi"` is the equipment slot. Ref: [Equipment Slots Data Table](#equipment-slots)

For an item, `"data"` captures the uses remaining.

```
      "item_kazu": 8, //Number of items
      "item": [
        {
          "item_id": 29, //toe shoes
          "soubi": 5, //other 2
          "data": 0
        },
        {
          "item_id": 26, //antitoxin
          "soubi": 0, //not equipped
          "data": 4 //uses left
        },
        {
          "item_id": 15, //leather armor
          "soubi": 2, //armor
          "data": 0
        },
        {
          "item_id": 33, //gauntlet
          "soubi": 4, //other 1
          "data": 0
        },
        {
          "item_id": 73, //escape talisman
          "soubi": 0, //not equipped
          "data": 1 //uses left
        },
        {
          "item_id": 4, //half helmet
          "soubi": 1, //helmet
          "data": 0
        },
        {
          "item_id": 25, //medicine
          "soubi": 0,
          "data": 4 //uses left
        },
        {
          "item_id": 25, //medicine
          "soubi": 0, 
          "data": 6 //uses left
        },
        {
          "item_id": 106, 
          "soubi": 0,
          "data": 0
        }
      ],
```

#### Weapons

`"buki_data"` stores info on the weapon for that character. You can give characters different weapons by changing the `"buki_id"`.

The `"monsyo"` array stores which Rune pieces are attached. The first element in the array stores the index of which type is equipped.

```
      "buki_data": {
        "buki_id": 2, //Gremio's Axe
        "level": 5,
        "monsyo": [
          4, //Which of the following is attached? Lightning
          0, //Fire Rune Pieces
          0, //Water Rune Pieces
          0, //Earth Rune Pieces
          1, //Lightning Rune Pieces
          0  //Wind Rune Pieces
        ]
      },
``` 

#### Runes

`"monsyo_data"` is the Rune attached to the character. Ref: [Runes Data Table](#runes-1)

```
      "monsyo_data": {
        "monsyo_id": 3, //Water Orb
        "monsyo_level": 0,
        "monsyo_exp": 0
      }
```

### member_flag

This array appears to store which characters have been recruited, with a value of `9` indicating recruited, `0` not recruited. The index appears to match the ID from the [Characters Data Table](#characters.)

## Data Tables

### Characters
Used in `"chara_code"`, `"b_chara"`, and `"chara_no"`

| ID   | Character |
| ---: | :-------- |
|   0 | Eileen|
|   1 | Cleo|
|   2 | Gremio|
|   3 | Camille|
|   4 | Kirkis|
|   5 | Mose|
|   6 | Pahn|
|   7 | Luikan|
|   8 | Tir McDohl|
|   9 | Sylvina|
|  10 | Sonya|
|  11 | Anji|
|  12 | Varkas|
|  13 | Ronnie Bell|
|  14 | Kuromimi|
|  15 | Krin|
|  16 | Kasim|
|  17 | Flik|
|  18 | Fukien|
|  19 | Futch|
|  20 | Gen|
|  21 | Humphrey|
|  22 | Kage|
|  23 | Kasumi|
|  24 | Kun To|
|  25 | Kwanda Rosman|
|  26 | Luc|
|  27 | Mathiu|
|  28 | Milich|
|  29 | Milia|
|  30 | Lepant|
|  31 | Sydonia|
|  32 | Tai Ho|
|  33 | Tengaar|
|  34 | Tesla|
|  35 | Viktor|
|  36 | Valeria|
|  37 | Warren|
|  38 | Yam Koo|
|  39 | Juppo|
|  40 | Kessler|
|  41 | Leonardo|
|  42 | Griffith|
|  43 | Kanak|
|  44 | Giovanni|
|  45 | Kimberly|
|  46 | Marie|
|  47 | Lorelai|
|  48 | Alen|
|  49 | Grenshiel|
|  50 | Vincent De Boule|
|  51 | Rubi|
|  52 | Morgan|
|  53 | Clive|
|  54 | Sarah|
|  55 | Fuma|
|  56 | Lotte|
|  57 | Esmeralda|
|  58 | Templeton|
|  59 | Hellion|
|  60 | Apple|
|  61 | Mina|
|  62 | Sheena|
|  63 | Hix|
|  64 | Crowley|
|  65 | Fu Su Lu|
|  66 | Eikei|
|  67 | Kamandol|
|  68 | Quincy|
|  69 | Meese|
|  70 | Maas|
|  71 | Mace|
|  72 | Moose|
|  73 | Blackman|
|  74 | Kreutz|
|  75 | Stallion|
|  76 | Meg|
|  77 | Joshua|
|  78 | Ledon|
|  79 | Taggart|
|  80 | Gon|
|  81 | Kirke|
|  82 | Maximillian|
|  83 | Sancho|
|  84 | Georges|
|  85 | Roc|
|  86 | Melodye|
|  87 | Window|
|  88 | Gaspar|
|  89 | Onil|
|  90 | Zen|
|  91 | Kai|
|  92 | Sergei|
|  93 | Hugo|
|  94 | Ivanov|
|  95 | Sansuke|
|  96 | Jabba|
|  97 | Viki|
|  98 | Qlon|
|  99 | Jeane|
| 100 | Kasios|
| 101 | Antonio|
| 102 | Lester|
| 103 | Marco|
| 104 | Chapman|
| 105 | Chandler|
| 106 | Leon Silverberg|
| 107 | Pesmerga|
| 108 | Ted|
| 109 | Odessa|

### Items
Used in `"item_id"`

| ID   | Item      |
| ---: | :-------- |
| 1   | Bandana                     |
| 2   | Headband                    |
| 3   | Pointy Hat                  |
| 4   | Half Helmet                 |
| 5   | Headgear                    |
| 6   | Full Helmet                 |
| 7   | Silver Hat                  |
| 8   | Horned Helmet               |
| 9   | Robe                        |
| 10  | Tunic                       |
| 11  | Fur Robe                    |
| 12  | Chest Plate                 |
| 13  | Guard Robe                  |
| 14  | Martial Arts Robe           |
| 15  | Leather Armor               |
| 16  | Half Armor                  |
| 17  | Magic Robe                  |
| 18  | Ninja Garb                  |
| 19  | Dragon Armor                |
| 20  | Master's Robe               |
| 21  | Full Armor                  |
| 22  | Taikyoku Tunic              |
| 23  | Master's Garb               |
| 24  | Windspun Armor              |
| 25  | Medicine                    |
| 26  | Antitoxin                   |
| 27  | Wooden Shoes                |
| 28  | Boots                       |
| 29  | Toe Shoes                   |
| 30  | Winged Boots                |
| 31  | Earth Boots                 |
| 32  | Gloves                      |
| 33  | Gauntlet                    |
| 34  | Silverlet                   |
| 35  | Goldlet                     |
| 36  | Main-Gauche                 |
| 37  | Power Gloves                |
| 38  | Cape                        |
| 39  | Fur Cape                    |
| 40  | Cape of Darkness            |
| 41  | Crimson Cape                |
| 42  | Circlet                     |
| 43  | Blue Ribbon                 |
| 44  | Feather                     |
| 45  | Silver Ring                 |
| 46  | Greaves                     |
| 47  | Shoulder Pads               |
| 48  | Emblem                      |
| 49  | Star Earrings               |
| 50  | Rose Brooch                 |
| 51  | Guard Ring                  |
| 52  | Speed Ring                  |
| 53  | Power Ring                  |
| 54  | Collar                      |
| 55  | Silver Collar               |
| 56  | Gold Collar                 |
| 57  | Fire Rune Piece             |
| 58  | Water Rune Piece            |
| 59  | Wind Rune Piece             |
| 60  | Lightning Rune Piece        |
| 61  | Earth Rune Piece            |
| 62  | Fire Orb                    |
| 63  | Water Orb                   |
| 64  | Wind Orb                    |
| 65  | Lightning Orb               |
| 66  | Earth Orb                   |
| 67  | Wooden Shield               |
| 68  | Iron Shield                 |
| 69  | Chaos Shield                |
| 70  | Earth Shield                |
| 71  | Needle                      |
| 72  | Mega Medicine               |
| 73  | Escape Talisman             |
| 74  | STR Rune Piece              |
| 75  | DEX Rune Piece              |
| 76  | PROT Rune Piece             |
| 77  | MAG Rune Piece              |
| 78  | SPD Rune Piece              |
| 79  | LCK Rune Piece              |
| 80  | Dragon Incense              |
| 81  | Blinking Mirror             |
| 82  | Suiko Map                   |
| 83  | Sacrificial Buddha          |
| 84  | Astral Predictions          |
| 85  | Earring                     |
| 86  | Flowing Water Cane          |
| 87  | Fake Orders                 |
| 88  | Fire Spear                  |
| 89  | Moonlight Herb              |
| 90  | Mathiu's Letter             |
| 91  | Sound Set 0                 |
| 92  | Sound Set 1                 |
| 93  | Sound Set 2                 |
| 94  | Sound Set 3                 |
| 95  | Window Set 0                |
| 96  | Window Set 1                |
| 97  | Window Set 2                |
| 98  | Window Set 3                |
| 99  | Red Paint                   |
| 100 | Blue Paint                  |
| 101 | Yellow Paint                |
| 102 | Green Paint                 |
| 103 | White Paint                 |
| 104 | Black Paint                 |
| 105 | Pink Paint                  |
| 106 | Old Book Vol 1              |
| 107 | Old Book Vol 2              |
| 108 | Old Book Vol 3              |
| 109 | Old Book Vol 4              |
| 110 | Old Book Vol 5              |
| 111 | Old Book Vol 6              |
| 112 | Old Book Vol 7              |
| 113 | Old Book Vol 8              |
| 114 | Defective Urn               |
| 115 | ??? Urn                     |
| 116 | Flower Vase                 |
| 117 | Wide Urn                    |
| 118 | ??? Urn                     |
| 119 | Blue Dragon Urn             |
| 120 | ??? Urn                     |
| 121 | ??? Urn                     |
| 122 | ??? Urn                     |
| 123 | Hex Doll                    |
| 124 | ??? Ornament                |
| 125 | Chinese Dish                |
| 126 | Peeing Boy                  |
| 127 | ??? Ornament                |
| 128 | Knight Statue               |
| 129 | ??? Ornament                |
| 130 | ??? Painting                |
| 131 | ??? Painting                |
| 132 | Lovers' Garden              |
| 133 | ??? Painting                |
| 134 | Beauties of Nature          |
| 135 | Boar Orb                    |
| 136 | Shrike Orb                  |
| 137 | Falcon Orb                  |
| 138 | Blaze Orb                   |
| 139 | Gadget Orb                  |
| 140 | Clone Orb                   |
| 141 | Double-Jab Orb              |
| 142 | Killer Orb                  |
| 143 | Counter Orb                 |
| 144 | Spark Orb                   |
| 145 | Haziness Orb                |
| 146 | Gale Orb                    |
| 147 | Sunbeam Orb                 |
| 148 | Speed Orb                   |
| 149 | Fortune Orb                 |
| 150 | Prosperity Orb              |
| 151 | Champion's Orb              |
| 152 | Turtle Orb                  |
| 153 | Phero Orb                   |
| 154 | Nameless Urn                |
| 155 | Opal                        |
| 156 | Soap                        |
| 157 | Soy Sauce                   |
| 158 | Salt                        |
| 159 | Yardstick                   |
| 160 | Sugar                       |
| 161 | Red Flower Seeds            |
| 162 | Blue Flower Seeds           |
| 163 | Yellow Flower Seeds         |
| 164 | Resurrection Orb            |
| 165 | Rage Orb                    |
| 166 | Flowing Orb                 |
| 167 | Cyclone Orb                 |
| 168 | Mother Earth Orb            |
| 169 | Thunder Orb                 |
| 170 | ??? Painting                |
| 171 | Sound Orb                   |
| 172 | Window Orb                  |
| 173 | Illustrated War Scroll      |
| 174 | Binoculars                  |
| 175 | Kirinji                     |
| 176 | Engine                      |
| 177 | Blueprints                  |
| 178 | Bronze Axe                  |
| 179 | Mathiu's Letter             |

### Equipment Slots
Used in `"soubi"`

| soubi | Equipment slot |
| ----------: | :------------- |
| 0 | Not equipped |
| 1 | Helmet |
| 2 | Armor |
| 3 | Shield |
| 4 | Other 1 |
| 5 | Other 2 |
| 129 | Non-removable Helmet |
| 130 | Non-removable Armor |
| 131 | Non-removable Shield |
| 132 | Non-removable Other 1 |
| 133 | Non-removable Other 2 |

### Runes
Used in `"monsyo_id"`
| ID   | Rune      |
| ---: | :-------- |
|   0 | Not Equipped|
|   1 | Soul Eater|
|   2 | Fire|
|   3 | Water|
|   4 | Wind|
|   5 | Lightning|
|   6 | Earth|
|   7 | Resurrection|
|   8 | Boar|
|   9 | Shrike|
|  10 | Falcon|
|  11 | Blaze|
|  12 | Gadget|
|  13 | Clone|
|  14 | Double-Jab|
|  15 | Killer|
|  16 | Counter|
|  17 | Spark|
|  18 | Haziness|
|  19 | Gale|
|  20 | Sunbeam|
|  21 | Speed|
|  22 | Fortune|
|  23 | Prosperity|
|  24 | Champion's|
|  25 | Turtle|
|  26 | Phero|
|  27 | Rage|
|  28 | Flowing|
|  29 | Cyclone|
|  30 | Mother Earth|
|  31 | Thunder|
|  32 | ???????|
|  33 | High-Speed|
