stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "I've got you! Bringing you up now!", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a3_lift voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 48
