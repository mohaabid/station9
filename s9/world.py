"""Where everything is. Every coordinate in the map lives here.

Three areas share one column of chunks (x -16..79, z -16..47):
  SURFACE  ground y=100, open sky, the lift house sits right over the shaft
  B8       floor y=50, rooms y51-53, ceiling y=54   (staff level)
  B9       floor y=40, rooms y41-43, ceiling y=44   (containment level)
Two stairwells join B8 and B9: the main one by the lift, and the service one in the east.
"""

FORCELOAD = ((-16, -16), (79, 47))

# =========================================================================
# SURFACE
# =========================================================================
GROUND = 100                       # top of the ground; you walk at y=101
SURF_MIN, SURF_MAX = (-14, -14), (77, 45)
DY_CAGE = 50                       # surface cage sits 50 above the B8 cage (same x/z)

TRUCK_START = (69.5, 101, 18.5, 90)   # x y z yaw  (facing west, towards the gate)
GATE = ((66, 101, 16), (66, 103, 18))
FENCE_X = 66
HUT = ((31, 101, 27), (36, 103, 31))          # interior
HUT_DOOR = (33, 101, 26)
LIFT_HOUSE = ((0, 101, 13), (11, 105, 26))    # interior (the cage is inside it)
LIFT_HOUSE_DOOR = ((12, 101, 19), (12, 103, 20))
CALL_BUTTON = (7, 102, 21)
SIGNIN_BUTTON = (35, 102, 26)                  # outside wall? no: inside, see build
KIT_BARREL = (31, 101, 31)

# =========================================================================
# THE CAGE (identical at the surface and at B8; B9 has only the shaft bottom)
# =========================================================================
CAGE = ((2, 0, 18), (5, 2, 21))          # interior, y relative to the floor-above block
CAGE_GATE = ((6, 0, 19), (6, 2, 20))     # the shutter, y relative
CAGE_B9_BUTTON = (3, 1, 18)              # facing south, on the north wall
CAGE_LIGHT_LEVER = (5, 1, 18)            # facing south
CAGE_RELEASE = (2, 1, 19)                # facing east (B8 only matters)
CAGE_LAMP = (4, 3, 20)                   # in the ceiling


def cage_y(level):
    return {"surface": 101, "b8": 51}[level]


def rel(p, y0):
    return (p[0], p[1] + y0, p[2])


# =========================================================================
# UNDERGROUND ROOMS
# Rooms in build order: later rooms win shared walls. Boxes are interiors.
# =========================================================================
def R(box, wall, accent, floor, ceil, **kw):
    return dict(box=box, wall=wall, accent=accent, floor=floor, ceil=ceil, **kw)


B9_FLOOR, B9_CEIL = 40, 44
B8_FLOOR, B8_CEIL = 50, 54

B9 = {
    "office": R(((10, 41, 11), (20, 43, 17)), "light_gray_terracotta", "gray_terracotta", "dark_oak_planks", "smooth_stone",
                wall_scatter=[("moss_block", .04)]),
    "washroom": R(((11, 41, 7), (13, 43, 9)), "white_terracotta", "light_gray_terracotta", "polished_diorite", "smooth_stone"),
    "reflection": R(((11, 41, 3), (13, 43, 5)), "white_terracotta", "light_gray_terracotta", "polished_diorite", "smooth_stone"),
    "alcove": R(((10, 41, 0), (14, 43, 1)), "light_gray_terracotta", "gray_terracotta", "dark_oak_planks", "smooth_stone"),
    "records": R(((25, 41, 5), (32, 43, 10)), "gray_terracotta", "light_gray_terracotta", "spruce_planks", "smooth_stone",
                 wall_scatter=[("moss_block", .03)]),
    "lockroom": R(((36, 41, 5), (45, 43, 10)), "light_gray_concrete", "gray_concrete", "polished_andesite", "smooth_stone",
                  wall_scatter=[("cyan_terracotta", .05)]),
    "north": R(((22, 41, 12), (53, 43, 13)), "deepslate_bricks", "polished_deepslate", "deepslate_tiles", "smooth_basalt",
               wall_scatter=[("cracked_deepslate_bricks", .15)], floor_scatter=[("cracked_deepslate_tiles", .10)]),
    "containment": R(((26, 41, 22), (36, 43, 30)), "polished_deepslate", "deepslate_tiles", "polished_blackstone", "smooth_basalt",
                     wall_scatter=[("sculk", .06)], floor_scatter=[("sculk", .07)]),
    "corridor": R(((7, 41, 19), (48, 43, 20)), "deepslate_bricks", "polished_deepslate", "deepslate_tiles", "smooth_basalt",
                  wall_scatter=[("cracked_deepslate_bricks", .15)], floor_scatter=[("cracked_deepslate_tiles", .12)]),
    "shaft9": R(((2, 41, 18), (5, 43, 21)), "waxed_oxidized_copper", "waxed_oxidized_cut_copper", "gravel", "waxed_oxidized_cut_copper"),
    "tunnel1": R(((58, 41, 27), (59, 43, 35)), "waxed_oxidized_cut_copper", "waxed_weathered_copper", "waxed_exposed_cut_copper",
                 "polished_deepslate", wall_scatter=[("waxed_oxidized_copper", .12)]),
    "tunnel2": R(((47, 41, 34), (59, 43, 35)), "waxed_oxidized_cut_copper", "waxed_weathered_copper", "waxed_exposed_cut_copper",
                 "polished_deepslate", wall_scatter=[("waxed_oxidized_copper", .12)]),
    "generator": R(((50, 41, 15), (60, 43, 25)), "waxed_weathered_cut_copper", "polished_deepslate", "polished_andesite", "smooth_basalt",
                   floor_scatter=[("andesite", .15)]),
    # tall: joins B9 and B8
    "stairs": R(((8, 41, 22), (12, 53, 31)), "deepslate_tiles", "polished_deepslate", "deepslate_tiles", "smooth_basalt"),
    "service": R(((58, 41, 36), (59, 53, 45)), "waxed_oxidized_cut_copper", "waxed_weathered_copper", "waxed_exposed_cut_copper",
                 "polished_deepslate"),
}

