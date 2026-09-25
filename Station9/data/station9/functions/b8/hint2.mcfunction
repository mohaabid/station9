execute if score #talk s9 matches 1.. run return run scoreboard players remove #hint s9 100
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "I dug it out of an old maintenance ticket. Try zero, two, one, four.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_hint2 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 107
