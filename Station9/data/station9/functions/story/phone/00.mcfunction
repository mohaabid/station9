stopsound @a voice
tellraw @a ["", {"text": "[Phone] ", "color": "dark_aqua"}, {"text": "Reyes?: ", "color": "dark_aqua"}, {"text": "Hey. It's Reyes. I'm down here with you. I'm in the kitchen, behind the door. ...Come and see.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.phone voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 201