B8 = {
    "cage8": R(((2, 51, 18), (5, 53, 21)), "waxed_oxidized_copper", "waxed_oxidized_cut_copper", "waxed_weathered_cut_copper",
               "waxed_oxidized_cut_copper"),
    "lobby": R(((7, 51, 14), (20, 53, 20)), "white_terracotta", "light_blue_terracotta", "polished_diorite", "smooth_quartz",
               wall_scatter=[("light_gray_terracotta", .06)]),
    "dormhall": R(((24, 51, 1), (25, 53, 14)), "light_gray_terracotta", "white_terracotta", "spruce_planks", "smooth_quartz"),
    "dormA": R(((18, 51, 8), (22, 53, 12)), "white_terracotta", "brown_terracotta", "spruce_planks", "smooth_quartz"),
    "dormB": R(((18, 51, 1), (22, 53, 5)), "white_terracotta", "brown_terracotta", "spruce_planks", "smooth_quartz"),
    "dormC": R(((27, 51, 8), (31, 53, 12)), "white_terracotta", "brown_terracotta", "spruce_planks", "smooth_quartz"),
    "dormD": R(((27, 51, 1), (31, 53, 5)), "white_terracotta", "brown_terracotta", "spruce_planks", "smooth_quartz"),
    "cafeteria": R(((34, 51, 4), (47, 53, 14)), "white_concrete", "light_gray_concrete", "white_terracotta", "smooth_quartz",
                   floor_scatter=[("light_gray_terracotta", .5)]),
    "kitchen": R(((35, 51, -2), (40, 53, 2)), "white_concrete", "iron_block", "smooth_stone", "smooth_quartz"),
    "hall": R(((21, 51, 16), (52, 53, 17)), "white_terracotta", "light_blue_terracotta", "polished_diorite", "smooth_quartz",
              wall_scatter=[("light_gray_terracotta", .08)], floor_scatter=[("diorite", .1)]),
    "lab": R(((22, 51, 19), (31, 53, 25)), "white_concrete", "cyan_terracotta", "smooth_quartz", "smooth_quartz"),
    "specimen": R(((22, 51, 27), (31, 53, 32)), "polished_deepslate", "deepslate_tiles", "polished_blackstone", "smooth_basalt",
                  wall_scatter=[("sculk", .05)]),
    "comms": R(((34, 51, 19), (42, 53, 25)), "gray_concrete", "black_concrete", "gray_concrete", "smooth_stone"),
    "security": R(((45, 51, 19), (49, 53, 24)), "light_gray_concrete", "gray_concrete", "gray_carpet", "smooth_stone"),
    "servicec": R(((51, 51, 18), (52, 53, 47)), "waxed_oxidized_cut_copper", "waxed_weathered_copper", "waxed_exposed_cut_copper",
                  "polished_deepslate", wall_scatter=[("waxed_oxidized_copper", .12)]),
    "servicee": R(((53, 51, 46), (59, 53, 47)), "waxed_oxidized_cut_copper", "waxed_weathered_copper", "waxed_exposed_cut_copper",
                  "polished_deepslate"),
}

