# it went home. The fuse is at its feet.
execute if score #watched s9 matches 1 run return 0
scoreboard players set #cscene s9 2
tp @e[tag=s9_hunter] 31.5 41 29.5 180 0
scoreboard players set #hnode s9 39
scoreboard players set #hnext s9 -1
scoreboard players set #htarget s9 39
scoreboard players set #hmode s9 3
scoreboard players set #hspd s9 115
scoreboard players set #lost s9 0
scoreboard players set #hgrace s9 0
scoreboard players set #hwait s9 0
setblock 31 44 23 minecraft:redstone_lamp[lit=true]
setblock 31 44 28 minecraft:redstone_lamp[lit=true]
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "The fuses are in the cell. ...It's in there. Standing in the corner. Keep your light on it and take the fuse.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_contain voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 135
