"""Everything that places blocks. Each build step is its own function so a restart can
spread the rebuild over several ticks."""
import math
import random

from . import world as W
from .mc import (book, call, door, fill, fn, lectern, setblock, sign, snbt, txt)

rng = random.Random(9)
STEPS = []          # build functions in order; reset runs one per tick


def step(name, *lines):
    fn(f"build/{name}", *lines)
    STEPS.append(f"build/{name}")


def lamp(name, on):
    return setblock(W.LAMPS[name], f"minecraft:redstone_lamp[lit={'true' if on else 'false'}]")


def stairs(p, block, facing, half="bottom", shape="straight"):
    return setblock(p, f"minecraft:{block}[facing={facing},half={half},shape={shape}]")


def slab(p, block, kind="top"):
    return setblock(p, f"minecraft:{block}[type={kind}]")


def button(p, facing, face="wall", kind="stone"):
    return setblock(p, f"minecraft:{kind}_button[face={face},facing={facing}]")


def bars(a, b, axis):
    st = "north=true,south=true" if axis == "z" else "east=true,west=true"
    return fill(a, b, f"minecraft:iron_bars[{st}]")


# =========================================================================
# UNDERGROUND
# =========================================================================
def wall_owner(rooms, openings):
    owner = {}

    def interior(p):
        return any(W.inside(p, r["box"]) for r in rooms.values())

    def opening(p):
        return any(W.inside(p, box) for box, _ in openings.values())

    for name, r in rooms.items():
        (x1, y1, z1), (x2, y2, z2) = r["box"]
        for y in range(y1, y2 + 1):
            for x in range(x1 - 1, x2 + 2):
                for z in range(z1 - 1, z2 + 2):
                    if x in (x1 - 1, x2 + 1) or z in (z1 - 1, z2 + 1):
                        p = (x, y, z)
                        if not interior(p) and not opening(p):
                            owner[p] = name
    return owner


OWN9 = wall_owner(W.B9, W.B9_OPEN)
OWN8 = wall_owner(W.B8, W.B8_OPEN)
LOCKER_CELLS = {p for p, _ in W.LOCKERS} | {(x, y + 1, z) for (x, y, z), _ in W.LOCKERS}

CHASE_ROOMS = {"generator": (43,), "tunnel1": (43,), "tunnel2": (43,), "service": (45, 50),
               "servicec": (53,), "servicee": (53,), "hall": (53,), "cafeteria": (53,), "lobby": (53,)}
EMERGENCY = sorted(p for own in (OWN9, OWN8) for p, room in own.items()
                   if room in CHASE_ROOMS and p[1] in CHASE_ROOMS[room] and (p[0] + p[2]) % 5 == 0
                   and p not in LOCKER_CELLS)


def carve(rooms):
    """Walls of every room first, then every interior, so an interior always wins."""
    out = []
    for name, r in rooms.items():
        (x1, y1, z1), (x2, y2, z2) = r["box"]
        out += fill((x1 - 1, y1 - 1, z1 - 1), (x2 + 1, y2 + 1, z2 + 1), f"minecraft:{r['wall']}")
        out += fill((x1 - 1, y1, z1 - 1), (x2 + 1, y1, z2 + 1), f"minecraft:{r['accent']}")
    air = []
    for name, r in rooms.items():
        (x1, y1, z1), (x2, y2, z2) = r["box"]
        air += fill((x1, y1, z1), (x2, y2, z2), "minecraft:air")
        air += fill((x1, y1 - 1, z1), (x2, y1 - 1, z2), f"minecraft:{r['floor']}")
        air += fill((x1, y2 + 1, z1), (x2, y2 + 1, z2), f"minecraft:{r['ceil']}")
    return out, air


def wear(rooms, owner):
    out = []
    for p, room in sorted(owner.items()):
        if p in LOCKER_CELLS:
            continue
        for block, chance in rooms[room].get("wall_scatter", []):
            if rng.random() < chance:
                out.append(setblock(p, f"minecraft:{block}"))
                break
    for name, r in rooms.items():
        (x1, y1, z1), (x2, _, z2) = r["box"]
        for block, chance in r.get("floor_scatter", []):
            for x in range(x1, x2 + 1):
                for z in range(z1, z2 + 1):
                    if rng.random() < chance:
                        out.append(setblock((x, y1 - 1, z), f"minecraft:{block}"))
    return out


def openings(table):
    return [fill(a, b, f"minecraft:{block}") for (a, b), block in table.values()]


def all_doors():
    out = []
    for name, (p, facing, hinge, wood) in W.DOORS.items():
        out += door(p, facing, wood=wood, hinge=hinge)
    return out


def locker_doors():
    out = []
    for p, facing in W.LOCKERS:
        out += door(p, facing, wood="warped", hinge="left")
    return out


def cage(y0, level):
    """The lift cage interior details; identical at the surface and on B8."""
    f = y0 - 1   # floor block
    return [
        fill((1, f, 17), (6, f + 4, 22), "minecraft:waxed_oxidized_copper"),
        fill((1, f + 1, 17), (6, f + 1, 22), "minecraft:waxed_oxidized_cut_copper"),
        fill((2, y0, 18), (5, y0 + 2, 21), "minecraft:air"),
        fill((2, f, 18), (5, f, 21), "minecraft:waxed_weathered_cut_copper"),
        fill((2, f + 4, 18), (5, f + 4, 21), "minecraft:waxed_oxidized_cut_copper"),
        fill((6, y0, 19), (6, y0 + 2, 20), "minecraft:iron_block"),
        setblock((2, f, 18), "minecraft:waxed_oxidized_cut_copper"), setblock((5, f, 21), "minecraft:waxed_oxidized_cut_copper"),
        button((3, y0 + 1, 18), "south"),
        sign((3, y0 + 2, 18), "south", ["", "v  B9", "", ""], color="white", glow=True),
        sign((4, y0 + 1, 18), "south", ["LIFT 2", "B1 - B9", "", "MAX LOAD 1"], color="white"),
        setblock((5, y0 + 1, 18), "minecraft:lever[face=wall,facing=south,powered=false]"),
        sign((5, y0 + 2, 18), "south", ["CAGE", "LIGHT", "", ""], color="white"),
        button((2, y0 + 1, 19), "east", kind="polished_blackstone"),
        sign((2, y0 + 2, 19), "east", ["DOOR", "RELEASE", "", ""], color="red", glow=True),
        setblock((2, y0 + 2, 21), "minecraft:cobweb"),
        setblock((5, y0, 21), "minecraft:chain[axis=y]"),
        setblock((4, f + 4, 20), "minecraft:redstone_lamp[lit=false]"),
    ]


