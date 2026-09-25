"""The story, act by act.

Stages (#stage):
  0 not started   1 opening shots   2 surface   3 lift ride down   4 B8
  5 B9, no card   6 has keycard     7 containment open   8 has fuse
  9 the escape    10 ride up        11 finished
"""
import json
import math

from . import ai
from . import world as W
from .build import door, fill, lamp, setblock
from .mc import (NS, actionbar, after, box_selector, call, fmt, fn, in_box, near, pos, sched, set_sign_lines, snd,
                 snd_me, timeline, txt)
from .systems import (checkpoint, clear, drop, has, item_arg, lines, objective, say, say_len)

STORY_FLAGS = []


def flag(name):
    STORY_FLAGS.append(f"#{name}")
    return f"#{name}"


def once(name, *cmds):
    """Commands that run the first time only (sets the flag)."""
    f = flag(name)
    fn(f"once/{name.lower()}", f"scoreboard players set {f} s9 1", *cmds)
    return f"execute if score {f} s9 matches 0 run {call(f'once/{name.lower()}')}"


def pressed(p, kind="#minecraft:buttons"):
    return f"execute if block {pos(p)} {kind}[powered=true]"


def unpress(p, facing, face="wall", kind="stone"):
    return setblock(p, f"minecraft:{kind}_button[face={face},facing={facing},powered=false]")


def flicker(name, ticks, fname=None):
    fname = (fname or f"fx/on_{name}").lower()
    fn(fname, lamp(name, True))
    return [lamp(name, False), sched(fname, ticks)]


def shake(n):
    return [f"scoreboard players set #shake s9 {n}", sched("fx/shake", 1)]


def title(t, sub="", color="dark_red", times=(10, 60, 20), sub_color="gray"):
    return [f"title @a times {times[0]} {times[1]} {times[2]}", "title @a subtitle " + txt(sub, color=sub_color),
            "title @a title " + txt(t, color=color, bold=True)]


def tp_rel(dy):
    return f"execute as @a at @s run tp @s ~ ~{dy} ~"


def ghost(p, yaw, tag="s9_ghost"):
    x, y, z = p
    return [f"kill @e[tag={tag}]",
            f'summon minecraft:wither_skeleton {fmt(x)} {y} {fmt(z)} {{Tags:["s9","s9_ghost","{tag}"],NoAI:1b,Silent:1b,'
            f'Invulnerable:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",HandItems:[{{}},{{}}],'
            f'ArmorItems:[{{}},{{}},{{}},{{}}],Rotation:[{yaw}f,0f]}}']


def bye(tag):
    return [f"tp @e[tag={tag}] 0 -60 0", f"kill @e[tag={tag}]"]


# =========================================================================
# EFFECTS
# =========================================================================
LIGHTNING = [(-12, 126, -10), (76, 125, -12), (-10, 124, 44), (40, 126, -14), (78, 124, 40), (20, 127, 46)]


def effects():
    fn("fx/shake",
       "scoreboard players remove #shake s9 1",
       "scoreboard players operation #p s9 = #shake s9",
       "scoreboard players operation #p s9 %= #2 s9",
       "execute if score #p s9 matches 0 as @a at @s run tp @s ~ ~ ~ ~1.4 ~-1.1",
       "execute if score #p s9 matches 1 as @a at @s run tp @s ~ ~ ~ ~-1.4 ~1.1",
       f"execute if score #shake s9 matches 1.. run {sched('fx/shake', 1)}")
    strikes = ["execute store result score #r s9 run random value 0..%d" % (len(LIGHTNING) - 1)]
    strikes += [f"execute if score #r s9 matches {i} run summon minecraft:lightning_bolt {pos(p)}" for i, p in enumerate(LIGHTNING)]
    fn("fx/lightning", strikes)
    fn("fx/storm",
       "# lightning at random, while you're on the surface",
       f"execute if entity @a[y=95,dy=100] run {call('fx/lightning')}",
       "execute store result score #st s9 run random value 500..1500",
       "execute store result storage station9:fx d.t int 1 run scoreboard players get #st s9",
       "function station9:fx/storm_m with storage station9:fx d")
    fn("fx/storm_m", f"$schedule function {NS}:fx/storm $(t)t")
    from .mc import scheduled
    scheduled.add("fx/storm")


# =========================================================================
# ACT 0: OPENING SHOTS AND THE SURFACE
# =========================================================================
def look(frm, at):
    dx, dy, dz = at[0] - frm[0], at[1] - frm[1], at[2] - frm[2]
    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
    return round(yaw, 2), round(pitch, 2)


SHOTS = [  # (start, end, look-at start, look-at end, frames)
    ((64, 125, 40), (55, 121, 31), (3.5, 116, 19.5), (3.5, 114, 19.5), 110),
    ((45, 104.5, 28), (40, 104, 24), (6, 104, 20), (8, 103, 20), 90),
    ((24, 102.8, 21), (17.5, 102.5, 20.2), (12, 103.5, 19.8), (12, 103.2, 19.6), 90),
]


def camera():
    frames = []
    for a, b, la, lb, n in SHOTS:
        for i in range(n):
            t = i / (n - 1)
            t = t * t * (3 - 2 * t)
            p = [a[k] + (b[k] - a[k]) * t for k in range(3)]
            at = [la[k] + (lb[k] - la[k]) * t for k in range(3)]
            yaw, pitch = look(p, at)
            frames.append("{x:%.3fd,y:%.3fd,z:%.3fd,yaw:%.2ff,pitch:%.2ff}" % (p[0], p[1], p[2], yaw, pitch))
    fn("cam/init", f"data modify storage {NS}:cam frames set value [{','.join(frames)}]")
    fn("cam/tick",
       "execute store result storage station9:cam i.i int 1 run scoreboard players get #cam s9",
       "function station9:cam/frame with storage station9:cam i",
       "scoreboard players add #cam s9 1")
    fn("cam/frame", "$execute as @a run function station9:cam/tp with storage station9:cam frames[$(i)]")
    fn("cam/tp", "$tp @s $(x) $(y) $(z) $(yaw) $(pitch)")
    return len(frames)


