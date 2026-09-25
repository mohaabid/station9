scoreboard players remove #charge s9 1
scoreboard players set #beam s9 0
scoreboard players set #ls s9 0
# a dying battery stutters
scoreboard players set #flick s9 0
execute if score #charge s9 matches ..540 store result score #flick s9 run random value 1..9
execute if score #flick s9 matches 1 run return run function station9:light/off
execute if score #flick s9 matches 2 if predicate station9:chance_5 run execute as @a at @s run playsound station9:sfx.flash_buzz master @s ~ ~ ~ 0.5 1.0
execute anchored eyes positioned ^ ^ ^ run function station9:light/ray
