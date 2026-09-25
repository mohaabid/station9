scoreboard players set #hwait s9 130
execute as @e[tag=s9_hunter] at @s run tp @s ~ ~ ~ facing entity @e[tag=s9_lkt,limit=1] feet
execute as @e[tag=s9_hunter] at @s run tp @s ~ ~ ~ ~ 0
execute at @e[tag=s9_hunter] run playsound station9:sfx.sniff hostile @a ~ ~1.6 ~ 1.2 0.8 0
schedule function station9:ai/locker_breath 40t
