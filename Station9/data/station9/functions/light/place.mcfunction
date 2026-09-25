execute align xyz positioned ~.5 ~.5 ~.5 if entity @e[tag=s9_lp,distance=..0.1] run return 0
execute at @e[tag=s9_lp] if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air
execute align xyz positioned ~.5 ~.5 ~.5 run tp @e[tag=s9_lp] ~ ~ ~
execute if score #charge s9 matches 541.. if block ~ ~ ~ #station9:airy run setblock ~ ~ ~ minecraft:light[level=14]
execute if score #charge s9 matches ..540 if block ~ ~ ~ #station9:airy run setblock ~ ~ ~ minecraft:light[level=10]
