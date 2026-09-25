scoreboard players set #s_nofuse s9 1
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Generator B is missing its fuse. There are spares in containment, but that door needs a level 3 keycard.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_nofuse voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 127
