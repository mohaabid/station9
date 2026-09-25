setblock 28 42 20 minecraft:stone_button[face=wall,facing=north]
execute if score #stage s9 matches 3 run function station9:event/k_open
execute if score #stage s9 matches 2 run function station9:event/k_deny
