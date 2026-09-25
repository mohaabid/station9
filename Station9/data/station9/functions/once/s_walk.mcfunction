scoreboard players set #s_walk s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Nobody's been on site for 41 days. The guard walked off the job the night it went dark. Can't say I blame him.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_walk voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 142
