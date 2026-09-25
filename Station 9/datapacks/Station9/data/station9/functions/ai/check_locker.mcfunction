scoreboard players set #hmode s9 4
scoreboard players set #hspd s9 90
scoreboard players set #hwait s9 0
scoreboard players set #lkphase s9 0
tag @e[tag=s9_lkt] remove s9_lkt
execute as @a[tag=s9_hidden] at @s align xyz positioned ~.5 ~ ~.5 as @e[tag=s9_locker,distance=..0.3] run tag @s add s9_lkt
scoreboard players operation #htarget s9 = #lk s9
function station9:ai/retarget
