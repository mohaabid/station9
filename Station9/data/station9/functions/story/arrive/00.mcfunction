stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Reyes here, radio check. ...Good, I've got you. Sorry about the weather. Welcome to Site 9.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_arrive voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 135
