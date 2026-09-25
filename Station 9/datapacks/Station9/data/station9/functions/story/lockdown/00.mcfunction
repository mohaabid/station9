stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Power's up! Every level is lighting up on my board!", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a3_power voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 67
