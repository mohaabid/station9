tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Your heart rate just spiked. What did you see? ...Okay. Keep going.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_window voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 108
