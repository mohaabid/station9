#!/usr/bin/env python3
"""
STATION 9 -- a short Minecraft horror map, generated as a datapack.

    python3 generate.py          -> writes ./Station9 (Java 1.20.4, pack_format 26)

Every coordinate in the map lives in this file, so the build and the scripted
events can never drift apart. Edit the constants, re-run, reload the world.
"""
import json
import os
import random
import shutil
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Station9")
NS = "station9"
rng = random.Random(9)

# Tuning knobs -----------------------------------------------------------
HUNTER_SPEED = 0.34        # Subject 9's movement speed attribute during the chase
HUNTER_LEASH = 16          # if it falls further behind than this, it "catches up"
HUNTER_HEADSTART = 70      # ticks between the tunnel opening and Subject 9 breaking in
RESPAWN_GRACE = 100        # ticks after a death before it comes back

# ------------------------------------------------------------------------
files = {}
scheduled = set()


def flat(lines):
    for line in lines:
        if isinstance(line, (list, tuple)):
            yield from flat(line)
        elif line is not None:
            yield line


def fn(name, *lines):
    files.setdefault(name, []).extend(flat(lines))


def call(name):
    return f"function {NS}:{name}"


def sched(name, ticks):
    scheduled.add(name)
    return f"schedule function {NS}:{name} {ticks}t"


def txt(text, **style):
    return json.dumps(dict(text=text, **style), ensure_ascii=False)


