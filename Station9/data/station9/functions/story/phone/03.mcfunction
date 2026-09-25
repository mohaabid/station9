stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Who were you talking to? ...The station phones have been dead for six weeks.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_phone_after voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 90
