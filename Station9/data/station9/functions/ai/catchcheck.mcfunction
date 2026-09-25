execute if score #hgrace s9 matches 1.. run return 0
execute if score #catching s9 matches 1 run return 0
execute if score #frozen s9 matches 1 run return 0
execute as @e[tag=s9_hunter] at @s if entity @a[tag=!s9_hidden,gamemode=adventure,distance=..1.3] run function station9:ai/catch
