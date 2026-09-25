"""Scripted playthrough with a bot player. Run sections: python3 tests/play.py act0 [act1 ...]"""
import json
import sys
import time

sys.path.insert(0, __import__("os").path.dirname(__file__))
from bot import Bot   # noqa: E402
from rcon import Rcon  # noqa: E402

r = Rcon()
b = None


def score(name):
    out = r.cmd(f"scoreboard players get #{name} s9")
    try:
        return int(out.split(" has ")[1].split(" ")[0])
    except Exception:
        return None


def show_log(filt=None):
    for e in b.log():
        text = e.get("text", "")
        if e["kind"] == "sound" and "station9" not in text:
            continue
        if filt and not any(f in text for f in filt):
            continue
        print(f"   [{e['kind']}] {text[:150]}")


def wait_stage(n, timeout=120):
    t = time.time()
    while time.time() - t < timeout:
        if score("stage") == n:
            return True
        time.sleep(0.5)
    print("   !! stage", score("stage"), "expected", n)
    return False


def step(msg):
    print(f"== {msg}  (stage {score('stage')}, pos {fmtpos()})")


def fmtpos():
    p = b.pos() if b else None
    return f"{p['x']:.1f},{p['y']:.1f},{p['z']:.1f}" if p else "-"


def act0():
    step("waiting for the opening shots to end")
    assert wait_stage(2, 90)
    time.sleep(1)
    step("on the surface")
    print("  ", b.route(points=[[64, 18.5], [50, 19], [34, 22], [33.5, 24.8]]))
    print("  ", b.use_block(x=33, y=101, z=26))
    print("  ", b.route(points=[[33.5, 26.5], [33.5, 28.5]]))
    step("in the hut")
    print("  ", b.use_block(x=36, y=101, z=27))
    time.sleep(1)
    print("  ", b.open_take(x=31, y=101, z=31))
    time.sleep(2)
    print("   inventory:", b.inv())
    print("   kit flag:", score("kit"))
    show_log()
    step("to the lift house")
    print("  ", b.route(points=[[33.5, 25.5], [33, 22], [14, 19.5], [8.5, 20.5]]))
    print("  ", b.use_block(x=7, y=102, z=21))
    time.sleep(11)
    print("   gate:", b.block(x=6, y=101, z=19))
    print("  ", b.route(points=[[5.5, 20], [3.5, 20]]))
    time.sleep(1)
    print("  ", b.use_block(x=3, y=102, z=18))
    time.sleep(3)
    step("riding")
    show_log()
    assert wait_stage(4, 90)
    step("arrived B8")
    show_log()


def act1():
    step("B8: door release")
    print("  ", b.use_block(x=2, y=52, z=19))
    time.sleep(3.5)
    print("   gate:", b.block(x=6, y=51, z=19), b.block(x=6, y=53, z=19))
    print("  ", b.route(points=[[5.5, 20], [8.5, 19.5], [13, 17.5], [21, 17], [37.5, 17]]))
    print("  ", b.use_block(x=38, y=51, z=18))
    print("  ", b.route(points=[[38.5, 18.6], [38.5, 22], [39.6, 24.3]]))
    print("  ", b.use_block(x=40, y=52, z=25))
    time.sleep(2)
    print("   relay flag", score("s_relay"))
    time.sleep(38)
    show_log()
    step("security keypad")
    print("  ", b.route(points=[[38.5, 22], [38.5, 18.6], [38.5, 17], [47.5, 17]]))
    print("  ", b.use_block(x=47, y=51, z=18))
    print("  ", b.route(points=[[47.5, 18.6], [47.5, 21.5]]))
    for d in "0214":
        pos = {"0": (49, 51, 23), "1": (49, 53, 20), "2": (49, 53, 21), "3": (49, 53, 22), "4": (49, 52, 20)}[d]
        print("   key", d, b.use_block(x=pos[0], y=pos[1], z=pos[2]))
        time.sleep(0.4)
    time.sleep(1)
    print("   code flag", score("s_code"), "stair door", b.block(x=11, y=51, z=21))
    show_log()
    step("phone in the cafeteria")
    print("  ", b.route(points=[[47.5, 18.6], [47.5, 17], [45, 17], [45, 14], [45, 8]]))
    time.sleep(2)
    print("  ", b.use_block(x=46, y=52, z=4))
    time.sleep(16)
    show_log()
    step("lab and tape")
    print("  ", b.route(points=[[45, 14], [45, 17], [27, 17], [27, 18.6], [27, 22]]))
    b.lookat(x=26.5, y=52.5, z=30.5)
    time.sleep(2.5)
    print("   window flag", score("window"))
    print("  ", b.route(points=[[29.5, 24], [30.5, 25.2]]))
    print("  ", b.use_block(x=30, y=51, z=26))
    print("  ", b.route(points=[[30.5, 27], [23.5, 30.5]]))
    print("  ", b.use_block(x=22, y=52, z=30))
    time.sleep(4)
    show_log()
    step("to the stairs")
    print("  ", b.route(points=[[30.5, 27.5], [30.5, 25.2], [27, 22], [27, 18.6], [27, 17], [20, 17], [12, 19.5], [12, 21.2]]))
    print("  ", b.route(points=[[12, 23], [12, 29.5], [10.5, 30.3], [9, 29.2], [9, 22.8], [9, 20.3]]))
    time.sleep(2)
    show_log()
    print("   stage", score("stage"))


