execute unless score #stage s9 matches 5..7 run return 0
execute if score #talk s9 matches 1.. run return run schedule function station9:line/a2_nofuse 20t
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Generator B is missing its fuse. There are spares in containment, but that door needs a level 3 keycard.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_nofuse voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 127
