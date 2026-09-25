execute as @a[tag=!s9_seen] run function station9:join
execute if score #talk s9 matches 1.. run scoreboard players remove #talk s9 1
execute if score #stage s9 matches 2..10 run scoreboard players add #time s9 1
execute if score #stage s9 matches 2.. as @a at @s run function station9:player/tick
execute if score #stage s9 matches 2.. run function station9:amb/tick
execute if score #stage s9 matches 2 run function station9:surface/tick
execute if score #stage s9 matches 3 run function station9:ride/tick
execute if score #stage s9 matches 4 run function station9:b8/tick
execute if score #stage s9 matches 5..8 run function station9:b9/tick
execute if score #hmode s9 matches 1.. run function station9:ai/tick
execute if score #stage s9 matches 9 run function station9:chase/tick
execute if score #stage s9 matches 10 run function station9:end/tick
function station9:story/always
execute as @a[scores={s9_deaths=1..}] run function station9:player/died
