"""Game systems: startup, the per-tick loop, voices, objectives, the flashlight,
lockers, noise, checkpoints and ambience."""
import json

from . import world as W
from .build import lamp
from .mc import (NS, actionbar, call, dur_ticks, fn, fmt, manifest, sched, scheduled, snd, snd_me, txt)
from .script import L, SPEAKERS

# Tuning ---------------------------------------------------------------------------------
BATTERY_TICKS = 3600        # one battery lasts three minutes of use
LOW_BATTERY = 540           # below this the light stutters
LIGHT_LEVEL = 14
LIGHT_RANGE = 22            # ray steps of 0.5 blocks

ITEMS = {
    "light": ('carrot_on_a_stick', 9101, "s9light", "Flashlight", "white", "Right-click: on / off"),
    "battery": ('iron_nugget', 9102, "s9batt", "Battery", "yellow", "Swapped in automatically"),
    "keycard": ('tripwire_hook', 9103, "s9key", "Keycard - M. Marsh", "aqua", "Level 3 access"),
    "fuse": ('blaze_rod', 9104, "s9fuse", "Fuse (30A)", "gold", "Generator B"),
}

FLAGS = ["#stage", "#time", "#deaths", "#light", "#charge", "#fried", "#talk", "#amb", "#area", "#hudt",
         "#tapes", "#t_hale1", "#t_hale2", "#t_marsh", "#marsh", "#ending", "#signed", "#kit", "#cam",
         "#hmode", "#hnode", "#hnext", "#htarget", "#hspd", "#hwait", "#tab", "#hgrace", "#hdist", "#hstride",
         "#watched", "#wtime", "#frozen", "#los", "#beam", "#pnode", "#lost", "#stingcd", "#catching",
         "#hidden", "#code", "#digits", "#e", "#seenago", "#lkphase"]


def item_nbt(kind, count=1):
    iid, cmd, tag, name, color, lore = ITEMS[kind]
    display = (f"display:{{Name:{json.dumps(txt(name, italic=False, color=color))},"
               f"Lore:[{json.dumps(txt(lore, color='dark_gray', italic=False))}]}}")
    return f'{{id:"minecraft:{iid}",Count:{count}b,tag:{{{tag}:1b,CustomModelData:{cmd},{display}}}}}'


def item_arg(kind):
    iid, cmd, tag, name, color, lore = ITEMS[kind]
    display = (f"display:{{Name:{json.dumps(txt(name, italic=False, color=color))},"
               f"Lore:[{json.dumps(txt(lore, color='dark_gray', italic=False))}]}}")
    return f"minecraft:{iid}{{{tag}:1b,CustomModelData:{cmd},{display}}}"


def give(kind, count=1):
    return f"give @a {item_arg(kind)} {count}"


def drop(kind, p):
    return (f'summon minecraft:item {fmt(p[0])} {fmt(p[1])} {fmt(p[2])} {{Tags:["s9"],Age:-32768s,PickupDelay:0s,'
            f'Motion:[0d,0d,0d],Item:{item_nbt(kind)}}}')


def has(kind, who="@a"):
    iid, cmd, tag, *_ = ITEMS[kind]
    return f"entity {who}[nbt={{Inventory:[{{tag:{{{tag}:1b}}}}]}}]"


def clear(kind, count=None):
    iid, cmd, tag, *_ = ITEMS[kind]
    return f"clear @a minecraft:{iid}{{{tag}:1b}}" + (f" {count}" if count is not None else "")


# =========================================================================
# VOICES
# =========================================================================
PREFIX = {"radio": "Radio", "garble": "Radio", "pa": "PA", "tape": "Tape", "tape_shaky": "Tape", "phone": "Phone",
          "whisper": None}


