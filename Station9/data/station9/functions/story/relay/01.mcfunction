stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "There you are! I lost you for four minutes. The cage brakes locked at B8. Are you hurt? ...Okay. Okay.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_contact voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 144
