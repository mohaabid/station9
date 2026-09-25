scoreboard players set #s_deny s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Level 3. Marsh had level 3. Try the staff office, north side of the corridor.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_deny voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 111
