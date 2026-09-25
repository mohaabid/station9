stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Every time your light is on it, it stops. The second it's dark, it moves. Keep it in the light.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_rule voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 120