def act0():
    nframes = camera()
    s1 = SHOTS[0][4]
    s2 = s1 + SHOTS[1][4]
    fn("story/begin",
       "scoreboard players set #stage s9 1",
       "scoreboard players set #cam s9 0",
       call("cam/init"),
       "gamemode spectator @a",
       "effect clear @a",
       "effect give @a minecraft:saturation infinite 0 true",
       "weather rain 1000000", "time set 18000",
       timeline("story/opening", [
           (0, title("STATION 9", "Site 9  -  41 days since last contact", times=(40, 90, 30))),
           (45, [call("fx/lightning")]),
           (s1 - 6, ["effect give @a minecraft:blindness 1 0 true"]),
           (s2 - 6, ["effect give @a minecraft:blindness 1 0 true"]),
           (nframes - 10, ["effect give @a minecraft:blindness 2 0 true"]),
           (nframes, [call("story/surface")]),
       ]))

    fn("story/surface",
       "scoreboard players set #stage s9 2",
       "scoreboard players set #time s9 0",
       "gamemode adventure @a",
       f"tp @a {fmt(W.TRUCK_START[0])} {W.TRUCK_START[1]} {fmt(W.TRUCK_START[2])} {W.TRUCK_START[3]} 0",
       "effect give @a minecraft:blindness 2 0 true",
       objective("Sign in at the security hut", "Through the gate, on the left"),
       sched("fx/storm", 400),
       lines("story/arrive", ["a0_arrive", "a0_gate"], gap=14, start=50, then=["scoreboard players set #s_intro s9 1"]))
    STORY_FLAGS.append("#s_intro")

    hut_door = (W.HUT_DOOR[0] + .5, 101, W.HUT_DOOR[2] + .5)
    signin = (36, 101, 27)
    cage_box = ((2, 101, 18), (4, 103, 21))
    fn("surface/tick",
       f"execute if score #s_intro s9 matches 1 if score #talk s9 matches ..0 if score #kit s9 matches 0 "
       f"if entity @a[x=-20,y=95,z=-20,dx=83.5,dy=40,dz=70] run " + once("s_walk", say("a0_walk")),
       f"execute if score #s_intro s9 matches 1 if score #talk s9 matches ..0 if score #signed s9 matches 0 if score #kit s9 matches 0 "
       f"if entity @a[{near(hut_door, 5)}] run " + once("s_hut", say("a0_hut")),
       f"{pressed(signin)} run {call('surface/signin')}",
       f"execute if score #kit s9 matches 0 if {has('light')} run {call('surface/kit')}",
       f"execute if score #kit s9 matches 1 run scoreboard players add #inhut s9 1",
       f"execute if score #inhut s9 matches 500.. if score #talk s9 matches ..0 if entity @a[{box_selector((31, 101, 27), (36, 103, 31))}] run "
       + once("s_coffee", say("a0_coffee")),
       f"{pressed(W.CALL_BUTTON)} run {call('surface/call')}",
       f"execute if score #s_called s9 matches 2 if entity @a[{box_selector(*cage_box)}] run " + once("s_incage", say("a0_in_cage"),
                                                                                                  objective("Press B9")),
       f"{pressed(W.rel(W.CAGE_B9_BUTTON, 101))} run {call('surface/b9')}")
    STORY_FLAGS.extend(["#inhut"])

    fn("surface/signin",
       unpress(signin, "west", kind="spruce"),
       f"execute if score #signed s9 matches 1 run return 0",
       "scoreboard players set #signed s9 1",
       set_sign_lines((36, 102, 27), ["CONTRACTOR B9", "01:12  -", "", ""], color="blue"),
       snd("minecraft:item.book.page_turn", signin, 1, 1, "block"),
       after(20, "surface/signed", say("a0_signed")))

    fn("surface/kit",
       "scoreboard players set #kit s9 1",
       "scoreboard players set #light s9 0",
       lines("story/kit", ["a0_kit", "a0_to_lift"], gap=20, start=10,
             then=objective("Call the lift", "Lift house, north-west, under the headframe")))

    fn("surface/call",
       unpress(W.CALL_BUTTON, "east"),
       snd("sfx.beep_key", W.CALL_BUTTON, 1, 1, "block"),
       "execute if score #s_called s9 matches 1.. run return 0",
       f"execute if score #kit s9 matches 0 run return run {call('surface/call_nokit')}",
       "scoreboard players set #s_called s9 1",
       say("a0_called"),
       objective("Wait for the lift"),
       timeline("story/lift_arrives", [
           (20, [snd("amb.lift_ride", (4, 104, 20), 0.9, 1.2, "block")]),
           (60, [snd("sfx.roof_step", (4, 96, 20), 1.2, 0.7)]),
           (150, ["stopsound @a block station9:amb.lift_ride", snd("sfx.gate_open", (6, 102, 20), 1.2, 1, "block"),
                  lamp("E0", True)]),
           (180, [fill((6, 101, 19), (6, 103, 20), "minecraft:air"), "scoreboard players set #s_called s9 2",
                  objective("Get in the lift")]),
       ]))
    STORY_FLAGS.append("#s_called")
    fn("surface/call_nokit",
       actionbar("The lift won't come. You need your kit first.", "red"),
       snd("sfx.beep_bad", W.CALL_BUTTON, 1, 1, "block"))

    doorway = ((5, 101, 18), (8, 103, 21))
    fn("surface/b9",
       unpress(W.rel(W.CAGE_B9_BUTTON, 101), "south"),
       "execute unless score #s_called s9 matches 2 run return 0",
       f"execute unless entity @a[{box_selector(*cage_box)}] run return 0",
       "scoreboard players set #s_called s9 3",
       snd("sfx.beep_key", W.rel(W.CAGE_B9_BUTTON, 101), 1, 1, "block"),
       f"tp @a[{box_selector(*doorway)}] 3.5 101 20 -90 0",
       fill((6, 101, 19), (6, 103, 20), "minecraft:iron_block"),
       snd("sfx.gate_close", (6, 102, 20), 1.3, 1, "block"),
       objective("Lift 2", "Going down"),
       after(40, "story/descend", call("story/ride")))


# =========================================================================
# THE RIDE DOWN
# =========================================================================
def ride():
    roof_y = W.B8_CEIL + 1
    steps = [(470, 2.5, 21.0), (493, 3.1, 20.4), (511, 3.6, 19.9), (537, 4.2, 19.2), (566, 4.7, 18.9), (578, 5.0, 18.4),
             (606, 5.5, 18.0)]
    floors = [(0, "B1"), (125, "B2"), (250, "B3"), (375, "B4"), (500, "B5"), (625, "B6"), (750, "B7"), (905, "B8")]
    ev = [(0, ["scoreboard players set #stage s9 3", tp_rel(-W.DY_CAGE), lamp("E0", False), lamp("E8", True),
               "stopsound @a ambient", snd_me("amb.lift_ride", .8, 1, "ambient")])]
    ev += [(t, ["scoreboard players display name #o2 s9_hud " + txt("  Lift 2:  " + f, color="gray"),
                "scoreboard players set #o2 s9_hud 1"]) for t, f in floors]
    ev += [(30, say("a0_ride1")), (30 + say_len("a0_ride1") + 30, say("a0_ride2")),
           (420, [snd_me("sfx.roof_thump", 1, 1, "hostile", "~ ~3 ~"), shake(10), flicker("E8", 6, "fx/on_E8a")])]
    ev += [(t, [snd("sfx.roof_step", (x, roof_y, z), 1.3, 1.0)]) for t, x, z in steps]
    ev += [(640, say("a0_ride3")),
           (770, [snd("sfx.scrape", (6.5, 52, 18.5), 1.4, 1.0), flicker("E8", 3, "fx/on_E8b")]),
           (820, say("a0_ride4")),
           (905, ["stopsound @a ambient station9:amb.lift_ride", "stopsound @a voice", snd_me("sfx.crash", 1, 1),
                  lamp("E8", False), shake(22), "effect give @a minecraft:darkness 7 0 true",
                  "effect give @a minecraft:blindness 3 0 true", "scoreboard players reset #o2 s9_hud"]),
           (1020, say("a1_static")),
           (1130, [lamp("E8", True), snd("minecraft:block.redstone_torch.burnout", (4, 53, 20), .3, 1.4, "block")]),
           (1136, flicker("E8", 4, "fx/on_E8c")),
           (1160, ["scoreboard players set #stage s9 4", checkpoint(W.CP_B8),
                   objective("Get out of the lift", "Press DOOR RELEASE")])]
    timeline("story/ride", ev)
    fn("ride/tick", "# the ride is on rails")


