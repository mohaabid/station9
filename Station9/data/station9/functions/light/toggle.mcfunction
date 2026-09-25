execute unless predicate station9:holding_light run return 0
execute if score #fried s9 matches 1 run return run execute as @a at @s run playsound station9:sfx.flash_off master @s ~ ~ ~ 0.6 0.6
scoreboard players add #light s9 1
execute if score #light s9 matches 2.. run scoreboard players set #light s9 0
execute if score #light s9 matches 1 run execute as @a at @s run playsound station9:sfx.flash_on master @s ~ ~ ~ 0.6 1.0
execute if score #light s9 matches 0 run execute as @a at @s run playsound station9:sfx.flash_off master @s ~ ~ ~ 0.6 1.0
