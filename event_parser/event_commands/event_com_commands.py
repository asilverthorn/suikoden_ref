from types import MappingProxyType
from typing import List
from event_commands.event_command import EventCommand

def omovek_var_len(event_json: List[int], param_idx: int) -> List[int]:
	''' Method that returns the parameters for the OMoveK eventcom command (5)'''
	params = []
	
	# First 3 params are always fixed
	for i in range(3):
		params.append(event_json[param_idx])
		param_idx +=1
	
	# Then it goes in increments of 2 (direction + steps). If the direction that's read is 0x1e, then exit the loop
	while(param_idx < len(event_json)):
		param = event_json[param_idx]
		params.append(param)
		param_idx+=1
		if 0x1e == param:
			break
		else:
			# not the exit direction, read the next parameter too
			params.append(event_json[param_idx])
			param_idx+=1
	return params

## Commented out -- there are examples of OMoveAK being called with the first parameter = 8 and being followed by a non-existent command.
## This tells me that I'm interpreting the 7 < iVar8 incorrectly -- it's possibly checking the current state of things rather than the parameter
# def omoveak_var_len(event_json: List[int], param_idx: int) -> List[int]:
# 	''' Method that returns the parameters for the OMoveAK eventcom command (90)'''
# 	params = []
	
# 	# First parameter is fixed
# 	params.append(event_json[param_idx])
# 	param_idx += 1
	
# 	if 7 >= params[0]:
# 		# in this case, it goes into a loop looking for 0x1e, similar to OMoveK
# 		while(param_idx < len(event_json)):
# 			param = event_json[param_idx]
# 			params.append(param)
# 			param_idx+=1
# 			if 0x1e == param:
# 				break
# 			else:
# 				# read the next parameter too
# 				params.append(event_json[param_idx])
# 				param_idx+=1
# 	return params
	

def anime_chenge_var_len(event_json: List[int], param_idx: int) -> List[int]:
	''' Method that returns the parameters for the AnimeChenge eventcom command (89)'''
	params = []
	# first 2 parameters are fixed
	for i in range(2):
		params.append(event_json[param_idx])
		param_idx += 1
	if 2 == params[1]:
		# in this case, read one more parameter
		params.append(event_json[param_idx])
		param_idx += 1
	return params

def machi_chenge_var_len(event_json: List[int], param_idx: int) -> List[int]:
	'''
	Variable length param method for MachiChenge (13) and MachiChengeM (140), based on EVENTCON ECMachiChengeBase
	'''
	params = []

	# First parameter is fixed
	params.append(event_json[param_idx])
	param_idx += 1

	if(5 == params[0]):
		# read 3
		for i in range(3):
			params.append(event_json[param_idx])
			param_idx +=1
	elif(6 != params[0]):
		# read 3
		for i in range(3):
			params.append(event_json[param_idx])
			param_idx +=1
	
	# read 2 more
	for i in range(2):
		params.append(event_json[param_idx])
		param_idx +=1

	return params

def basic_count_var_len(event_json: List[int], param_idx: int) -> List[int]:
	'''
	Variable length param method for various methods that have a fixed parameter that's a count of the remaining ones
	'''
	params = []

	# First parameter is fixed
	params.append(event_json[param_idx])
	param_idx +=1 

	# Next, it appears to just treat param[0] as the count
	for i in range(params[0]):
		params.append(event_json[param_idx])
		param_idx +=1

	return params

def party_open_p_var_len(event_json: List[int], param_idx: int) -> List[int]:
	'''
	Variable length param method for PartyOpenP (52), based on EVENTCON ECPartyOpenP, and InitPartyOpenP (65), based on EVENTCON ECInitPartyOpenP
	'''
	params = []

	# First parameter is fixed
	params.append(event_json[param_idx])
	param_idx += 1

	# Next, it appears to read 5 parameters in a loop, with param[0] as the count
	for i in range(params[0]):
		for j in range(5):
			params.append(event_json[param_idx])
			param_idx += 1
	
	return params

def overlay_go_var_len(event_json: List[int], param_idx: int) -> List[int]:
	'''
	Variable length param method for various Overlay methods that have 2 fixed parameters and the second is the count of remaining
	'''
	params = []
	# first 2 parameters are fixed
	for i in range(2):
		params.append(event_json[param_idx])
		param_idx += 1

	# Next, it reads 1 per param[1]
	for i in range(params[1]):
		params.append(event_json[param_idx])
		param_idx += 1
	return params

