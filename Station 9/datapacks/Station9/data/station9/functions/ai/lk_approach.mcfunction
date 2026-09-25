# walk the last few steps right up to the locker door
execute as @e[tag=s9_hunter] at @s unless entity @e[tag=s9_lkt,distance=..1.25] facing entity @e[tag=s9_lkt,limit=1] feet run return run tp @s ^ ^ ^0.08 ~ 0
scoreboard players set #lkphase s9 2
function station9:ai/lk_wait
