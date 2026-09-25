# the cage light follows its lever
execute if score #ride s9 matches 1 if block 5 52 18 minecraft:lever[powered=true] run setblock 4 54 20 minecraft:redstone_lamp[lit=false]
execute if score #ride s9 matches 1 if block 5 52 18 minecraft:lever[powered=false] run setblock 4 54 20 minecraft:redstone_lamp[lit=true]
execute if score #ending s9 matches 2 if entity @a[x=13,y=95,z=0,dx=70,dy=40,dz=45] run execute if score #s_walked s9 matches 0 run function station9:once/s_walked
