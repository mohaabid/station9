"""Shortcuts for testing: jump straight to a point in the story (after one full start)."""
from . import world as W
from .mc import call, fmt, fn
from .systems import give


def build():
    common = [call("reset"), call("reset_entities"), "gamemode adventure @a", "effect clear @a",
              "effect give @a minecraft:saturation infinite 0 true",
              give("light"), give("battery", 2), "scoreboard players set #kit s9 1", "scoreboard players set #s_relay s9 1",
              "scoreboard players set #s_code s9 1", "scoreboard players set #s_release s9 1",
              "fill 11 51 21 12 53 21 minecraft:air", "fill 6 51 19 6 52 20 minecraft:air",
              call("build/lamps_off"), call("build/b8_backup")]
    fn("debug/b9", common, "scoreboard players set #stage s9 4",
       f"tp @a {fmt(W.CP_B9[0])} 41 {fmt(W.CP_B9[2])} -90 0", call("story/b9_arrive"))
    fn("debug/roam", common, "scoreboard players set #stage s9 4",
       f"tp @a {fmt(W.CP_B9[0])} 41 {fmt(W.CP_B9[2])} -90 0", call("story/b9_arrive"), call("b9/teach_3"),
       "scoreboard players set #hgrace s9 0", "stopsound @a voice")
    fn("debug/chase", common, "scoreboard players set #stage s9 8",
       call("build/b9_backup"), "tp @a 52.5 41 20.5 -90 0", "scoreboard players set #tab s9 1",
       "fill 30 41 21 31 43 21 minecraft:air", call("gen/1"))