SHELLS = [((-1, 38, -4), (63, 46, 38)), ((-1, 48, -4), (63, 56, 49)), ((56, 38, 36), (61, 56, 49)), ((6, 38, 20), (14, 56, 33))]

# Openings through walls: (box, initial block)
B9_OPEN = {
    "shaft_door": (((6, 41, 19), (6, 43, 20)), "iron_block"),
    "stairs9": (((8, 41, 21), (9, 43, 21)), "air"),
    "contain_n": (((30, 41, 21), (31, 43, 21)), "iron_bars[east=true,west=true]"),
    "contain_s": (((35, 41, 31), (36, 43, 31)), "iron_block"),
    "gen_w": (((49, 41, 19), (49, 43, 20)), "air"),
    "gen_n": (((52, 41, 14), (53, 43, 14)), "air"),
    "gen_s": (((58, 41, 26), (59, 43, 26)), "iron_block"),
    "office_door": (((15, 41, 18), (15, 42, 18)), "air"),
    "office_east": (((21, 41, 13), (21, 42, 13)), "air"),
    "wash_arch": (((12, 41, 10), (12, 43, 10)), "air"),
    "refl_arch": (((12, 41, 2), (12, 43, 2)), "air"),
    "mirror": (((11, 41, 6), (13, 43, 6)), "light_gray_stained_glass_pane[east=true,west=true]"),
    "records": (((28, 41, 11), (28, 42, 11)), "air"),
    "lockroom": (((40, 41, 11), (41, 43, 11)), "air"),
}
B8_OPEN = {
    "cage8_gate": (((6, 51, 19), (6, 53, 20)), "iron_block"),
    "stairs8": (((11, 51, 21), (12, 53, 21)), "iron_block"),
    "lobby_hall": (((21, 51, 16), (21, 53, 17)), "air"),
    "dormhall": (((24, 51, 15), (25, 53, 15)), "air"),
    "dormA": (((23, 51, 10), (23, 52, 10)), "air"),
    "dormB": (((23, 51, 3), (23, 52, 3)), "air"),
    "dormC": (((26, 51, 10), (26, 52, 10)), "air"),
    "dormD": (((26, 51, 3), (26, 52, 3)), "air"),
    "cafe1": (((36, 51, 15), (37, 53, 15)), "air"),
    "cafe2": (((44, 51, 15), (45, 53, 15)), "air"),
    "kitchen": (((37, 51, 3), (37, 52, 3)), "air"),
    "lab": (((26, 51, 18), (27, 53, 18)), "air"),
    "specimen": (((30, 51, 26), (30, 52, 26)), "air"),
    "window": (((23, 52, 26), (28, 53, 26)), "glass_pane[east=true,west=true]"),
    "comms": (((38, 51, 18), (38, 52, 18)), "air"),
    "security": (((47, 51, 18), (47, 52, 18)), "air"),
    "servicec": (((51, 51, 18), (52, 53, 18)), "air"),
}

# Wooden doors placed after the openings: (lower block, facing, hinge, wood)
DOORS = {
    "office": ((15, 41, 18), "north", "left", "dark_oak"),
    "office_east": ((21, 41, 13), "east", "left", "dark_oak"),
    "records": ((28, 41, 11), "north", "right", "spruce"),
    "dormA": ((23, 51, 10), "west", "left", "spruce"),
    "dormB": ((23, 51, 3), "west", "right", "spruce"),
    "dormC": ((26, 51, 10), "east", "right", "spruce"),
    "dormD": ((26, 51, 3), "east", "left", "spruce"),
    "kitchen": ((37, 51, 3), "north", "left", "birch"),
    "specimen": ((30, 51, 26), "south", "left", "dark_oak"),
    "comms": ((38, 51, 18), "south", "left", "dark_oak"),
    "security": ((47, 51, 18), "south", "right", "dark_oak"),
}

