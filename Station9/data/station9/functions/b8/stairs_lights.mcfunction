setblock 34 51 16 minecraft:air
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Every level between you and B9 is dark on my board. Keep going down.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_stairs voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 96
function station9:story/stairs_down
