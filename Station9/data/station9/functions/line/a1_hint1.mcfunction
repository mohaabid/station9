execute unless score #stage s9 matches 4..4 run return 0
execute if score #talk s9 matches 1.. run return run schedule function station9:line/a1_hint1 20t
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Security on that shift used times for their codes. The time something happened. Hale's lab logs might have it.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_hint1 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 138
