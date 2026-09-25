execute if score #talk s9 matches 1.. run return run scoreboard players remove #hint s9 100
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Security on that shift used times for their codes. The time something happened. Hale's lab logs might have it.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_hint1 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 138
