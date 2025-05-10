from utils import tab_print
from typing import List

# Special params have multiple purposes:
#  1) they are used to translate values to text
#  2) any special params will be counted

# Dictionary of character numbers to the character name
CHANO = {
    (0,): "N/A",
    (1,): "Riou",
    (2,): "Flik",
    (3,): "Viktor",
    (4,): "Viki",
    (5,): "Sheena",
    (6,): "Clive",
    (7,): "Hix",
    (8,): "Tengaar",
    (9,): "Futch",
    (10,): "Humphrey",
    (11,): "Georg",
    (12,): "Valeria",
    (13,): "Pesmerga",
    (14,): "Lorelai",
    (15,): "Shin",
    (16,): "Rikimaru",
    (17,): "Tomo",
    (18,): "Nanami",
    (19,): "Eilie",
    (20,): "Rina",
    (21,): "Bolgan",
    (22,): "Tuta",
    (23,): "Hanna",
    (24,): "Millie",
    (25,): "Karen",
    (26,): "Shiro",
    (27,): "Zamza",
    (28,): "Gengen",
    (29,): "Gabocha",
    (30,): "Kinnison",
    (31,): "Shilo",
    (32,): "Miklotov",
    (33,): "Camus",
    (34,): "Hauser",
    (35,): "FreedY",
    (36,): "Kahn",
    (37,): "Amada",
    (38,): "Tai Ho",
    (39,): "Anita",
    (40,): "Bob",
    (41,): "Meg",
    (42,): "Gadget",
    (43,): "Ayda",
    (44,): "Killey",
    (45,): "Sierra",
    (46,): "Oulan",
    (47,): "Genshu",
    (48,): "Mukumuku",
    (49,): "Abizboah",
    (50,): "Feather",
    (51,): "Badeaux",
    (52,): "Tsai",
    (53,): "Luc",
    (54,): "Chaco",
    (55,): "Nina",
    (56,): "Sid",
    (57,): "Yoshino",
    (58,): "Gijimu",
    (59,): "Koyu",
    (60,): "Lo Wen",
    (61,): "Mazus",
    (62,): "Sasuke",
    (63,): "Mondo",
    (64,): "Vincent",
    (65,): "Simone",
    (66,): "Hai Yo",
    (67,): "Stallion",
    (68,): "Wakaba",
    (69,): "LCChan",
    (70,): "Gantetsu",
    (71,): "Hoi",
    (72,): "Siegfried",
    (73,): "Kasumi",
    (74,): "Rulodia",
    (75,): "Makumaku",
    (76,): "Mikumiku",
    (77,): "Mekumeku",
    (78,): "Mokumoku",
    (79,): "Chuchura",
    (80,): "Jowy",
    (81,): "Jowy2",
    (82,): "McDohl",
    (83,): "Millie2",
    (85,): "Apple",
    (86,): "Templeton",
    (87,): "Kiba",
    (88,): "Fitcher",
    (89,): "Shu",
    (90,): "Tetsu",
    (91,): "Leona",
    (92,): "Huan",
    (93,): "Jess",
    (94,): "Hilda",
    (95,): "Alex",
    (96,): "Emilia",
    (97,): "Tenkou",
    (98,): "Barbara",
    (99,): "Richmond",
    (100,): "Yam Koo",
    (101,): "Teresa",
    (102,): "Yuzu",
    (103,): "Taki",
    (104,): "Tony",
    (105,): "Adlai",
    (106,): "Gordon",
    (107,): "Hans",
    (108,): "Connell",
    (109,): "Lebrante",
    (110,): "Tessai",
    (111,): "Raura",
    (112,): "Annallee",
    (113,): "Pico",
    (114,): "Alberto",
    (115,): "Jude",
    (116,): "Jeane",
    (117,): "Ridley",
    (118,): "Klaus",
    (119,): "Maximillian",
    (120,): "Marlowe",
    (121,): "Gilbert",
    (122,): "Boris",
    (123,): "Pilika",
    (124,): "Pilika2",
    (125,): "Gremio",
}

