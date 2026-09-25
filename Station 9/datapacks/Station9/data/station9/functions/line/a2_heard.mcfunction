execute unless score #stage s9 matches 5..8 run return 0
execute if score #talk s9 matches 1.. run return run schedule function station9:line/a2_heard 20t
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "It heard you. Walk. Don't run.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_heard voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 55
