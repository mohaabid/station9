execute unless score #stage s9 matches 4..5 run return 0
execute if score #talk s9 matches 1.. run return run schedule function station9:line/a1_stairs 20t
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Every level between you and B9 is dark on my board. Keep going down.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_stairs voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 96