# Found by hooking GAME_WORK.eventFlgON and eventFlgOFF
EVENT_FLAG = {

    # Multipurpose event bits
    (0, 1): "Multipurpose",
    (0, 2): "Multipurpose",
    (0, 4): "Multipurpose",
    (0, 8): "Multipurpose",
    (0, 16): "Multipurpose",
    (0, 32): "Multipurpose",
    (0, 64): "Multipurpose",
    (0, 128): "Multipurpose",
    ## These appear to get toggled with different speech selections
    (238, 1): "Multipurpose",
    (238, 2): "Multipurpose",
    (238, 4): "Multipurpose",
    (238, 8): "Multipurpose",
    (238, 16): "Multipurpose",
    (238, 32): "Multipurpose",
    (238, 64): "Multipurpose",
    (238, 128): "Multipurpose",
    ## These appear to control some screen effects
    (237, 1): "Multipurpose",
    (237, 2): "Multipurpose",
    (237, 4): "Multipurpose",
    (237, 8): "Multipurpose",
    (237, 16): "Multipurpose",
    (237, 32): "Multipurpose",
    (237, 64): "Multipurpose",
    (237, 128): "Multipurpose",


    # map changes
    (55, 4): "EnteredSwallow", # North Swallow Pass
    
    # Ryube events
    (52, 4): "EnteredRyube",
    ## Rikimaru
    (165, 2): "RikimaruFed",
    (165, 4): "RikimaruNoPay", # didn't pay for Rikimaru's meal
    (165, 8): "RikimaruPay", # paid for Rikimaru's meal
    (165, 16): "RikimaruRecruited",
    ## Millie
    (165, 32): "HelpingMillie", # in Ryube, agree to help Millie
    (165, 64): "HelpingMillie", # in Ryube, agreed to help Millie
    (160, 4): "BonaparteSeen", # in Ryube Forest, see Bonaparte
    (160, 8): "MillieRecruited",
    ## Shiro, Kinnison
    (207, 16): "PutBabyBirdInNest",
    (207, 32): "DeniedBabyBird", # deny putting baby bird in nest
    (207, 64): "CantSayToKinnison", # choose "I can't say" to Kinnison
    (207, 128): "ShiroRecruited", # and Kinnison too, but more importantly, Shiro

    (165, 128): "EnteredWorldMap", #after recruiting Ryube characters. Stops getting set after starting Pilika's quest

    # Toto
    (52, 2): "EnteredToto",
    (206, 16): "ZamzaRecruited",
    (166, 4): "MetPilika",
    (160, 16): "NoToPilika", # say, "That's kind of far" when Pilika asks you to go to Muse
    (166, 8): "GotPilikasMoney", # Received Pilika's money to buy Wooden Amulet

    # Going to Muse
    (54, 128): "EnteredWhiteDeer",
    (54, 2): "EnteredMuseHighlandCheckpoint",
    (54, 4): "EnteredMuseMatildaCheckpoint",
    (54, 8): "EnteredMuseGreenhillCheckpoint",
    (51, 32): "EnteredGreenhill",
    (51, 16): "EnteredForestVillage",
    (216, 128): "SpokeToWakaba", #in Forest Village about her Master
    (216, 8): "SpokeToTony",
    (88, 16): "LeftForestVillage", # turned off after exiting Forest Village
    (53, 4): "EnteredTwoRiver",
    (51, 2): "EnteredCoronet",
    (51, 1): "EnteredMuse",
    (151, 32): "MuseBlacksmithDoor", # ON when standing at the blacksmith door, OFF when you step away -- multipurpose?
    (166, 16): "BoughtWoodenAmulet", 

    # After Toto Burned
    (166, 32): "TotoBurned",
    (52, 8): "EnteredMercFort",
    (166, 128): "BriefedViktorFlik", # briefed Viktor and Flik on Toto
    (167, 1): "SpokeWithJowy", # spoke with Jowy about trust
    (167, 2): "GoingToViktorToHelp", #going to speak with Viktor about helping
    (167, 4): "ShownFireSpears", # when asked to go to Tsai
    (167, 8): "GoingToTsai", # agreed to ask Tsai for help
    (167, 16): "GoingToTsai", # after receiving the money from Flik

    (52, 16): "EnteredRadat",

    (167, 64): "NothingToTsai", # say "nothing in particular" to Tsai
    (167, 128): "RecruitedTsai",

    (239, 128): "RyubeManKilled", # flips ON and OFF when Luca killed man in Ryube

    (168, 2): "RyubeBurned",

    (208, 2): "SpokeWithHanna",
    (208, 1): "HannaRecruited",

    (168, 4): "PilikaJoinedConvoy", # pilika joins convoy at merc fort
    (168, 8): "TsaiLeftParty", # after talking to Viktor and Flik and Tsai left to repair the Fire Spears
    (168, 16): "IUnderstand", # after selecting "I understand" rather than "I want to fight"
    (169, 1): "AnotherChoice", # after speaking to Viktor again about wanting to fight
    (168, 32): "IWantToFight", # after choosing "I want to fight"
    (169, 2): "ScratchedFlik", # after attacking Flik in duel
    (169, 4): "AfterFlikDuel", # after the duel with Flik

    (169, 8): "MercFortAttackStart",
    (169, 16): "NeedMoreTime", # after selecting "We still need more time..." before the battle
    (169, 32): "MercFortBattle", # right before the war battle begins for the merc fort
    (169, 64): "MercFortBattleWon",
    (169, 128): "WaitAMinute", # between two battles, choose "Wait a minute"

    (170, 1): "MercFortBattle2",
    (170, 2): "MercFortBattle2Lost",
    (170, 4): "MercFortLookingForPilika", 
    (160, 32): "MercFortLookingForPilika",
    (176, 1): "FightSoldier1", # first battle within fort
    (170, 128): "FightSoldier2", # second battle by fireplace
    (170, 32): "FightSoldier3", # third battle by stairs
    (176, 2): "FightSoldier4", # fourth battle at top of stairs
    (176, 4): "FightSoldier4", # same

    (237, 32): "MercFortShaking", #when screen is shaking
    (237, 64): "MercFortExplosion", # when screen is red
    (237, 128): "MercFortShaking", # when screen is shaking

    (170, 8): "MercFortDestroyed",
    (171, 1): "LeftMercFort", # after leaving destroyed fort for world map

    (171, 2): "PilikaShrine", # after Pilika leaves the party and goes to the Shrine
    (171, 32): "PilikaInShrine", # after Pilika enters the shrine
    (171, 2): "FlashbackPrison",
    (171, 4): "FlashbackDone",
    (171, 8): "AcceptPower",
    (171, 16): "ShrineDone",

    (23, 8): "WeaponLvl14", # Suspected -- prereq for Genshu recruitment
    
}