def say(key, force=True):
    """Subtitle + voice. Sets #talk so incidental lines can wait their turn."""
    ln = L[key]
    label, color, _, style = SPEAKERS[ln["who"]]
    ticks = dur_ticks(f"voice/{key}")
    prefix = PREFIX[style]
    if prefix is None:
        parts = [dict(text=ln["text"], color="dark_gray", italic=True)]
    else:
        parts = [dict(text=f"[{prefix}] ", color=color), dict(text=f"{label}: ", color=color),
                 dict(text=ln["text"], color="gray", italic=True)]
    out = []
    if force:
        out.append("stopsound @a voice")
    out += ["tellraw @a " + json.dumps([""] + parts, ensure_ascii=False),
            f"execute as @a at @s run playsound {NS}:voice.{key} voice @s ~ ~ ~ 1 1",
            f"scoreboard players set #talk s9 {ticks}"]
    return out


def say_later(key, stages):
    """An incidental line: waits until nobody is talking, and is dropped if the moment has passed."""
    lo, hi = stages
    name = f"line/{key}"
    fn(name,
       f"execute unless score #stage s9 matches {lo}..{hi} run return 0",
       f"execute if score #talk s9 matches 1.. run return run {sched(name, 20)}",
       say(key, force=False))
    return call(name)


def say_len(key):
    return dur_ticks(f"voice/{key}")


def lines(name, keys, gap=10, start=0, then=None):
    """A chain of voice lines, each starting after the previous one ends."""
    events = []
    t = start
    for k in keys:
        events.append((t, say(k)))
        t += say_len(k) + gap
    if then:
        events.append((t, then))
    from .mc import timeline
    return timeline(name, events)


# =========================================================================
# OBJECTIVES (the sidebar)
# =========================================================================
def objective(text, sub=None):
    out = ["scoreboard players reset * s9_hud",
           "scoreboard players set #o1 s9_hud 2",
           "scoreboard players display name #o1 s9_hud " + txt("> " + text, color="gold"),
           snd_me("minecraft:ui.toast.in", .5, 1.2)]
    if sub:
        out += ["scoreboard players set #o2 s9_hud 1",
                "scoreboard players display name #o2 s9_hud " + txt("  " + sub, color="gray", italic=True)]
    return out


