scoreboard players set #s_watch s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Don't take your eyes off it.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_watch voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 42
