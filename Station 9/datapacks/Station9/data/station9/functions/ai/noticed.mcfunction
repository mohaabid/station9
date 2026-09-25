# you just caught sight of it: a sting if it's close and it's been a while
execute if score #stingcd s9 matches 1.. run return 0
execute as @e[tag=s9_hunter] at @s if entity @a[distance=..12] run function station9:ai/sting