# Lockers: the door cell sits in a wall. facing points from the corridor into the locker.
LOCKERS = [
    # B9 main corridor
    ((24, 41, 18), "north"), ((35, 41, 18), "north"), ((44, 41, 18), "north"),
    ((19, 41, 21), "south"), ((41, 41, 21), "south"),
    # B9 north corridor
    ((33, 41, 11), "north"), ((47, 41, 11), "north"), ((25, 41, 14), "south"), ((45, 41, 14), "south"),
    # B9 staff locker room (north wall)
    ((37, 41, 4), "north"), ((38, 41, 4), "north"), ((39, 41, 4), "north"), ((42, 41, 4), "north"), ((43, 41, 4), "north"),
    ((44, 41, 4), "north"),
    # B9 office, generator, dead-end tunnel
    ((8, 41, 18), "north"), ((61, 41, 19), "east"), ((49, 41, 33), "north"),
    # B8 hall and service corridor (for the escape)
    ((29, 51, 15), "north"), ((49, 51, 15), "north"), ((33, 51, 18), "south"), ((43, 51, 18), "south"),
    ((50, 51, 30), "west"), ((53, 51, 38), "east"),
    # B8 lobby
    ((14, 51, 13), "north"),
]

# =========================================================================
# LAMPS: redstone lamps set straight into ceilings (no redstone behind them)
# =========================================================================
LAMPS = {
    # surface cage and B8 cage
    "E0": (4, 104, 20), "E8": (4, 54, 20),
    # B8
    "L1": (10, 54, 17), "L2": (17, 54, 17),
    "H1": (24, 54, 16), "H2": (31, 54, 17), "H3": (40, 54, 16), "H4": (48, 54, 17),
    "D1": (24, 54, 7), "DA": (20, 54, 10), "DB": (20, 54, 3), "DC": (29, 54, 10), "DD": (29, 54, 3),
    "F1": (38, 54, 9), "F2": (44, 54, 9), "KI": (37, 54, 0),
    "LB1": (24, 54, 22), "LB2": (29, 54, 22), "SP": (27, 54, 30),
    "CM": (38, 54, 22), "SE": (47, 54, 21),
    "S1": (52, 54, 25), "S2": (51, 54, 38), "S3": (56, 54, 46),
    # B9
    "C1": (10, 44, 19), "C2": (21, 44, 20), "C3": (33, 44, 19), "C4": (45, 44, 20),
    "O1": (15, 44, 14), "W1": (12, 44, 8), "R1": (12, 44, 4), "A1": (12, 44, 0),
    "N1": (27, 44, 12), "N2": (38, 44, 13), "N3": (49, 44, 12), "REC": (28, 44, 7), "LCK": (40, 44, 7),
    "K1": (31, 44, 23), "K2": (31, 44, 28),
    "G1": (52, 44, 17), "G2": (58, 44, 17), "G3": (52, 44, 23), "G4": (58, 44, 23),
    "T1": (58, 44, 31), "T2": (53, 44, 35),
    # stairwells (lamps in the walls)
    "ST1": (7, 43, 25), "ST2": (10, 48, 32), "ST3": (13, 52, 25), "SS1": (60, 45, 39), "SS2": (60, 50, 44),
}
B8_BACKUP = ["L1", "H2", "H4", "SE", "LB1", "CM", "DC", "S1"]
B9_BACKUP = ["C1", "C2", "C4", "W1", "R1", "K1", "K2", "G1", "N2", "REC", "LCK", "ST1"]
STAIR_LAMPS = ["ST3", "ST2", "ST1"]

# =========================================================================
# KEY POSITIONS
# =========================================================================
B8_ARRIVE = (4.0, 51, 20.0)
RELAY_LEVER = (40, 52, 25)            # comms room, south wall (facing north)
STAIR_DOOR8 = ((11, 51, 21), (12, 53, 21))
STAIR_BUTTON8 = (13, 52, 20)          # on the lobby wall beside the stair door, facing north
KEYPAD8 = {  # digit -> button position on the security office east wall (x=50), facing west
    1: (49, 53, 20), 2: (49, 53, 21), 3: (49, 53, 22),
    4: (49, 52, 20), 5: (49, 52, 21), 6: (49, 52, 22),
    7: (49, 51, 20), 8: (49, 51, 21), 9: (49, 51, 22),
}
KEYPAD8_ZERO = (49, 51, 23)
KEYPAD8_SIGN = (49, 53, 23)
CODE = "0214"
PHONE = (46, 52, 4)                   # cafeteria north wall, facing south
TAPE_HALE1 = (22, 52, 30)             # specimen room desk (button on top of the recorder)
TAPE_HALE2 = (31, 42, 10)
TAPE_MARSH = (11, 42, 1)
BATTERIES = [(30.5, 52, 2.5), (46.5, 52.1, 12.5), (23.5, 52.1, 20.5),       # B8: dorm D, cafeteria, lab
             (26.5, 42.1, 5.5), (44.5, 41.2, 9.5), (11.5, 42.1, 16.5)]      # B9: records, lockers, office
