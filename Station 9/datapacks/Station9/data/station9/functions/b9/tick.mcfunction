execute if score #teach s9 matches 1..3 run function station9:b9/teach
execute if score #stage s9 matches 5 if entity @a[nbt={Inventory:[{tag:{s9key:1b}}]}] run function station9:b9/got_key
execute if score #stage s9 matches 7 if entity @a[nbt={Inventory:[{tag:{s9fuse:1b}}]}] run function station9:b9/got_fuse
execute if block 28 42 20 #minecraft:buttons[powered=true] run function station9:b9/keypad
execute if block 53 42 20 minecraft:lever[powered=true] run function station9:b9/lever
execute if block 31 42 10 #minecraft:buttons[powered=true] run function station9:tape/hale2
execute if block 11 42 1 #minecraft:buttons[powered=true] run function station9:tape/marsh
execute if score #stage s9 matches 5..7 if entity @a[x=50.3,y=41,z=15.3,dx=9.4,dy=2,dz=9.4] run execute if score #s_nofuse s9 matches 0 run function station9:once/s_nofuse
# the mirror: look into it, then turn around
execute if score #mirror s9 matches 0 if entity @a[x=11.3,y=41,z=7.3,dx=1.4,dy=2,dz=1.4,y_rotation=140..180] run function station9:b9/mirror_1
execute if score #mirror s9 matches 0 if entity @a[x=11.3,y=41,z=7.3,dx=1.4,dy=2,dz=1.4,y_rotation=-180..-140] run function station9:b9/mirror_1
execute if score #mirror s9 matches 1 if entity @a[y_rotation=-100..100] run function station9:b9/mirror_2
execute if score #mirror s9 matches 1 unless entity @a[x=11.3,y=41,z=7.3,dx=1.4,dy=2,dz=1.4] run function station9:b9/mirror_2
execute if entity @a[x=10.3,y=41,z=0.3,dx=3.4,dy=2,dz=0.4] run execute if score #s_marsh s9 matches 0 run function station9:once/s_marsh
execute if score #cscene s9 matches 1 if entity @a[x=26.3,y=41,z=23.3,dx=9.4,dy=2,dz=6.4] run function station9:b9/cell_scene
# whispers, once each, when it is far away
scoreboard players add #b9t s9 1
execute if score #b9t s9 matches 3000.. if score #talk s9 matches ..0 as @a at @s unless entity @e[tag=s9_hunter,distance=..18] run execute if score #s_wh1 s9 matches 0 run function station9:once/s_wh1
execute if score #b9t s9 matches 8000.. if score #talk s9 matches ..0 if score #on s9 matches 1 as @a at @s unless entity @e[tag=s9_hunter,distance=..18] run execute if score #s_wh2 s9 matches 0 run function station9:once/s_wh2
