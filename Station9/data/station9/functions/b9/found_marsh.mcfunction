scoreboard players set #marsh s9 1
setblock 12 44 0 minecraft:redstone_lamp[lit=true]
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Oh, God. That's Marsh. ...I'm sorry. Take his recorder.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_marsh voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 84