KIT_BATTERY = 1

B9_ARRIVE = (9.0, 41, 22.5)
KEYCARD_AT = (18.5, 42.05, 11.5)
FUSE_AT = (31.5, 41.1, 27.5)
KEYPAD9 = (28, 42, 20)
KEYPAD9_SIGN = (28, 43, 20)
LEVER = (53, 42, 20)
GEN_SIGN = (53, 43, 20)
CELL_SPOT = (31.5, 41, 29.5)
MARSH_BODY = (13.3, 41, 0.7)

# Checkpoints (x y z yaw)
CP_B8 = (8.5, 51, 19.5, -90)
CP_B9 = (9.0, 41, 20.0, -90)
CP_CONTAIN = (31.0, 41, 20.0, 0)
CP_GEN = (58.5, 41, 24.5, 0)

# Chase
HUNTER_BREACH = (49.5, 41, 20.0)
COLLAPSE = ((38, 51, 16), (43, 53, 17))
COLLAPSE_TRIGGER = ((46, 51, 16), (52, 53, 17))
DEADEND_BOX = ((47, 41, 34), (52, 43, 35))


def expanded(box, floor, ceil):
    (x1, y1, z1), (x2, y2, z2) = box
    return (x1 - 1, y1 - 1, z1 - 1), (x2 + 1, y2 + 1, z2 + 1)


def inside(p, box):
    (x1, y1, z1), (x2, y2, z2) = box
    return x1 <= p[0] <= x2 and y1 <= p[1] <= y2 and z1 <= p[2] <= z2


# =========================================================================
# CREATURE GRAPH: nodes on walkable centre lines, feet height
# =========================================================================
NODES = {
    # B9 main corridor
    "c09": (9.0, 41, 20.0), "c15": (15.5, 41, 20.0), "c21": (21.5, 41, 20.0), "c27": (27.5, 41, 20.0),
    "c31": (31.0, 41, 20.0), "c37": (37.5, 41, 20.0), "c43": (43.5, 41, 20.0), "c48": (48.0, 41, 20.0),
    # stairs (main)
    "s9b": (9.0, 41, 22.5), "sAt": (9.0, 46, 28.5), "sL": (10.5, 46, 30.5), "sBb": (12.0, 46, 29.5), "sBt": (12.0, 51, 23.5),
    "s8x": (12.0, 51, 21.0),
    # office + washroom
    "ofd": (15.5, 41, 18.4), "ofc": (15.5, 41, 15.0), "ofe": (19.5, 41, 13.5), "ofx": (21.6, 41, 13.5),
    "wa": (12.5, 41, 10.5), "wac": (12.5, 41, 8.3),
    # north corridor and its rooms
    "n23": (23.0, 41, 13.0), "n28": (28.5, 41, 13.0), "n34": (34.5, 41, 13.0), "n40": (40.5, 41, 13.0),
    "n46": (46.5, 41, 13.0), "n53": (53.0, 41, 13.0),
    "recd": (28.5, 41, 11.3), "recc": (28.5, 41, 8.0), "lkd": (41.0, 41, 11.3), "lkc": (41.0, 41, 7.5),
    # generator
    "gw": (49.6, 41, 20.0), "gnd": (53.0, 41, 14.6), "gnw": (52.0, 41, 16.5), "gne": (58.5, 41, 16.5),
    "gsw": (52.0, 41, 23.5), "gs": (59.0, 41, 24.0), "gsd": (59.0, 41, 26.5),
    # containment
    "kd": (31.0, 41, 21.5), "ki": (31.0, 41, 23.5), "kc": (31.5, 41, 27.5), "kw": (27.5, 41, 27.0), "ke": (35.0, 41, 27.0),
    # tunnels
    "t1n": (59.0, 41, 28.5), "t1s": (59.0, 41, 35.0), "t2e": (55.0, 41, 35.0), "t2d": (48.5, 41, 35.0),
    "ssb": (59.0, 41, 35.5), "sst": (59.0, 51, 45.5),
    # B8 service
    "se8": (59.0, 51, 47.0), "sew": (52.0, 51, 47.0), "sc40": (52.0, 51, 40.0), "sc30": (52.0, 51, 30.0),
    "sc20": (52.0, 51, 20.0),
    # B8 hall
    "h51": (51.5, 51, 17.0), "h47": (47.5, 51, 17.0), "h45": (45.0, 51, 17.0), "h41": (41.0, 51, 17.0),
    "h37": (37.0, 51, 17.0), "h31": (31.0, 51, 17.0), "h27": (27.0, 51, 17.0), "h25": (25.0, 51, 17.0),
    "h21": (21.0, 51, 17.0),
    # B8 rooms
    "cfd2": (45.0, 51, 14.6), "cf2": (45.0, 51, 11.0), "cf1": (37.0, 51, 11.0), "cfd1": (37.0, 51, 14.6),
    "lbe": (19.0, 51, 17.0), "lbc": (13.0, 51, 17.5), "lbg": (8.0, 51, 19.8),
    "dcs": (25.0, 51, 13.5), "dcn": (25.0, 51, 4.0),
    "labd": (27.0, 51, 18.4), "labc": (27.0, 51, 22.0),
    "cmd": (38.5, 51, 18.4), "cmc": (38.5, 51, 22.0), "sed": (47.5, 51, 18.4), "sec": (47.5, 51, 21.0),
}

