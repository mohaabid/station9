stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Hang on. Your cage weight reads wrong. It's about two hundred and forty kilos too heavy.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.e_heavy voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 118
