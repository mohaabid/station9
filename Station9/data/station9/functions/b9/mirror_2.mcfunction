scoreboard players set #mirror s9 2
tp @e[tag=s9_mirror] 0 -60 0
kill @e[tag=s9_mirror]
fill 12 41 6 12 42 6 minecraft:air
particle minecraft:block minecraft:light_gray_stained_glass 12.5 42 6.5 0.3 0.5 0.1 1 50 force
playsound minecraft:block.glass.break block @a 12.5 42.5 6.5 1.4 0.7 0
setblock 12 44 8 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_w1 40t
setblock 12 44 4 minecraft:redstone_lamp[lit=false]
effect give @a minecraft:darkness 3 0 true
