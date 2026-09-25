"""Small helpers that turn Python into 1.20.4 commands."""
import json
import math
import os
import re

NS = "station9"
files = {}          # function name -> list of commands
scheduled = set()   # every function we ever schedule (reset clears them all)

_manifest = None


def manifest():
    global _manifest
    if _manifest is None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sounds", "manifest.json")
        with open(path) as f:
            _manifest = json.load(f)
    return _manifest


def flat(lines):
    for line in lines:
        if isinstance(line, (list, tuple)):
            yield from flat(line)
        elif line is not None:
            yield line


def fn(name, *lines):
    assert re.fullmatch(r"[a-z0-9_./-]+", name), f"bad function name {name!r}"
    files.setdefault(name, []).extend(flat(lines))
    return call(name)


def call(name):
    return f"function {NS}:{name}"


def sched(name, ticks, append=False):
    scheduled.add(name)
    return f"schedule function {NS}:{name} {max(1, int(ticks))}t{' append' if append else ''}"


def txt(text, **style):
    return json.dumps(dict(text=text, **style), ensure_ascii=False)


def snbt(s):
    """Quote a string for SNBT (used for JSON text stored inside NBT)."""
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def fmt(v):
    """Floats keep a decimal point: Minecraft centres whole numbers (48 -> 48.5)."""
    if isinstance(v, float):
        s = f"{v:.3f}".rstrip("0")
        return s + "0" if s.endswith(".") else s
    return str(v)


def pos(p):
    return " ".join(fmt(v) for v in p)


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


def mc(block):
    return block if ":" in block else "minecraft:" + block


# --- sound ---------------------------------------------------------------------------------
def snd(name, at, vol=1.0, pitch=1.0, source="hostile", who="@a", minvol=0):
    """A positional sound at a block position. `name` without a namespace is one of ours."""
    sid = name if ":" in name else f"{NS}:{name}"
    return f"playsound {sid} {source} {who} {pos(at)} {fmt(vol)} {fmt(pitch)} {fmt(minvol)}"


def snd_me(name, vol=1.0, pitch=1.0, source="master", offset="~ ~ ~"):
    """A sound played at each player (for stereo sounds: in their head)."""
    sid = name if ":" in name else f"{NS}:{name}"
    return f"execute as @a at @s run playsound {sid} {source} @s {offset} {fmt(vol)} {fmt(pitch)}"


def dur_ticks(sound):
    return int(math.ceil(manifest()[sound]["dur"] * 20))


# --- text ------------------------------------------------------------------------------------
def tell(parts):
    return "tellraw @a " + json.dumps([""] + parts, ensure_ascii=False)


def actionbar(text, color="gray"):
    return "title @a actionbar " + txt(text, color=color)


def sign(p, facing, lines, color="black", glow=False, wood="dark_oak", wall=True):
    msgs = [txt(l) for l in (lines + ["", "", "", ""])[:4]]
    front = f'{{color:"{color}",has_glowing_text:{1 if glow else 0}b,messages:[{",".join(snbt(m) for m in msgs)}]}}'
    kind = f"{wood}_wall_sign[facing={facing}]" if wall else f"{wood}_sign[rotation={facing}]"
    return setblock(p, f"minecraft:{kind}{{front_text:{front},is_waxed:1b}}")


def set_sign_lines(p, lines, color=None):
    msgs = ",".join(snbt(txt(l)) for l in (lines + ["", "", "", ""])[:4])
    out = [f"data modify block {pos(p)} front_text.messages set value [{msgs}]"]
    if color:
        out.append(f'data modify block {pos(p)} front_text.color set value "{color}"')
    return out


def door(p, facing, open_=False, wood="dark_oak", hinge="left"):
    x, y, z = p
    st = f"facing={facing},hinge={hinge},open={'true' if open_ else 'false'}"
    kind = wood if wood.endswith("door") else f"{wood}_door"
    return [setblock((x, y, z), f"minecraft:{kind}[{st},half=lower]"),
            setblock((x, y + 1, z), f"minecraft:{kind}[{st},half=upper]")]


def book(title, author, pages):
    ps = ",".join(snbt(txt(p)) for p in pages)
    return f'{{id:"minecraft:written_book",Count:1b,tag:{{title:{json.dumps(title)},author:{json.dumps(author)},pages:[{ps}]}}}}'


def lectern(p, facing, title, author, pages):
    return setblock(p, f"minecraft:lectern[facing={facing},has_book=true]{{Book:{book(title, author, pages)},Page:0}}")


def box_selector(a, b):
    """Players whose feet are inside the block box a..b (inclusive).

    Selector volumes match any hitbox that *touches* [x, x+dx+1], so a player standing
    in a doorway still counts. Inset by the player's half-width (0.3) so only the
    player's centre matters.
    """
    assert b[0] > a[0] and b[2] > a[2], f"box {a}..{b} too thin for a selector; use in_box()"
    return (f"x={fmt(a[0] + .3)},y={fmt(a[1])},z={fmt(a[2] + .3)},"
            f"dx={fmt(round(b[0] - a[0] - .6, 2))},dy={fmt(b[1] - a[1])},dz={fmt(round(b[2] - a[2] - .6, 2))}")


predicates = {}


def in_box(a, b):
    """`predicate ...` true when the entity's feet are inside the block box a..b (exact)."""
    key = "box/" + "_".join(str(v).replace("-", "m") for v in (*a, *b))
    predicates[key] = {"condition": "minecraft:location_check", "predicate": {"position": {
        "x": {"min": a[0], "max": b[0] + 1}, "y": {"min": a[1], "max": b[1] + 1}, "z": {"min": a[2], "max": b[2] + 1}}}}
    return f"predicate {NS}:{key}"


def near(p, r):
    return f"x={fmt(p[0])},y={fmt(p[1])},z={fmt(p[2])},distance=..{fmt(r)}"


# --- timelines -------------------------------------------------------------------------------
def timeline(name, events):
    """events: [(tick, [commands...]), ...]. Returns the command that starts it.

    Each event becomes its own function, all scheduled from the first one, so one
    `schedule clear` per step stops the whole thing.
    """
    starter = [f"# timeline {name}"]
    for i, (t, cmds) in enumerate(events):
        step = f"{name}/{i:02d}"
        fn(step, cmds)
        starter.append(call(step) if t == 0 else sched(step, t))
    return fn(name, starter)


def after(ticks, name, *cmds):
    """Run commands `ticks` from now as a named one-off function."""
    fn(name, *cmds)
    return sched(name, ticks)
