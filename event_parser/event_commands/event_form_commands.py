from types import MappingProxyType
from event_commands.event_command import EventCommand
# Static map of eventForm commands to associated info
EventFormCommands = MappingProxyType({
	0: EventCommand(0, "NOP", {}, "No-op; often followed by 255, 254 for `eventCom`s that always execute"),
	1: EventCommand(2, "px", {}, "Return 0 if `px` (player x location) < param1 or `px` > param2"),
	2: EventCommand(2, "py", {}, "Return 0 if `py` (player y location) < param1 or `py` > param2"),
	3: EventCommand(2, "EvFlg_NAND", {0: ("EVENT_FLAG", 1)}, "Checks `event_flag` `!(event_flag[param1] & param2)` -- inverse logic of cmd 4"),
	4: EventCommand(2, "EvFlg_AND", {0: ("EVENT_FLAG", 1)}, "Checks `event_flag` `event_flag[param1] & param2` -- inverse logic of cmd 3"),
	5: EventCommand(1, "EVENT_HUMAN", {}, "Checks `EVENT_HUMAN[param1] `"),
	6: EventCommand(1, "ewflg", {}, "Checks `EVENTCON ewflg` against param1"),
	7: EventCommand(1, "ewflg", {}, "Checks `EVENTCON ewflg` against param1"),
	8: EventCommand(1, "direction", {}, "Checks `SYS_WORK pad_dat` bits, which are set based on direction; param1 has values 0-3"), #button pressed check
	9: EventCommand(1, "player_move", {}, "Checks a value in `EVENT_HUMAN[0]`, `EVENTCON.targetMoveDir`, and `EVENTCON.gSlopeMove`"),
	10: EventCommand(1, "px_lt", {}, "Checks `px` < param1"),
	11: EventCommand(1, "py_lt", {}, "Checks `py` < param1"),
	12: EventCommand(1, "px_gt", {}, "Checks `px` > param1"),
	13: EventCommand(1, "py_gt", {}, "Checks `py` > param1"),
	14: EventCommand(3, "pnin", {}, "Checks `EVENTCON.pnin`; param1 indicates an `EVENT_HUMAN` index"),
	15: EventCommand(3, "pnin", {}, "Checks `EVENTCON.pnin`; param1 indicates an `EVENT_HUMAN` index"),
	16: EventCommand(2, "char_in_party", {1: ("CHANO", 0)}, "Checks if a character (by `chano`) is in party (param2). param1 controls the boolean logic: <br> param1 == 1 && in_party(param2): execute next command <br /> param1 == 1 && !in_party(param2): return 0 (stop script) <br /> param1 == 0 && in_party(param2): return 0 <br /> param1 == 0 && !in_party(param2): execute next command"),
	#17: EventCommand(0, "N/A", {}, "Default case -- just returns 0"),
	18: EventCommand(2, "potch", {}, "Checks if param2 * 100 <= party gold (potch)"),
	19: EventCommand(1, "EvFlg_255_NAND", {}, "Checks `!(event_flag[255] & param1)` -- inverse logic of cmd 20"), 
	20: EventCommand(1, "EvFlg_255_AND", {}, "Checks `event_flag[255] & param1` -- inverse logic of cmd 19"), 
	21: EventCommand(1, "direction", {}, "Checks `SYS_WORK pad_dat` bits, which are set based on direction; param1 has values 0-3"), # button not pressed check
	22: EventCommand(1, "player", {}, "Checks `EVENT_HUMAN[0]` field against param1"),
	23: EventCommand(2, "G2_cha_flag", {0: ("CHANO", 0), 1: ('CHA_FLAG_MODE', 0)}, "Checks `G2_cha_flag(param2, param1)` <br/> param1 = character number (`chano`) <br /> param2 = mode: `4` = character recruited, not dead or on leave, not in party; `9` = character in party"),
	24: EventCommand(2, "G2_cha_flag", {0: ("CHANO", 0), 1: ('CHA_FLAG_MODE', 0)}, "Checks `G2_cha_flag(param2, param1)` <br/> param1 = character number (`chano`) <br /> param2 = mode"), 
	25: EventCommand(1, "rand", {}, "Checks random number between 0 and param1"),
	26: EventCommand(5, "G2_item_num2", {1: ("ITEM", 1)}, "Checks `G2_item_num2` - param1 = a flag, param2 = item kind, param3 = item number, param4 = quantity"),
	27: EventCommand(2, "TkFlg_NAND", {0: ('T_BOX_FLAG', 1)}, "Checks `GAME_WORK !(t_box_flag[param1] & param2)`"),
	28: EventCommand(2, "TkFlg_AND", {0: ('T_BOX_FLAG', 1)}, "Checks `GAME_WORK t_box_flag[param1] & param2`"),
	29: EventCommand(2, "TwFlg_NAND", {0: ("MAP_IN_OUT_FLAG", 1)}, "Checks `!(map_in_out_flag[param1] & param2)`"),
	30: EventCommand(2, "TwFlg_AND", {0: ("MAP_IN_OUT_FLAG", 1)}, "Checks `map_in_out_flag[param1] & param2`"),
	31: EventCommand(4, "px", {}, "Checks `px` - Per Omnigamer: Serves as a version of 0x1 for location ranges larger than 0xFF. Except it works in a fairly odd way; it has 4 operands that work out to two location values. The first operand is how many multiples of 100 (decimal) to add to the second operand, and the same for the third and fourth. First overall value is minimum X value, second is maximum."),
	32: EventCommand(4, "py", {}, "Checks `py`"),
	33: EventCommand(2, "base_lv", {}, "Checks `GAME_WORK base_lv` (Castle level) against param2. <br /> param1 == 0: return 0 if param2 != `base_lv` <br /> param1 == 1: return 0 if `base_lv` < param2 <br /> param1 == 2: return 0 if `base_lv` > param2"),
	34: EventCommand(2, "hon_flag", {}, "Checks `GAME_WORK hon_flag`"),
	35: EventCommand(2, "hon_flag", {}, "Checks `GAME_WORK hon_flag`"),
	36: EventCommand(3, "EVENT_HUMAN", {}, "Checks `EVENT_HUMAN[param2]`"),
	37: EventCommand(5, "event_time", {}, "Checks `GAME_WORK event_time. param1 = flag (0/1, inverts logic); param2 = event_time idx; param3 = seconds, param4 = minutes, param5 = hours. checks that event_time[param2] < (param3 * 60 + param4) * 60 + p5`"),
	38: EventCommand(2, "G2_pamem_num", {}, "Checks `G2_pamem_num(0)` and `(4)`"), # possibly current vs max count? with param1 being the type of check
	39: EventCommand(3, "G2_chara_love", {1: ("CHANO", 0)}, "Checks G2_chara_love; param1 is a mode of some sort. param2 = chano"),
	40: EventCommand(2, "shop_data", {}, "Checks `GAME_WORK shop_data.event_no` against param2"),
	41: EventCommand(6, "px_py", {}, "Variable parameters; checks px and py"),
	254: EventCommand(0, "NOP"),
	255: EventCommand(1, "END", {}, "End of eventForm. param1 is always 254; if it reaches this `eventForm` cmd, it will start executing the `eventCom` via a return 1")
})
