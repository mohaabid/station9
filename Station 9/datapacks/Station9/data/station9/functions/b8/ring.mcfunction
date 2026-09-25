execute if score #s_answered s9 matches 1 run return 0
scoreboard players add #rings s9 1
execute if score #rings s9 matches 4.. run return 0
playsound station9:sfx.phone_ring block @a 46 52 4 1.6 1 0
execute store result score #st s9 run random value 260..520
execute store result storage station9:fx d.t int 1 run scoreboard players get #st s9
function station9:b8/ring_m with storage station9:fx d
