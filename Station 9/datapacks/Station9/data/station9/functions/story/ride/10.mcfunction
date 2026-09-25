stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Get it running and every light in the place comes back on. The recovery team goes down in the morning. In and out.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_ride2 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 135
