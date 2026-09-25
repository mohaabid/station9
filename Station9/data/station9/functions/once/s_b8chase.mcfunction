scoreboard players set #s_b8chase s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "The cage has power now! Get to the lift!", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a3_b8 voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 61
setblock 4 54 20 minecraft:redstone_lamp[lit=true]
fill 6 51 19 6 53 20 minecraft:air