def main_stairs():
    """Two flights between B9 (y41) and B8 (y51) with a landing at y46."""
    out = ["# main stairwell: lane A x8-9 climbs south, landing, lane B x11-12 climbs north",
           fill((10, 41, 22), (10, 53, 28), "minecraft:polished_deepslate"),        # divider
           fill((11, 41, 22), (12, 45, 31), "minecraft:deepslate_tiles"),           # under lane B
           fill((8, 41, 29), (12, 44, 31), "minecraft:deepslate_tiles"),            # under the landing
           fill((8, 45, 29), (12, 45, 31), "minecraft:polished_deepslate")]         # landing floor (walk y46)
    for k in range(1, 6):
        z = 23 + k
        out += fill((8, 41, z), (9, 40 + k - 1, z), "minecraft:deepslate_tiles") if k > 1 else []
        out += fill((8, 40 + k, z), (9, 40 + k, z), "minecraft:polished_deepslate_stairs[facing=south]")
    for k in range(1, 6):
        z = 29 - k
        out += fill((11, 41, z), (12, 45 + k - 1, z), "minecraft:deepslate_tiles")
        out += fill((11, 45 + k, z), (12, 45 + k, z), "minecraft:polished_deepslate_stairs[facing=north]")
    out += [fill((11, 41, 22), (12, 49, 23), "minecraft:deepslate_tiles"),
            fill((11, 50, 22), (12, 50, 23), "minecraft:polished_deepslate"),        # B8 landing (walk y51)
            sign((8, 44, 22), "south", ["", "B8  ^", "", ""], color="white"),
            sign((12, 53, 23), "west", ["", "B9  v", "", ""], color="white"),
            sign((9, 48, 31), "north", ["", "LEVEL B8-B9", "STAIRWELL B", ""], color="white"),
            setblock((12, 49, 31), "minecraft:cobweb"), setblock((8, 53, 22), "minecraft:cobweb")]
    return out


def service_stairs():
    out = ["# service stairs: a straight flight south from tunnel 1 (y41) to B8 (y51)"]
    for k in range(1, 11):
        z = 35 + k
        if k > 1:
            out += fill((58, 41, z), (59, 40 + k - 1, z), "minecraft:waxed_exposed_cut_copper")
        out += fill((58, 40 + k, z), (59, 40 + k, z), "minecraft:waxed_cut_copper_stairs[facing=south]")
    out += [fill((58, 41, 46), (59, 49, 47), "minecraft:waxed_exposed_cut_copper"),
            fill((58, 50, 46), (59, 50, 47), "minecraft:waxed_exposed_cut_copper"),
            sign((57, 43, 35), "south", ["SERVICE", "STAIRS", "B8  ^", ""], color="white"),
            sign((57, 53, 47), "north", ["", "SERVICE", "CORRIDOR  <", ""], color="white")]
    return out


