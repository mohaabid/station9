tp @e[tag=s9_aim,limit=1] ~ ~ ~ ~ ~
execute store result score #ay s9 run data get entity @e[tag=s9_aim,limit=1] Rotation[0] 100
execute store result score #ap s9 run data get entity @e[tag=s9_aim,limit=1] Rotation[1] 100
execute store result score #py s9 run data get entity @s Rotation[0] 100
execute store result score #pp s9 run data get entity @s Rotation[1] 100
scoreboard players operation #ay s9 -= #py s9
scoreboard players operation #ay s9 %= #36000 s9
execute if score #ay s9 matches 18000.. run scoreboard players remove #ay s9 36000
scoreboard players operation #ap s9 -= #pp s9
execute if score #ay s9 matches -5200..5200 if score #ap s9 matches -4200..4200 run scoreboard players set #cand s9 1
scoreboard players set #rs s9 0
function station9:ai/los_ray