PNO = {
}

WINDOW_MSG = {
	# these are left undefined; however, by tracking it as a "special param", it'll be counted
}

MAP_MNO = {
	# used by MapChenge -- may be the same as MAP_NO? Uncertain
}

WORLD_MAP_REGION = {
}

AREA_NO = {
    (0,): "Kyaro_Area_A",
    (1,): "MercFort_Area_B",
    (2,): "Muse_Area_C",
    (3,): "NorthWindow_Area_D",
    (4,): "Greenhill_Area_E",
    (5,): "Gregminster_Area_F",
    (6,): "Tinto_Area_G",
    (7,): "TwoRiver_Area_H",
    (8,): "Rockaxe_Area_I",
    (9,): "LRen_Area_J",
    (10,): "HQ_Area_K",
    (12,): "WorldMap"
}

TOWN_MAP = {
}

FILE_NO = {
}

BATTLE_NO = {
}

SOUND = {
}

MAP_IN_OUT_FLAG = {
}

T_BOX_FLAG = {
}

CHA_FLAG_MODE = {
    (1,): "Recruited",
    (30,): "StartRecruit", # possibly -- seems to be set when initiating the recruitment dialog
    (31,): "Recruit", 
    #(37,): "Recruit", # and add to convoy?
    #(38,): "Left", # when Tsai left the party
    #(39,): "Left", # when Tsai left the party
}

ITEM = {
    # 0 = Regular items
    (0, 30): "SacrificialJizo",
    (0, 39): "FlintStone",
    (0, 47): "IronHammer",
    (0, 48): "CopperHammer",
    (0, 49): "SilverHammer",
    (0, 50): "GoldHammer",

    # 16 = Equipment
    (16, 38): "WoodenShield",
    (16, 46): "Boots", 
    (16, 75): "RoseBrooch",

    # 32 = Runes
    (32, 5): "WindOrb",

    # 48 = Farming
    (48, 1): "CabbageSeed",
    (48, 2): "PotatoSeed",
    (48, 3): "SpinachSeed",
    (48, 4): "TomatoSeed",
    (48, 5): "Chick",
    (48, 6): "Piglet",
    (48, 7): "Lamb",
    (48, 8): "Calf",

    # 64 = Trade
    (64, 6): "CeladonUrn",

    # 80 = Base Item
}

def get_special_param_str(special_param_str: str, param: tuple[int, ...]) -> str:
    # Don't tuplize single values (ex: "(0,)" => "0")
    param_str = str(param)

    if isinstance(param, tuple) and 1 == len(param):
        param_str = str(param[0])

    default = f"{param_str} "
    if(special_param_str in globals()):
        global_obj = globals()[special_param_str]
        if(param in global_obj):
            return f"{global_obj[param]}({param_str}) "
        else:
            return default
    else:
        print(f"WARNING: Unknown special param: {special_param_str}")
        return default
    
class SpecialParamsTracker:
    """
    Class used to track special param usage
    """
    def __init__(self):
        # A dictionary where each key is a special_param and each value is a set of the parameter values seen
        self.special_params_used = {}

    def add(self, special_param_str: str, param_values: tuple[int, ...]):
        # track that it used this special param -- initialize it as a set if this is the first time it's been seen here
        if(special_param_str not in self.special_params_used):
            self.special_params_used[special_param_str] = set()
        self.special_params_used[special_param_str].add(param_values)

    def print_info(self, tabs: int):
        if not self.special_params_used:
            tab_print(tabs, f"NONE")

        for key, value_set in self.special_params_used.items():
            sorted_values = ""
            for value in sorted(value_set):
                sorted_values += get_special_param_str(key, value)

            tab_print(tabs, f"{key}: {sorted_values}")
