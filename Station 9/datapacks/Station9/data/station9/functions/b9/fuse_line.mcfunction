stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "It's gone. ...It's heading east. It knows where you're going.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_after_fuse voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 77