# =========================================================================
# ACT 1: B8
# =========================================================================
def act1():
    cafe_box = ((34, 51, 4), (47, 53, 14))
    lab_box = ((22, 51, 19), (31, 53, 25))
    dormA_box = ((18, 51, 8), (22, 53, 12))
    b9_box = ((7, 41, 19), (14, 43, 21))
    fn("b8/tick",
       f"{pressed(W.rel(W.CAGE_RELEASE, 51))} run {call('b8/release')}",
       f"{pressed(W.RELAY_LEVER, 'minecraft:lever')} run " + once("s_relay", call("b8/relay")),
       f"{pressed(W.STAIR_BUTTON8)} run {call('b8/stair_button')}",
       *[f"{pressed(p)} run {call(f'b8/key{d}')}" for d, p in W.KEYPAD8.items()],
       f"{pressed(W.KEYPAD8_ZERO)} run {call('b8/key0')}",
       f"{pressed(W.PHONE)} run {call('b8/phone_answer')}",
       f"{pressed(W.TAPE_HALE1)} run {call('tape/hale1')}",
       "# the code hints",
       f"execute if score #s_relay s9 matches 1 if score #s_code s9 matches 0 run scoreboard players add #hint s9 1",
       f"execute if score #hint s9 matches 4800 run {call('b8/hint1')}",
       f"execute if score #hint s9 matches 9600 run {call('b8/hint2')}",
       "# small things",
       f"execute if entity @a[{box_selector((24, 51, 2), (25, 53, 13))}] run " + once("s_doorA", call("b8/door_opens")),
       f"execute if entity @a[{box_selector(*dormA_box)}] run scoreboard players set #inA s9 1",
       f"execute if score #inA s9 matches 1 unless entity @a[{box_selector((17, 51, 1), (26, 53, 14))}] run "
       + once("s_bed", call("b8/bed_empty")),
       f"execute if entity @a[{near((23.5, 51, 3.5), 2.2)}] run " + once("s_knock", call("b8/knock")),
       f"execute if score #s_relay s9 matches 1 if entity @a[{box_selector(*cafe_box)}] run " + once("s_ring", call("b8/phone_ring")),
       f"execute if score #s_relay s9 matches 1 if entity @a[{box_selector(*lab_box)}] run " + once("s_window", call("b8/window")),
       f"execute if score #window s9 matches 1 run {call('b8/window_tick')}",
       f"execute if score #s_code s9 matches 1 if entity @a[{box_selector((8, 51, 14), (20, 53, 20))}] run "
       + once("s_ceiling", call("b8/ceiling_steps")),
       f"execute if score #s_code s9 matches 1 if entity @a[x=21,y=50,z=15,dx=10,dy=4,dz=3,y_rotation=45..135] run "
       + once("s_turn", call("b8/turn_back")),
       f"execute if score #s_turn s9 matches 1 if entity @a[x=21,y=50,z=15,dx=30,dy=4,dz=3,y_rotation=-135..-45] run "
       + once("s_turn2", snd_me("sfx.sting_dread", .4)),
       "# down the stairs",
       f"execute if score #s_code s9 matches 1 if entity @a[{box_selector((8, 41, 22), (12, 47, 31))}] run " + once("s_st3", call("b8/stairs_lights")),
       f"execute if entity @a[{box_selector(*b9_box)}] run {call('story/b9_arrive')}")
    STORY_FLAGS.extend(["#hint", "#inA", "#window", "#wlook"])

    fn("b8/release",
       unpress(W.rel(W.CAGE_RELEASE, 51), "east", kind="polished_blackstone"),
       snd("sfx.beep_key", W.rel(W.CAGE_RELEASE, 51), 1, 1, "block"),
       "execute if score #s_release s9 matches 1 run return 0",
       "scoreboard players set #s_release s9 1",
       snd("sfx.gate_open", (6, 52, 20), 1.2, 0.8, "block"),
       after(40, "b8/gate_jammed",
             fill((6, 51, 19), (6, 52, 20), "minecraft:air"),
             snd("sfx.bang", (6, 52, 20), 0.7, 1.3),
             objective("Find the comms room", "B8 - east side of the hall")))
    STORY_FLAGS.append("#s_release")

    fn("b8/relay",
       snd("sfx.relay_boot", W.RELAY_LEVER, 1.2, 1, "block"),
       after(40, "b8/relay_lights", call("build/b8_backup"), snd_me("sfx.lights_on", .5, 1.2, "block")),
       lines("story/relay", ["a1_relay", "a1_contact", "a1_contact2", "a1_locked"], gap=12, start=60,
             then=objective("Find the stairwell override code", "Security office, east end of the hall")))

    fn("b8/stair_button",
       unpress(W.STAIR_BUTTON8, "north"),
       "execute if score #s_code s9 matches 1 run return 0",
       snd("sfx.beep_bad", W.STAIR_BUTTON8, 1, 1, "block"),
       actionbar("STAIRWELL B: LOCKDOWN.  Override at Security.", "red"))

    # keypad
    for d, p in list(W.KEYPAD8.items()) + [(0, W.KEYPAD8_ZERO)]:
        fn(f"b8/key{d}",
           unpress(p, "west"),
           "execute if score #s_relay s9 matches 0 run return run " + actionbar("The panel is dead. No power.", "dark_gray"),
           "execute if score #s_code s9 matches 1 run return 0",
           "execute if score #kpwait s9 matches 1 run return 0",
           snd("sfx.beep_key", p, 1, 1, "block"),
           "scoreboard players operation #code s9 *= #10 s9",
           f"scoreboard players add #code s9 {d}",
           "scoreboard players add #digits s9 1",
           call("b8/key_show"))
    STORY_FLAGS.append("#kpwait")
    shows = ["_ _ _ _", "* _ _ _", "* * _ _", "* * * _", "* * * *"]
    fn("b8/key_show",
       *[f"execute if score #digits s9 matches {i} run " + set_sign_lines(W.KEYPAD8_SIGN, ["STAIR OVERRIDE", s, "", ""])[0]
         for i, s in enumerate(shows)],
       f"execute if score #digits s9 matches 4 if score #code s9 matches {int(W.CODE)} run return run {call('b8/code_ok')}",
       f"execute if score #digits s9 matches 4 run {call('b8/code_bad')}")
    fn("b8/code_bad",
       "scoreboard players set #kpwait s9 1",
       snd("sfx.beep_bad", W.KEYPAD8_SIGN, 1, 1, "block"),
       set_sign_lines(W.KEYPAD8_SIGN, ["STAIR OVERRIDE", "DENIED", "", ""], "red"),
       after(30, "b8/code_reset", "scoreboard players set #code s9 0", "scoreboard players set #digits s9 0",
             "scoreboard players set #kpwait s9 0",
             set_sign_lines(W.KEYPAD8_SIGN, ["STAIR OVERRIDE", "_ _ _ _", "", ""], "lime")))
    fn("b8/code_ok",
       "scoreboard players set #s_code s9 1",
       snd("sfx.beep_ok", W.KEYPAD8_SIGN, 1, 1, "block"),
       set_sign_lines(W.KEYPAD8_SIGN, ["STAIR OVERRIDE", "ACCEPTED", "", ""], "lime"),
       fill(*W.STAIR_DOOR8, "minecraft:air"),
       snd("sfx.gate_open", (12, 52, 21), 1.2, 1, "block"),
       lamp("ST3", True), lamp("ST2", True), lamp("ST1", True),
       say("a1_code_ok"),
       objective("Go down to B9", "Stairwell B, in the lobby"))
    STORY_FLAGS.append("#s_code")

    fn("b8/hint1", "execute if score #talk s9 matches 1.. run return run scoreboard players remove #hint s9 100", say("a1_hint1"))
    fn("b8/hint2", "execute if score #talk s9 matches 1.. run return run scoreboard players remove #hint s9 100", say("a1_hint2"))

    fn("b8/door_opens",
       door(W.DOORS["dormA"][0], "west", open_=True, wood="spruce", hinge="left"),
       snd("sfx.door_creak", (23.5, 52, 10.5), 1.1, 1, "block"))

    fn("b8/bed_empty",
       "# you left Hale's room. The sheet isn't on the bed anymore.",
       setblock((19, 52, 9), "minecraft:air"), setblock((19, 52, 10), "minecraft:air"),
       setblock((21, 51, 11), "minecraft:white_carpet"), setblock((20, 51, 12), "minecraft:white_carpet"),
       door(W.DOORS["dormA"][0], "west", open_=False, wood="spruce", hinge="left"),
       snd("minecraft:block.wooden_door.close", (23.5, 52, 10.5), 0.9, 0.7, "block"))

    fn("b8/knock", snd("sfx.knock", (22.5, 52, 3.5), 1.2, 1, "hostile"))

    fn("b8/phone_ring",
       "scoreboard players set #rings s9 0",
       call("b8/ring"))
    fn("b8/ring",
       "execute if score #s_answered s9 matches 1 run return 0",
       "scoreboard players add #rings s9 1",
       "execute if score #rings s9 matches 4.. run return 0",
       snd("sfx.phone_ring", W.PHONE, 1.6, 1, "block"),
       "execute store result score #st s9 run random value 260..520",
       "execute store result storage station9:fx d.t int 1 run scoreboard players get #st s9",
       "function station9:b8/ring_m with storage station9:fx d")
    fn("b8/ring_m", f"$schedule function {NS}:b8/ring $(t)t")
    from .mc import scheduled
    scheduled.add("b8/ring")
    STORY_FLAGS.extend(["#rings", "#s_answered"])

    fn("b8/phone_answer",
       unpress(W.PHONE, "south"),
       "execute unless score #s_ring s9 matches 1 run return 0",
       "execute if score #s_answered s9 matches 1 run return 0",
       "scoreboard players set #s_answered s9 1",
       "stopsound @a block station9:sfx.phone_ring",
       snd_me("sfx.phone_up", .9),
       timeline("story/phone", [
           (8, say("phone")),
           (8 + say_len("phone") + 5, [snd_me("sfx.phone_down", .9)]),
           (8 + say_len("phone") + 30, [door(W.DOORS["kitchen"][0], "north", open_=True, wood="birch"),
                                        snd("sfx.door_creak", (37.5, 52, 3.5), 1.2, 0.85, "block")]),
           (8 + say_len("phone") + 80, say("a1_phone_after")),
       ]))

    fn("b8/window",
       *ghost((26.5, 51, 30.5), 180, "s9_window"),
       lamp("SP", True),
       "scoreboard players set #window s9 1")
    fn("b8/window_tick",
       "# look at it through the glass, or walk to its door, and it is gone",
       f"execute if entity @a[{box_selector((22, 51, 19), (31, 53, 25))},y_rotation=-50..50] run scoreboard players add #wlook s9 1",
       f"execute if score #wlook s9 matches 30.. run {call('b8/window_gone')}",
       f"execute if entity @a[{box_selector((29, 51, 25), (31, 53, 27))}] run {call('b8/window_gone')}",
       f"execute unless entity @a[{box_selector((21, 51, 18), (32, 53, 33))}] run {call('b8/window_gone_quiet')}")
    fn("b8/window_gone",
       "scoreboard players set #window s9 2",
       lamp("SP", False), bye("s9_window"),
       snd_me("sfx.sting_hit", .35),
       after(8, "b8/window_lamp", lamp("SP", True)),
       after(60, "b8/window_line", say("a1_window", force=False)))
    fn("b8/window_gone_quiet", "scoreboard players set #window s9 2", bye("s9_window"))

    ceiling = [(0, 10, 17), (18, 12, 17.6), (31, 14, 18), (52, 16, 17.5), (61, 17.5, 16.8), (88, 19, 16.4)]
    fn("b8/ceiling_steps", timeline("story/ceiling", [(t, [snd("sfx.roof_step", (x, 56, z), 1.5, 0.8)]) for t, x, z in ceiling]))

    fn("b8/turn_back",
       "# behind you, the hall is not how you left it",
       lamp("H3", False), lamp("H4", False),
       setblock((34, 51, 16), "minecraft:spruce_stairs[facing=west]"),
       *[c for d in ("dormA", "dormB", "dormC", "dormD") for c in door(W.DOORS[d][0], W.DOORS[d][1], open_=True,
                                                                        wood="spruce", hinge=W.DOORS[d][2])])

    fn("b8/stairs_lights",
       setblock((34, 51, 16), "minecraft:air"),
       say("a1_stairs", force=False),
       timeline("story/stairs_down", [
           (40, [lamp("ST3", False), snd("minecraft:block.iron_door.close", (12, 52, 22), 0.8, 0.5, "block")]),
           (120, [lamp("ST2", False)]),
       ]))


