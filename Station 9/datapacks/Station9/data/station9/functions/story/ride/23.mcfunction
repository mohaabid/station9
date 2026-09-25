stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "...can you hear... cage brakes... B8... don't...", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_static voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 98
