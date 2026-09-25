setblock 31 44 23 minecraft:redstone_lamp[lit=false]
setblock 31 44 28 minecraft:redstone_lamp[lit=false]
tp @e[tag=s9_cell] 0 -200 0
kill @e[tag=s9_cell]
execute as @a at @s run playsound minecraft:entity.elder_guardian.curse hostile @s ~ ~ ~ 1 0.6
effect give @a minecraft:darkness 3 0 true
schedule function station9:event/k_scare_4 40t