def b9_details():
    d = []
    # --- corridor -------------------------------------------------------------
    d += ["# B9 corridor",
          sign((10, 42, 20), "north", ["OFFICES  >", "CONTAINMENT  >", "GENERATOR B  >", ""], color="white"),
          sign((15, 43, 19), "south", ["", "OFFICE 9-A", "", ""], color="white"),
          sign((32, 43, 20), "north", ["CONTAINMENT", "B9", "SUBJECT 9", ""], color="red", glow=True),
          button(W.KEYPAD9, "north"),
          sign(W.KEYPAD9_SIGN, "north", ["KEYCARD", "LEVEL 3", "", ""], color="yellow", glow=True),
          sign((47, 43, 19), "south", ["", "GENERATOR B", ">>>", ""], color="white"),
          sign((7, 43, 19), "east", ["", "LIFT 2", "OUT OF", "SERVICE"], color="white"),
          setblock((14, 41, 19), "minecraft:candle[candles=4,lit=false]"),
          setblock((17, 41, 19), "minecraft:white_candle[candles=2,lit=false]"),
          setblock((39, 44, 20), "minecraft:air"), setblock((39, 45, 20), "minecraft:air"),
          setblock((38, 41, 20), "minecraft:cobbled_deepslate"),
          setblock((39, 41, 20), "minecraft:cobbled_deepslate_slab[type=bottom]"),
          setblock((40, 41, 20), "minecraft:cobbled_deepslate_stairs[facing=west]"),
          setblock((47, 43, 20), "minecraft:cobweb"), setblock((48, 43, 19), "minecraft:cobweb")]
    d += [setblock(p, "minecraft:redstone_wire") for p in
          [(31, 41, 20), (30, 41, 20), (29, 41, 19), (27, 41, 19), (26, 41, 19), (24, 41, 20)]]

    # --- office 9-A (kept clear on the lines the creature walks) ----------------
    d += ["# Office 9-A",
          fill((16, 41, 11), (19, 41, 11), "minecraft:dark_oak_slab[type=top]"),
          setblock((17, 41, 12), "minecraft:dark_oak_stairs[facing=south]"),
          setblock((19, 42, 11), "minecraft:white_carpet"),
          fill((10, 41, 12), (10, 42, 13), "minecraft:bookshelf"),
          setblock((10, 41, 15), "minecraft:barrel[facing=east]"), setblock((10, 41, 16), "minecraft:barrel[facing=east]"),
          setblock((10, 42, 16), "minecraft:barrel[facing=up]"), setblock((11, 41, 16), "minecraft:barrel[facing=up]"),
          setblock((12, 41, 15), "minecraft:white_carpet"), setblock((18, 41, 16), "minecraft:white_carpet"),
          setblock((20, 43, 11), "minecraft:cobweb"), setblock((10, 43, 17), "minecraft:cobweb"),
          fill((20, 41, 16), (20, 41, 17), "minecraft:dark_oak_slab[type=top]"),
          setblock((20, 42, 16), "minecraft:flower_pot"),
          sign((20, 43, 15), "west", ["IT MOVES", "WHEN THE", "LIGHTS", "GO OUT"], color="red", glow=True),
          lectern((13, 41, 16), "south", "Night Log", "Dr. E. Hale", [
              "NIGHT LOG\nDr. E. Hale\nStation 9 - Level B9\n\nIf you are reading this, the power is still out.\n\nDo not trust the dark.",
              "Day 112\nSubject 9 has stopped eating. It stands at the glass all day, facing the office.\n\nFacing us.",
              "Day 115\nPower dip at 02:14. The cell field dropped for less than a second.\n\nWhen the lights came back, it was pressed against the glass. It had been at the back wall.",
              "Day 118\nMarsh says it only moves in the dark. I told him to get some sleep.\n\nDay 121\nMarsh is gone. His keycard was on my desk this morning.\n\nI did not put it there.",
              "Day 122\nThe mirrors stopped showing us.\n\nOnly it.\n\nThe generator is failing. If it dies, the cell opens.",
          ]),
          setblock((16, 42, 11), "minecraft:candle[candles=3,lit=false]"),
          setblock((11, 41, 11), "minecraft:white_candle[candles=4,lit=false]")]

    # --- washroom and the room behind the mirror -----------------------------------
    d += ["# Washroom + the room behind the mirror",
          setblock((11, 41, 7), "minecraft:cauldron"), setblock((13, 41, 7), "minecraft:cauldron"),
          setblock((11, 41, 5), "minecraft:cauldron"), setblock((13, 41, 5), "minecraft:cauldron"),
          fill((10, 41, 0), (10, 42, 0), "minecraft:bookshelf"),
          setblock((14, 41, 0), "minecraft:barrel[facing=up]"),
          setblock((10, 41, 1), "minecraft:redstone_wire"), setblock((11, 41, 2), "minecraft:redstone_wire"),
          setblock((11, 41, 1), "minecraft:smooth_basalt"), button((11, 42, 1), "north", face="floor", kind="polished_blackstone"),
          sign((11, 43, 0), "south", ["M. MARSH", "(recorder)", "", "PRESS PLAY"], color="white"),
          setblock((12, 43, 0), "minecraft:cobweb"), setblock((14, 43, 1), "minecraft:cobweb")]

    # --- records ---------------------------------------------------------------------------
    d += ["# Records",
          fill((25, 41, 5), (25, 42, 9), "minecraft:bookshelf"), fill((32, 41, 5), (32, 42, 7), "minecraft:bookshelf"),
          setblock((26, 41, 5), "minecraft:barrel[facing=up]"), setblock((27, 41, 5), "minecraft:barrel[facing=up]"),
          setblock((29, 41, 5), "minecraft:barrel[facing=south]"), setblock((29, 42, 5), "minecraft:barrel[facing=south]"),
          setblock((31, 41, 10), "minecraft:smooth_basalt"), button((31, 42, 10), "north", face="floor", kind="polished_blackstone"),
          sign((32, 42, 10), "west", ["DR. E. HALE", "(recorder)", "", "PRESS PLAY"], color="white"),
          fill((30, 41, 8), (31, 41, 8), "minecraft:spruce_slab[type=top]"),
          setblock((30, 42, 8), "minecraft:white_carpet"),
          lectern((27, 41, 9), "east", "Incident 41", "Station 9", [
              "INCIDENT 41\nGenerator B failure\n\n00:52  Generator B trips.\n00:52  Backup at 30%.\n00:53  Cell field OFFLINE.",
              "00:58  B9 staff report the containment door open.\n\n01:03  Lift 2 called to B9.\n\n01:04  Lift 2 arrives at the surface EMPTY.",
              "01:10  All B9 staff unaccounted for.\n\n01:11  Site evacuated.\n\nRecovery pending main power.",
          ]),
          setblock((32, 43, 5), "minecraft:cobweb")]

    # --- staff locker room ---------------------------------------------------------------------
    d += ["# Staff locker room",
          sign((38, 43, 10), "north", ["", "STAFF", "LOCKERS", ""], color="white"),
          fill((38, 41, 7), (43, 41, 7), "minecraft:spruce_slab[type=bottom]"),
          fill((44, 41, 9), (45, 41, 9), "minecraft:spruce_slab[type=bottom]"),
          setblock((36, 41, 10), "minecraft:barrel[facing=up]"), setblock((45, 41, 5), "minecraft:cauldron"),
          sign((40, 42, 5), "south", ["", "MARSH  M.", "", ""], color="black"),
          setblock((36, 43, 5), "minecraft:cobweb")]

    # --- north corridor --------------------------------------------------------------------------
    d += ["# North corridor",
          sign((22, 43, 13), "east", ["GENERATOR B >", "RECORDS >", "LOCKERS >", ""], color="white"),
          sign((53, 43, 12), "west", ["", "GENERATOR B", "v", ""], color="white"),
          setblock((31, 41, 12), "minecraft:cobbled_deepslate_slab[type=bottom]"),
          setblock((50, 43, 13), "minecraft:cobweb")]

    # --- containment ------------------------------------------------------------------------------
    cell = [fill((28, 41, 25), (34, 43, 25), "minecraft:glass"),
            fill((28, 41, 26), (28, 43, 30), "minecraft:glass"),
            fill((34, 41, 26), (34, 43, 30), "minecraft:glass"),
            fill((31, 41, 25), (31, 43, 25), "minecraft:air"),       # torn open from the inside
            setblock((30, 43, 25), "minecraft:air"), setblock((32, 41, 25), "minecraft:air")]
    claws = [setblock((x, y, 31), "minecraft:cracked_deepslate_tiles")
             for x, y in [(29, 42), (29, 43), (30, 41), (30, 42), (32, 42), (32, 43), (33, 41), (33, 42)]]
    d += ["# Containment B9", cell, claws,
          setblock((30, 43, 29), "minecraft:chain[axis=y]"), setblock((32, 43, 29), "minecraft:chain[axis=y]"),
          setblock((32, 42, 29), "minecraft:chain[axis=y]"),
          setblock((29, 43, 30), "minecraft:glow_lichen[south=true]"),
          setblock((33, 42, 30), "minecraft:glow_lichen[south=true]"),
          fill((29, 40, 26), (33, 40, 30), "minecraft:sculk", "replace minecraft:polished_blackstone"),
          fill((26, 41, 24), (26, 41, 26), "minecraft:polished_deepslate_slab[type=top]"),
          sign((32, 42, 22), "south", ["", "<<  EXIT", "", ""], color="white"),
          lectern((27, 41, 23), "east", "Subject 9", "Containment", [
              "SUBJECT 9\nContainment protocol\n\nClass: UNKNOWN\nHeight: 2.4 m\nDiet: none observed\nSleep: none observed",
              "1. Keep the lights on.\n\n2. Never look away from it in the dark.\n\n3. If the field fails, do NOT restore main power without a clear exit.",
              "(handwritten)\n\nIt isn't afraid of the light.\n\nIt just can't SEE in the dark.\n\nThe generator turns every light on at once.",
              "It will see you.\n\n- Marsh",
          ])]
    d += [setblock(p, "minecraft:redstone_wire") for p in [(31, 41, 26), (31, 41, 24), (31, 41, 23), (30, 41, 22)]]

    # --- generator B ------------------------------------------------------------------------------
    d += ["# Generator B",
          fill((54, 41, 18), (56, 43, 22), "minecraft:iron_block"),
          fill((54, 41, 18), (56, 41, 22), "minecraft:polished_deepslate"),
          setblock((54, 43, 19), "minecraft:blast_furnace[facing=west]"),
          setblock((54, 43, 21), "minecraft:blast_furnace[facing=west]"),
          setblock((54, 42, 18), "minecraft:observer[facing=west]"),
          setblock((54, 42, 22), "minecraft:observer[facing=west]"),
          setblock(W.LEVER, "minecraft:lever[face=wall,facing=west]"),
          sign(W.GEN_SIGN, "west", ["GENERATOR B", "FUSE: MISSING", "", "PULL TO START"], color="red", glow=True),
          setblock((50, 41, 15), "minecraft:barrel[facing=up]"), setblock((51, 41, 15), "minecraft:barrel[facing=up]"),
          setblock((50, 42, 15), "minecraft:barrel[facing=south]"),
          setblock((60, 41, 15), "minecraft:chipped_anvil[facing=north]"),
          setblock((60, 41, 16), "minecraft:grindstone[face=floor,facing=north]"),
          setblock((50, 41, 25), "minecraft:cauldron"),
          sign((57, 43, 25), "north", ["MAINTENANCE", "TUNNEL", "vvv", ""], color="white"),
          setblock((60, 43, 25), "minecraft:cobweb")]

    # --- tunnels -----------------------------------------------------------------------------------
    d += ["# Maintenance tunnels",
          setblock((59, 44, 28), "minecraft:iron_bars"),
          sign((58, 43, 33), "east", ["", "LIFT  <<<", "(via B8)", ""], color="white"),
          fill((47, 41, 34), (47, 42, 35), "minecraft:cobbled_deepslate"),
          setblock((47, 43, 35), "minecraft:gravel"), setblock((48, 41, 35), "minecraft:cobbled_deepslate_stairs[facing=east]"),
          setblock((48, 41, 34), "minecraft:gravel"), setblock((47, 43, 34), "minecraft:cobbled_deepslate"),
          sign((50, 43, 34), "south", ["", "TUNNEL 2", "COLLAPSED", ""], color="red", glow=True)]

    d += main_stairs() + service_stairs()
    return d


