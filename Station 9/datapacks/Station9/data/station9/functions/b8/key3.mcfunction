setblock 49 53 22 minecraft:stone_button[face=wall,facing=west,powered=false]
execute if score #s_relay s9 matches 0 run return run title @a actionbar {"text": "The panel is dead. No power.", "color": "dark_gray"}
execute if score #s_code s9 matches 1 run return 0
execute if score #kpwait s9 matches 1 run return 0
playsound station9:sfx.beep_key block @a 49 53 22 1 1 0
scoreboard players operation #code s9 *= #10 s9
scoreboard players add #code s9 3
scoreboard players add #digits s9 1
function station9:b8/key_show
