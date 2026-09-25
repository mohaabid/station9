#!/usr/bin/env python3
"""
Turn a server-built world folder into a singleplayer save:
renames the level, turns cheats on (for the restart button) and adds the icon.

    python3 package_world.py <server world dir> <output save dir>
"""
import gzip
import io
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --- minimal NBT reader/writer -------------------------------------------------
END, BYTE, SHORT, INT, LONG, FLOAT, DOUBLE, BYTES, STRING, LIST, COMPOUND, INTS, LONGS = range(13)
SIMPLE = {BYTE: ">b", SHORT: ">h", INT: ">i", LONG: ">q", FLOAT: ">f", DOUBLE: ">d"}


def read_payload(f, t):
    if t in SIMPLE:
        fmt = SIMPLE[t]
        return struct.unpack(fmt, f.read(struct.calcsize(fmt)))[0]
    if t == STRING:
        n = struct.unpack(">H", f.read(2))[0]
        return f.read(n).decode("utf-8")
    if t in (BYTES, INTS, LONGS):
        n = struct.unpack(">i", f.read(4))[0]
        size = {BYTES: 1, INTS: 4, LONGS: 8}[t]
        return (t, f.read(n * size), n)
    if t == LIST:
        et = f.read(1)[0]
        n = struct.unpack(">i", f.read(4))[0]
        return (LIST, et, [read_payload(f, et) for _ in range(n)])
    if t == COMPOUND:
        out = {}
        while True:
            ct = f.read(1)[0]
            if ct == END:
                return out
            name = read_payload(f, STRING)
            out[name] = (ct, read_payload(f, ct))
    raise ValueError(f"bad tag {t}")


def write_payload(f, t, v):
    if t in SIMPLE:
        f.write(struct.pack(SIMPLE[t], v))
    elif t == STRING:
        b = v.encode("utf-8")
        f.write(struct.pack(">H", len(b)) + b)
    elif t in (BYTES, INTS, LONGS):
        f.write(struct.pack(">i", v[2]) + v[1])
    elif t == LIST:
        _, et, items = v
        f.write(bytes([et]) + struct.pack(">i", len(items)))
        for it in items:
            write_payload(f, et, it)
    elif t == COMPOUND:
        for name, (ct, cv) in v.items():
            f.write(bytes([ct]))
            write_payload(f, STRING, name)
            write_payload(f, ct, cv)
        f.write(bytes([END]))


def load(path):
    with gzip.open(path, "rb") as g:
        f = io.BytesIO(g.read())
    t = f.read(1)[0]
    name = read_payload(f, STRING)
    return name, read_payload(f, t)


def save(path, name, root):
    f = io.BytesIO()
    f.write(bytes([COMPOUND]))
    write_payload(f, STRING, name)
    write_payload(f, COMPOUND, root)
    with gzip.open(path, "wb") as g:
        g.write(f.getvalue())


# --------------------------------------------------------------------------------
def main(src, dst):
    if os.path.exists(dst):
        sys.exit(f"{dst} already exists - not overwriting it")
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("session.lock", "level.dat_old"))
    name, root = load(os.path.join(dst, "level.dat"))
    data = root["Data"][1]
    data["LevelName"] = (STRING, "Station 9")
    data["allowCommands"] = (BYTE, 1)
    save(os.path.join(dst, "level.dat"), name, root)
    shutil.copy(os.path.join(HERE, "Station9", "pack.png"), os.path.join(dst, "icon.png"))
    check = load(os.path.join(dst, "level.dat"))[1]["Data"][1]
    print("LevelName:", check["LevelName"][1], "| allowCommands:", check["allowCommands"][1],
          "| GameType:", check["GameType"][1], "| spawn:", check["SpawnX"][1], check["SpawnY"][1], check["SpawnZ"][1])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
