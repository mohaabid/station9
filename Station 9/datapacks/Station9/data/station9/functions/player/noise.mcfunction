# sprinting carries a long way, walking a little, sneaking not at all
execute if entity @s[tag=s9_hidden] run return 0
execute if score @s s9_sprint matches 1.. at @s if entity @e[tag=s9_hunter,distance=..20] run return run function station9:ai/heard
execute if score @s s9_walk matches 1.. at @s if entity @e[tag=s9_hunter,distance=..6] run function station9:ai/heard
