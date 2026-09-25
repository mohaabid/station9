scoreboard players set #s_hut s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "That's the hut. Sign the sheet by the door. Company rules, even now.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_hut voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 92
