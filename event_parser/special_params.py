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
    (35,): "Freed Y.",
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
    (69,): "LCC",
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
    (84,): "",
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

EVENT_FLAG = {
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

CHARA_STATUS = {
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