# (a, b, door) : door is None (always open) or the name of a state flag
EDGES = [
    ("c09", "c15"), ("c15", "c21"), ("c21", "c27"), ("c27", "c31"), ("c31", "c37"), ("c37", "c43"), ("c43", "c48"),
    ("c09", "s9b"), ("s9b", "sAt"), ("sAt", "sL"), ("sL", "sBb"), ("sBb", "sBt"), ("sBt", "s8x", "stairs8"), ("s8x", "lbc"),
    ("c15", "ofd"), ("ofd", "ofc"), ("ofc", "ofe"), ("ofe", "ofx"), ("ofx", "n23"), ("ofc", "wa"), ("wa", "wac"),
    ("n23", "n28"), ("n28", "n34"), ("n34", "n40"), ("n40", "n46"), ("n46", "n53"),
    ("n28", "recd"), ("recd", "recc"), ("n40", "lkd"), ("lkd", "lkc"),
    ("n53", "gnd", "gen_n"), ("gnd", "gnw"),
    ("c48", "gw", "gen_w"), ("gw", "gnw"), ("gw", "gsw"), ("gnw", "gne"), ("gne", "gs"), ("gsw", "gs"),
    ("c31", "kd", "contain_n"), ("kd", "ki"), ("ki", "kc"), ("ki", "kw"), ("ki", "ke"), ("kw", "kc"), ("ke", "kc"),
    ("gs", "gsd", "gen_s"), ("gsd", "t1n"), ("t1n", "t1s"), ("t1s", "t2e"), ("t2e", "t2d"),
    ("t1s", "ssb"), ("ssb", "sst"), ("sst", "se8"), ("se8", "sew"), ("sew", "sc40"), ("sc40", "sc30"), ("sc30", "sc20"),
    ("sc20", "h51"),
    ("h51", "h47"), ("h47", "h45"), ("h45", "h41", "hall_mid"), ("h41", "h37", "hall_mid"), ("h37", "h31"), ("h31", "h27"),
    ("h27", "h25"), ("h25", "h21"), ("h21", "lbe"), ("lbe", "lbc"), ("lbc", "lbg"),
    ("h45", "cfd2"), ("cfd2", "cf2"), ("cf2", "cf1"), ("cf1", "cfd1"), ("cfd1", "h37"),
    ("h25", "dcs"), ("dcs", "dcn"), ("h27", "labd"), ("labd", "labc"), ("h37", "cmd"), ("cmd", "cmc"),
    ("h47", "sed"), ("sed", "sec"),
]

# Which doors are open in each routing table
TABLES = {
    0: {"stairs8", "gen_n", "gen_w", "hall_mid"},                                   # B9, containment still locked
    1: {"stairs8", "gen_n", "gen_w", "hall_mid", "contain_n"},                      # containment open
    2: {"stairs8", "gen_w", "contain_n", "gen_s", "hall_mid"},                      # the escape
    3: {"stairs8", "gen_w", "contain_n", "gen_s"},                                  # the escape, hall collapsed
}

# Where it wanders when it has nothing better to do (B9 only)
ROAM = ["c15", "c27", "c37", "c48", "ofc", "wac", "n28", "n40", "n53", "recc", "lkc", "gnw", "gs", "c09"]
ROAM_CONTAINED = ["ki", "kc", "kw", "ke"]