def bg_free_overlay_go_var_len(event_json: List[int], param_idx: int) -> List[int]:
	'''
	Read 3, param[2] is length of remaining
	'''
	params = []
	# first 2 parameters are fixed
	for i in range(3):
		params.append(event_json[param_idx])
		param_idx += 1

	# Next, it reads 1 per param[2]
	for i in range(params[2]):
		params.append(event_json[param_idx])
		param_idx += 1

	return params

def renz_idou_s_var_len(event_json: List[int], param_idx: int) -> List[int]:
	'''
	Read 1 param (count), read that many times in a loop until it hits 255, 254, then read 1 more -- it should be 0x32
	'''
	params = []

	# get count
	params.append(event_json[param_idx])
	param_idx += 1

	for i in range(params[0]):
		while(param_idx < len(event_json)):
			# read until 255 (0xff)
			param = event_json[param_idx]
			params.append(param)
			param_idx += 1

			if 0xff == param:
				# read one more, it should be 0xfe (254)
				param = event_json[param_idx]
				params.append(param)
				param_idx += 1

				if 0xfe != param:
					raise ValueError(f"RenzIdouS does not match the expected pattern of a sub-command ending with 255 254. Value read after 255: {param} @ {param_idx-1}")
				else:
					break # out of loop after finding 255 254
	
	# read one more, it should be 0x32
	param = event_json[param_idx]
	params.append(param)
	param_idx +=1 

	if 0x32 != param:
		raise ValueError(f"RenzIdouS does not match the expected pattern of concluding with 50 (0x32). Value read: {param} @ {param_idx-1}")

	return params

def time_set_var_len(event_json: List[int], param_idx: int) -> List[int]:
	''' Translating logic from EVENTCON ECTimeSet that results in it calling COMMAND_LINE_Advance '''
	params = []

	# first 2 parameters are fixed
	for i in range(2):
		params.append(event_json[param_idx])
		param_idx += 1
	
	if params[0] == 0:
		pass # no extra params read in
	elif params[0] != 1:
		if params[0] == 2:
			# read 1 more
			params.append(event_json[param_idx])
			param_idx += 1
		elif params[0] == 3:
			# read 1 more
			params.append(event_json[param_idx])
			param_idx += 1

	return params

def sentaku_jump_var_len(event_json: List[int], param_idx: int) -> List[int]:
	''' Read until it hits 255 '''
	params = []
	while(param_idx < len(event_json)):
		# read until 255 (0xff)
		param = event_json[param_idx]
		params.append(param)
		param_idx += 1

		if 0xff == param:
			break
	return params

