setblock 53 42 20 minecraft:lever[face=wall,facing=west,powered=false]
execute if score #stage s9 matches 8 run return run function station9:gen/1
playsound minecraft:block.lever.click block @a 53 42 20 1 0.5 0
title @a actionbar {"text": "Generator B: FUSE MISSING", "color": "red"}
