scoreboard players set #s_coffee s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Is Frank's coffee machine still in there? Worst coffee on the mountain. Don't drink it. Six weeks.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_coffee voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 125
