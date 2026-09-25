scoreboard players set #s_caught s9 1
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "...You're back. I thought I'd lost you. Stay out of its reach.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_caught voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 77