def b8_details():
    d = []
    # --- lobby -----------------------------------------------------------------------------------------
    d += ["# B8 lobby",
          fill((14, 51, 14), (17, 51, 14), "minecraft:quartz_slab[type=top]"),
          setblock((14, 51, 15), "minecraft:quartz_stairs[facing=north]"), setblock((17, 51, 15), "minecraft:quartz_stairs[facing=north]"),
          setblock((15, 52, 14), "minecraft:flower_pot"), setblock((16, 51, 15), "minecraft:spruce_stairs[facing=south]"),
          sign((9, 53, 14), "south", ["STATION 9", "LEVEL B8", "STAFF", ""], color="white", glow=True),
          sign((10, 52, 14), "south", ["DORMS    ^", "CAFETERIA  >", "LAB  COMMS  >", "SECURITY  >"], color="white"),
          sign((11, 52, 14), "south", ["STAIRWELL B", "B9  v", "(beside you)", ""], color="white"),
          fill((7, 51, 14), (7, 51, 16), "minecraft:light_blue_terracotta"),
          stairs((8, 51, 14), "quartz_stairs", "south"), stairs((8, 51, 15), "quartz_stairs", "south"),
          setblock((20, 51, 14), "minecraft:potted_dead_bush"), setblock((7, 51, 20), "minecraft:potted_dead_bush"),
          sign((13, 53, 20), "north", ["STAIRWELL B", "LOCKDOWN", "OVERRIDE AT", "SECURITY"], color="red", glow=True),
          button(W.STAIR_BUTTON8, "north"),
          sign((7, 53, 19), "east", ["", "LIFT 2", "", ""], color="white"),
          setblock((20, 53, 20), "minecraft:cobweb")]

    # --- dormitories -------------------------------------------------------------------------------------
    d += ["# Dormitory hall",
          sign((23, 53, 16), "south", ["", "DORMITORIES", "", ""], color="white"),
          sign((24, 53, 11), "east", ["", "A - HALE", "", ""], color="white"),
          sign((24, 53, 4), "east", ["", "B - VACANT", "", ""], color="white"),
          sign((25, 53, 11), "west", ["", "C - OKAFOR", "", ""], color="white"),
          sign((25, 53, 4), "west", ["", "D - MARSH", "", ""], color="white"),
          setblock((25, 51, 1), "minecraft:potted_dead_bush")]

    def dorm(x0, z0, name):
        # x0,z0 = north-west interior corner; rooms are 5x5
        return [setblock((x0, 51, z0 + 1), "minecraft:white_bed[facing=north,part=head]"),
                setblock((x0, 51, z0 + 2), "minecraft:white_bed[facing=north,part=foot]"),
                setblock((x0 + 4, 51, z0), "minecraft:spruce_slab[type=top]"),
                setblock((x0 + 3, 51, z0), "minecraft:barrel[facing=up]"),
                setblock((x0, 51, z0 + 4), "minecraft:spruce_stairs[facing=east]"),
                setblock((x0, 53, z0), "minecraft:cobweb")]

    # A: Hale's room. Something lies under the sheet.
    d += ["# Dorm A (Hale)",
          fill((19, 51, 9), (19, 51, 10), "minecraft:white_wool"),
          fill((18, 51, 9), (18, 51, 10), "minecraft:spruce_slab[type=bottom]"),
          setblock((19, 52, 9), "minecraft:snow[layers=4]"), setblock((19, 52, 10), "minecraft:snow[layers=3]"),
          setblock((22, 51, 8), "minecraft:spruce_slab[type=top]"), setblock((21, 51, 8), "minecraft:barrel[facing=up]"),
          sign((18, 53, 12), "north", ["", "(a photo of", "a dog)", ""], color="black"),
          setblock((22, 53, 12), "minecraft:cobweb")]
    # B: barricaded from the inside
    d += ["# Dorm B (barricaded)",
          dorm(18, 1, "B"),
          setblock((22, 51, 3), "minecraft:barrel[facing=west]"), setblock((22, 52, 3), "minecraft:barrel[facing=west]"),
          setblock((22, 51, 2), "minecraft:crafting_table"), setblock((22, 51, 4), "minecraft:bookshelf"),
          setblock((23, 52, 4), "minecraft:glass_pane[north=true,south=true]"),
          sign((19, 52, 5), "north", ["IIII IIII IIII", "IIII IIII IIII", "IIII IIII IIII", "IIII IIII I"], color="black"),
          sign((18, 52, 3), "east", ["IT STANDS", "WHERE THE", "LIGHT", "ENDS"], color="black"),
          sign((20, 52, 1), "south", ["DON'T", "OPEN", "THE", "DOOR"], color="black")]
    # C: Okafor's room: the code clue
    d += ["# Dorm C (Okafor)",
          dorm(27, 8, "C"),
          lectern((31, 51, 10), "west", "Note", "R. Okafor", [
              "Changed the stairwell override again.\n\nHale's rule now: the code is the TIME the first power dip happened.\n\n24 hour clock, four digits.",
              "No more sticky notes on the panel.\n\nIf you forgot, Hale's recordings are in the lab.\n\n- R. Okafor, Security",
          ])]
    # D: Marsh's room
    d += ["# Dorm D (Marsh)",
          dorm(27, 1, "D"),
          setblock((30, 51, 2), "minecraft:spruce_slab[type=top]"),
          sign((31, 52, 3), "west", ["41 DAYS", "", "WHERE", "ARE YOU"], color="black"),
          setblock((27, 52, 5), "minecraft:potted_dead_bush")]

    # --- cafeteria + kitchen --------------------------------------------------------------------------
    tables = []
    for tx, tz in [(39, 5), (42, 5), (39, 8), (42, 8), (39, 13), (42, 13)]:
        tables += [fill((tx, 51, tz), (tx + 1, 51, tz), "minecraft:spruce_slab[type=top]"),
                   stairs((tx, 51, tz + 1 if tz < 13 else tz - 1), "spruce_stairs", "north" if tz < 13 else "south")]
    d += ["# Cafeteria", tables,
          fill((34, 51, 4), (34, 51, 12), "minecraft:quartz_slab[type=top]"),
          setblock((46, 51, 12), "minecraft:quartz_slab[type=top]"), setblock((47, 51, 12), "minecraft:quartz_slab[type=top]"),
          fill((47, 51, 5), (47, 52, 6), "minecraft:red_concrete"), setblock((47, 53, 5), "minecraft:glass"),
          sign((46, 52, 6), "west", ["VENDING", "", "OUT OF", "ORDER"], color="white"),
          button(W.PHONE, "south"),
          sign((46, 53, 4), "south", ["PHONE", "EXT 9-114", "", ""], color="white"),
          stairs((44, 51, 6), "spruce_stairs", "east", half="top"),
          sign((35, 53, 4), "south", ["", "KITCHEN", "^", ""], color="white"),
          setblock((47, 53, 14), "minecraft:cobweb")]
    d += ["# Kitchen",
          fill((35, 51, -2), (36, 53, -2), "minecraft:iron_block"),
          setblock((36, 52, -1), "minecraft:air"), setblock((36, 51, -1), "minecraft:iron_block"),
          setblock((38, 51, -2), "minecraft:smoker[facing=south]"), setblock((39, 51, -2), "minecraft:furnace[facing=south]"),
          setblock((40, 51, -2), "minecraft:cauldron"),
          stairs((38, 51, 0), "spruce_stairs", "south"),
          sign((35, 52, 0), "east", ["FREEZER", "", "KEEP", "CLOSED"], color="white")]

    # --- lab + specimen room ---------------------------------------------------------------------------
    d += ["# Lab",
          fill((22, 51, 19), (22, 51, 25), "minecraft:quartz_slab[type=top]"),
          fill((23, 51, 20), (24, 51, 20), "minecraft:quartz_slab[type=top]"),
          setblock((22, 52, 21), "minecraft:brewing_stand"), setblock((22, 52, 23), "minecraft:brewing_stand"),
          fill((31, 51, 19), (31, 51, 23), "minecraft:quartz_slab[type=top]"),
          setblock((31, 52, 20), "minecraft:end_rod[facing=up]"), setblock((31, 52, 22), "minecraft:flower_pot"),
          sign((24, 53, 19), "south", ["SUBJECT 9", "- no rest -", "- no food -", "- no sleep -"], color="black"),
          sign((29, 53, 19), "south", ["02:14", "!!!", "", ""], color="red"),
          sign((22, 53, 25), "north", ["OBSERVATION", "", "", ""], color="white")]
    d += ["# Specimen room",
          setblock((22, 51, 30), "minecraft:smooth_basalt"),
          button(W.TAPE_HALE1, "north", face="floor", kind="polished_blackstone"),
          sign((22, 52, 29), "east", ["DR. E. HALE", "(recorder)", "", "PRESS PLAY"], color="white"),
          setblock((27, 51, 31), "minecraft:chipped_anvil[facing=east]"),
          setblock((27, 52, 32), "minecraft:chain[axis=y]"), setblock((27, 53, 32), "minecraft:chain[axis=y]"),
          setblock((26, 53, 32), "minecraft:chain[axis=x]"),
          fill((23, 50, 28), (30, 50, 31), "minecraft:sculk", "replace minecraft:polished_blackstone"),
          setblock((31, 53, 27), "minecraft:cobweb")]

    # --- comms ---------------------------------------------------------------------------------------------
    racks = []
    for x in (35, 36, 40, 41):
        for z in range(20, 25):
            if (x, z) == (40, 24) or (x, z) == (41, 24):
                continue
            racks += [setblock((x, 51, z), "minecraft:black_concrete"), setblock((x, 52, z), "minecraft:iron_block"),
                      setblock((x, 53, z), "minecraft:black_concrete")]
    d += ["# Comms", racks,
          setblock(W.RELAY_LEVER, "minecraft:lever[face=wall,facing=north,powered=false]"),
          sign((39, 52, 25), "north", ["COMMS", "RELAY", "RESET", ">>"], color="yellow", glow=True),
          fill((38, 51, 25), (38, 53, 25), "minecraft:iron_block"), fill((41, 51, 25), (41, 53, 25), "minecraft:iron_block")]

    # --- security --------------------------------------------------------------------------------------------
    keypad = [button(p, "west") for p in W.KEYPAD8.values()] + [button(W.KEYPAD8_ZERO, "west")]
    d += ["# Security office", keypad,
          sign(W.KEYPAD8_SIGN, "west", ["STAIR OVERRIDE", "_ _ _ _", "", ""], color="lime", glow=True),
          sign((49, 52, 19), "west", ["1 2 3", "4 5 6", "7 8 9", "  0 >"], color="white"),
          fill((45, 51, 19), (45, 51, 22), "minecraft:gray_concrete"),
          fill((45, 52, 20), (45, 52, 21), "minecraft:black_concrete"),
          sign((46, 52, 20), "east", ["CAM 1", "LOBBY", "", "-NO SIGNAL-"], color="gray", glow=True),
          sign((46, 52, 21), "east", ["CAM 4", "B9 CELL", "", "-NO SIGNAL-"], color="gray", glow=True),
          stairs((46, 51, 21), "spruce_stairs", "west"),
          sign((47, 53, 24), "north", ["DUTY OFFICER", "R. OKAFOR", "", ""], color="white")]

    # --- hall + service corridor -----------------------------------------------------------------------------
    d += ["# Hall",
          sign((22, 53, 17), "north", ["", "HALL B8", "", ""], color="white"),
          sign((50, 52, 17), "north", ["SERVICE STAIRS", "LOCKED", "maintenance", "only"], color="red", glow=True),
          setblock((50, 53, 16), "minecraft:cobweb")]
    d += ["# Service corridor",
          fill((51, 53, 20), (51, 53, 45), "minecraft:polished_basalt[axis=z]"),
          sign((51, 52, 45), "east", ["", "SERVICE", "STAIRS  v", ""], color="white"),
          setblock((52, 53, 33), "minecraft:cobweb")]
    return d


