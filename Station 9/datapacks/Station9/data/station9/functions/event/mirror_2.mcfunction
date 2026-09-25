scoreboard players set #mirror s9 2
tp @e[tag=s9_mirror] 0 -200 0
kill @e[tag=s9_mirror]
setblock 12 42 6 minecraft:air
particle minecraft:block minecraft:light_gray_stained_glass 12.5 42.5 6.5 0.3 0.3 0.1 1 40 force
playsound minecraft:block.glass.break block @a 12.5 42.5 6.5 1.4 0.7 1
setblock 12 44 8 minecraft:redstone_lamp[lit=false]
setblock 12 44 4 minecraft:redstone_lamp[lit=false]
effect give @a minecraft:darkness 3 0 true
