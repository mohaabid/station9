execute if score #e5 s9 matches 0 unless score #htarget s9 = #pnode s9 if entity @a[tag=!s9_hidden] run function station9:ai/to_player
scoreboard players set #hspd s9 232
execute as @e[tag=s9_hunter] at @s unless entity @a[distance=..20] run scoreboard players set #hspd s9 300
execute if score #watched s9 matches 1 run scoreboard players set #hspd s9 55
