scoreboard players remove #alarm s9 1
scoreboard players operation #p s9 = #alarm s9
scoreboard players operation #p s9 %= #2 s9
execute if score #p s9 matches 0 run execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.7 1.0
execute if score #p s9 matches 1 run execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.7 0.7
execute if score #alarm s9 matches 1.. run schedule function station9:fx/alarm 8t
