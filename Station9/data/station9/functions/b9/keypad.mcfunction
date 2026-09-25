setblock 28 42 20 minecraft:stone_button[face=wall,facing=north,powered=false]
execute if score #stage s9 matches 6 run return run function station9:b9/k_open
execute unless score #stage s9 matches 5 run return 0
title @a actionbar {"text": "ACCESS DENIED - LEVEL 3 KEYCARD REQUIRED", "color": "red"}
playsound station9:sfx.beep_bad block @a 28 42 20 1 1 0
execute if score #s_deny s9 matches 0 run function station9:once/s_deny
