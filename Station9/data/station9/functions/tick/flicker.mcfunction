execute store result score #f s9 run random value 1..100
execute if score #f s9 matches 1..4 if block 21 44 20 minecraft:redstone_lamp[lit=true] run function station9:fx/c2_off
execute if score #f s9 matches 55..100 if block 21 44 20 minecraft:redstone_lamp[lit=false] run setblock 21 44 20 minecraft:redstone_lamp[lit=true]