# =========================================================================
# CORE
# =========================================================================
def core(build_steps, start_story):
    fn("load",
       "scoreboard objectives add s9 dummy",
       "scoreboard objectives add s9_id dummy",
       "scoreboard objectives add s9_ln dummy",
       "scoreboard objectives add s9_age dummy",
       "scoreboard objectives add s9_walk minecraft.custom:minecraft.walk_one_cm",
       "scoreboard objectives add s9_sprint minecraft.custom:minecraft.sprint_one_cm",
       "scoreboard objectives add s9_click minecraft.used:minecraft.carrot_on_a_stick",
       "scoreboard objectives add s9_deaths deathCount",
       "scoreboard objectives add s9_bat dummy",
       'scoreboard objectives add s9_hud dummy {"text":"STATION 9","color":"dark_red","bold":true}',
       "scoreboard objectives modify s9_hud numberformat blank",
       "scoreboard objectives setdisplay sidebar s9_hud",
       *[f"scoreboard players set #{n} s9 {n}" for n in (2, 5, 10, 20, 60, 100, 1000, 36000, 18000, -1)],
       "execute unless score #stage s9 = #stage s9 run scoreboard players set #stage s9 0",
       f"forceload add {W.FORCELOAD[0][0]} {W.FORCELOAD[0][1]} {W.FORCELOAD[1][0]} {W.FORCELOAD[1][1]}",
       call("rules"))

    fn("rules",
       *[f"gamerule {k} {v}" for k, v in [
           ("doDaylightCycle", "false"), ("doWeatherCycle", "false"), ("doMobSpawning", "false"),
           ("doWardenSpawning", "false"), ("doPatrolSpawning", "false"), ("doTraderSpawning", "false"),
           ("doInsomnia", "false"), ("mobGriefing", "false"), ("keepInventory", "true"),
           ("doImmediateRespawn", "true"), ("randomTickSpeed", "0"), ("announceAdvancements", "false"),
           ("doFireTick", "false"), ("commandBlockOutput", "false"), ("spawnRadius", "0"),
           ("doEntityDrops", "false"), ("sendCommandFeedback", "false"), ("showDeathMessages", "false"),
           ("naturalRegeneration", "true"), ("fallDamage", "false"), ("doTileDrops", "false"),
           ("maxCommandChainLength", "1000000"), ("disableRaids", "true"), ("doVinesSpread", "false")]],
       "difficulty normal", "time set 18000", "weather rain 1000000")

    fn("tick",
       f"execute as @a[tag=!s9_seen] run {call('join')}",
       "execute if score #talk s9 matches 1.. run scoreboard players remove #talk s9 1",
       "execute if score #stage s9 matches 2..10 run scoreboard players add #time s9 1",
       f"execute if score #stage s9 matches 2.. as @a at @s run {call('player/tick')}",
       f"execute if score #stage s9 matches 2.. run {call('amb/tick')}",
       f"execute if score #stage s9 matches 2 run {call('surface/tick')}",
       f"execute if score #stage s9 matches 3 run {call('ride/tick')}",
       f"execute if score #stage s9 matches 4 run {call('b8/tick')}",
       f"execute if score #stage s9 matches 5..8 run {call('b9/tick')}",
       f"execute if score #hmode s9 matches 1.. run {call('ai/tick')}",
       f"execute if score #stage s9 matches 9 run {call('chase/tick')}",
       f"execute if score #stage s9 matches 10 run {call('end/tick')}",
       call("story/always"),
       f"execute as @a[scores={{s9_deaths=1..}}] run {call('player/died')}")

    fn("join",
       "tag @s add s9_seen",
       f"execute if score #stage s9 matches 0 run tp @s {fmt(W.TRUCK_START[0])} {W.TRUCK_START[1]} {fmt(W.TRUCK_START[2])} {W.TRUCK_START[3]} 0",
       "execute if score #stage s9 matches 0 run effect give @s minecraft:blindness 6 0 true",
       f"execute if score #stage s9 matches 0 run {sched('start', 40)}",
       'execute if score #stage s9 matches 1.. run tellraw @s ["",' + txt("[Station 9] ", color="dark_red") + ","
       + json.dumps({"text": "Click here to restart the map", "color": "gray", "underlined": True,
                     "clickEvent": {"action": "run_command", "value": f"/function {NS}:start"}}) + "]")

    # A restart rebuilds the whole station over a few ticks, then starts the story.
    starter = ["# Rebuild everything and play from the top",
               "title @a times 0 200 20", "title @a title " + txt(" "),
               "title @a subtitle " + txt("rebuilding the station...", color="dark_gray"),
               "effect give @a minecraft:blindness 30 0 true",
               "gamemode spectator @a",
               call("reset")]
    for i, s in enumerate(build_steps):
        starter.append(sched(s, 2 + 2 * i) if i else call(s))
    starter.append(sched("start2", 4 + 2 * len(build_steps)))
    fn("start", starter)
    fn("start2", call("reset_entities"), start_story)

    reset = ["# Put the whole station back to its starting state"]
    reset += ["kill @e[tag=s9]", call("rules"), "stopsound @a", "effect clear @a", "clear @a",
              "scoreboard players reset * s9_hud"]
    reset += [f"scoreboard players set {f} s9 0" for f in FLAGS]
    reset += ["scoreboard players set #hnext s9 -1", "scoreboard players set #charge s9 %d" % BATTERY_TICKS,
              "scoreboard players set @a s9_deaths 0", "scoreboard players set @a s9_click 0",
              "tag @a remove s9_hidden",
              f"setworldspawn {int(W.TRUCK_START[0])} {W.TRUCK_START[1]} {int(W.TRUCK_START[2])}",
              f"spawnpoint @a {int(W.TRUCK_START[0])} {W.TRUCK_START[1]} {int(W.TRUCK_START[2])}",
              "effect give @a minecraft:saturation infinite 0 true",
              "data remove storage station9:ai m"]
    fn("reset_head", reset)   # the schedule clears are appended at the very end (see finish())


def finish():
    """Written last, once every scheduled function is known."""
    from .mc import files
    clears = [f"schedule clear {NS}:{s}" for s in sorted(scheduled) if s != "start2" and not s.startswith("build/")]
    files["reset"] = files.pop("reset_head") + clears


