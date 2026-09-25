scoreboard players set @s s9_deaths 0
scoreboard players add #deaths s9 1
effect give @s minecraft:darkness 4 0 true
effect give @s minecraft:blindness 2 0 true
effect give @s minecraft:saturation infinite 0 true
tag @s remove s9_hidden
function station9:light/off
execute if score #stage s9 matches 5..8 run function station9:ai/respawned
execute if score #stage s9 matches 9 run function station9:chase/respawned
