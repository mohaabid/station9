execute if score #sees s9 matches 1 run scoreboard players set #lost s9 0
execute if score #sees s9 matches 0 run scoreboard players add #lost s9 1
execute if score #lost s9 matches 0 if score #e5 s9 matches 0 unless score #htarget s9 = #pnode s9 run function station9:ai/to_player
scoreboard players set #hspd s9 115
execute as @e[tag=s9_hunter] at @s if entity @a[tag=!s9_hidden,distance=..6] run scoreboard players set #hspd s9 215
execute if score #lost s9 matches 160.. run function station9:ai/give_up
