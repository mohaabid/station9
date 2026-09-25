"""The resource pack (1.20.4, pack_format 22): our sounds, a new skin for Subject 9,
metal lockers, and icons for the flashlight, batteries, keycard and fuse.

Textures are painted here in code, so the whole pack rebuilds from this repository."""
import json
import os
import random
import re
import shutil
import struct
import zlib

from .mc import manifest

rng = random.Random(99)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# vanilla sounds that tick or click on their own; silenced as a safety net
MUTE = ["block.candle.ambient", "block.sculk_sensor.clicking", "block.sculk_sensor.clicking_stop",
        "block.sculk_shrieker.shriek", "block.sculk.spread", "block.redstone_torch.burnout"]


def png(w, h, px):
    """px: rows of (r,g,b,a)."""
    raw = b"".join(b"\x00" + bytes(c for p in row for c in p) for row in px)
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def canvas(w, h, c=(0, 0, 0, 0)):
    return [[c for _ in range(w)] for _ in range(h)]


def rect(px, x, y, w, h, c, jitter=0):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if jitter:
                j = rng.randint(-jitter, jitter)
                px[yy][xx] = (max(0, min(255, c[0] + j)), max(0, min(255, c[1] + j)), max(0, min(255, c[2] + j)), c[3])
            else:
                px[yy][xx] = c


# --- Subject 9 --------------------------------------------------------------------------------
SKIN = (214, 208, 198, 255)
SKIN_D = (170, 162, 152, 255)
SKIN_DD = (118, 110, 104, 255)
VOID = (8, 6, 8, 255)


def subject9():
    px = canvas(64, 32)
    # head (0,0) 8x8x8: top, bottom, sides, face, back
    rect(px, 8, 0, 8, 8, SKIN_D, 10)       # top
    rect(px, 16, 0, 8, 8, SKIN_DD, 8)      # bottom
    rect(px, 0, 8, 8, 8, SKIN_D, 10)       # right side
    rect(px, 8, 8, 8, 8, SKIN, 8)          # face
    rect(px, 16, 8, 8, 8, SKIN_D, 10)      # left side
    rect(px, 24, 8, 8, 8, SKIN_D, 10)      # back
    # a long, empty face: two tall black eyes, a thin mouth that is too wide
    for x, y in [(9, 10), (10, 10), (9, 11), (10, 11), (9, 12), (10, 12), (13, 10), (14, 10), (13, 11), (14, 11), (13, 12), (14, 12)]:
        px[y][x] = VOID
    px[13][10] = SKIN_DD
    px[13][13] = SKIN_DD
    for x in range(9, 15):
        px[14][x] = (60, 30, 32, 255)
    px[15][9] = SKIN_DD
    px[15][14] = SKIN_DD
    # veins on the scalp and temples
    for x, y in [(10, 1), (11, 2), (11, 3), (12, 4), (2, 10), (3, 11), (3, 12), (18, 9), (19, 10), (26, 11), (27, 12)]:
        px[y][x] = (140, 128, 150, 255)
    # body (16,16) 8x12x4: ribs showing through
    rect(px, 20, 16, 8, 4, SKIN_D, 8)
    rect(px, 28, 16, 8, 4, SKIN_DD, 8)
    rect(px, 16, 20, 4, 12, SKIN_D, 10)
    rect(px, 20, 20, 8, 12, SKIN, 8)
    rect(px, 28, 20, 4, 12, SKIN_D, 10)
    rect(px, 32, 20, 8, 12, SKIN_D, 10)
    for y in (22, 24, 26):
        for x in range(21, 27):
            if x != 24:
                px[y][x] = SKIN_DD
    for y in range(21, 31):
        px[y][24] = SKIN_D
    for y in range(29, 32):
        for x in range(20, 28):
            px[y][x] = SKIN_D
    for y in (23, 25, 27):
        for x in range(33, 39):
            px[y][x] = SKIN_DD
    # arms (40,16) and legs (0,16), 2x12x2: pale, ending in black fingers and feet
    for ox in (40, 0):
        rect(px, ox + 2, 16, 4, 2, SKIN_D, 6)
        rect(px, ox, 18, 8, 12, SKIN, 10)
        for x in range(ox, ox + 8, 2):
            px[18 + rng.randint(2, 9)][x] = SKIN_D
        rect(px, ox, 27 if ox == 40 else 28, 8, 3 if ox == 40 else 2, (30, 26, 28, 255), 6)
    return png(64, 32, px)


# --- the metal locker door (replaces the warped door) -------------------------------------------------
STEEL = (104, 110, 116, 255)
STEEL_D = (70, 75, 80, 255)
STEEL_L = (140, 146, 150, 255)


def locker_door(top):
    px = canvas(16, 16)
    rect(px, 0, 0, 16, 16, STEEL, 6)
    for i in range(16):
        px[i][0] = STEEL_D
        px[i][15] = STEEL_D
    if top:
        for i in range(16):
            px[0][i] = STEEL_D
        for y in (3, 5, 7, 9):            # vents you can peek through
            for x in range(4, 12):
                px[y][x] = (0, 0, 0, 0)
            for x in range(4, 12):
                px[y + 1][x] = STEEL_L
        rect(px, 5, 12, 6, 2, (200, 196, 180, 255))     # name plate
    else:
        for i in range(16):
            px[15][i] = STEEL_D
        rect(px, 11, 1, 2, 4, (40, 42, 44, 255))         # handle
        rect(px, 4, 9, 8, 1, STEEL_D)
        rect(px, 4, 12, 8, 1, STEEL_D)
    return png(16, 16, px)


