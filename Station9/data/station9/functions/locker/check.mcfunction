scoreboard players set #in s9 0
execute align xyz positioned ~.5 ~ ~.5 as @e[tag=s9_locker,distance=..0.3] at @s if block ~ ~ ~ minecraft:warped_door[open=false] run scoreboard players set #in s9 1
execute if score #in s9 matches 1 unless entity @s[tag=s9_hidden] run function station9:locker/enter
execute if score #in s9 matches 0 if entity @s[tag=s9_hidden] run function station9:locker/leave
execute if entity @s[tag=s9_hidden] if predicate station9:chance_1 run execute as @a at @s run playsound station9:sfx.held_breath master @s ~ ~ ~ 0.35 1.0
