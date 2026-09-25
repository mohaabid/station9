# at the end of its route and you're right there: straight at you
execute unless score #los s9 matches 1 unless score #hmode s9 matches 5 run return 0
execute as @e[tag=s9_hunter] at @s unless entity @a[tag=!s9_hidden,distance=..10] run return 0
execute store result storage station9:ai m.spd double 0.001 run scoreboard players get #hspd s9
function station9:ai/approach_m with storage station9:ai m
scoreboard players operation #hdist s9 += #hspd s9
execute if score #hdist s9 >= #hstride s9 run function station9:ai/footstep