# =========================================================================
# SURFACE
# =========================================================================
def pit_height(x, z):
    """How high the cliffs rise above the ground at column x,z (0 in the yard)."""
    inner = [(-8, 62, -8, 40), (62, 79, 14, 22)]
    d = 99
    for x1, x2, z1, z2 in inner:
        dx = max(x1 - x, 0, x - x2)
        dz = max(z1 - z, 0, z - z2)
        d = min(d, math.hypot(dx, dz))
    if d <= 0:
        return 0
    wobble = 2.5 * math.sin(x * 0.37 + z * 0.11) + 2 * math.sin(z * 0.29 - x * 0.07)
    return int(max(1, min(26, 4 + d * 2.4 + wobble)))


def surface_terrain():
    (xa, za), (xb, zb) = W.FORCELOAD
    out = ["# The pit: bedrock of stone, a muddy yard, cliffs all round",
           fill((xa, 88, za), (xb, 99, zb), "minecraft:stone"),
           fill((xa, 100, za), (xb, 100, zb), "minecraft:coarse_dirt"),
           fill((xa, 101, za), (xb, 140, zb), "minecraft:air")]
    for x in range(xa, xb + 1):
        z = za
        while z <= zb:
            h = pit_height(x, z)
            if h == 0:
                z += 1
                continue
            # merge runs of equal height into one fill
            z2 = z
            while z2 + 1 <= zb and pit_height(x, z2 + 1) == h:
                z2 += 1
            stone = rng.choice(["stone", "stone", "andesite", "tuff", "cobblestone"])
            out += fill((x, 101, z), (x, 100 + h, z2), f"minecraft:{stone}")
            top = rng.choice(["grass_block", "podzol", "coarse_dirt", "grass_block"])
            out += fill((x, 100 + h, z), (x, 100 + h, z2), f"minecraft:{top}")
            z = z2 + 1
    # yard ground texture
    for _ in range(900):
        x, z = rng.randint(-8, 62), rng.randint(-8, 40)
        out.append(setblock((x, 100, z), "minecraft:" + rng.choice(
            ["gravel", "gravel", "mud", "packed_mud", "podzol", "dirt", "rooted_dirt", "mud"])))
    for cx, cz, r in [(30, 10, 2), (48, 30, 3), (20, 2, 2), (55, 12, 2), (10, 34, 2)]:
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                if (x - cx) ** 2 + (z - cz) ** 2 <= r * r:
                    out.append(setblock((x, 100, z), "minecraft:water"))
    # the road: gate -> lift house, with a spur to the hut
    out += fill((13, 100, 17), (79, 100, 21), "minecraft:gravel")
    out += fill((32, 100, 22), (34, 100, 25), "minecraft:gravel")
    for _ in range(80):
        x, z = rng.randint(13, 79), rng.randint(17, 21)
        out.append(setblock((x, 100, z), "minecraft:" + rng.choice(["coarse_dirt", "mud", "packed_mud"])))
    # trees along the cliff tops
    for _ in range(140):
        x, z = rng.randint(xa, xb), rng.randint(za, zb)
        h = pit_height(x, z)
        if h >= 10:
            out += tree(x, 101 + h, z)
    return out