# =========================================================================
# ACT 2: B9
# =========================================================================
def act2():
    wash = box_selector((11, 41, 7), (13, 43, 9))
    contain_box = ((26, 41, 23), (36, 43, 30))
    fn("story/b9_arrive",
       "execute unless score #stage s9 matches 4 run return 0",
       "scoreboard players set #stage s9 5",
       checkpoint(W.CP_B9),
       call("build/b9_backup"), lamp("ST1", False),
       "scoreboard players set #tab s9 0",
       ai.summon("c48", 90), ai.mode(6),
       "scoreboard players set #teach s9 1",
       say("a2_arrive"),
       objective("Restore Generator B", "East end of the corridor"))
    STORY_FLAGS.extend(["#teach", "#tw", "#tt", "#tu"])

    fn("b9/tick",
       f"execute if score #teach s9 matches 1..3 run {call('b9/teach')}",
       f"execute if score #stage s9 matches 5 if {has('keycard')} run {call('b9/got_key')}",
       f"execute if score #stage s9 matches 7 if {has('fuse')} run {call('b9/got_fuse')}",
       f"{pressed(W.KEYPAD9)} run {call('b9/keypad')}",
       f"{pressed(W.LEVER, 'minecraft:lever')} run {call('b9/lever')}",
       f"{pressed(W.TAPE_HALE2)} run {call('tape/hale2')}",
       f"{pressed(W.TAPE_MARSH)} run {call('tape/marsh')}",
       f"execute if score #stage s9 matches 5..7 if entity @a[{box_selector((50, 41, 15), (60, 43, 25))}] run "
       + once("s_nofuse", say("a2_nofuse", force=False)),
       "# the mirror: look into it, then turn around",
       f"execute if score #mirror s9 matches 0 if entity @a[{wash},y_rotation=140..180] run {call('b9/mirror_1')}",
       f"execute if score #mirror s9 matches 0 if entity @a[{wash},y_rotation=-180..-140] run {call('b9/mirror_1')}",
       f"execute if score #mirror s9 matches 1 if entity @a[y_rotation=-100..100] run {call('b9/mirror_2')}",
       f"execute if score #mirror s9 matches 1 unless entity @a[{wash}] run {call('b9/mirror_2')}",
       f"execute if entity @a[{box_selector((10, 41, 0), (14, 43, 1))}] run " + once("s_marsh", call("b9/found_marsh")),
       f"execute if score #cscene s9 matches 1 if entity @a[{box_selector(*contain_box)}] run {call('b9/cell_scene')}",
       "# whispers, once each, when it is far away",
       "scoreboard players add #b9t s9 1",
       f"execute if score #b9t s9 matches 3000.. if score #talk s9 matches ..0 "
       f"as @a at @s unless entity @e[tag=s9_hunter,distance=..18] run " + once("s_wh1", say("wh_hear", force=False)),
       f"execute if score #b9t s9 matches 8000.. if score #talk s9 matches ..0 if score #on s9 matches 1 "
       f"as @a at @s unless entity @e[tag=s9_hunter,distance=..18] run " + once("s_wh2", say("wh_off", force=False)))
    STORY_FLAGS.extend(["#mirror", "#cscene", "#b9t"])

    # the first sighting teaches the rule: it only moves when you can't see it
    step_lamps = {1: ("c43", "C4"), 2: ("c37", "C3"), 3: (None, "C3")}
    fn("b9/teach",
       "scoreboard players add #tt s9 1",
       "execute if score #watched s9 matches 1 run scoreboard players add #tw s9 1",
       "execute if score #watched s9 matches 1 run scoreboard players set #tu s9 0",
       "execute if score #watched s9 matches 0 run scoreboard players add #tu s9 1",
       f"execute if score #teach s9 matches 2.. if score #tu s9 matches 60.. run {call('b9/teach_3')}",
       "execute if score #tw s9 matches 25.. if score #talk s9 matches ..0 run " + once("s_watch", say("a2_watch")),
       f"execute if score #teach s9 matches 1 if score #tw s9 matches 70.. run {call('b9/teach_1')}",
       f"execute if score #teach s9 matches 2 if score #tw s9 matches 50.. run {call('b9/teach_2')}",
       f"execute if score #teach s9 matches 3 if score #tw s9 matches 40.. run {call('b9/teach_3')}",
       f"execute if score #tt s9 matches 900.. run {call('b9/teach_3')}",
       f"execute as @e[tag=s9_hunter] at @s if entity @a[distance=..7] run {call('b9/teach_3')}")
    fn("b9/teach_1", "scoreboard players set #teach s9 2", "scoreboard players set #tw s9 0",
       flicker("C4", 9, "fx/on_C4t"), ai.place("c43", 90))
    fn("b9/teach_2", "scoreboard players set #teach s9 3", "scoreboard players set #tw s9 0",
       flicker("C3", 9, "fx/on_C3t"), flicker("C4", 9, "fx/on_C4u"), ai.place("c37", 90))
    fn("b9/teach_3",
       "execute if score #teach s9 matches 4 run return 0",
       "scoreboard players set #teach s9 4",
       flicker("C3", 12, "fx/on_C3u"), flicker("C4", 12, "fx/on_C4v"), flicker("C2", 12, "fx/on_C2t"),
       snd("sfx.step", (40, 41, 20), 1.4, 0.9),
       ai.place("gnw"), ai.mode(1, "wander"), "scoreboard players set #hgrace s9 400", call("ai/roam"),
       lines("story/rule", ["a2_gone", "a2_rule"], gap=30, start=40),
       after(40 + say_len("a2_gone") + say_len("a2_rule") + 700, "story/lockers_line", say("a2_lockers", force=False)))

    fn("b9/got_key",
       "scoreboard players set #stage s9 6",
       say("a2_key"),
       objective("Open Containment", "Keycard lock, middle of the corridor"),
       after(50, "b9/office_slam", f"execute if entity @a[{box_selector((10, 41, 11), (20, 43, 17))}] run {call('b9/office_slam_now')}"))
    fn("b9/office_slam_now",
       door(W.DOORS["office"][0], "north", wood="dark_oak"),
       snd("minecraft:entity.zombie.attack_wooden_door", (15, 42, 18), 1.2, 0.8),
       snd("minecraft:block.wooden_door.close", (15, 42, 18), 1, 0.6, "block"),
       flicker("O1", 30, "fx/on_O1"),
       "effect give @a minecraft:darkness 3 0 true")

    fn("b9/keypad",
       unpress(W.KEYPAD9, "north"),
       f"execute if score #stage s9 matches 6 run return run {call('b9/k_open')}",
       "execute unless score #stage s9 matches 5 run return 0",
       actionbar("ACCESS DENIED - LEVEL 3 KEYCARD REQUIRED", "red"),
       snd("sfx.beep_bad", W.KEYPAD9, 1, 1, "block"),
       once("s_deny", say("a2_deny")))
    fn("b9/k_open",
       "scoreboard players set #stage s9 7",
       "scoreboard players set #tab s9 1",
       "scoreboard players set #cscene s9 1",
       fill(*W.B9_OPEN["contain_n"][0], "minecraft:air"),
       snd("sfx.beep_ok", W.KEYPAD9, 1, 1, "block"),
       snd("sfx.gate_open", (31, 42, 21), 1, 1, "block"),
       set_sign_lines(W.KEYPAD9_SIGN, ["ACCESS", "GRANTED", "", ""], "lime"),
       checkpoint(W.CP_CONTAIN),
       objective("Find a fuse", "Containment"))

    fn("b9/cell_scene",
       "# it went home. The fuse is at its feet.",
       "execute if score #watched s9 matches 1 run return 0",
       "scoreboard players set #cscene s9 2",
       f"tp @e[tag=s9_hunter] {pos(W.CELL_SPOT)} 180 0",
       f"scoreboard players set #hnode s9 {ai.NODE_IDS['kc']}", "scoreboard players set #hnext s9 -1",
       f"scoreboard players set #htarget s9 {ai.NODE_IDS['kc']}",
       ai.mode(3, "hunt"), "scoreboard players set #lost s9 0", "scoreboard players set #hgrace s9 0",
       "scoreboard players set #hwait s9 0",
       lamp("K1", True), lamp("K2", True),
       say("a2_contain"))

    fn("b9/got_fuse",
       "scoreboard players set #stage s9 8",
       "scoreboard players set #cscene s9 3",
       "# the lights die, and when they come back it's gone",
       lamp("K1", False), lamp("K2", False), "scoreboard players set #fried s9 1",
       snd_me("sfx.flash_buzz", .7),
       ai.place("gs"), ai.mode(3, "hunt"), "scoreboard players set #lost s9 60", "scoreboard players set #hgrace s9 120",
       say("a2_fuse"),
       after(50, "b9/fuse_lights", lamp("K1", True), "scoreboard players set #fried s9 0"),
       after(50 + say_len("a2_fuse") + 20, "b9/fuse_line", say("a2_after_fuse")),
       objective("Bring the fuse to Generator B", "East end. It's waiting there."))

    fn("b9/lever",
       setblock(W.LEVER, "minecraft:lever[face=wall,facing=west,powered=false]"),
       f"execute if score #stage s9 matches 8 run return run {call('gen/1')}",
       snd("minecraft:block.lever.click", W.LEVER, 1, 0.5, "block"),
       actionbar("Generator B: FUSE MISSING", "red"))

    fn("b9/mirror_1",
       "scoreboard players set #mirror s9 1",
       *ghost((12.5, 41, 2.5), 0, "s9_mirror"),
       snd("minecraft:entity.player.breath", (12.5, 42, 9.8), .5, .5))
    fn("b9/mirror_2",
       "scoreboard players set #mirror s9 2",
       bye("s9_mirror"),
       fill((12, 41, 6), (12, 42, 6), "minecraft:air"),
       "particle minecraft:block minecraft:light_gray_stained_glass 12.5 42 6.5 0.3 0.5 0.1 1 50 force",
       snd("minecraft:block.glass.break", (12.5, 42.5, 6.5), 1.4, .7, "block"),
       flicker("W1", 40, "fx/on_W1"), lamp("R1", False),
       "effect give @a minecraft:darkness 3 0 true")

    fn("b9/found_marsh",
       "scoreboard players set #marsh s9 1",
       lamp("A1", True),
       say("a2_marsh", force=False))


