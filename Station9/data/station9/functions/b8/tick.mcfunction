execute if block 2 52 19 #minecraft:buttons[powered=true] run function station9:b8/release
execute if block 40 52 25 minecraft:lever[powered=true] run execute if score #s_relay s9 matches 0 run function station9:once/s_relay
execute if block 13 52 20 #minecraft:buttons[powered=true] run function station9:b8/stair_button
execute if block 49 53 20 #minecraft:buttons[powered=true] run function station9:b8/key1
execute if block 49 53 21 #minecraft:buttons[powered=true] run function station9:b8/key2
execute if block 49 53 22 #minecraft:buttons[powered=true] run function station9:b8/key3
execute if block 49 52 20 #minecraft:buttons[powered=true] run function station9:b8/key4
execute if block 49 52 21 #minecraft:buttons[powered=true] run function station9:b8/key5
execute if block 49 52 22 #minecraft:buttons[powered=true] run function station9:b8/key6
execute if block 49 51 20 #minecraft:buttons[powered=true] run function station9:b8/key7
execute if block 49 51 21 #minecraft:buttons[powered=true] run function station9:b8/key8
execute if block 49 51 22 #minecraft:buttons[powered=true] run function station9:b8/key9
execute if block 49 51 23 #minecraft:buttons[powered=true] run function station9:b8/key0
execute if block 46 52 4 #minecraft:buttons[powered=true] run function station9:b8/phone_answer
execute if block 22 52 30 #minecraft:buttons[powered=true] run function station9:tape/hale1
# the code hints
execute if score #s_relay s9 matches 1 if score #s_code s9 matches 0 run scoreboard players add #hint s9 1
execute if score #hint s9 matches 4800 run function station9:b8/hint1
execute if score #hint s9 matches 9600 run function station9:b8/hint2
# small things
execute if entity @a[x=24.3,y=51,z=2.3,dx=0.4,dy=2,dz=10.4] run execute if score #s_doorA s9 matches 0 run function station9:once/s_doora
execute if entity @a[x=18.3,y=51,z=8.3,dx=3.4,dy=2,dz=3.4] run scoreboard players set #inA s9 1
execute if score #inA s9 matches 1 unless entity @a[x=17.3,y=51,z=1.3,dx=8.4,dy=2,dz=12.4] run execute if score #s_bed s9 matches 0 run function station9:once/s_bed
execute if entity @a[x=23.5,y=51,z=3.5,distance=..2.2] run execute if score #s_knock s9 matches 0 run function station9:once/s_knock
execute if score #s_relay s9 matches 1 if entity @a[x=34.3,y=51,z=4.3,dx=12.4,dy=2,dz=9.4] run execute if score #s_ring s9 matches 0 run function station9:once/s_ring
execute if score #s_relay s9 matches 1 if entity @a[x=22.3,y=51,z=19.3,dx=8.4,dy=2,dz=5.4] run execute if score #s_window s9 matches 0 run function station9:once/s_window
execute if score #window s9 matches 1 run function station9:b8/window_tick
execute if score #s_code s9 matches 1 if entity @a[x=8.3,y=51,z=14.3,dx=11.4,dy=2,dz=5.4] run execute if score #s_ceiling s9 matches 0 run function station9:once/s_ceiling
execute if score #s_code s9 matches 1 if entity @a[x=21,y=50,z=15,dx=10,dy=4,dz=3,y_rotation=45..135] run execute if score #s_turn s9 matches 0 run function station9:once/s_turn
execute if score #s_turn s9 matches 1 if entity @a[x=21,y=50,z=15,dx=30,dy=4,dz=3,y_rotation=-135..-45] run execute if score #s_turn2 s9 matches 0 run function station9:once/s_turn2
# down the stairs
execute if score #s_code s9 matches 1 if entity @a[x=8.3,y=41,z=22.3,dx=3.4,dy=6,dz=8.4] run execute if score #s_st3 s9 matches 0 run function station9:once/s_st3
execute if entity @a[x=7.3,y=41,z=19.3,dx=6.4,dy=2,dz=1.4] run function station9:story/b9_arrive