def tree(x, y, z):
    h = rng.randint(6, 10)
    out = fill((x, y, z), (x, y + h - 1, z), "minecraft:spruce_log[axis=y]")
    for k, r in enumerate([2, 2, 1, 2, 1, 1, 0]):
        yy = y + h - 5 + k
        if r:
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if abs(dx) + abs(dz) <= r + (1 if r > 1 else 0) and (dx or dz):
                        out.append(setblock((x + dx, yy, z + dz), "minecraft:spruce_leaves[persistent=true]"))
    out.append(setblock((x, y + h, z), "minecraft:spruce_leaves[persistent=true]"))
    return out


def surface_compound():
    out = ["# Fence line and gate",
           bars((W.FENCE_X, 101, -8), (W.FENCE_X, 102, 15), "z"), bars((W.FENCE_X, 101, 19), (W.FENCE_X, 102, 40), "z"),
           fill((W.FENCE_X, 103, -8), (W.FENCE_X, 103, 40), "minecraft:chain[axis=z]"),
           fill((W.FENCE_X, 103, 16), (W.FENCE_X, 103, 18), "minecraft:air"),
           bars((W.FENCE_X - 1, 101, 19), (W.FENCE_X - 1, 102, 22), "z"),     # the gate, slid open
           fill((W.FENCE_X, 101, 15), (W.FENCE_X, 104, 15), "minecraft:polished_blackstone_wall"),
           fill((W.FENCE_X, 101, 19), (W.FENCE_X, 104, 19), "minecraft:polished_blackstone_wall"),
           sign((W.FENCE_X + 1, 102, 14), "east", ["STATION 9", "SITE ACCESS", "AUTHORISED", "PERSONNEL ONLY"], color="white"),
           sign((W.FENCE_X + 1, 102, 20), "east", ["DANGER", "DEEP SHAFT", "", "HARD HATS"], color="red", glow=True)]

    # the truck you came in, headlights on
    out += ["# Truck",
            fill((71, 101, 17), (76, 101, 19), "minecraft:black_concrete"),
            fill((71, 102, 17), (73, 103, 19), "minecraft:white_concrete"),
            fill((71, 103, 17), (71, 103, 19), "minecraft:black_stained_glass"),
            fill((74, 102, 17), (76, 102, 19), "minecraft:white_concrete"),
            setblock((70, 101, 17), "minecraft:pearlescent_froglight"), setblock((70, 101, 19), "minecraft:pearlescent_froglight"),
            setblock((70, 101, 18), "minecraft:gray_concrete"),
            fill((72, 100, 16), (72, 100, 16), "minecraft:coal_block"), fill((75, 100, 16), (75, 100, 16), "minecraft:coal_block"),
            setblock((68, 101, 18), "minecraft:light[level=11]"), setblock((66, 102, 17), "minecraft:light[level=9]")]

    # security hut
    (x1, y1, z1), (x2, y2, z2) = W.HUT
    out += ["# Security hut",
            fill((x1 - 1, 100, z1 - 1), (x2 + 1, 104, z2 + 1), "minecraft:light_gray_concrete"),
            fill((x1 - 1, 101, z1 - 1), (x2 + 1, 101, z2 + 1), "minecraft:gray_concrete"),
            fill((x1, y1, z1), (x2, y2, z2), "minecraft:air"),
            fill((x1, 100, z1), (x2, 100, z2), "minecraft:spruce_planks"),
            fill((x1 - 2, 105, z1 - 2), (x2 + 2, 105, z2 + 2), "minecraft:dark_oak_slab[type=bottom]"),
            fill((x1, 102, z1 - 1), (x1 + 1, 102, z1 - 1), "minecraft:glass_pane[east=true,west=true]"),
            fill((x2 - 1, 102, z1 - 1), (x2, 102, z1 - 1), "minecraft:glass_pane[east=true,west=true]"),
            fill((x2 + 1, 102, z1 + 1), (x2 + 1, 102, z1 + 3), "minecraft:glass_pane[north=true,south=true]"),
            door(W.HUT_DOOR, "south", wood="spruce"),
            sign((W.HUT_DOOR[0] + 1, 103, W.HUT_DOOR[2] - 1), "north", ["", "SECURITY", "", ""], color="white", glow=True),
            setblock((33, 103, 29), "minecraft:lantern[hanging=true]"),
            # desk + monitor along the back wall
            fill((32, 101, 31), (35, 101, 31), "minecraft:spruce_slab[type=top]"),
            setblock((33, 102, 31), "minecraft:black_concrete"), setblock((34, 102, 31), "minecraft:black_concrete"),
            sign((33, 102, 30), "north", ["CAM 3", "B9", "", "NO SIGNAL"], color="gray", glow=True),
            sign((34, 102, 30), "north", ["CAM 1", "LIFT HOUSE", "", "NO SIGNAL"], color="gray", glow=True),
            stairs((33, 101, 30), "spruce_stairs", "north"),
            # the guard's abandoned dinner
            setblock((35, 102, 31), "minecraft:flower_pot"),
            # coffee machine
            setblock((36, 101, 30), "minecraft:polished_andesite"), setblock((36, 102, 30), "minecraft:brewing_stand"),
            sign((36, 101, 29), "north", ["FRANK'S", "COFFEE", "", "(do not)"], color="black"),
            # sign-in board: east wall
            sign((36, 103, 28), "west", ["SIGN IN / OUT", "NAME  LVL IN OUT", "", ""], color="black"),
            sign((36, 102, 28), "west", ["E.HALE B9 0610 -", "M.MARSH B9 2240 -", "R.OKAFOR B8 1800 -", "J.TAN B9 2300 -"],
                 color="black"),
            sign((36, 102, 27), "west", ["", "", "", ""], color="blue"),
            button((36, 101, 27), "west", kind="spruce"),
            sign((36, 103, 27), "west", ["", "PRESS TO", "SIGN IN", ""], color="black"),
            # gear locker
            setblock(W.KIT_BARREL, "minecraft:barrel[facing=up]{CustomName:'{\"text\":\"Contractor kit\"}'}"),
            sign((31, 102, 31), "north", ["", "CONTRACTOR", "KIT", ""], color="black"),
            setblock((31, 101, 27), "minecraft:barrel[facing=east]"),
            sign((31, 103, 29), "east", ["NOTICE", "Lights ON at", "all times on B9", "- Management"], color="black"),
            sign((31, 102, 29), "east", ["LOST DOG", "answers to", "BISCUIT", ""], color="black"),
            sign((31, 102, 28), "east", ["41 days", "no word.", "I'm going home.", "- Frank"], color="black"),
            setblock((32, 101, 27), "minecraft:potted_dead_bush")]

    # lift house around the cage, headframe on top
    (lx1, ly1, lz1), (lx2, ly2, lz2) = W.LIFT_HOUSE
    out += ["# Lift house",
            fill((lx1 - 1, 100, lz1 - 1), (lx2 + 1, ly2 + 1, lz2 + 1), "minecraft:waxed_weathered_cut_copper"),
            fill((lx1 - 1, 101, lz1 - 1), (lx2 + 1, 101, lz2 + 1), "minecraft:polished_deepslate"),
            fill((lx1, ly1, lz1), (lx2, ly2, lz2), "minecraft:air"),
            fill((lx1, 100, lz1), (lx2, 100, lz2), "minecraft:polished_andesite"),
            fill(*W.LIFT_HOUSE_DOOR, "minecraft:air"),
            fill((lx2 + 1, 103, lz1 + 1), (lx2 + 1, 104, lz1 + 3), "minecraft:glass"),
            fill((lx2 + 1, 103, lz2 - 3), (lx2 + 1, 104, lz2 - 1), "minecraft:glass"),
            sign((13, 104, 21), "east", ["SHAFT 9", "LIFT 2", "B1 - B9", ""], color="white", glow=True),
            sign((13, 104, 18), "east", ["", "HEADFRAME", "KEEP CLEAR", ""], color="red"),
            setblock((10, 105, 19), "minecraft:lantern[hanging=true]"),
            button(W.CALL_BUTTON, "east"),
            sign((7, 103, 21), "east", ["", "CALL", "LIFT", ""], color="yellow", glow=True),
            setblock((11, 101, 14), "minecraft:barrel[facing=up]"), setblock((11, 101, 15), "minecraft:barrel[facing=up]"),
            setblock((0, 101, 25), "minecraft:chipped_anvil[facing=north]")]
    out += cage(101, "surface")
    # headframe: four legs, braces and two sheave wheels
    for x, z in [(1, 17), (6, 17), (1, 22), (6, 22)]:
        out += fill((x, 107, z), (x, 128, z), "minecraft:polished_blackstone_wall")
    for y in range(110, 128, 6):
        out += fill((1, y, 17), (6, y, 17), "minecraft:polished_blackstone")
        out += fill((1, y, 22), (6, y, 22), "minecraft:polished_blackstone")
        out += fill((1, y, 17), (1, y, 22), "minecraft:polished_blackstone")
        out += fill((6, y, 17), (6, y, 22), "minecraft:polished_blackstone")
    for zz in (19, 20):
        for a in range(0, 360, 15):
            wx = 3.5 + 3.2 * math.cos(math.radians(a))
            wy = 131 + 3.2 * math.sin(math.radians(a))
            out.append(setblock((int(round(wx)), int(round(wy)), zz), "minecraft:iron_block"))
        out.append(setblock((3, 131, zz), "minecraft:iron_block"))
    out += fill((3, 107, 20), (3, 128, 20), "minecraft:chain[axis=y]")
    out += fill((1, 128, 17), (6, 128, 22), "minecraft:polished_blackstone_slab[type=bottom]")

    # yard props
    out += ["# Yard",
            fill((44, 101, 30), (50, 103, 32), "minecraft:orange_concrete"), fill((44, 104, 30), (50, 106, 32), "minecraft:blue_concrete"),
            fill((50, 101, 1), (56, 103, 3), "minecraft:green_concrete"),
            fill((20, 101, 4), (26, 101, 6), "minecraft:polished_basalt[axis=x]"),
            fill((21, 102, 4), (25, 102, 5), "minecraft:polished_basalt[axis=x]"),
            fill((22, 103, 4), (24, 103, 4), "minecraft:polished_basalt[axis=x]")]
    for x, z, lit in [(40, 14, True), (20, 30, False), (15, 24, True), (58, 24, True)]:
        out += fill((x, 101, z), (x, 106, z), "minecraft:dark_oak_fence")
        out.append(setblock((x, 107, z), f"minecraft:redstone_lamp[lit={'true' if lit else 'false'}]"))
        if lit:
            out.append(setblock((x, 104, z + 1), "minecraft:light[level=10]"))
    out += [sign((40, 102, 13), "north", ["", "SITE 9", "", ""], color="white")]
    return out


