setblock 13 52 20 minecraft:stone_button[face=wall,facing=north,powered=false]
execute if score #s_code s9 matches 1 run return 0
playsound station9:sfx.beep_bad block @a 13 52 20 1 1 0
title @a actionbar {"text": "STAIRWELL B: LOCKDOWN.  Override at Security.", "color": "red"}
