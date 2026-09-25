#!/usr/bin/env python3
"""
STATION 9 -- a Minecraft horror map (Java 1.20.4), generated.

    python3 generate.py

writes
    Station9/               the datapack (pack_format 26)
    build/resources/        the resource pack (pack_format 22)
    build/resources.zip     the same, zipped: goes in the world folder as resources.zip

Every coordinate lives in s9/world.py, every spoken line in s9/script.py, and the sounds
are made by tools/make_audio.py (already generated into assets/sounds). This script only
needs the Python standard library.
"""
import json
import os
import re
import shutil
import struct
import sys
import zipfile
import zlib
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from s9 import ai, build, debug, respack, story, systems  # noqa: E402
from s9.mc import NS, files, predicates  # noqa: E402

OUT = os.path.join(HERE, "Station9")
BUILD = os.path.join(HERE, "build")


def icon():
    rng = random.Random(9)
    glyph = ["01110", "10001", "10001", "01111", "00001", "00010", "11100"]   # a "9"
    n = 64
    rows = []
    for y in range(n):
        row = []
        for x in range(n):
            v = 14 + int(10 * (1 - abs(x - 32) / 32) * (1 - abs(y - 32) / 32))
            c = (v, v, v + 2)
            gx, gy = (x - 17) // 6, (y - 11) // 6
            if 0 <= gx < 5 and 0 <= gy < 7 and x >= 17 and y >= 11 and glyph[gy][gx] == "1":
                c = (150 + rng.randint(0, 40), 10, 12)
            row.append(c + (255,))
        rows.append(row)
    return respack.png(n, n, rows)


def check():
    """Every function we call or schedule must exist, and no line may be empty."""
    missing = set()
    for name, lines in files.items():
        for line in lines:
            if line.startswith("$"):
                continue
            for ref in re.findall(rf"function {NS}:([a-z0-9_/.\-]+)", line):
                if ref not in files:
                    missing.add((name, ref))
            for ref in re.findall(rf"{NS}:([a-z0-9_/]+)", line):
                pass
    if missing:
        for m in sorted(missing):
            print("  missing function:", m)
        sys.exit("generation failed")
    for name, lines in files.items():
        for line in lines:
            for sel in re.findall(r"@[aesp]\[([^\]]*)\]", line):
                keys = {kv.split("=")[0] for kv in sel.split(",") if "=" in kv}
                if keys & {"dx", "dy", "dz"} and not {"x", "z", "dx", "dz"} <= keys:
                    missing.add((name, "partial volume selector " + sel))
    events = respack.sounds_json()
    for name, lines in files.items():
        for line in lines:
            for ev in re.findall(r"(?:playsound|stopsound @a \w+) station9:([a-z0-9_.]+)", line):
                if ev not in events:
                    missing.add((name, "sound " + ev))
    if missing:
        for m in sorted(missing):
            print("  missing:", m)
        sys.exit("generation failed")
    for key in re.findall(r"predicate station9:([a-z0-9_/]+)", "\n".join(l for v in files.values() for l in v)):
        if key not in predicates:
            sys.exit(f"missing predicate {key}")


def write_datapack():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    base = os.path.join(OUT, "data", NS)
    for name, lines in files.items():
        path = os.path.join(base, "functions", name + ".mcfunction")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    for name, body in predicates.items():
        path = os.path.join(base, "predicates", name + ".json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(body, f, indent=1)
    for name, values in systems.tags().items():
        path = os.path.join(base, "tags", "blocks", name + ".json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({"values": values}, f, indent=1)
    tags = os.path.join(OUT, "data", "minecraft", "tags", "functions")
    os.makedirs(tags)
    for tag in ("load", "tick"):
        with open(os.path.join(tags, tag + ".json"), "w") as f:
            json.dump({"values": [f"{NS}:{tag}"]}, f, indent=2)
    with open(os.path.join(OUT, "pack.mcmeta"), "w") as f:
        json.dump({"pack": {"pack_format": 26, "description": "§4STATION 9§7 - a horror map"}}, f, indent=2)
    with open(os.path.join(OUT, "pack.png"), "wb") as f:
        f.write(icon())


def write_resources():
    res = os.path.join(BUILD, "resources")
    respack.write(res, icon())
    zpath = os.path.join(BUILD, "resources.zip")
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, names in os.walk(res):
            for n in sorted(names):
                full = os.path.join(root, n)
                z.write(full, os.path.relpath(full, res))
    return zpath


def main():
    steps = build.build()
    systems.predicates()
    systems.player()
    systems.ambience()
    ai.build()
    flags = []
    story.build(flags)
    debug.build()
    systems.FLAGS.extend(f for f in flags if f not in systems.FLAGS)
    systems.core(steps, f"function {NS}:story/begin")
    systems.finish()
    check()
    write_datapack()
    zpath = write_resources()
    count = sum(len(v) for v in files.values())
    print(f"Wrote {len(files)} functions, {count} commands, {len(predicates)} predicates -> {OUT}")
    print(f"Resource pack -> {zpath} ({os.path.getsize(zpath) // 1024} KB)")


if __name__ == "__main__":
    main()
