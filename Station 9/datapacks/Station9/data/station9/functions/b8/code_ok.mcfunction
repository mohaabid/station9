scoreboard players set #s_code s9 1
playsound station9:sfx.beep_ok block @a 49 53 23 1 1 0
data modify block 49 53 23 front_text.messages set value ['{"text": "STAIR OVERRIDE"}','{"text": "ACCEPTED"}','{"text": ""}','{"text": ""}']
data modify block 49 53 23 front_text.color set value "lime"
fill 11 51 21 12 53 21 minecraft:air
playsound station9:sfx.gate_open block @a 12 52 21 1.2 1 0
setblock 13 52 25 minecraft:redstone_lamp[lit=true]
setblock 10 48 32 minecraft:redstone_lamp[lit=true]
setblock 7 43 25 minecraft:redstone_lamp[lit=true]
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "That's it, the stairwell's open. Go down to B9.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_code_ok voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 79
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Go down to B9", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Stairwell B, in the lobby", "color": "gray", "italic": true}