def locker_item():
    px = canvas(16, 16)
    rect(px, 4, 1, 8, 14, STEEL, 6)
    for y in (3, 5, 7):
        rect(px, 6, y, 4, 1, (20, 20, 20, 255))
    rect(px, 10, 9, 1, 3, (40, 42, 44, 255))
    return png(16, 16, px)


# --- item icons ---------------------------------------------------------------------------------------
def sprite(rows, palette):
    px = canvas(16, 16)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                px[y][x] = palette[ch]
    return png(16, 16, px)


FLASHLIGHT = ["................", "................", "...........yy...", "..........yWWy..", ".........yWWWy..",
              "........sWWWy...", ".......sbsyy....", "......bbbs......", ".....bbbb.......", "....bbbb........",
              "...bbbb.........", "..bbbb..........", "..bbb...........", "..bb............", "................",
              "................"]
BATTERY = ["................", "................", "......gg........", ".....kkkk.......", ".....oooo.......",
           ".....oooo.......", ".....oOoo.......", ".....oOoo.......", ".....oooo.......", ".....kkkk.......",
           ".....kkkk.......", ".....kkkk.......", ".....kkkk.......", ".....kkkk.......", "................",
           "................"]
KEYCARD = ["................", "................", "................", "..wwwwwwwwwwww..", "..wwwwwwwwwwww..",
           "..BBBBBBBBBBBB..", "..wwwwwwwwwwww..", "..wyyww.kkkkww..", "..wyyww.kkkkww..", "..wwwww.kkkkww..",
           "..wwwwwwwwwwww..", "..wwwwwwwwwwww..", "................", "................", "................",
           "................"]
FUSE = ["................", "............ss..", "...........sSs..", "..........sgs...", ".........ggg....",
        "........grg.....", ".......grg......", "......grg.......", ".....ggg........", "....sgs.........",
        "...sSs..........", "...ss...........", "................", "................", "................",
        "................"]

PAL = {"y": (255, 236, 150, 255), "W": (255, 255, 220, 255), "s": (170, 170, 176, 255), "b": (36, 36, 40, 255),
       "g": (160, 160, 150, 255), "k": (30, 30, 30, 255), "o": (214, 120, 40, 255), "O": (250, 200, 120, 255),
       "w": (230, 232, 236, 255), "B": (50, 110, 200, 255), "S": (220, 220, 225, 255), "r": (220, 60, 40, 255)}

ITEM_MODELS = {  # vanilla item -> (custom model data, our model name, parent)
    "carrot_on_a_stick": (9101, "flashlight", "item/handheld_rod", "item/carrot_on_a_stick"),
    "iron_nugget": (9102, "battery", "item/generated", "item/iron_nugget"),
    "tripwire_hook": (9103, "keycard", "item/generated", "block/tripwire_hook"),
    "blaze_rod": (9104, "fuse", "item/handheld", "item/blaze_rod"),
}


def sounds_json():
    m = manifest()
    events = {}
    for name, info in sorted(m.items()):
        kind, base = name.split("/", 1)
        event = kind + "." + re.sub(r"_\d+$", "", base)
        entry = {"name": f"station9:{name}"}
        if info["dur"] > 4.0:
            entry["stream"] = True
        events.setdefault(event, {"sounds": []})["sounds"].append(entry)
    # a little pitch spread on the creature's footsteps
    for ev in ("sfx.step", "sfx.roof_step"):
        extra = [dict(s, pitch=p) for s in events[ev]["sounds"] for p in (0.9, 1.1)]
        events[ev]["sounds"] += extra
    for ev in MUTE:
        events[ev] = {"replace": True, "sounds": [{"name": "station9:sfx/silent"}]}
    events["block.nether_wood_door.open"] = {"replace": True, "sounds": [{"name": "station9:sfx/locker_open"}]}
    events["block.nether_wood_door.close"] = {"replace": True, "sounds": [{"name": "station9:sfx/locker_close"}]}
    return events


def write(out_dir, icon_png):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    def put(rel, data):
        path = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        mode = "wb" if isinstance(data, bytes) else "w"
        with open(path, mode) as f:
            f.write(data)

    put("pack.mcmeta", json.dumps({"pack": {"pack_format": 22, "description": "§4STATION 9§7 - sounds and textures"}}, indent=2))
    put("pack.png", icon_png)
    put("assets/station9/sounds.json", json.dumps(sounds_json(), indent=1))
    src = os.path.join(ROOT, "assets", "sounds")
    for name in manifest():
        shutil.copy(os.path.join(src, name + ".ogg"), os.path.join(_mk(out_dir, f"assets/station9/sounds/{name}.ogg")))
    put("assets/minecraft/textures/entity/skeleton/wither_skeleton.png", subject9())
    put("assets/minecraft/textures/block/warped_door_top.png", locker_door(True))
    put("assets/minecraft/textures/block/warped_door_bottom.png", locker_door(False))
    put("assets/minecraft/textures/item/warped_door.png", locker_item())
    for vanilla, (cmd, name, parent, tex) in ITEM_MODELS.items():
        put(f"assets/minecraft/models/item/{vanilla}.json", json.dumps({
            "parent": parent, "textures": {"layer0": tex},
            "overrides": [{"predicate": {"custom_model_data": cmd}, "model": f"station9:item/{name}"}]}, indent=1))
        put(f"assets/station9/models/item/{name}.json", json.dumps({
            "parent": "item/handheld" if name == "flashlight" else "item/generated",
            "textures": {"layer0": f"station9:item/{name}"}}, indent=1))
    for name, rows in [("flashlight", FLASHLIGHT), ("battery", BATTERY), ("keycard", KEYCARD), ("fuse", FUSE)]:
        put(f"assets/station9/textures/item/{name}.png", sprite(rows, PAL))


def _mk(out_dir, rel):
    path = os.path.join(out_dir, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path
