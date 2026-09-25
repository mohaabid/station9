execute if score @s s9_walk matches 1.. run scoreboard players add @s s9_fs 1
execute if score @s s9_sprint matches 1.. run scoreboard players add @s s9_fs 2
execute if score @s s9_walk matches 1.. run scoreboard players set @s s9_idle 0
execute if score @s s9_sprint matches 1.. run scoreboard players set @s s9_idle 0
execute unless score @s s9_walk matches 1.. unless score @s s9_sprint matches 1.. run scoreboard players add @s s9_idle 1
execute if score @s s9_fs matches 10.. run function station9:fx/footstep_far
execute if score @s s9_idle matches 14 if score #echoes s9 matches ..2 run function station9:fx/footstep_near
