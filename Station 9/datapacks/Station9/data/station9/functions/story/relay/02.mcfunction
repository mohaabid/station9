stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "The cage won't move until main power's back, so we do this the hard way. Take the stairs down to B9.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a1_contact2 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 136