# =========================================================================
# TAPES
# =========================================================================
def tapes():
    for key, p, flag_ in [("hale1", W.TAPE_HALE1, "#t_hale1"), ("hale2", W.TAPE_HALE2, "#t_hale2"), ("marsh", W.TAPE_MARSH, "#t_marsh")]:
        fn(f"tape/{key}",
           unpress(p, "north", face="floor", kind="polished_blackstone"),
           f"execute if score #tapeon s9 matches 1.. run return 0",
           f"scoreboard players set #tapeon s9 {say_len('tape_' + key)}",
           f"execute if score {flag_} s9 matches 0 run scoreboard players add #tapes s9 1",
           f"scoreboard players set {flag_} s9 1",
           say(f"tape_{key}"))
    STORY_FLAGS.append("#tapeon")
    fn("tape/tick", "execute if score #tapeon s9 matches 1.. run scoreboard players remove #tapeon s9 1")


# =========================================================================
# ACT 3: THE GENERATOR AND THE ESCAPE
# =========================================================================
HEADSTART = 80


def act3():
    fn("gen/1",
       "scoreboard players set #stage s9 9",
       "scoreboard players set #hmode s9 0",
       bye("s9_hunter"), bye("s9_ghost"),
       clear("fuse"),
       set_sign_lines(W.GEN_SIGN, ["GENERATOR B", "FUSE: OK", "", "RUNNING"], "lime"),
       "stopsound @a ambient",
       call("build/b9_all_on"), call("build/b8_all_on"),
       snd_me("sfx.gen_start", 1, 1, "block"), snd_me("sfx.lights_on", 1, 1, "block"),
       snd("sfx.gen_hum", (55, 42, 20), 1.5, 1, "block"),
       objective("..."),
       timeline("story/lockdown", [
           (20, say("a3_power")),
           (20 + say_len("a3_power") + 20, say("a3_wait")),
           (20 + say_len("a3_power") + 20 + say_len("a3_wait") + 5,
            [fill(*W.B9_OPEN["gen_w"][0], "minecraft:iron_block"), fill(*W.B9_OPEN["gen_n"][0], "minecraft:iron_block"),
             snd("minecraft:block.iron_door.close", (49, 42, 20), 1.5, .5, "block"),
             snd("sfx.bang", (49, 42, 20), 0.8, 1.2), snd_me("sfx.siren", .9, 1),
             title(" ", "!! LOCKDOWN !!", times=(5, 40, 10), sub_color="red")]),
       ]))
    t0 = 20 + say_len("a3_power") + 20 + say_len("a3_wait") + 5
    fn("gen/lockdown2", say("a3_lockdown"))
    after_pa = t0 + 30 + say_len("a3_lockdown")

    def bang(v, n):
        return [snd("sfx.bang", (48, 42, 20), v, 1.0), shake(n)]

    timeline("gen/sequence", [
        (t0 + 30, [call("gen/lockdown2")]),
        (after_pa + 10, bang(1.2, 6)),
        (after_pa + 37, bang(1.6, 7) + [lamp("G1", False), lamp("G3", False)]),
        (after_pa + 55, bang(2.0, 9) + [call("gen/blackout")]),
        (after_pa + 55 + HEADSTART, [call("gen/breach")]),
    ])
    fn("gen/1", call("gen/sequence"))

    fn("gen/blackout",
       call("build/lamps_off"), call("build/emergency_on"),
       snd("minecraft:entity.warden.roar", (47, 42, 20), 1.5, .8),
       "stopsound @a block station9:sfx.gen_hum",
       "scoreboard players set #fried s9 1", "scoreboard players set #light s9 0",
       snd_me("sfx.flash_buzz", .8),
       "execute as @a at @s anchored eyes run particle minecraft:electric_spark ^ ^-0.3 ^0.6 0.1 0.1 0.1 0.3 20 force @s",
       "effect give @a minecraft:darkness 3 0 true",
       fill(*W.B9_OPEN["gen_s"][0], "minecraft:air"),
       snd("minecraft:block.piston.contract", (58.5, 42, 26), 1.2, .5, "block"),
       checkpoint(W.CP_GEN),
       "scoreboard players set #tab s9 2",
       say("a3_run"),
       title(" ", "RUN", times=(5, 30, 10), sub_color="dark_red"),
       objective("Get to the lift", "Tunnel south, service stairs up to B8"))

    fn("gen/breach",
       fill(*W.B9_OPEN["gen_w"][0], "minecraft:air"),
       "particle minecraft:explosion 49.5 42 20 0.3 0.8 0.5 0 6 force",
       snd("minecraft:entity.generic.explode", (49.5, 42, 20), 1.2, .6),
       snd("sfx.scream", (49.5, 42, 20), 1.0, 0.8),
       ai.summon("gw", -90), ai.mode(5, "chase"),
       "scoreboard players set #hgrace s9 0",
       call("ai/to_player"))

    fn("chase/tick",
       f"execute if entity @a[y=49,dy=6] run " + once("s_b8chase", say("a3_b8"), lamp("E8", True),
                                                      fill((6, 51, 19), (6, 53, 20), "minecraft:air")),
       f"execute if entity @a[{box_selector(*W.COLLAPSE_TRIGGER)}] run " + once("s_collapse", call("chase/collapse")),
       f"execute if entity @a[{box_selector((2, 51, 18), (4, 53, 21))}] run {call('end/1')}",
       "execute if score #siren s9 matches 1.. run scoreboard players remove #siren s9 1",
       f"execute if score #siren s9 matches 1 run {snd_me('sfx.siren', .6, 0.95)}")
    STORY_FLAGS.append("#siren")

    fn("chase/collapse",
       f"tp @a[{box_selector(*W.COLLAPSE)}] 45 51 17",
       fill(W.COLLAPSE[0], W.COLLAPSE[1], "minecraft:cobbled_deepslate"),
       fill((38, 53, 16), (43, 53, 17), "minecraft:gravel"),
       setblock((43, 51, 16), "minecraft:cobbled_deepslate_stairs[facing=east]"),
       setblock((43, 52, 17), "minecraft:air"), setblock((38, 52, 16), "minecraft:air"),
       "particle minecraft:campfire_cosy_smoke 42 52 17 1.5 1 0.5 0.02 80 force",
       "particle minecraft:block minecraft:gravel 42 53 17 2 0.5 0.5 1 120 force",
       snd_me("sfx.collapse", 1, 1, "block"),
       shake(14),
       "scoreboard players set #tab s9 3",
       "scoreboard players set #hnext s9 -1",
       call("ai/route"),
       say("a3_collapse"))

    fn("chase/respawned",
       "# back at the generator; it comes through the door again after a moment",
       ai.place("gw", -90), ai.mode(5, "chase"),
       "scoreboard players set #hgrace s9 100",
       call("ai/to_player"),
       title(" ", "It lets you go. For now.", times=(10, 50, 20), sub_color="dark_red"))
    fn("chase/resume",
       "execute unless score #stage s9 matches 9 run return 0",
       ai.mode(5, "chase"), call("ai/to_player"))


