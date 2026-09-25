stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Got the kit? Right-click the flashlight to switch it on. Batteries don't last long down there, so grab any spares you find.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_kit voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 157
