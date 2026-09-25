tag @s add s9_hidden
scoreboard players set #hidden s9 1
execute align xyz positioned ~.5 ~ ~.5 as @e[tag=s9_locker,distance=..0.3] run scoreboard players operation #lk s9 = @s s9_ln
execute if score #hmode s9 matches 1.. run function station9:ai/hid