def watch_state():
    return {k: score(k) for k in ("hmode", "hnode", "hnext", "htarget", "watched", "cand", "los", "lit", "frozen", "teach", "tw", "pnode")}


def act2_teach():
    step("look at it")
    b.lookat(x=48.0, y=43.1, z=20.0)
    for i in range(8):
        time.sleep(1)
        print("  ", watch_state(), r.cmd("data get entity @e[tag=s9_hunter,limit=1] Pos"))
        b.lookat(x=float(r.cmd("data get entity @e[tag=s9_hunter,limit=1] Pos[0]").split(": ")[-1].rstrip("d")), y=43.1, z=20.0)
    show_log()
    step("look away")
    b.look(yaw=0, pitch=0)
    for i in range(10):
        time.sleep(1)
        print("  ", watch_state())
    show_log()

def hpos():
    out = r.cmd("data get entity @e[tag=s9_hunter,limit=1] Pos")
    try:
        return [round(float(v.strip().rstrip("d")), 1) for v in out.split("[")[1].split("]")[0].split(",")]
    except Exception:
        return None


def ai_state():
    return {k: score(k) for k in ("hmode", "hnode", "hnext", "htarget", "hspd", "hwait", "hgrace", "watched", "frozen", "los", "sees", "pnode")}


def roam():
    print(r.cmd("function station9:debug/roam"))
    time.sleep(2)
    step("roaming: watch where it goes for 25 s (player faces west, away)")
    b.look(yaw=1.57, pitch=0)
    for i in range(25):
        time.sleep(1)
        print("  ", hpos(), ai_state())
    show_log()


def noise():
    step("sprint back and forth near the office")
    b.route(points=[[15.5, 20], [30, 20], [15.5, 20]], sprint=True)
    for i in range(12):
        time.sleep(1)
        print("  ", hpos(), ai_state())
    show_log()


def hide():
    step("hide in the locker at 24 41 18")
    print(b.route(points=[[24.5, 19.6]]))
    print(b.use_block(x=24, y=41, z=18))
    print(b.route(points=[[24.5, 18.5]], tol=0.2))
    print(b.use_block(x=24, y=41, z=18))
    time.sleep(1)
    print("   hidden:", score("hidden"), r.cmd("execute if entity @a[tag=s9_hidden]"))
    for i in range(10):
        time.sleep(1)
        print("  ", hpos(), ai_state())
    show_log()


def caught():
    step("stand in front of it in the dark, facing away")
    h = hpos()
    r.cmd(f"tp @a {h[0] - 3} 41 {h[2]} 90 0")
    for i in range(8):
        time.sleep(1)
        print("  ", hpos(), ai_state(), "deaths", score("deaths"))
    show_log()



# --- main ---

if __name__ == "__main__":
    b = Bot()
    try:
        for sec in sys.argv[1:]:
            globals()[sec]()
    finally:
        print("final pos", fmtpos(), "stage", score("stage"))
        b.close()
