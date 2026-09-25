stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Thanks. ...Huh. Marsh never signed out. None of the B9 shift did.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_signed voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 95
