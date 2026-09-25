scoreboard players set #catching s9 1
effect give @a minecraft:slowness 2 255 true
effect give @a minecraft:jump_boost 2 200 true
execute as @a at @s run tp @s ~ ~ ~ facing entity @e[tag=s9_hunter,limit=1] eyes
execute as @a at @s rotated ~ 0 positioned ^ ^ ^1.0 run tp @e[tag=s9_hunter] ~ ~ ~ facing entity @a[limit=1] feet
execute as @e[tag=s9_hunter] at @s run tp @s ~ ~ ~ ~ 0
execute as @a at @s run playsound station9:sfx.scream hostile @s ~ ~ ~ 1 1
execute as @a at @s run playsound station9:sfx.sting_hit master @s ~ ~ ~ 0.9 1
schedule function station9:ai/catch2 14t