# =========================================================================
# PLAYER: flashlight, batteries, lockers, noise
# =========================================================================
def player():
    fn("player/tick",
       "# right-click toggles the flashlight",
       f"execute if score @s s9_click matches 1.. run {call('light/toggle')}",
       "scoreboard players set @s s9_click 0",
       f"execute store result score @s s9_bat run clear @s minecraft:iron_nugget{{s9batt:1b}} 0",
       "scoreboard players set #on s9 0",
       f"execute if score #light s9 matches 1 if score #fried s9 matches 0 if predicate {NS}:holding_light run scoreboard players set #on s9 1",
       f"execute if score #on s9 matches 1 if score #charge s9 matches ..0 run {call('light/empty')}",
       f"execute if score #on s9 matches 1 run {call('light/on')}",
       f"execute if score #on s9 matches 0 run {call('light/off')}",
       "scoreboard players add #hudt s9 1",
       f"execute if score #hudt s9 matches 10.. if predicate {NS}:holding_light run {call('light/hud')}",
       "execute if score #hudt s9 matches 10.. run scoreboard players set #hudt s9 0",
       f"{call('locker/check')}",
       f"execute if score #stage s9 matches 5..9 run {call('player/noise')}",
       "scoreboard players set @s s9_walk 0",
       "scoreboard players set @s s9_sprint 0")

    fn("light/toggle",
       f"execute unless predicate {NS}:holding_light run return 0",
       "execute if score #fried s9 matches 1 run return run " + snd_me("sfx.flash_off", .6, .6),
       "scoreboard players add #light s9 1",
       "execute if score #light s9 matches 2.. run scoreboard players set #light s9 0",
       "execute if score #light s9 matches 1 run " + snd_me("sfx.flash_on", .6),
       "execute if score #light s9 matches 0 run " + snd_me("sfx.flash_off", .6))

    fn("light/empty",
       "# out of charge: swap in a spare if there is one",
       f"execute if score @s s9_bat matches 1.. run {call('light/swap')}",
       "execute if score @s s9_bat matches 0 run scoreboard players set #on s9 0",
       "execute if score @s s9_bat matches 0 run scoreboard players set #light s9 0",
       "execute if score @s s9_bat matches 0 run " + actionbar("Flashlight: battery dead", "red"))
    fn("light/swap",
       "clear @s minecraft:iron_nugget{s9batt:1b} 1",
       f"scoreboard players set #charge s9 {BATTERY_TICKS}",
       snd_me("sfx.flash_on", .8, .8),
       actionbar("New battery", "yellow"))

    fn("light/on",
       "scoreboard players remove #charge s9 1",
       "scoreboard players set #beam s9 0",
       "scoreboard players set #ls s9 0",
       "# a dying battery stutters",
       "scoreboard players set #flick s9 0",
       f"execute if score #charge s9 matches ..{LOW_BATTERY} store result score #flick s9 run random value 1..9",
       f"execute if score #flick s9 matches 1 run return run {call('light/off')}",
       f"execute if score #flick s9 matches 2 if predicate {NS}:chance_5 run " + snd_me("sfx.flash_buzz", .5),
       f"execute anchored eyes positioned ^ ^ ^ run {call('light/ray')}")

    fn("light/ray",
       "scoreboard players add #ls s9 1",
       "# stop at the creature so it stands in the beam",
       f"execute positioned ~ ~-1.6 ~ if entity @e[tag=s9_hunter,distance=..1.1] run scoreboard players set #beam s9 1",
       f"execute if score #beam s9 matches 1 run return run {call('light/place')}",
       f"execute unless block ^ ^ ^0.5 #{NS}:beam_through run return run {call('light/place')}",
       f"execute if score #ls s9 matches {LIGHT_RANGE}.. run return run {call('light/place')}",
       f"execute positioned ^ ^ ^0.5 run {call('light/ray')}")

    fn("light/place",
       f"execute align xyz positioned ~.5 ~.5 ~.5 if entity @e[tag=s9_lp,distance=..0.1] run return 0",
       f"execute at @e[tag=s9_lp] if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air",
       "execute align xyz positioned ~.5 ~.5 ~.5 run tp @e[tag=s9_lp] ~ ~ ~",
       f"execute if score #charge s9 matches {LOW_BATTERY + 1}.. if block ~ ~ ~ #{NS}:airy run setblock ~ ~ ~ minecraft:light[level={LIGHT_LEVEL}]",
       f"execute if score #charge s9 matches ..{LOW_BATTERY} if block ~ ~ ~ #{NS}:airy run setblock ~ ~ ~ minecraft:light[level=10]")

    fn("light/off",
       "scoreboard players set #beam s9 0",
       f"execute at @e[tag=s9_lp] if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air",
       "tp @e[tag=s9_lp] 0.5 -60 0.5")

    bars = 10
    hud = ["scoreboard players operation #pc s9 = #charge s9",
           f"scoreboard players operation #pc s9 *= #{bars} s9",
           f"scoreboard players set #cap s9 {BATTERY_TICKS}",
           "scoreboard players operation #pc s9 /= #cap s9"]
    for n in range(bars + 1):
        bar = [dict(text="|" * n, color="yellow" if n > 2 else "red"), dict(text="|" * (bars - n), color="dark_gray")]
        hud.append(f"execute if score #pc s9 matches {n} run title @s actionbar " + json.dumps(
            [dict(text="Flashlight ", color="gray")] + bar + [dict(text="   spare: ", color="gray"),
                                                              {"score": {"name": "@s", "objective": "s9_bat"}, "color": "white"}]))
    fn("light/hud", "execute if score #fried s9 matches 1 run return run " +
       "title @s actionbar " + txt("Flashlight: burnt out", color="dark_red"), hud)

    # --- lockers ---------------------------------------------------------------------------
    fn("locker/check",
       "scoreboard players set #in s9 0",
       f"execute align xyz positioned ~.5 ~ ~.5 as @e[tag=s9_locker,distance=..0.3] at @s "
       "if block ~ ~ ~ minecraft:warped_door[open=false] run scoreboard players set #in s9 1",
       f"execute if score #in s9 matches 1 unless entity @s[tag=s9_hidden] run {call('locker/enter')}",
       f"execute if score #in s9 matches 0 if entity @s[tag=s9_hidden] run {call('locker/leave')}",
       f"execute if entity @s[tag=s9_hidden] if predicate {NS}:chance_1 run " + snd_me("sfx.held_breath", .35))
    fn("locker/enter",
       "tag @s add s9_hidden",
       "scoreboard players set #hidden s9 1",
       f"execute align xyz positioned ~.5 ~ ~.5 as @e[tag=s9_locker,distance=..0.3] run scoreboard players operation #lk s9 = @s s9_ln",
       f"execute if score #hmode s9 matches 1.. run {call('ai/hid')}")
    fn("locker/leave",
       "tag @s remove s9_hidden",
       "scoreboard players set #hidden s9 0",
       f"execute if score #hmode s9 matches 4 if score #hwait s9 matches 1.. at @e[tag=s9_hunter] if entity @s[distance=..4] run {call('ai/catch')}")

    fn("player/noise",
       "# sprinting carries a long way, walking a little, sneaking not at all",
       "execute if entity @s[tag=s9_hidden] run return 0",
       f"execute if score @s s9_sprint matches 1.. at @s if entity @e[tag=s9_hunter,distance=..20] run return run {call('ai/heard')}",
       f"execute if score @s s9_walk matches 1.. at @s if entity @e[tag=s9_hunter,distance=..6] run {call('ai/heard')}")

    # --- death -------------------------------------------------------------------------------
    fn("player/died",
       "scoreboard players set @s s9_deaths 0",
       "scoreboard players add #deaths s9 1",
       "effect give @s minecraft:darkness 4 0 true",
       "effect give @s minecraft:blindness 2 0 true",
       "effect give @s minecraft:saturation infinite 0 true",
       "tag @s remove s9_hidden",
       f"{call('light/off')}",
       f"execute if score #stage s9 matches 5..8 run {call('ai/respawned')}",
       f"execute if score #stage s9 matches 9 run {call('chase/respawned')}")