def biome():
    """Rain needs a rainy biome (the void has none). fillbiome is capped at 32768 blocks."""
    (xa, za), (xb, zb) = W.FORCELOAD
    out = []
    for x in range(xa, xb + 1, 16):
        for y in (96, 128):
            out.append(f"fillbiome {x} {y} {za} {min(xb, x + 15)} {y + 31} {zb} minecraft:dark_forest")
    return out


# =========================================================================
# BUILD STEPS
# =========================================================================
def build():
    step("surface_terrain", surface_terrain())
    step("surface_compound", surface_compound(), biome())
    step("shells", "# The solid rock both levels are carved from", [fill(a, b, "minecraft:deepslate") for a, b in W.SHELLS])
    walls, air = carve({**W.B9, **W.B8})
    step("rooms_walls", walls)
    step("rooms_air", air)
    step("wear", wear(W.B9, OWN9), wear(W.B8, OWN8))
    step("openings", openings(W.B9_OPEN), openings(W.B8_OPEN), all_doors(), locker_doors())
    step("details9", b9_details())
    step("details8", b8_details(), cage(51, "b8"))
    fn("build/emergency_off", [setblock(p, "minecraft:deepslate_redstone_ore[lit=false]") for p in EMERGENCY])
    fn("build/emergency_on", [setblock(p, "minecraft:deepslate_redstone_ore[lit=true]") for p in EMERGENCY])
    STEPS.append("build/emergency_off")
    fn("build/lamps_off", [lamp(n, False) for n in W.LAMPS])
    fn("build/b8_backup", [lamp(n, True) for n in W.B8_BACKUP])
    fn("build/b9_backup", [lamp(n, True) for n in W.B9_BACKUP])
    fn("build/b9_all_on", [lamp(n, True) for n in W.LAMPS if W.LAMPS[n][1] < 50])
    fn("build/b8_all_on", [lamp(n, True) for n in W.LAMPS if 50 <= W.LAMPS[n][1] < 100])
    STEPS.append("build/lamps_off")
    return STEPS
