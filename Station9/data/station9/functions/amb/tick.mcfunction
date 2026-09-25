scoreboard players set #na s9 0
execute as @a[y=95,dy=100] run scoreboard players set #na s9 1
execute as @a[y=47,dy=10] run scoreboard players set #na s9 2
execute as @a[y=30,dy=16] run scoreboard players set #na s9 3
execute if score #stage s9 matches 3 run scoreboard players set #na s9 0
execute if score #stage s9 matches 9..10 run scoreboard players set #na s9 0
execute unless score #na s9 = #area s9 run function station9:amb/switch
scoreboard players remove #amb s9 1
execute if score #amb s9 matches ..0 run function station9:amb/play
