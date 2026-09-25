scoreboard players set #stage s9 7
scoreboard players set #tab s9 1
scoreboard players set #cscene s9 1
fill 30 41 21 31 43 21 minecraft:air
playsound station9:sfx.beep_ok block @a 28 42 20 1 1 0
playsound station9:sfx.gate_open block @a 31 42 21 1 1 0
data modify block 28 43 20 front_text.messages set value ['{"text": "ACCESS"}','{"text": "GRANTED"}','{"text": ""}','{"text": ""}']
data modify block 28 43 20 front_text.color set value "lime"
spawnpoint @a 31 41 20 0
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Find a fuse", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Containment", "color": "gray", "italic": true}
