stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "The stairwell's in lockdown. There's an override panel in the security office, east end of the hall. It needs the duty code.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_locked voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 155