# =========================================================================
# THE RIDE UP AND THE TWO ENDINGS
# =========================================================================
def ending():
    doorway = ((5, 51, 18), (8, 53, 21))
    lever8 = W.rel(W.CAGE_LIGHT_LEVER, 51)
    fn("end/1",
       "scoreboard players set #stage s9 10",
       "scoreboard players set #hmode s9 0",
       f"tp @a[{box_selector(*doorway)}] 3.5 51 20 90 0",
       fill((6, 51, 19), (6, 53, 20), "minecraft:iron_block"),
       snd("sfx.gate_close", (6, 52, 20), 1.5, 1, "block"),
       bye("s9_hunter"), "kill @e[tag=s9_node]", "kill @e[tag=s9_locker]",
       setblock(lever8, "minecraft:lever[face=wall,facing=south,powered=false]"),
       lamp("E8", True),
       objective("Lift 2", "Going up"),
       timeline("story/up", [
           (5, say("a3_lift")),
           (40, [snd("sfx.knock", (7, 52, 20), 1.6, 0.9), shake(5)]),
           (75, [snd("sfx.bang", (7, 52, 20), 1.2, 1.1), shake(8)]),
           (110, ["scoreboard players set #ride s9 1", snd_me("amb.lift_ride", .8, 1, "ambient")]),
       ] + [(110 + 110 * i, ["scoreboard players display name #o2 s9_hud " + txt(f"  Lift 2:  B{8 - i}", color="gray"),
                             "scoreboard players set #o2 s9_hud 1"]) for i in range(8)]
         + [(250, say("e_ride")),
            (500, [call("end/thump")]),
            (990, [call("end/arrive")])]))
    STORY_FLAGS.extend(["#ride", "#dark"])

    fn("end/tick",
       "# the cage light follows its lever",
       f"execute if score #ride s9 matches 1 if block {pos(lever8)} minecraft:lever[powered=true] run {lamp('E8', False)}",
       f"execute if score #ride s9 matches 1 if block {pos(lever8)} minecraft:lever[powered=false] run {lamp('E8', True)}",
       f"execute if score #ending s9 matches 2 if entity @a[x=13,y=95,z=0,dx=70,dy=40,dz=45] run " + once("s_walked", call("end/b_out")))

    fn("end/thump",
       "# it's on the roof. Is your light on?",
       snd_me("sfx.roof_thump", 1, 1, "hostile", "~ ~3 ~"), shake(10),
       f"execute if block {pos(lever8)} minecraft:lever[powered=true] run return run {call('end/b')}",
       call("end/a"))
    roof = [(20, 2.4, 20.5), (43, 3.0, 19.8), (70, 3.9, 19.2), (84, 4.4, 18.9), (120, 4.9, 18.5)]
    fn("end/a",
       "scoreboard players set #ending s9 1",
       timeline("end/a_seq", [(40, say("e_heavy"))] +
                [(t, [snd("sfx.roof_step", (x, 55, z), 1.3, 1.0)]) for t, x, z in roof] +
                [(200, flicker("E8", 5, "fx/on_E8d"))]))
    fn("end/b",
       "scoreboard players set #ending s9 2",
       timeline("end/b_seq", [(40, say("e_dark"))] +
                [(t + 60, [snd("sfx.roof_step", (x, 55, z), 1.0, 0.9)]) for t, x, z in roof] +
                [(260, [snd("sfx.sniff", (3.5, 55, 20), 1.4, 0.8)]), (330, [snd("sfx.breath", (4, 55, 19.5), 1.2, 0.8)])]))

    fn("end/arrive",
       "scoreboard players set #ride s9 0",
       "stopsound @a ambient station9:amb.lift_ride",
       "scoreboard players reset #o2 s9_hud",
       tp_rel(W.DY_CAGE),
       "execute if score #ending s9 matches 2 run " + lamp("E0", False),
       "execute if score #ending s9 matches 1 run " + lamp("E0", True),
       snd("sfx.gate_open", (6, 102, 20), 1.2, 1, "block"),
       after(40, "end/gate_up", fill((6, 101, 19), (6, 103, 20), "minecraft:air")),
       f"execute if score #ending s9 matches 1 run {sched('end/a_scare', 90)}",
       f"execute if score #ending s9 matches 2 run {sched('end/b_line', 60)}")

    # Ending 1: it came up with you
    fn("end/a_scare",
       lamp("E0", False),
       after(12, "end/a_scare2",
             *ghost((2.7, 101, 20.0), -90, "s9_final"),
             "execute as @a at @s run tp @s ~ ~ ~ facing entity @e[tag=s9_final,limit=1] eyes",
             "effect give @a minecraft:slowness 2 255 true",
             lamp("E0", True),
             "execute as @a at @s run playsound station9:sfx.scream hostile @s ~ ~ ~ 1 1",
             "execute as @a at @s run playsound station9:sfx.sting_hit master @s ~ ~ ~ 1 1",
             after(16, "end/a_black", lamp("E0", False), bye("s9_final"), "effect give @a minecraft:blindness 5 0 true",
                   title("THE END", "Ending 1 of 2:  Passenger", times=(10, 90, 30)),
                   sched("end/stats", 110))))

    # Ending 2: lights out
    fn("end/b_line", say("e_out"), objective("Walk away", "Leave the lift house"))
    fn("end/b_out",
       fill((6, 101, 19), (6, 103, 20), "minecraft:iron_block"),
       snd("sfx.gate_close", (6, 102, 20), 1.4, 1, "block"),
       after(30, "end/b_down", snd("amb.lift_ride", (4, 100, 20), 1.2, 0.8, "block"), call("fx/lightning")),
       after(90, "end/b_title", title("ESCAPED", "Ending 2 of 2:  Lights Out", color="green", times=(20, 100, 30)),
             sched("end/stats", 130)))

    fn("end/stats",
       "scoreboard players set #stage s9 11",
       "scoreboard players operation #sec s9 = #time s9",
       "scoreboard players operation #sec s9 /= #20 s9",
       "scoreboard players operation #min s9 = #sec s9",
       "scoreboard players operation #min s9 /= #60 s9",
       "scoreboard players operation #sec s9 %= #60 s9",
       'tellraw @a ["",' + txt("\n  S T A T I O N   9\n", color="dark_red", bold=True) + "]",
       'tellraw @a ["",' + txt("  Time: ", color="gray") + ',{"score":{"name":"#min","objective":"s9"},"color":"white"},'
       + txt("m ", color="white") + ',{"score":{"name":"#sec","objective":"s9"},"color":"white"},' + txt("s", color="white")
       + "," + txt("     Deaths: ", color="gray") + ',{"score":{"name":"#deaths","objective":"s9"},"color":"white"}'
       + "," + txt("     Tapes: ", color="gray") + ',{"score":{"name":"#tapes","objective":"s9"},"color":"white"},'
       + txt("/3", color="white") + "]",
       'execute if score #ending s9 matches 1 run tellraw @a ["",' + txt("  Ending 1 of 2: Passenger.", color="gray")
       + "," + txt("  (Marsh knew another way.)", color="dark_gray", italic=True) + "]",
       'execute if score #ending s9 matches 2 run tellraw @a ["",' + txt("  Ending 2 of 2: Lights Out.", color="gray") + "]",
       'tellraw @a ["",' + txt("  ") + "," + json.dumps({
           "text": "[ Play again ]", "color": "gold", "bold": True,
           "clickEvent": {"action": "run_command", "value": f"/function {NS}:start"},
           "hoverEvent": {"action": "show_text", "contents": "Rebuild the station and start over"}}) + "]",
       'tellraw @a ""')