# Static map of eventCom commands to associated info
EventComCommands = MappingProxyType({
	0: EventCommand(1, 'ODispOn'),
	1: EventCommand(1, 'ODispOff'),
	2: EventCommand(3, 'OPosSet'),
	3: EventCommand(2, 'ODirSet'),
	4: EventCommand(4, 'OPosMoveK'),
	5: EventCommand(-1, 'OMoveK', {}, 'Move Character', omovek_var_len),

	7: EventCommand(1, 'VramPosSet'), # used?
	8: EventCommand(0, 'DmSrnMake'), #used?
	9: EventCommand(2, 'EvFlgSet', {0: 'EVENT_FLAG'}),
	10: EventCommand(2, 'EvFlgOff', {0: 'EVENT_FLAG'}),
	11: EventCommand(3, 'SrnBWIO', {}, 'Modifies background BlackIn/Out, WhiteIn/Out'),
	12: EventCommand(3, 'MapChenge', {0: 'MAP_MNO'}, 'sets mno, px, and py'),
	13: EventCommand(-1, 'MachiChenge', {}, '', machi_chenge_var_len), 

	18: EventCommand(0, 'PushKey'), # used?

	20: EventCommand(3, 'WindowFace', {0: 'CHANO'}, ''), # used? param[0] is referred to as FPNO; it appears to be the character portrait
	21: EventCommand(0, 'WindowFaceEnd'), # used?
	22: EventCommand(1, 'WindowFacePos'), # used?
	23: EventCommand(2, 'WindowHenji', {0: 'WINDOW_MFNO'}, 'Dialog'),
	24: EventCommand(3, 'WindowSerifu', {1: 'WINDOW_MFNO'}, 'Dialog'),
	25: EventCommand(4, 'WindowAnime', {1: 'CHANO', 2: 'WINDOW_MFNO'}, 'Dialog'), # param[1] is referred to as FPNO; it appears to be the character portrait shown
	26: EventCommand(2, 'WindowEvent', {0: 'WINDOW_MFNO'}, 'Dialog'),
	27: EventCommand(6, 'WindowFreeSize'),
	28: EventCommand(3, 'SrnScroll'),
	29: EventCommand(1, 'SrnBaseScroll'),
	30: EventCommand(-1, 'OverlayGo', {}, '', overlay_go_var_len),
	31: EventCommand(3, 'FieldCdRead', {1: 'AREA_NO', 2: 'FILE_NO'}, ''),
	32: EventCommand(-1, 'MemMapChenge'), # variable based on compos
	33: EventCommand(-1, 'PartySet', {1: 'CHANO', 2: 'CHANO', 3: 'CHANO', 4: 'CHANO', 5: 'CHANO', 6: 'CHANO', 7: 'CHANO'}, 'Sets required members of party', basic_count_var_len),
	34: EventCommand(0, 'PartyClear'),
	35: EventCommand(-1, 'MachiChenge', {}, '', machi_chenge_var_len),
	36: EventCommand(1, 'WkEvFlgSet'),
	37: EventCommand(1, 'WkEvFlgOff'),
	38: EventCommand(0, 'PartyOpenN'),
	39: EventCommand(0, 'PartyCloseN'),
	40: EventCommand(-1, 'WindowSentaku'), # 3 fixed, 2 per param[2], but also has a skip based on < 7
	41: EventCommand(-1, 'SentakuJump', {}, ''), # manipulates the cmdIdx directly -- script commands.txt says that it "Runs through up to 0xFFFE bytes or until it hits 0xFF looking for a match"
	42: EventCommand(6, 'WarEventGo'),
	43: EventCommand(2, 'OSpeedSet', {}, 'sets the spd for the associated EVENT_HUMAN'),
	44: EventCommand(0, 'MapCut', {}, 'sets bit 0x2000 in syust'),
	45: EventCommand(0, 'MapDouki', {}, 'clears bit 0x2000 in syust'),
	46: EventCommand(0, 'RenzokOn', {}, 'sets bit 0x40 in comst'),
	47: EventCommand(0, 'RenzokOff', {}, 'clears bit 0x40 in comst'), #TODO: these always follow a previous call to RenzokOn. Once all variable length fields are completed, an extra validation could be added for that
	48: EventCommand(-1, 'ObjPosMoveK'), # appears to have up to 7 params, in large part based on param[0] being < 7
	49: EventCommand(-1, 'RenzIdouS', {}, 'executes sub-commands', renz_idou_s_var_len), # TODO: parse sub-commands

	51: EventCommand(-1, 'LabelJump'), # appears to be only used once (vc14), in which case param[0] is 0. If it's non-zero, it loops and seems to manipulate the cmdIdx directly
	52: EventCommand(-1, 'PartyOpenP', {}, '', party_open_p_var_len),
	53: EventCommand(3, 'EvFlgWait', {1: 'EVENT_FLAG'}, 'Checks EVENT_FLAG with param[1] & param[2]. Loops backwards if it does not match. param[0] controls the desired behavior: 1 = return if flag set, 0 = return if flag not set'), # TODO: add validation check that accepts only 0 or 1 for param[0]
	54: EventCommand(2, 'WkEvFlgWait'),
	55: EventCommand(4, 'OPosMove'),
	56: EventCommand(7, 'ObjPosMove'),
	57: EventCommand(0, 'KeyCut', {}, 'sets bit 0x8000 in syust'),
	58: EventCommand(0, 'KeyRet', {}, 'clears bit 0x8000 in syust'),

	60: EventCommand(2, 'OAniChen'), #used?
	61: EventCommand(2, 'OSyuAniChen'),
	62: EventCommand(2, 'PartyDelIN', {1: 'CHANO'}),
	63: EventCommand(-1, 'InitPartySet', {1: 'CHANO', 2: 'CHANO', 3: 'CHANO', 4: 'CHANO', 5: 'CHANO', 6: 'CHANO', 7: 'CHANO'}, '', basic_count_var_len),
	64: EventCommand(0, 'InitPartyOpenN'),
	65: EventCommand(-1, 'InitPartyOpenP', {}, '', party_open_p_var_len),
	66: EventCommand(0, 'FieldCommandGo'), #used?
	67: EventCommand(-1, 'WindowjikanSentaku'), # variability appears to be 3 fixed, 2 per param[2], 2 more fixed, but has several Skips
	68: EventCommand(5, 'ObjColChenge', {}, 'Sets R G B (params[2-4]) of the specified EVENT_HUMAN (params[0])'),
	69: EventCommand(1, 'FIOControll'),
	70: EventCommand(2, 'MfreeOverlayGo'),
	71: EventCommand(2, 'CharEvFlgSet', {1: 'CHANO'}, 'Sets G2_SYS_G2_chat_flag'), # used?
	72: EventCommand(-1, 'ObjEfctCon'), # variable to 3 or 4 params, based in part on compos
	73: EventCommand(1, 'TimWait', {}, 'Loops until compos equals the parameter'),
	74: EventCommand(1, 'MachiStControll', {}, 'Sets bit 0 in mstatus'),
	75: EventCommand(-1, 'LPartySet', {1: 'CHANO', 2: 'CHANO', 3: 'CHANO', 4: 'CHANO', 5: 'CHANO', 6: 'CHANO', 7: 'CHANO'}, '', basic_count_var_len),
	76: EventCommand(5, 'SrnNanameScroll'),
	77: EventCommand(-1, 'OMoveTK'), # variable length based in part in param[0] (if < 7, different logic)
	78: EventCommand(1, 'WindowFaceHyojyo', {}, 'Sets kaono -- "face number"?'),
	79: EventCommand(1, 'WinEvFlgSet', {}, 'Sets given bit in event_flag[4][3]'),
	80: EventCommand(1, 'WinEvFlgOff', {}, 'Clears given bit in event_flag[4][3]'),
	81: EventCommand(2, 'WinEvFlgWait', {}, 'Loops until given bit (param[1]) in event_flag[4][3] is set or cleared, depending on param[0]'),
	82: EventCommand(0, 'WindowStopClear'),
	83: EventCommand(2, 'EventBattleGo', {1: 'BATTLE_NO'}, 'Calls EventBatlleSet(param[1], param[0])'),
	84: EventCommand(2, 'CharaStatus', {0: 'CHANO'}),
	85: EventCommand(-1, 'BGfreeOverlayGo', {}, '', bg_free_overlay_go_var_len),
	86: EventCommand(5, 'SurinukeSet', {0: 'AREA_NO', 1: 'TOWN_NO', 2: 'MAP_NO'}, 'Sets the escape destination for the map. Param names: s_area_no, s_town_no, s_map_no, s_x, and s_y'), # 
	87: EventCommand(1, 'SurinukeFlg', {}, 'Updates bit in msave_st'),
	88: EventCommand(0, 'Map16On'),
	89: EventCommand(-1, 'AnimeChenge', {}, '', anime_chenge_var_len),
	90: EventCommand(-1, 'OMoveAK', {}, ''), # see commented out method above
	91: EventCommand(2, 'SyuAnimeChenge'),
	92: EventCommand(-1, 'WindowIroSerifu'), # variable length based in part on param[2] (if < 7, different logic)
	93: EventCommand(3, 'OPriSet'),
	94: EventCommand(4, 'ObjFDIO'),
	95: EventCommand(0, 'ResetGo'),
	96: EventCommand(-1, 'ShopOverlayGo'), # complicated variable nature, based on current compos
	97: EventCommand(2, 'TkFlgSet'),
	98: EventCommand(2, 'TkFlgOff'),
	99: EventCommand(2, 'TwFlgSet'),
	100: EventCommand(2, 'TwFlgOff'),
	101: EventCommand(2, 'SoundCall', {}, 'Play Sounds'),
	102: EventCommand(1, 'BatBgm'),
	103: EventCommand(0, 'PartyRefresh', {}, 'Restore party HP/MP'),
	104: EventCommand(3, 'OHanSet', {}, 'calls ANIME_anmSetSemiOn/Off'),
	105: EventCommand(3, 'SoundRead', {}, 'Start BGM'),
	106: EventCommand(2, 'OJinPosSet', {}, 'Swaps info between the two given EVENT_HUMANs'),
	107: EventCommand(2, 'PartyMoney', {}, 'Calls G2_SYS_G2_party_gold'),
	108: EventCommand(1, 'Mfree640Go'),
	109: EventCommand(2, 'FieldCdSeek'),
	110: EventCommand(0, 'NOP'),
	111: EventCommand(0, 'HonSentaku', {}, 'sets senno to base_lv'),
	112: EventCommand(-1, 'OverlayPset', '', basic_count_var_len),
	113: EventCommand(0, 'PartyAllDel', {}, 'Empties the party'),
	114: EventCommand(3, 'SMapChenge', {0: 'MAP_MNO'}, 'Sets mno, px, py'),
	115: EventCommand(2, 'CharaLV', {0: 'CHANO'}),
	116: EventCommand(4, 'CharaSoutaiLV', {0: 'CHANO', 1: 'CHANO'}),
	117: EventCommand(2, 'SpeBgm', {}, 'sets spbgm'),
	118: EventCommand(5, 'WindowNameSerifu', {1: 'WINDOW_MFNO', 3: 'WINDOW_MFNO'}, 'param[0] is a EVENT_HUMAN. Sets nmfno, nmno, mfno, and mno for remaining params'),
	119: EventCommand(4, 'WindowNameHenji', {0: 'WINDOW_MFNO', 2: 'WINDOW_MFNO'}, 'Sets nmfno, nmno, mfno, and mno to param values'),
	120: EventCommand(4, 'WindowPartySerifu', {1: 'WINDOW_MFNO'}),
	121: EventCommand(1, 'BatParChg', {}, 'Sets MAPEVDAT batlno'),
	122: EventCommand(1, 'ShipONOFF', {}, 'sets or clears flag in mstatus'),
	123: EventCommand(-1, 'TimeSet', {}, '', time_set_var_len),
	124: EventCommand(2, 'TwGFlgSet', {}, 'sets bit in town_flag'),
	125: EventCommand(2, 'TwGFlgOff', {}, 'clears bit in town_flag'),
	126: EventCommand(2, 'ItemDel', {}, 'Calls G2_Sys_G2_deldel on a Party Item'),
	127: EventCommand(3, 'TwFlgWait', {}, 'Loops until map_in_out_flag set or cleared'),
	128: EventCommand(-1, 'YMOverlayGo', {}, '', overlay_go_var_len),
	129: EventCommand(3, 'CharaKouStatus', {1: 'CHANO'}, 'calls G2_SYS_G2_chara_love'),
	130: EventCommand(2, 'OAniCut', {}, 'set or clear osta bit 0x2000 (based on params[0]) for EVENT_HUMAN specified by params[1]'),
	131: EventCommand(2, 'HonFlgSet', {}, 'sets bit in game_data'),
	132: EventCommand(2, 'HonFlgOff', {}, 'clears bit in game_data'),
	133: EventCommand(1, 'RndBatCut', {}, 'sets or clears bit in est'),
	134: EventCommand(-1, 'OverlayPset2', {}, '', basic_count_var_len),
	135: EventCommand(0, 'EndMemory'), # used?
	136: EventCommand(1, 'PartyDel'), # used?
	137: EventCommand(0, 'OnCloseResetDialog', 'clears _showResetDialog'), # used?
	138: EventCommand(2, 'FixDoor'),
	139: EventCommand(-1, 'PartyDelExcludingCharaNo', {1: 'CHANO', 2: 'CHANO', 3: 'CHANO', 4: 'CHANO', 5: 'CHANO', 6: 'CHANO', 7: 'CHANO'}, '', basic_count_var_len), # appears to be unused
	140: EventCommand(-1, 'MachiChengeM', {}, '', machi_chenge_var_len),
	141: EventCommand(1, 'VsyncControl', {}, 'calls SystemObject_Force60FPS'),
	
	204: EventCommand(0, 'NOP'),
	254: EventCommand(0, 'NOP'),
	255: EventCommand(1, 'END')
})