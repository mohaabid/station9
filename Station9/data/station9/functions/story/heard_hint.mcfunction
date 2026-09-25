scoreboard players set #s_heard s9 1
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "It heard you. Walk. Don't run.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_heard voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 55
