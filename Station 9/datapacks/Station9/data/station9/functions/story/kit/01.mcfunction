stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "The lift house is at the north end, under the headframe. Call the cage.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_to_lift voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 86
