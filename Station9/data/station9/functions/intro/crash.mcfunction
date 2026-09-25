setblock 4 44 20 minecraft:redstone_lamp[lit=false]
execute as @a at @s run playsound minecraft:entity.generic.explode hostile @s ~ ~ ~ 0.7 0.5
execute as @a at @s run playsound minecraft:block.anvil.land hostile @s ~ ~ ~ 1 0.5
execute as @a at @s run playsound minecraft:block.chain.break hostile @s ~ ~ ~ 1 0.6
title @a actionbar {"text": "B9", "color": "dark_red"}
effect give @a minecraft:darkness 8 0 true
scoreboard players set #shake s9 14
schedule function station9:fx/shake 1t
schedule function station9:intro/2 60t
