stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Talk to me. ...Okay. Nearly there. B6. B7...", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_ride4 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 74
