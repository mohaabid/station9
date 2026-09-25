stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Wait. Containment B9 reads open. It's read open for 41 days.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a3_wait voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 109
