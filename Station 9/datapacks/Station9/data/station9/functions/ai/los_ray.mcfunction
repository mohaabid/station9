scoreboard players add #rs s9 1
execute positioned ~ ~-2.1 ~ if entity @e[tag=s9_hunter,distance=..0.9] run return run scoreboard players set #los s9 1
execute unless block ~ ~ ~ #station9:see_through run return 0
execute if score #rs s9 matches 88.. run return 0
execute positioned ^ ^ ^0.5 run function station9:ai/los_ray
