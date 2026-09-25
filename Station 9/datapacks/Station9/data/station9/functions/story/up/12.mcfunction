stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "B7. B6. ...You did it. I'm so sorry. Nobody told me what was down there.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.e_ride voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 114
