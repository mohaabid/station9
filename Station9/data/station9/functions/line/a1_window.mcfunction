execute unless score #stage s9 matches 4..4 run return 0
execute if score #talk s9 matches 1.. run return run schedule function station9:line/a1_window 20t
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Your heart rate just spiked. What did you see? ...Okay. Keep going.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_window voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 108
