execute store result storage station9:ai m.spd double 0.001 run scoreboard players get #hspd s9
function station9:ai/move with storage station9:ai m
scoreboard players operation #hdist s9 += #hspd s9
execute if score #hdist s9 >= #hstride s9 run function station9:ai/footstep