def checkpoint(cp):
    x, y, z, yaw = cp
    return f"spawnpoint @a {int(x)} {y} {int(z)} {yaw}"


# =========================================================================
# AMBIENCE: one long bed per area, restarted as it ends (never a short loop)
# =========================================================================
AREAS = {1: "amb.wind", 2: "amb.b8", 3: "amb.b9"}


def ambience():
    beds = {1: dur_ticks("amb/wind"), 2: dur_ticks("amb/b8"), 3: dur_ticks("amb/b9")}
    lines_ = ["scoreboard players set #na s9 0",
              "execute as @a[x=-100,y=95,z=-100,dx=300,dy=100,dz=300] run scoreboard players set #na s9 1",
              "execute as @a[x=-100,y=47,z=-100,dx=300,dy=10,dz=300] run scoreboard players set #na s9 2",
              "execute as @a[x=-100,y=30,z=-100,dx=300,dy=16,dz=300] run scoreboard players set #na s9 3",
              "execute if score #stage s9 matches 3 run scoreboard players set #na s9 0",
              "execute if score #stage s9 matches 9..10 run scoreboard players set #na s9 0",
              f"execute unless score #na s9 = #area s9 run {call('amb/switch')}",
              "scoreboard players remove #amb s9 1",
              f"execute if score #amb s9 matches ..0 run {call('amb/play')}"]
    fn("amb/tick", lines_)
    fn("amb/switch",
       *[f"stopsound @a ambient {NS}:{s}" for s in AREAS.values()],
       "scoreboard players operation #area s9 = #na s9",
       "scoreboard players set #amb s9 0")
    play = ["scoreboard players set #amb s9 999999"]
    vols = {1: .55, 2: .5, 3: .6}
    for a, s in AREAS.items():
        play += [f"execute if score #area s9 matches {a} run scoreboard players set #amb s9 {beds[a] - 30}",
                 f"execute if score #area s9 matches {a} as @a at @s run playsound {NS}:{s} ambient @s ~ ~ ~ {vols[a]} 1"]
    fn("amb/play", play)