def snbt(s):
    """Quote a string for SNBT (used for JSON text stored inside NBT)."""
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def fill(a, b, block, mode=""):
    x1, x2 = sorted((a[0], b[0]))
    y1, y2 = sorted((a[1], b[1]))
    z1, z2 = sorted((a[2], b[2]))
    step = max(1, 32768 // ((y2 - y1 + 1) * (z2 - z1 + 1)))
    suffix = f" {mode}" if mode else ""
    return [f"fill {xs} {y1} {z1} {min(x2, xs + step - 1)} {y2} {z2} {block}{suffix}"
            for xs in range(x1, x2 + 1, step)]


def setblock(p, block):
    return f"setblock {p[0]} {p[1]} {p[2]} {block}"


def sound(pos, name, vol=1.0, pitch=1.0, source="hostile", who="@a"):
    return f"playsound minecraft:{name} {source} {who} {pos[0]} {pos[1]} {pos[2]} {vol} {pitch} 1"


def sound_at_player(name, vol=1.0, pitch=1.0, offset="~ ~ ~", source="hostile"):
    return f"execute as @a at @s run playsound minecraft:{name} {source} @s {offset} {vol} {pitch}"


def radio(text):
    return [
        'tellraw @a ["",' + txt("[Radio] ", color="dark_aqua") + "," + txt(text, color="gray", italic=True) + "]",
        sound_at_player("block.note_block.bit", 0.35, 0.5, source="master"),
        sound_at_player("ui.button.click", 0.25, 1.8, source="master"),
    ]


def objective(text):
    return "title @a actionbar " + txt(text, color="gold")


def sign(pos, facing, lines, color="black", glow=False, wood="dark_oak"):
    msgs = [txt(l) for l in (lines + ["", "", "", ""])[:4]]
    front = f'{{color:"{color}",has_glowing_text:{1 if glow else 0}b,messages:[{",".join(snbt(m) for m in msgs)}]}}'
    return setblock(pos, f"minecraft:{wood}_wall_sign[facing={facing}]{{front_text:{front},is_waxed:1b}}")


def door(pos, facing, open_=False, wood="dark_oak", hinge="left"):
    x, y, z = pos
    st = f"facing={facing},hinge={hinge},open={'true' if open_ else 'false'}"
    return [setblock((x, y, z), f"minecraft:{wood}_door[{st},half=lower]"),
            setblock((x, y + 1, z), f"minecraft:{wood}_door[{st},half=upper]")]


def book(title, author, pages):
    ps = ",".join(snbt(txt(p)) for p in pages)
    return f'{{id:"minecraft:written_book",Count:1b,tag:{{title:{json.dumps(title)},author:{json.dumps(author)},pages:[{ps}]}}}}'


def summon_stalker(pos, yaw, tag):
    x, y, z = pos
    return [
        f'summon minecraft:wither_skeleton {x} {y} {z} {{Tags:["s9","s9_stalker","{tag}"],NoAI:1b,Silent:1b,'
        f'Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",'
        f'CustomName:{snbt(txt("Subject 9"))},Rotation:[{yaw}f,0f]}}',
        f"tp @e[tag={tag}] {x} {y} {z} {yaw} 0",
    ]


def summon_hunter(pos):
    x, y, z = pos
    return (
        f'summon minecraft:wither_skeleton {x} {y} {z} {{Tags:["s9","s9_hunter"],Silent:1b,Invulnerable:1b,'
        f'PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",'
        f'CustomName:{snbt(txt("Subject 9"))},Attributes:['
        f'{{Name:"minecraft:generic.movement_speed",Base:{HUNTER_SPEED}d}},'
        f'{{Name:"minecraft:generic.attack_damage",Base:100d}},'
        f'{{Name:"minecraft:generic.follow_range",Base:64d}},'
        f'{{Name:"minecraft:generic.knockback_resistance",Base:1d}}]}}'
    )


def item(pos, item_id, tag_key, name, color, lore):
    x, y, z = pos
    display = f"display:{{Name:{snbt(txt(name, italic=False, color=color))},Lore:[{snbt(txt(lore, color='dark_gray'))}]}}"
    return (f'summon minecraft:item {x} {y} {z} {{Tags:["s9"],Age:-32768s,PickupDelay:0s,'
            f'Item:{{id:"minecraft:{item_id}",Count:1b,tag:{{{tag_key}:1b,{display}}}}}}}')


def box_selector(a, b):
    """Players whose feet are inside the block box a..b (inclusive).

    Selector volumes match any hitbox that *touches* [x, x+dx+1], so a player
    standing in a doorway still counts. Inset by the player's half-width (0.3)
    so only the player's centre matters.
    """
    return (f"x={a[0] + .3},y={a[1]},z={a[2] + .3},"
            f"dx={round(b[0] - a[0] - .6, 2)},dy={b[1] - a[1]},dz={round(b[2] - a[2] - .6, 2)}")


# =========================================================================
# LAYOUT
# Floor is y=40, rooms are 3 tall (y41-43), ceiling y=44. Everything sits in
# a solid deepslate block so there is no sky and no light we didn't place.
# =========================================================================
FLOOR, CEIL = 40, 44
SHELL = ((-1, 38, -2), (63, 46, 38))

# Rooms in build order: later rooms win shared walls.
ROOMS = {
    "office": dict(box=((10, 41, 11), (20, 43, 17)), wall="light_gray_terracotta", accent="gray_terracotta",
                   floor="dark_oak_planks", ceil="smooth_stone", wall_scatter=[("moss_block", .04)]),
    "washroom": dict(box=((11, 41, 7), (13, 43, 9)), wall="white_terracotta", accent="light_gray_terracotta",
                     floor="polished_diorite", ceil="smooth_stone"),
    "reflection": dict(box=((11, 41, 3), (13, 43, 5)), wall="white_terracotta", accent="light_gray_terracotta",
                       floor="polished_diorite", ceil="smooth_stone"),
    "alcove": dict(box=((10, 41, 0), (14, 43, 1)), wall="light_gray_terracotta", accent="gray_terracotta",
                   floor="dark_oak_planks", ceil="smooth_stone"),
    "containment": dict(box=((26, 41, 22), (36, 43, 30)), wall="polished_deepslate", accent="deepslate_tiles",
                        floor="polished_blackstone", ceil="smooth_basalt",
                        wall_scatter=[("sculk", .06)], floor_scatter=[("sculk", .07)]),
    "corridor": dict(box=((7, 41, 19), (48, 43, 20)), wall="deepslate_bricks", accent="polished_deepslate",
                     floor="deepslate_tiles", ceil="smooth_basalt",
                     wall_scatter=[("cracked_deepslate_bricks", .15)], floor_scatter=[("cracked_deepslate_tiles", .12)]),
    "elevator": dict(box=((2, 41, 18), (5, 43, 21)), wall="waxed_oxidized_copper", accent="waxed_oxidized_cut_copper",
                     floor="waxed_weathered_cut_copper", ceil="waxed_oxidized_cut_copper"),
    "tunnel1": dict(box=((58, 41, 27), (59, 43, 35)), wall="waxed_oxidized_cut_copper", accent="waxed_weathered_copper",
                    floor="waxed_exposed_cut_copper", ceil="polished_deepslate",
                    wall_scatter=[("waxed_oxidized_copper", .12)]),
    "tunnel2": dict(box=((35, 41, 34), (59, 43, 35)), wall="waxed_oxidized_cut_copper", accent="waxed_weathered_copper",
                    floor="waxed_exposed_cut_copper", ceil="polished_deepslate",
                    wall_scatter=[("waxed_oxidized_copper", .12)]),
    "tunnel3": dict(box=((35, 41, 32), (36, 43, 33)), wall="waxed_oxidized_cut_copper", accent="waxed_weathered_copper",
                    floor="waxed_exposed_cut_copper", ceil="polished_deepslate"),
    "generator": dict(box=((50, 41, 15), (60, 43, 25)), wall="waxed_weathered_cut_copper", accent="polished_deepslate",
                      floor="polished_andesite", ceil="smooth_basalt", floor_scatter=[("andesite", .15)]),
}
CHASE_ROOMS = ["corridor", "containment", "generator", "tunnel1", "tunnel2", "tunnel3"]

# Openings through walls: (from, to, initial block)
ELEVATOR_DOOR = ((6, 41, 19), (6, 43, 20))
CONTAIN_N_DOOR = ((30, 41, 21), (31, 43, 21))
CONTAIN_S_DOOR = ((35, 41, 31), (36, 43, 31))
GEN_W_DOOR = ((49, 41, 19), (49, 43, 20))
GEN_S_DOOR = ((58, 41, 26), (59, 43, 26))
OFFICE_DOOR = (15, 41, 18)
WASH_ARCH = ((12, 41, 10), (12, 43, 10))
REFL_ARCH = ((12, 41, 2), (12, 43, 2))
MIRROR = ((11, 41, 6), (13, 43, 6))
OPENINGS = [
    (ELEVATOR_DOOR, "minecraft:iron_block"),
    (CONTAIN_N_DOOR, "minecraft:iron_bars[east=true,west=true]"),
    (CONTAIN_S_DOOR, "minecraft:iron_block"),
    (GEN_W_DOOR, "minecraft:air"),
    (GEN_S_DOOR, "minecraft:iron_block"),
    ((OFFICE_DOOR, (15, 42, 18)), "minecraft:air"),
    (WASH_ARCH, "minecraft:air"),
    (REFL_ARCH, "minecraft:air"),
    (MIRROR, "minecraft:light_gray_stained_glass_pane[east=true,west=true]"),
]

KEYPAD = (28, 42, 20)
LEVER = (53, 42, 20)
GEN_SIGN = (53, 43, 20)
KEYPAD_SIGN = (28, 43, 20)

# Lamps are redstone lamps set straight into the ceiling (no redstone, so they
# hold whatever state we give them).
LAMPS = {
    "E1": (4, 44, 20),
    "C1": (10, 44, 19), "C2": (21, 44, 20), "C3": (33, 44, 19), "C4": (45, 44, 20),
    "O1": (15, 44, 14),
    "W1": (12, 44, 8), "R1": (12, 44, 4),
    "K1": (31, 44, 23), "K2": (31, 44, 28),
    "G1": (52, 44, 17), "G2": (58, 44, 17), "G3": (52, 44, 23), "G4": (58, 44, 23),
    "T1": (58, 44, 31), "T2": (51, 44, 35), "T3": (42, 44, 34),
}
BACKUP_LAMPS = ["C1", "C2", "C4", "W1", "R1", "K1", "K2", "G1"]   # lit on the dying backup power
FLICKER = "C2"

# Positions the scripted entities use
SPAWN = (4, 41, 20)
ELEVATOR_BOX = ((2, 41, 18), (4, 43, 21))    # deep enough that you're clear of the shutter at x=6
DOORWAY_BOX = ((5, 41, 18), (7, 43, 21))     # anyone still here when the shutter drops gets pulled in
CORRIDOR_BOX = ((7, 41, 19), (48, 43, 20))
OFFICE_BOX = ((10, 41, 11), (20, 43, 17))
WASH_BOX = ((11, 41, 7), (13, 43, 9))
CONTAIN_BOX = ((26, 41, 23), (36, 43, 30))
GEN_BOX = ((50, 41, 15), (60, 43, 25))
STEAM_BOX = ((44, 41, 34), (48, 43, 35))
CHECKPOINT = (58, 41, 24)
HUNTER_ENTRY = (47.5, 41, 19.5)
KEYCARD_AT = (18.5, 42.05, 11.5)
FUSE_AT = (31.5, 41.1, 27.5)
OFFICE_CANDLES = [((16, 42, 11), "candle", 3), ((11, 41, 17), "white_candle", 4), ((20, 42, 13), "red_candle", 1)]


def lamp(name, on):
    return setblock(LAMPS[name], f"minecraft:redstone_lamp[lit={'true' if on else 'false'}]")


def expanded(room):
    (x1, y1, z1), (x2, y2, z2) = ROOMS[room]["box"]
    return (x1 - 1, FLOOR, z1 - 1), (x2 + 1, CEIL, z2 + 1)


def inside(p, box):
    (x1, y1, z1), (x2, y2, z2) = box
    return x1 <= p[0] <= x2 and y1 <= p[1] <= y2 and z1 <= p[2] <= z2


def is_interior(p):
    return any(inside(p, r["box"]) for r in ROOMS.values())


def is_opening(p):
    return any(inside(p, box) for box, _ in OPENINGS)


def wall_owner():
    owner = {}
    for name in ROOMS:
        (x1, _, z1), (x2, _, z2) = expanded(name)
        for y in range(41, 44):
            for x in range(x1, x2 + 1):
                for z in range(z1, z2 + 1):
                    if x in (x1, x2) or z in (z1, z2):
                        p = (x, y, z)
                        if not is_interior(p) and not is_opening(p):
                            owner[p] = name
    return owner


OWNER = wall_owner()
EMERGENCY = sorted(p for p, room in OWNER.items()
                   if room in CHASE_ROOMS and p[1] == 43 and (p[0] + p[2]) % 5 == 0)


# =========================================================================
# BUILD
# =========================================================================
def build():
    fn("build/shell", "# The solid rock everything is carved from", fill(*SHELL, "minecraft:deepslate"))

    rooms = ["# Walls, then interiors, floors and ceilings"]
    for name, r in ROOMS.items():
        a, b = expanded(name)
        rooms += fill(a, b, f"minecraft:{r['wall']}")
        rooms += fill((a[0], 41, a[2]), (b[0], 41, b[2]), f"minecraft:{r['accent']}")
    for name, r in ROOMS.items():
        (x1, y1, z1), (x2, y2, z2) = r["box"]
        rooms += fill((x1, y1, z1), (x2, y2, z2), "minecraft:air")
        rooms += fill((x1, FLOOR, z1), (x2, FLOOR, z2), f"minecraft:{r['floor']}")
        rooms += fill((x1, CEIL, z1), (x2, CEIL, z2), f"minecraft:{r['ceil']}")
    fn("build/rooms", rooms)

    wear = ["# Cracks, moss and sculk creeping over the walls and floors"]
    for pos, room in sorted(OWNER.items()):
        for block, chance in ROOMS[room].get("wall_scatter", []):
            if rng.random() < chance:
                wear.append(setblock(pos, f"minecraft:{block}"))
                break
    for name, r in ROOMS.items():
        (x1, _, z1), (x2, _, z2) = r["box"]
        for block, chance in r.get("floor_scatter", []):
            for x in range(x1, x2 + 1):
                for z in range(z1, z2 + 1):
                    if rng.random() < chance:
                        wear.append(setblock((x, FLOOR, z), f"minecraft:{block}"))
    fn("build/wear", wear)

    fn("build/openings", "# Doors, shutters, arches and the mirror",
       [fill(a, b, block) for (a, b), block in OPENINGS],
       door(OFFICE_DOOR, "north"))

    build_details()
    fn("build/emergency_off", [setblock(p, "minecraft:deepslate_redstone_ore[lit=false]") for p in EMERGENCY])
    fn("build/emergency_on", [setblock(p, "minecraft:deepslate_redstone_ore[lit=true]") for p in EMERGENCY])
    fn("build/lamps_backup", [lamp(n, n in BACKUP_LAMPS) for n in LAMPS])
    fn("build/lamps_all_on", [lamp(n, True) for n in LAMPS])
    fn("build/lamps_all_off", [lamp(n, False) for n in LAMPS])

    fn("build/all",
       call("build/shell"), call("build/rooms"), call("build/wear"), call("build/openings"),
       call("build/details"), call("build/emergency_off"), call("build/lamps_backup"))


def build_details():
    d = []
    # --- Lift ---------------------------------------------------------------
    d += ["# Lift", setblock((3, 42, 18), "minecraft:stone_button[face=wall,facing=south]"),
          setblock((3, 41, 18), "minecraft:stone_button[face=wall,facing=south]"),
          sign((4, 42, 18), "south", ["LIFT 2", "B1 - B9", "", "MAX LOAD 1"], color="white"),
          fill((2, 44, 18), (5, 44, 21), "minecraft:waxed_oxidized_cut_copper"),
          setblock((2, 43, 21), "minecraft:cobweb")]

    # --- Corridor -----------------------------------------------------------
    d += ["# Corridor",
          sign((8, 42, 19), "south", ["OFFICES  >", "CONTAINMENT  >", "GENERATOR B  >", ""], color="white"),
          sign((15, 43, 19), "south", ["", "OFFICE 9-A", "", ""], color="white"),
          sign((32, 43, 20), "north", ["CONTAINMENT", "B9", "SUBJECT 9", ""], color="red", glow=True),
          setblock(KEYPAD, "minecraft:stone_button[face=wall,facing=north]"),
          sign(KEYPAD_SIGN, "north", ["KEYCARD", "LEVEL 3", "", ""], color="yellow", glow=True),
          sign((47, 43, 19), "south", ["", "GENERATOR B", ">>>", ""], color="white"),
          setblock((14, 41, 19), "minecraft:candle[candles=4,lit=true]"),
          setblock((17, 41, 19), "minecraft:white_candle[candles=2,lit=true]"),
          # the ceiling gave way here once
          setblock((39, 44, 20), "minecraft:air"), setblock((39, 45, 20), "minecraft:air"),
          setblock((38, 41, 20), "minecraft:cobbled_deepslate"),
          setblock((39, 41, 20), "minecraft:cobbled_deepslate_slab[type=bottom]"),
          setblock((40, 41, 20), "minecraft:cobbled_deepslate_stairs[facing=west]"),
          setblock((37, 41, 19), "minecraft:cobbled_deepslate_slab[type=bottom]"),
          setblock((47, 43, 20), "minecraft:cobweb"), setblock((48, 43, 19), "minecraft:cobweb")]
    # something was dragged out of containment
    d += [setblock(p, "minecraft:redstone_wire") for p in
          [(31, 41, 20), (30, 41, 20), (29, 41, 19), (27, 41, 19), (26, 41, 19), (24, 41, 20)]]

    # --- Office ---------------------------------------------------------------
    d += ["# Office 9-A",
          fill((16, 41, 11), (19, 41, 11), "minecraft:dark_oak_slab[type=top]"),
          setblock((17, 42, 11), "minecraft:observer[facing=south]"),
          setblock((19, 42, 11), "minecraft:white_carpet"),
          setblock((17, 41, 12), "minecraft:dark_oak_stairs[facing=south]"),
          setblock((19, 41, 15), "minecraft:dark_oak_stairs[facing=east,half=top]"),
          fill((20, 41, 13), (20, 41, 14), "minecraft:dark_oak_slab[type=top]"),
          fill((10, 41, 12), (10, 42, 13), "minecraft:bookshelf"),
          setblock((10, 41, 15), "minecraft:barrel[facing=east]"),
          setblock((10, 41, 16), "minecraft:barrel[facing=east]"),
          setblock((10, 42, 16), "minecraft:barrel[facing=up]"),
          setblock((14, 41, 13), "minecraft:white_carpet"), setblock((12, 41, 15), "minecraft:white_carpet"),
          setblock((16, 41, 15), "minecraft:white_carpet"), setblock((18, 41, 16), "minecraft:white_carpet"),
          setblock((20, 43, 11), "minecraft:cobweb"), setblock((10, 43, 17), "minecraft:cobweb"),
          setblock((20, 43, 17), "minecraft:cobweb"),
          sign((20, 43, 15), "west", ["IT MOVES", "WHEN THE", "LIGHTS", "GO OUT"], color="red", glow=True),
          setblock((14, 41, 16), "minecraft:lectern[facing=east,has_book=true]{Book:" + book(
              "Night Log", "Dr. E. Hale", [
                  "NIGHT LOG\nDr. E. Hale\nStation 9 - Level B9\n\nIf you are reading this, the power is still out.\n\nDo not trust the dark.",
                  "Day 112\nSubject 9 has stopped eating. It stands at the glass all day, facing the office.\n\nFacing us.",
                  "Day 115\nPower dip at 02:14. The cell field dropped for less than a second.\n\nWhen the lights came back, it was pressed against the glass. It had been at the back wall.",
                  "Day 118\nMarsh says it only moves in the dark. I told him to get some sleep.\n\nDay 121\nMarsh is gone. His keycard was on my desk this morning.\n\nI did not put it there.",
                  "Day 122\nThe mirrors stopped showing us.\n\nOnly it.\n\nThe generator is failing. If it dies, the cell opens.",
              ]) + ",Page:0}")]
    d += [setblock(p, f"minecraft:{kind}[candles={n},lit=true]") for p, kind, n in OFFICE_CANDLES]

    # --- Washroom and its reflection (mirrored across z=6) ----------------------
    d += ["# Washroom + the room behind the mirror",
          setblock((11, 41, 7), "minecraft:cauldron"), setblock((13, 41, 7), "minecraft:cauldron"),
          setblock((11, 41, 5), "minecraft:cauldron"), setblock((13, 41, 5), "minecraft:cauldron"),
          fill((10, 41, 0), (10, 42, 0), "minecraft:bookshelf")]

    # --- Containment ------------------------------------------------------------
    cell = [fill((28, 41, 25), (34, 43, 25), "minecraft:glass"),
            fill((28, 41, 26), (28, 43, 30), "minecraft:glass"),
            fill((34, 41, 26), (34, 43, 30), "minecraft:glass"),
            fill((31, 41, 25), (31, 42, 25), "minecraft:air"),       # torn open from the inside
            setblock((30, 43, 25), "minecraft:air"), setblock((32, 41, 25), "minecraft:air")]
    claws = [setblock((x, y, 31), "minecraft:cracked_deepslate_tiles")
             for x, y in [(29, 42), (29, 43), (30, 41), (30, 42), (32, 42), (32, 43), (33, 41), (33, 42)]]
    d += ["# Containment B9", cell, claws,
          setblock((30, 43, 29), "minecraft:chain[axis=y]"), setblock((32, 43, 29), "minecraft:chain[axis=y]"),
          setblock((32, 42, 29), "minecraft:chain[axis=y]"),
          setblock((29, 43, 30), "minecraft:glow_lichen[south=true]"),
          setblock((33, 42, 30), "minecraft:glow_lichen[south=true]"),
          setblock((33, 43, 26), "minecraft:glow_lichen[east=true]"),
          fill((29, FLOOR, 26), (33, FLOOR, 30), "minecraft:sculk", "replace minecraft:polished_blackstone"),
          setblock((27, 41, 28), "minecraft:sculk_sensor"),
          setblock((26, 41, 30), "minecraft:sculk_shrieker"),
          fill((26, 41, 24), (26, 41, 26), "minecraft:polished_deepslate_slab[type=top]"),
          sign((32, 42, 22), "south", ["", "<<  LIFT", "", ""], color="white"),
          setblock((27, 41, 23), "minecraft:lectern[facing=east,has_book=true]{Book:" + book(
              "Subject 9", "Containment", [
                  "SUBJECT 9\nContainment protocol\n\nClass: UNKNOWN\nHeight: 2.4 m\nDiet: none observed\nSleep: none observed",
                  "1. Keep the lights on.\n\n2. Never look away from it in the dark.\n\n3. If the field fails, do NOT restore main power without a clear exit.",
                  "(handwritten)\n\nIt isn't afraid of the light.\n\nIt just can't SEE in the dark.\n\nThe generator turns every light on at once.",
                  "It will see you.\n\n- Marsh",
              ]) + ",Page:0}")]
    d += [setblock(p, "minecraft:redstone_wire") for p in [(31, 41, 26), (31, 41, 24), (31, 41, 23), (30, 41, 22)]]

    # --- Generator B --------------------------------------------------------------
    d += ["# Generator B",
          fill((54, 41, 18), (56, 43, 22), "minecraft:iron_block"),
          fill((54, 41, 18), (56, 41, 22), "minecraft:polished_deepslate"),
          setblock((54, 43, 19), "minecraft:blast_furnace[facing=west]"),
          setblock((54, 43, 21), "minecraft:blast_furnace[facing=west]"),
          setblock((54, 42, 18), "minecraft:observer[facing=west]"),
          setblock((54, 42, 22), "minecraft:observer[facing=west]"),
          setblock(LEVER, "minecraft:lever[face=wall,facing=west]"),
          sign(GEN_SIGN, "west", ["GENERATOR B", "FUSE: MISSING", "", "PULL TO START"], color="red", glow=True),
          setblock((50, 41, 15), "minecraft:barrel[facing=up]"), setblock((51, 41, 15), "minecraft:barrel[facing=up]"),
          setblock((50, 42, 15), "minecraft:barrel[facing=south]"),
          setblock((60, 41, 15), "minecraft:chipped_anvil[facing=north]"),
          setblock((60, 41, 16), "minecraft:grindstone[face=floor,facing=north]"),
          setblock((50, 41, 25), "minecraft:cauldron"),
          sign((57, 43, 25), "north", ["MAINTENANCE", "TUNNEL", "vvv", ""], color="white"),
          setblock((60, 43, 25), "minecraft:cobweb")]

    # --- Maintenance tunnel ---------------------------------------------------------
    d += ["# Maintenance tunnel",
          setblock((59, 44, 28), "minecraft:iron_bars"), setblock((46, 44, 34), "minecraft:iron_bars"),
          setblock((38, 44, 35), "minecraft:iron_bars"),
          sign((58, 42, 33), "east", ["", "LIFT", "<<<", ""], color="white"),
          sign((50, 42, 34), "south", ["", "<<  LIFT", "(via B9)", ""], color="white")]

    fn("build/details", d)


# =========================================================================
# CORE: load / tick / start / reset
# =========================================================================
FLAGS = ["#stage", "#time", "#deaths", "#mirror", "#cstalk", "#cs_seen", "#kscare", "#kdeny", "#ghint",
         "#steam", "#hunter", "#ct", "#ride", "#alarm", "#shake", "#echoes"]


def core():
    fn("load",
       "scoreboard objectives add s9 dummy",
       "scoreboard objectives add s9_walk minecraft.custom:minecraft.walk_one_cm",
       "scoreboard objectives add s9_sprint minecraft.custom:minecraft.sprint_one_cm",
       "scoreboard objectives add s9_deaths deathCount",
       "scoreboard objectives add s9_age dummy",
       "scoreboard objectives add s9_fs dummy",
       "scoreboard objectives add s9_idle dummy",
       "scoreboard players set #2 s9 2",
       "scoreboard players set #20 s9 20",
       "scoreboard players set #60 s9 60",
       "execute unless score #stage s9 = #stage s9 run scoreboard players set #stage s9 0",
       "forceload add -16 -16 79 47",
       call("rules"))

    fn("rules",
       *[f"gamerule {k} {v}" for k, v in [
           ("doDaylightCycle", "false"), ("doWeatherCycle", "false"), ("doMobSpawning", "false"),
           ("doWardenSpawning", "false"), ("doPatrolSpawning", "false"), ("doTraderSpawning", "false"),
           ("doInsomnia", "false"), ("mobGriefing", "false"), ("keepInventory", "true"),
           ("doImmediateRespawn", "true"), ("randomTickSpeed", "0"), ("announceAdvancements", "false"),
           ("doFireTick", "false"), ("commandBlockOutput", "false"), ("spawnRadius", "0"),
           ("doEntityDrops", "false"), ("sendCommandFeedback", "false")]],
       "difficulty normal", "time set midnight", "weather clear")

    fn("tick",
       f"execute as @a[tag=!s9_seen] run {call('join')}",
       "execute if score #stage s9 matches 2..6 run scoreboard players add #time s9 1",
       f"execute if score #stage s9 matches 1..5 run {call('tick/flicker')}",
       f"execute if score #stage s9 matches 2..5 run {call('tick/explore')}",
       f"execute if score #stage s9 matches 6 run {call('tick/chase')}")

    fn("join",
       "tag @s add s9_seen",
       "execute if score #stage s9 matches 0 run effect give @s minecraft:blindness 5 0 true",
       "execute if score #stage s9 matches 0 run effect give @s minecraft:slow_falling 5 0 true",
       f"execute if score #stage s9 matches 0 run tp @s {SPAWN[0] + .5} {SPAWN[1]} {SPAWN[2] + .5} -90 0",
       f"execute if score #stage s9 matches 0 run {sched('start', 40)}",
       'execute if score #stage s9 matches 1.. run tellraw @s ["",' + txt("[Station 9] ", color="dark_red") + ","
       + json.dumps({"text": "Click here to restart the map", "color": "gray", "underlined": True,
                     "clickEvent": {"action": "run_command", "value": f"/function {NS}:start"}}) + "]")

    fn("start", "# Rebuild everything and play from the top", call("reset"), call("intro/0"))

    reset = ["# Put the whole station back to its starting state"]
    reset += [f"schedule clear {NS}:{s}" for s in sorted(scheduled | {"start"})]
    reset += ["kill @e[tag=s9]", call("build/all"), call("rules")]
    reset += [f"scoreboard players set {f} s9 0" for f in FLAGS]
    reset += ["scoreboard players set @a s9_deaths 0", "scoreboard players reset @e s9_age",
              f"setworldspawn {SPAWN[0]} {SPAWN[1]} {SPAWN[2]}", f"spawnpoint @a {SPAWN[0]} {SPAWN[1]} {SPAWN[2]}",
              "clear @a", "effect clear @a", "gamemode adventure @a",
              "effect give @a minecraft:saturation infinite 0 true",
              item(KEYCARD_AT, "tripwire_hook", "s9key", "Keycard - M. Marsh", "aqua", "Level 3 access"),
              item(FUSE_AT, "blaze_rod", "s9fuse", "Fuse (30A)", "gold", "Generator B")]
    files["reset"] = list(flat(reset))   # written last, once every scheduled function is known


# =========================================================================
# EFFECTS
# =========================================================================
def effects():
    fn("fx/shake",
       "scoreboard players remove #shake s9 1",
       "scoreboard players operation #p s9 = #shake s9",
       "scoreboard players operation #p s9 %= #2 s9",
       "execute if score #p s9 matches 0 as @a at @s run tp @s ~ ~ ~ ~1.6 ~-1.2",
       "execute if score #p s9 matches 1 as @a at @s run tp @s ~ ~ ~ ~-1.6 ~1.2",
       f"execute if score #shake s9 matches 1.. run {sched('fx/shake', 1)}")

    fn("fx/alarm",
       "scoreboard players remove #alarm s9 1",
       "scoreboard players operation #p s9 = #alarm s9",
       "scoreboard players operation #p s9 %= #2 s9",
       "execute if score #p s9 matches 0 run " + sound_at_player("block.note_block.bit", .7, 1.0, source="master"),
       "execute if score #p s9 matches 1 run " + sound_at_player("block.note_block.bit", .7, .7, source="master"),
       f"execute if score #alarm s9 matches 1.. run {sched('fx/alarm', 8)}")

    fn("fx/footstep_far",
       "scoreboard players set @s s9_fs 0",
       "execute rotated ~ 0 positioned ^ ^ ^-7 run playsound minecraft:block.deepslate_tiles.step hostile @s ~ ~ ~ 1 0.8")
    fn("fx/footstep_near",
       "scoreboard players add #echoes s9 1",
       "execute rotated ~ 0 positioned ^ ^ ^-3 run playsound minecraft:block.deepslate_tiles.step hostile @s ~ ~ ~ 1 0.75")

    fn("fx/c1_on", lamp("C1", True))
    fn("fx/e1_on", lamp("E1", True))
    fn("fx/c2_off", lamp(FLICKER, False), sound(LAMPS[FLICKER], "block.redstone_torch.burnout", .15, 1.6, "block"))


# =========================================================================
# TICK LOGIC
# =========================================================================
def ticks():
    x, y, z = LAMPS[FLICKER]
    fn("tick/flicker",
       "execute store result score #f s9 run random value 1..100",
       f"execute if score #f s9 matches 1..4 if block {x} {y} {z} minecraft:redstone_lamp[lit=true] run {call('fx/c2_off')}",
       f"execute if score #f s9 matches 55..100 if block {x} {y} {z} minecraft:redstone_lamp[lit=false] run {lamp(FLICKER, True)}")

    wash = box_selector(*WASH_BOX)
    fn("tick/explore",
       call("tick/ambient"),
       f"execute if score #stage s9 matches 2 run {call('tick/footsteps')}",
       f"execute if score #stage s9 matches 2 if entity @a[nbt={{Inventory:[{{tag:{{s9key:1b}}}}]}}] run {call('event/got_key')}",
       f"execute if score #stage s9 matches 4 if entity @a[nbt={{Inventory:[{{tag:{{s9fuse:1b}}}}]}}] run {call('event/got_fuse')}",
       f"execute if block {KEYPAD[0]} {KEYPAD[1]} {KEYPAD[2]} minecraft:stone_button[powered=true] run {call('event/keypad')}",
       f"execute if block {LEVER[0]} {LEVER[1]} {LEVER[2]} minecraft:lever[powered=true] run {call('event/lever')}",
       "# the mirror: look into it, then turn around",
       f"execute if score #mirror s9 matches 0 if entity @a[{wash},y_rotation=140..180] run {call('event/mirror_1')}",
       f"execute if score #mirror s9 matches 0 if entity @a[{wash},y_rotation=-180..-140] run {call('event/mirror_1')}",
       f"execute if score #mirror s9 matches 1 if entity @a[y_rotation=-100..100] run {call('event/mirror_2')}",
       f"execute if score #mirror s9 matches 1 unless entity @a[{wash}] run {call('event/mirror_2')}",
       f"execute if score #cstalk s9 matches 1 run {call('tick/cstalk')}",
       f"execute if score #kscare s9 matches 0 if score #stage s9 matches 4.. if entity @a[{box_selector(*CONTAIN_BOX)}] run {call('event/k_scare_1')}",
       f"execute if score #ghint s9 matches 0 if score #stage s9 matches 2..3 if entity @a[{box_selector(*GEN_BOX)}] run {call('event/gen_hint')}")

    fn("tick/ambient",
       "# roughly one distant noise every 20 seconds",
       "execute store result score #r s9 run random value 1..2000",
       "execute if score #r s9 matches 1 at @a run playsound minecraft:ambient.cave ambient @a ~ ~ ~ 0.8 0.8",
       "execute if score #r s9 matches 2 at @a run playsound minecraft:block.iron_door.close hostile @a ~12 ~ ~6 1 0.6",
       "execute if score #r s9 matches 3 at @a run playsound minecraft:entity.warden.heartbeat hostile @a ~ ~ ~ 0.5 0.7",
       "execute if score #r s9 matches 4 at @a run playsound minecraft:block.chain.step hostile @a ~-8 ~2 ~-8 1 0.5",
       "execute if score #r s9 matches 5 at @a run playsound minecraft:entity.wither_skeleton.ambient hostile @a ~-10 ~ ~10 0.5 0.5",
       "execute if score #r s9 matches 6 at @a run playsound minecraft:block.sculk_shrieker.shriek hostile @a ~15 ~ ~-10 0.4 0.6")

    fn("tick/footsteps",
       "# something walks behind you in the corridor, and stops a moment after you do",
       f"execute as @a[{box_selector(*CORRIDOR_BOX)}] at @s run {call('tick/footsteps_player')}",
       "scoreboard players set @a s9_walk 0",
       "scoreboard players set @a s9_sprint 0")
    fn("tick/footsteps_player",
       "execute if score @s s9_walk matches 1.. run scoreboard players add @s s9_fs 1",
       "execute if score @s s9_sprint matches 1.. run scoreboard players add @s s9_fs 2",
       "execute if score @s s9_walk matches 1.. run scoreboard players set @s s9_idle 0",
       "execute if score @s s9_sprint matches 1.. run scoreboard players set @s s9_idle 0",
       "execute unless score @s s9_walk matches 1.. unless score @s s9_sprint matches 1.. run scoreboard players add @s s9_idle 1",
       f"execute if score @s s9_fs matches 10.. run {call('fx/footstep_far')}",
       f"execute if score @s s9_idle matches 14 if score #echoes s9 matches ..2 run {call('fx/footstep_near')}")

    near = box_selector((7, 41, 19), (12, 43, 20))
    looking = box_selector((7, 41, 19), (20, 43, 20))
    fn("tick/cstalk",
       "# it vanishes once you've had a good look, or if you walk up to it",
       f"execute if entity @a[{looking},y_rotation=55..125] run scoreboard players add #cs_seen s9 1",
       f"execute if score #cstalk s9 matches 1 if score #cs_seen s9 matches 16.. run {call('event/cstalk_vanish')}",
       f"execute if score #cstalk s9 matches 1 if entity @a[{near}] run {call('event/cstalk_vanish')}",
       f"execute if score #cstalk s9 matches 1 if score #stage s9 matches 4.. run {call('event/cstalk_vanish')}")

    fn("tick/chase",
       "scoreboard players add #ct s9 1",
       f"execute if score #ct s9 matches 10.. run {call('chase/pulse')}",
       f"execute as @a[scores={{s9_deaths=1..}}] run {call('chase/died')}",
       f"execute if score #steam s9 matches 0 if entity @a[{box_selector(*STEAM_BOX)}] run {call('event/steam')}",
       f"execute if entity @a[{box_selector(*ELEVATOR_BOX)}] run {call('end/1')}")


# =========================================================================
# STORY
# =========================================================================
def intro():
    fn("intro/0",
       "scoreboard players set #stage s9 1",
       f"tp @a {SPAWN[0]} {SPAWN[1]} {SPAWN[2] + .5} -90 0",
       "effect give @a minecraft:blindness 5 0 true",
       lamp("E1", True),
       "title @a times 30 80 30",
       "title @a subtitle " + txt("Research Level B9  -  last contact 41 days ago", color="gray"),
       "title @a title " + txt("STATION 9", color="dark_red", bold=True),
       sound_at_player("ambient.cave", 1, .6, source="ambient"),
       sched("intro/1", 110))

    fn("intro/1",
       radio("Ops: Radio check. You're on the lift down to B9. The station's been dark for six weeks."),
       "scoreboard players set #ride s9 0",
       sched("intro/ride", 20))

    ride = ["scoreboard players add #ride s9 1",
            sound_at_player("entity.minecart.riding", .5, .6, source="block"),
            sound_at_player("block.chain.step", .6, .5, source="block")]
    for n in range(1, 9):
        ride.append(f"execute if score #ride s9 matches {n} run title @a actionbar " + txt(f"v  B{n}", color="dark_gray"))
    ride += [f"execute if score #ride s9 matches 3 run {r}" for r in
             radio("Ops: Get Generator B running - east end of the level. Then we bring you up.")]
    ride += [f"execute if score #ride s9 matches 6 run {lamp('E1', False)}",
             f"execute if score #ride s9 matches 6 run {sched('fx/e1_on', 3)}",
             f"execute if score #ride s9 matches 6 run {sound((4, 45, 20), 'entity.iron_golem.damage', .5, .5)}",
             f"execute if score #ride s9 matches ..7 run {sched('intro/ride', 30)}",
             f"execute if score #ride s9 matches 8.. run {call('intro/crash')}"]
    fn("intro/ride", ride)

    fn("intro/crash",
       lamp("E1", False),
       sound_at_player("entity.generic.explode", .7, .5),
       sound_at_player("block.anvil.land", 1, .5),
       sound_at_player("block.chain.break", 1, .6),
       "title @a actionbar " + txt("B9", color="dark_red"),
       "effect give @a minecraft:darkness 8 0 true",
       "scoreboard players set #shake s9 14", sched("fx/shake", 1),
       sched("intro/2", 60))

    fn("intro/2",
       radio("Ops: -sshhk- ...lost the li- ...you there? ...B9? -kssht-"),
       sched("intro/3", 90))

    fn("intro/3",
       fill(*ELEVATOR_DOOR, "minecraft:air"),
       sound((6, 42, 20), "block.piston.contract", 1, .5, "block"),
       sound((6, 42, 20), "block.iron_door.open", 1, .6, "block"),
       "scoreboard players set #stage s9 2",
       "scoreboard players set #time s9 0",
       radio("Ops: ...signal's bad. Generator B. East end. Go."),
       objective("Restore power: find Generator B (east)"))


def events():
    # --- the keycard, the office door ------------------------------------------------
    fn("event/got_key",
       "scoreboard players set #stage s9 3",
       radio("Ops: That's Marsh's keycard. ...He never signed out."),
       sound_at_player("entity.warden.heartbeat", 1, .8),
       summon_stalker((8.5, 41, 19.5), -90, "s9_cstalk"),
       "scoreboard players set #cstalk s9 1",
       "scoreboard players set #cs_seen s9 0",
       sched("event/office_slam", 50))

    x, y, z = OFFICE_DOOR
    fn("event/office_slam",
       f"execute if entity @a[{box_selector(*OFFICE_BOX)}] run {call('event/office_slam_now')}")
    fn("event/office_slam_now",
       door(OFFICE_DOOR, "north"),
       sound((x, y + 1, z), "entity.zombie.attack_wooden_door", 1.2, .8),
       sound((x, y + 1, z), "block.wooden_door.close", 1, .6, "block"),
       [setblock(p, f"minecraft:{kind}[candles={n},lit=false]") for p, kind, n in OFFICE_CANDLES],
       sound_at_player("block.candle.extinguish", 1, .8, source="block"),
       "effect give @a minecraft:darkness 3 0 true")

    fn("event/cstalk_vanish",
       "scoreboard players set #cstalk s9 2",
       lamp("C1", False),
       "tp @e[tag=s9_cstalk] 0 -200 0",
       "kill @e[tag=s9_cstalk]",
       sound((8.5, 42, 19.5), "entity.enderman.teleport", .5, .4),
       sched("fx/c1_on", 25))

    # --- the mirror --------------------------------------------------------------------
    fn("event/mirror_1",
       "scoreboard players set #mirror s9 1",
       summon_stalker((12.5, 41, 2.5), 0, "s9_mirror"),
       sound((12.5, 42, 9.8), "entity.player.breath", .5, .5))
    fn("event/mirror_2",
       "scoreboard players set #mirror s9 2",
       "tp @e[tag=s9_mirror] 0 -200 0",
       "kill @e[tag=s9_mirror]",
       setblock((12, 42, 6), "minecraft:air"),
       "particle minecraft:block minecraft:light_gray_stained_glass 12.5 42.5 6.5 0.3 0.3 0.1 1 40 force",
       sound((12.5, 42.5, 6.5), "block.glass.break", 1.4, .7, "block"),
       lamp("W1", False), lamp("R1", False),
       "effect give @a minecraft:darkness 3 0 true")

    # --- containment door --------------------------------------------------------------
    fn("event/keypad",
       setblock(KEYPAD, "minecraft:stone_button[face=wall,facing=north]"),
       f"execute if score #stage s9 matches 3 run {call('event/k_open')}",
       f"execute if score #stage s9 matches 2 run {call('event/k_deny')}")
    fn("event/k_open",
       "scoreboard players set #stage s9 4",
       fill(*CONTAIN_N_DOOR, "minecraft:air"),
       sound(KEYPAD, "block.note_block.pling", 1, 2, "block"),
       sound((30.5, 42, 21), "block.iron_door.open", 1, .6, "block"),
       sound((30.5, 42, 21), "block.piston.contract", 1, .6, "block"),
       f"data modify block {KEYPAD_SIGN[0]} {KEYPAD_SIGN[1]} {KEYPAD_SIGN[2]} front_text.messages set value "
       f"[{snbt(txt('ACCESS'))},{snbt(txt('GRANTED'))},'\"\"','\"\"']",
       f"data modify block {KEYPAD_SIGN[0]} {KEYPAD_SIGN[1]} {KEYPAD_SIGN[2]} front_text.color set value \"lime\"")
    fn("event/k_deny",
       "title @a actionbar " + txt("ACCESS DENIED - LEVEL 3 KEYCARD REQUIRED", color="red"),
       sound(KEYPAD, "block.note_block.bass", 1, .5, "block"),
       f"execute if score #kdeny s9 matches 0 run {call('event/k_deny_hint')}")
    fn("event/k_deny_hint",
       "scoreboard players set #kdeny s9 1",
       radio("Ops: Keycard lock? Try the staff office - north side of the corridor."))

    fn("event/k_scare_1",
       "scoreboard players set #kscare s9 1",
       lamp("K1", False),
       sound(LAMPS["K1"], "block.redstone_torch.burnout", .3, 1.4, "block"),
       sched("event/k_scare_2", 6))
    fn("event/k_scare_2",
       lamp("K1", True),
       summon_stalker((31.5, 41, 29.5), 180, "s9_cell"),
       sched("event/k_scare_3", 35))
    fn("event/k_scare_3",
       lamp("K1", False), lamp("K2", False),
       "tp @e[tag=s9_cell] 0 -200 0",
       "kill @e[tag=s9_cell]",
       sound_at_player("entity.elder_guardian.curse", 1, .6),
       "effect give @a minecraft:darkness 3 0 true",
       sched("event/k_scare_4", 40))
    fn("event/k_scare_4",
       lamp("K1", True),
       radio("Ops: You still with me? Your camera cut out for a second."))

    fn("event/got_fuse",
       "scoreboard players set #stage s9 5",
       radio("Ops: A fuse? Good. Get it into Generator B."),
       sound_at_player("entity.warden.heartbeat", 1, .9),
       objective("Bring the fuse to Generator B"))

    fn("event/gen_hint",
       "scoreboard players set #ghint s9 1",
       radio("Ops: No fuse? There are spares in Containment. That door needs a Level 3 keycard."))

    fn("event/lever",
       f"execute if score #stage s9 matches 5 run {call('gen/1')}",
       f"execute unless score #stage s9 matches 5..6 run {call('event/lever_no')}")
    fn("event/lever_no",
       setblock(LEVER, "minecraft:lever[face=wall,facing=west]"),
       sound(LEVER, "block.lever.click", 1, .5, "block"),
       "title @a actionbar " + txt("Generator B: FUSE MISSING", color="red"))

    fn("event/steam",
       "scoreboard players set #steam s9 1",
       "particle minecraft:campfire_signal_smoke 46.5 42.5 35.6 0.2 0.4 0.1 0.03 60 force",
       sound((46.5, 42.5, 35.5), "block.fire.extinguish", 1.3, .6, "block"),
       sound((46.5, 42.5, 35.5), "entity.generic.extinguish_fire", 1.3, .5, "block"),
       "scoreboard players set #shake s9 4", sched("fx/shake", 1))


def generator_and_chase():
    fn("gen/1",
       "scoreboard players set #stage s9 6",
       "clear @a minecraft:blaze_rod{s9fuse:1b}",
       f"data modify block {GEN_SIGN[0]} {GEN_SIGN[1]} {GEN_SIGN[2]} front_text.messages[1] set value {snbt(txt('FUSE: OK'))}",
       f"data modify block {GEN_SIGN[0]} {GEN_SIGN[1]} {GEN_SIGN[2]} front_text.color set value \"lime\"",
       call("build/lamps_all_on"),
       sound((55, 42, 20), "block.beacon.activate", 1.5, .7, "block"),
       sound((55, 42, 20), "block.piston.extend", 1, .5, "block"),
       sound((55, 42, 20), "block.respawn_anchor.charge", 1, .6, "block"),
       "title @a actionbar " + txt("POWER RESTORED", color="green"),
       radio("Ops: POWER'S UP! Every level is lighting up on my board -"),
       sched("gen/2", 70))

    fn("gen/2",
       radio("Ops: ...wait. Containment B9 reads OPEN. It's read open for six weeks-"),
       fill(*GEN_W_DOOR, "minecraft:iron_block"),
       sound((49, 42, 20), "block.iron_door.close", 1.5, .5, "block"),
       sound((49, 42, 20), "block.anvil.land", 1, .5, "block"),
       "title @a actionbar " + txt("!! LOCKDOWN !!", color="red", bold=True),
       "scoreboard players set #alarm s9 18", sched("fx/alarm", 1),
       sched("gen/3", 50))

    bang = lambda v: [sound((48, 42, 20), "entity.zombie.attack_iron_door", v, .6),
                      sound((48, 42, 20), "entity.ravager.attack", v * .7, .5),
                      "scoreboard players set #shake s9 6", sched("fx/shake", 1)]
    fn("gen/3", bang(1.2), sched("gen/3b", 22))
    fn("gen/3b", bang(1.6), lamp("G1", False), lamp("G3", False), sched("gen/3c", 16))
    fn("gen/3c",
       bang(2.0),
       call("build/lamps_all_off"), call("build/emergency_on"),
       sound((47, 42, 20), "entity.warden.roar", 1.5, .8),
       "effect give @a minecraft:darkness 3 0 true",
       fill(*GEN_S_DOOR, "minecraft:air"), fill(*CONTAIN_S_DOOR, "minecraft:air"),
       sound((58.5, 42, 26), "block.piston.contract", 1.2, .5, "block"),
       f"spawnpoint @a {CHECKPOINT[0]} {CHECKPOINT[1]} {CHECKPOINT[2]}",
       radio("Ops: IT'S AT THE DOOR! Maintenance tunnel - south side - get back to the lift! RUN!"),
       "title @a times 5 30 10",
       "title @a title " + txt(" "),
       "title @a subtitle " + txt("RUN", color="dark_red", bold=True),
       sched("gen/4", HUNTER_HEADSTART))

    fn("gen/4",
       fill(*GEN_W_DOOR, "minecraft:air"),
       "particle minecraft:explosion 49.5 42 20 0.3 0.8 0.5 0 6 force",
       sound((49.5, 42, 20), "entity.generic.explode", 1.2, .6),
       call("chase/release_now"))

    fn("chase/release_now",
       summon_hunter(HUNTER_ENTRY),
       sound(HUNTER_ENTRY, "entity.warden.emerge", 1.2, .9),
       "scoreboard players set #hunter s9 1",
       "scoreboard players set #ct s9 0")
    fn("chase/release",
       "# only if the chase is still on",
       f"execute if score #stage s9 matches 6 run {call('chase/release_now')}")

    fn("chase/pulse",
       "scoreboard players set #ct s9 0",
       f"execute if score #hunter s9 matches 1 run {call('chase/trail')}",
       "execute at @e[tag=s9_hunter] run playsound minecraft:entity.warden.step hostile @a ~ ~ ~ 1.4 0.6",
       "execute as @a at @s if entity @e[tag=s9_hunter,distance=..12] run playsound minecraft:entity.warden.heartbeat master @s ~ ~ ~ 1 1.2",
       "execute store result score #r s9 run random value 1..6",
       "execute if score #r s9 matches 1 at @e[tag=s9_hunter] run playsound minecraft:entity.wither_skeleton.ambient hostile @a ~ ~ ~ 1.2 0.4")

    fn("chase/trail",
       "# breadcrumbs: if it falls too far behind, it reappears where you were 3 seconds ago",
       'execute at @a run summon minecraft:marker ~ ~ ~ {Tags:["s9","s9_trail"]}',
       "scoreboard players add @e[tag=s9_trail] s9_age 1",
       "kill @e[tag=s9_trail,scores={s9_age=13..}]",
       f"execute as @e[tag=s9_hunter] at @s unless entity @a[distance=..{HUNTER_LEASH}] "
       "run tp @s @e[tag=s9_trail,scores={s9_age=6},limit=1]")

    fn("chase/died",
       "scoreboard players set @s s9_deaths 0",
       "scoreboard players add #deaths s9 1",
       "scoreboard players set #hunter s9 0",
       "tp @e[tag=s9_hunter] 0 -200 0",
       "kill @e[tag=s9_hunter]",
       "kill @e[tag=s9_trail]",
       "effect give @a minecraft:darkness 5 0 true",
       "title @a times 10 60 20",
       "title @a title " + txt(" "),
       "title @a subtitle " + txt("It lets you go. For now.", color="dark_red"),
       sched("chase/release", RESPAWN_GRACE))


def ending():
    fn("end/1",
       "scoreboard players set #stage s9 7",
       "scoreboard players set #hunter s9 0",
       "scoreboard players set #alarm s9 0",
       f"tp @a[{box_selector(*DOORWAY_BOX)}] 3.5 41 20 90 0",
       fill(*ELEVATOR_DOOR, "minecraft:iron_block"),
       sound((6, 42, 20), "block.iron_door.close", 1.5, .5, "block"),
       sound((6, 42, 20), "block.anvil.land", 1, .6, "block"),
       "tp @e[tag=s9_hunter] 0 -200 0",
       "kill @e[tag=s9_hunter]",
       "kill @e[tag=s9_trail]",
       lamp("E1", True),
       radio("Ops: I've got you! Hold on - bringing you up!"),
       sched("end/2", 20))
    knock = lambda v: [sound((7, 42, 20), "entity.zombie.attack_iron_door", v, .5),
                       "scoreboard players set #shake s9 5", sched("fx/shake", 1)]
    fn("end/2", knock(1.4), sched("end/3", 22))
    fn("end/3", knock(1.8), "scoreboard players set #ride s9 10", sched("end/ride", 25))

    ride = ["scoreboard players remove #ride s9 1",
            sound_at_player("entity.minecart.riding", .5, .7, source="block"),
            sound_at_player("block.chain.step", .6, .6, source="block")]
    for n in range(1, 10):
        ride.append(f"execute if score #ride s9 matches {n} run title @a actionbar " + txt(f"^  B{n}", color="dark_gray"))
    ride += [f"execute if score #ride s9 matches 2.. run {sched('end/ride', 28)}",
             f"execute if score #ride s9 matches ..1 run {call('end/4')}"]
    fn("end/ride", ride)

    fn("end/4",
       "title @a times 20 80 20",
       "title @a title " + txt("ESCAPED", color="green", bold=True),
       "title @a subtitle " + txt("Station 9  -  Level B9", color="gray"),
       sound_at_player("block.beacon.deactivate", 1, .8, source="block"),
       sched("end/5", 140))
    fn("end/5",
       lamp("E1", False),
       sound_at_player("entity.warden.sniff", 1.2, .6, offset="^ ^ ^-1.5"),
       "title @a times 10 60 10",
       "title @a title " + txt(" "),
       "title @a subtitle " + txt("The lift is heavier than it should be.", color="dark_gray", italic=True),
       sched("end/6", 80))
    fn("end/6",
       "tp @a 5.3 41 20.0 90 -8",
       summon_stalker((2.6, 41, 20.0), -90, "s9_final"),
       lamp("E1", True),
       sound_at_player("entity.warden.roar", 1.6, .9),
       sound_at_player("entity.elder_guardian.curse", 1, .5),
       sched("end/7", 14))
    fn("end/7",
       lamp("E1", False),
       "tp @e[tag=s9_final] 0 -200 0",
       "kill @e[tag=s9_final]",
       "effect give @a minecraft:blindness 4 0 true",
       "title @a times 10 80 30",
       "title @a title " + txt("THE END", color="dark_red", bold=True),
       "title @a subtitle " + txt(""),
       sched("end/8", 70))

    fn("end/8",
       "scoreboard players operation #sec s9 = #time s9",
       "scoreboard players operation #sec s9 /= #20 s9",
       "scoreboard players operation #min s9 = #sec s9",
       "scoreboard players operation #min s9 /= #60 s9",
       "scoreboard players operation #sec s9 %= #60 s9",
       'tellraw @a ["",' + txt("\n  S T A T I O N   9\n", color="dark_red", bold=True) + "]",
       'tellraw @a ["",' + txt("  Time: ", color="gray") + ',{"score":{"name":"#min","objective":"s9"},"color":"white"},'
       + txt("m ", color="white") + ',{"score":{"name":"#sec","objective":"s9"},"color":"white"},' + txt("s", color="white")
       + "," + txt("     Deaths: ", color="gray") + ',{"score":{"name":"#deaths","objective":"s9"},"color":"white"}]',
       'tellraw @a ["",' + txt("  ") + "," + json.dumps({
           "text": "[ Play again ]", "color": "gold", "bold": True,
           "clickEvent": {"action": "run_command", "value": f"/function {NS}:start"},
           "hoverEvent": {"action": "show_text", "contents": "Rebuild the station and start over"}}) + "]",
       'tellraw @a ""')


# =========================================================================
# OUTPUT
# =========================================================================
def png(width, height, pixels):
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in pixels)
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def icon():
    glyph = ["01110", "10001", "10001", "01111", "00001", "00010", "11100"]   # a "9"
    n = 64
    px = []
    for y in range(n):
        row = []
        for x in range(n):
            v = 14 + int(10 * (1 - abs(x - 32) / 32) * (1 - abs(y - 32) / 32))
            c = (v, v, v + 2)
            gx, gy = (x - 17) // 6, (y - 11) // 6
            if 0 <= gx < 5 and 0 <= gy < 7 and x >= 17 and y >= 11 and glyph[gy][gx] == "1":
                c = (150 + rng.randint(0, 40), 10, 12)
            row.append(c)
        px.append(row)
    return png(n, n, px)


def write():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    base = os.path.join(OUT, "data", NS, "functions")
    for name, lines in files.items():
        path = os.path.join(base, name + ".mcfunction")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    tags = os.path.join(OUT, "data", "minecraft", "tags", "functions")
    os.makedirs(tags)
    for tag in ("load", "tick"):
        with open(os.path.join(tags, tag + ".json"), "w") as f:
            json.dump({"values": [f"{NS}:{tag}"]}, f, indent=2)
    with open(os.path.join(OUT, "pack.mcmeta"), "w") as f:
        json.dump({"pack": {"pack_format": 26, "description": "§4STATION 9§7 - a short horror map"}}, f, indent=2)
    with open(os.path.join(OUT, "pack.png"), "wb") as f:
        f.write(icon())
    count = sum(len(v) for v in files.values())
    print(f"Wrote {len(files)} functions, {count} commands, {len(EMERGENCY)} emergency lights -> {OUT}")


if __name__ == "__main__":
    build()
    effects()
    ticks()
    intro()
    events()
    generator_and_chase()
    ending()
    core()          # last: reset needs the full list of scheduled functions
    write()
