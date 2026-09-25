# you're back at the checkpoint; it goes somewhere far away and waits
scoreboard players set #hgrace s9 160
scoreboard players set #hmode s9 1
scoreboard players set #hspd s9 55
execute if score #stage s9 matches 5..6 run function station9:ai/far_west
execute if score #stage s9 matches 7..8 run function station9:ai/far_east
execute if score #s_caught s9 matches 0 run schedule function station9:story/caught_line 60t
