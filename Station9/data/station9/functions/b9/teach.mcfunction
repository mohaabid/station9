scoreboard players add #tt s9 1
execute if score #watched s9 matches 1 run scoreboard players add #tw s9 1
execute if score #watched s9 matches 1 run scoreboard players set #tu s9 0
execute if score #watched s9 matches 0 run scoreboard players add #tu s9 1
execute if score #teach s9 matches 2.. if score #tu s9 matches 60.. run function station9:b9/teach_3
execute if score #tw s9 matches 25.. if score #talk s9 matches ..0 run execute if score #s_watch s9 matches 0 run function station9:once/s_watch
execute if score #teach s9 matches 1 if score #tw s9 matches 70.. run function station9:b9/teach_1
execute if score #teach s9 matches 2 if score #tw s9 matches 50.. run function station9:b9/teach_2
execute if score #teach s9 matches 3 if score #tw s9 matches 40.. run function station9:b9/teach_3
execute if score #tt s9 matches 900.. run function station9:b9/teach_3
execute as @e[tag=s9_hunter] at @s if entity @a[distance=..7] run function station9:b9/teach_3
