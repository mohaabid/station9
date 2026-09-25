setblock 2 52 19 minecraft:polished_blackstone_button[face=wall,facing=east,powered=false]
playsound station9:sfx.beep_key block @a 2 52 19 1 1 0
execute if score #s_release s9 matches 1 run return 0
scoreboard players set #s_release s9 1
playsound station9:sfx.gate_open block @a 6 52 20 1.2 0.8 0
schedule function station9:b8/gate_jammed 40t
