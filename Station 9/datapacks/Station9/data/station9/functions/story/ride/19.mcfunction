stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "What was that? ...Your cage camera just cut out. Probably debris on the roof. Stay still.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_ride3 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 109
