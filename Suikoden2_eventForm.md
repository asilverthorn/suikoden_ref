## Overview

This document captures how to parse the `eventdata.mapeventdat[?].eventdat[?].eventForm` values found within the various map MonoBehavior files extractable from the Suikoden I & II remaster bundles.

This document is based on reverse engineering the `EVENTCON$$EventFormTbl` function.

The `eventForm` controls whether the associated eventCom commands execute. If it reaches the end of the eventForm without running into a `return 0`.

`eventForm`s appear to be always executed in a loop while on the map in question.

## eventForm table

Note: the "num params" column indicates the number of values that follow the eventForm cmd before the next eventForm cmd. By personal convention, I refer to them as param1 - param5.

| `eventForm` cmd | num params | Notes |
|------|----------|----------|
| 0    |        0 | No-op; often followed by 255, 254 for eventComs that always execute on a map |
| 1    |        2 | Checks `px` (player x location) |
| 2    |        2 | Checks `py` (player y location) |
| 3    |        2 | Checks `event_flag` `!(event_flag[param1] & param2)` -- inverse logic of cmd 4 |
| 4    |        2 | Checks `event_flag` `event_flag[param1] & param2` -- inverse logic of cmd 3 |
| 5    |        1 | Checks `EVENT_HUMAN[param1] `|
| 6    |        1 | Compare param1 against `EVENTCON ewflg` |
| 7    |        1 | Compare param1 against `EVENTCON ewflg` |
| 8    |        1 | Checks `SYS_WORK pad_dat` bits; param1 has values 0-3 |
| 9    |        1 | Checks a value in `EVENT_HUMAN[0]`, `EVENTCON.targetMoveDir`, and `EVENTCON.gSlopeMove` |
| 10   |        1 | Checks `px` < param1 |
| 11   |        1 | Checks `py` < param1 |
| 12   |        1 | Checks `px` > param1 |
| 13   |        1 | Checks `py` > param1 |
| 14   |        3 | Checks `EVENTCON.pnin`; param1 indicates an `EVENT_HUMAN` index |
| 15   |        3 | Checks `EVENTCON.pnin`; param1 indicates an `EVENT_HUMAN` index |
| 16   |        2 | Checks if a character (by `chano`) is in party (param2) |
| 17   |        0 | Just returns 0 |
| 18   |        2 | Checks if param2 * 100 <= party gold (potch) |
| 19   |        1 | Checks `!(event_flag[255] & param1)` -- inverse logic of cmd 20 |
| 20   |        1 | Checks `event_flag[255] & param1` -- inverse logic of cmd 19|
| 21   |        1 | Checks `SYS_WORK pad_dat` bits; param1 has values 0-3 |
| 22   |        1 | Checks `EVENT_HUMAN[0]` field against param1 |
| 23   |        2 | Checks `G2_cha_flag(param2, param1)` <br/> param2 = mode <br/> param1 = character number |
| 24   |        2 | Checks `G2_cha_flag(param2, param1)` <br/> param2 = mode <br/> param1 = character number |
| 25   |        1 | Checks random number between 0 and param1 |
| 26   |        5 | Checks `G2_item_num2` |
| 27   |        2 | Checks `GAME_WORK t_box_flag[param1] & param2` |
| 28   |        2 | Checks `GAME_WORK t_box_flag[param1] & param2` |
| 29   |        2 | Checks `!(map_in_out_flag[param1] & param2)` |
| 30   |        2 | Checks `map_in_out_flag[param1] & param2` |
| 31   |        4 | Checks `px` |
| 32   |        4 | Checks `py` |
| 33   |        2 | Checks `GAME_WORK base_lv` (Castle level) against param2. <br /> param1 == 0 checks param2 != `base_lv` <br /> param1 == 1 checks `base_lv` < param2 <br /> param1 == 2 checks `base_lv` > param2|
| 34   |        2 | Checks `GAME_WORK hon_flag` |
| 35   |        2 | Checks `GAME_WORK hon_flag` |
| 36   |        3 | Checks `EVENT_HUMAN[param2]` |
| 37   |        5 | Checks `GAME_WORK event_time` |
| 38   |        2 | Checks `G2_pamem_num(0)` and `(4)` |
| 39   |        4 | Unknown; could be variable length (if param3 == 0, it doesn't read param4)   |
| 40   |        2 | Checks `GAME_WORK shop_data.event_no` against param2 |
| 255  |        1 | param1 is always 254; if it reaches this `eventForm` cmd, it will start executing the `eventCom` via a return 1 |


## examples

### Zamza in Toto Inn
vb03.json's `mapeventdat[1].eventdat[62]` is an event that allows recruitment of Zamza (`chano`: 27) in the unburned Toto (`ano` / `area_no`: 1 / b, `vno` / `town_no`: 2) Inn (`mno`: 1) if Nanami (`chano`: 18) is in the party.

```
            "eventForm": [
              3,   //cmd - !(event_flag[param1] & param2)
              166, //param1 -- event flag idx
              2,   //param2 -- event flag value to NAND
              4,   //cmd event_flag[param1] & param2 -- if true, returns, else continues
              206, //param1 -- event flag idx
              16,  //param2
              16,  //cmd: is character in party
              1,   //param1. 1 causes EventFormTbl to return 0 if following character is not found
              18,  //param2. cha_no 18: nanami
              5,   //cmd: ???
              41,  //param1: event_human index
              255,
              254
            ],
            "eventCom": [
              84,  //cmd: recruit character
              27,  //zamza
              30,  //end
              115, //cmd: set character to level
              27,  //zamza
              6,   //level 6
              ...
```

### Hanna in Burned Toto
vb04.json's `mapeventdat[0].eventdat[37]` is the event that allows recruitment of Hanna in the burned Toto

```
            "eventForm": [
              3,   //cmd: event_flag
              166, //flag num
              32,  //param
              4,   //cmd: event_flag check
              208, //flag num
              1,   //param
              4,   //cmd: event_flag check
              208, //flag num
              2,   //param
              4,   //cmd: event_flag check
              151, //flag num
              64,  //param
              5,   //cmd: unknown
              18,  // event_human index
              9,   //cmd: event_human[0] check
              0,   // param
              255,
              254
            ],
            "eventCom": [
              84, //cmd: recruit character
              23, //hanna
              30, //end
              ...
```

### Genshu in Coronet
vc18.json contains multiple events that enable recruitment of Genshu if you are at castle level 4

```
            "eventForm": [
              33, //cmd: base level check
              2,  //look for base_lv > param2
              3,  //param2. Requires base_lv > 3
              5,  //cmd: event_human check
              8,  //param: event_human
              255,
              254
            ],
            "eventCom": [
              84, //cmd: recruit character
              47, //Genshu
              30, //done
              ...
```

## Other references

See https://github.com/asilverthorn/suikoden_ref/blob/main/Suikoden%20II%20Recruit%20eventCom.csv for character numbers and location file names

See https://github.com/pyriell/gs2-bugfixes/blob/master/reference/script%20commands.txt for a breakdown of `eventCom`s as they worked in the PS1 version