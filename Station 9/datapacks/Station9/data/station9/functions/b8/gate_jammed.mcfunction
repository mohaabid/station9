fill 6 51 19 6 52 20 minecraft:air
playsound station9:sfx.bang hostile @a 6 52 20 0.7 1.3 0
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Find the comms room", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  B8 - east side of the hall", "color": "gray", "italic": true}
