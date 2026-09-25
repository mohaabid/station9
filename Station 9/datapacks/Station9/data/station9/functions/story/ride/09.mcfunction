stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Here's the job. Generator B, bottom level. It failed 41 days ago and took the whole station with it.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_ride1 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 130
