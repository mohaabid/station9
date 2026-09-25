stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Where did it go? It was right there. ...Keep your light on. Keep moving.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_gone voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 94
