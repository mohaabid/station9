# right-click toggles the flashlight
execute if score @s s9_click matches 1.. run function station9:light/toggle
scoreboard players set @s s9_click 0
execute store result score @s s9_bat run clear @s minecraft:iron_nugget{s9batt:1b} 0
scoreboard players set #on s9 0
execute if score #light s9 matches 1 if score #fried s9 matches 0 if predicate station9:holding_light run scoreboard players set #on s9 1
execute if score #on s9 matches 1 if score #charge s9 matches ..0 run function station9:light/empty
execute if score #on s9 matches 1 run function station9:light/on
execute if score #on s9 matches 0 run function station9:light/off
scoreboard players add #hudt s9 1
execute if score #hudt s9 matches 10.. if predicate station9:holding_light run function station9:light/hud
execute if score #hudt s9 matches 10.. run scoreboard players set #hudt s9 0
function station9:locker/check
execute if score #stage s9 matches 5..9 run function station9:player/noise
scoreboard players set @s s9_walk 0
scoreboard players set @s s9_sprint 0
