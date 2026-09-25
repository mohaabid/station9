scoreboard players remove #shake s9 1
scoreboard players operation #p s9 = #shake s9
scoreboard players operation #p s9 %= #2 s9
execute if score #p s9 matches 0 as @a at @s run tp @s ~ ~ ~ ~1.4 ~-1.1
execute if score #p s9 matches 1 as @a at @s run tp @s ~ ~ ~ ~-1.4 ~1.1
execute if score #shake s9 matches 1.. run schedule function station9:fx/shake 1t