# =========================================================================
# SMALL LINES + ENTITIES AT RESET
# =========================================================================
def misc():
    fn("story/always", call("tape/tick"))
    fn("story/heard_hint", "scoreboard players set #s_heard s9 1", say("a2_heard", force=False))
    fn("story/caught_line", "scoreboard players set #s_caught s9 1", say("a2_caught", force=False))
    STORY_FLAGS.extend(["#s_heard", "#s_caught"])

    kit = W.KIT_BARREL
    marsh = ('summon minecraft:armor_stand %s 40.45 %s {Tags:["s9"],NoGravity:1b,Invulnerable:1b,ShowArms:1b,NoBasePlate:1b,'
             'DisabledSlots:4144959,Rotation:[200f,0f],Pose:{Head:[38f,10f,0f],Body:[4f,0f,0f],LeftArm:[-12f,0f,-8f],'
             'RightArm:[-20f,0f,12f],LeftLeg:[-85f,-12f,0f],RightLeg:[-88f,14f,0f]},'
             'ArmorItems:[{id:"minecraft:leather_boots",Count:1b,tag:{display:{color:3355443}}},'
             '{id:"minecraft:leather_leggings",Count:1b,tag:{display:{color:4473924}}},'
             '{id:"minecraft:leather_chestplate",Count:1b,tag:{display:{color:14540253}}},'
             '{id:"minecraft:player_head",Count:1b}]}') % (fmt(W.MARSH_BODY[0]), fmt(W.MARSH_BODY[2]))
    fn("reset_entities",
       ai.entities(),
       call("ai/init"),
       f"item replace block {pos(kit)} container.12 with {item_arg('light')} 1",
       f"item replace block {pos(kit)} container.14 with {item_arg('battery')} 1",
       drop("keycard", W.KEYCARD_AT),
       drop("fuse", W.FUSE_AT),
       *[drop("battery", p) for p in W.BATTERIES],
       marsh)


def build(files_flags):
    effects()
    act0()
    ride()
    act1()
    act2()
    tapes()
    act3()
    ending()
    misc()
    files_flags.extend(STORY_FLAGS)