# =========================================================================
# PREDICATES AND TAGS
# =========================================================================
def predicates():
    from .mc import predicates as P
    P["holding_light"] = {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {
        "equipment": {"mainhand": {"items": ["minecraft:carrot_on_a_stick"], "nbt": "{s9light:1b}"}}}}
    P["lit"] = {"condition": "minecraft:location_check", "predicate": {"light": {"light": {"min": 6}}}}
    P["bright"] = {"condition": "minecraft:location_check", "predicate": {"light": {"light": {"min": 9}}}}
    P["sneaking"] = {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {"is_sneaking": True}}}
    for n in (1, 2, 5, 10, 25, 50):
        P[f"chance_{n}"] = {"condition": "minecraft:random_chance", "chance": n / 100}


SEE_THROUGH = ["minecraft:air", "minecraft:cave_air", "minecraft:void_air", "#minecraft:doors", "minecraft:light", "minecraft:glass", "#minecraft:impermeable", "minecraft:glass_pane",
               "#minecraft:all_signs", "#minecraft:buttons", "minecraft:lever", "minecraft:redstone_wire", "minecraft:cobweb",
               "#minecraft:candles", "minecraft:iron_bars", "minecraft:chain", "#minecraft:flower_pots", "minecraft:snow",
               "#minecraft:wool_carpets", "minecraft:glow_lichen", "minecraft:end_rod", "minecraft:lantern",
               "minecraft:brewing_stand", "minecraft:water", "#minecraft:rails", "minecraft:tripwire",
               "minecraft:light_gray_stained_glass_pane", "minecraft:black_stained_glass_pane"]
AIRY = ["minecraft:air", "minecraft:cave_air", "minecraft:light"]
BEAM_THROUGH = [b for b in SEE_THROUGH if b != "#minecraft:doors"]


def tags():
    return {"see_through": SEE_THROUGH, "beam_through": BEAM_THROUGH, "airy": AIRY}
