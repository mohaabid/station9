execute if score #s_intro s9 matches 1 if score #talk s9 matches ..0 if score #kit s9 matches 0 if entity @a[x=-20,y=95,z=-20,dx=83.5,dy=40,dz=70] run execute if score #s_walk s9 matches 0 run function station9:once/s_walk
execute if score #s_intro s9 matches 1 if score #talk s9 matches ..0 if score #signed s9 matches 0 if score #kit s9 matches 0 if entity @a[x=33.5,y=101,z=26.5,distance=..5] run execute if score #s_hut s9 matches 0 run function station9:once/s_hut
execute if block 36 101 27 #minecraft:buttons[powered=true] run function station9:surface/signin
execute if score #kit s9 matches 0 if entity @a[nbt={Inventory:[{tag:{s9light:1b}}]}] run function station9:surface/kit
execute if score #kit s9 matches 1 run scoreboard players add #inhut s9 1
execute if score #inhut s9 matches 500.. if score #talk s9 matches ..0 if entity @a[x=31.3,y=101,z=27.3,dx=4.4,dy=2,dz=3.4] run execute if score #s_coffee s9 matches 0 run function station9:once/s_coffee
execute if block 7 102 21 #minecraft:buttons[powered=true] run function station9:surface/call
execute if score #s_called s9 matches 2 if entity @a[x=2.3,y=101,z=18.3,dx=1.4,dy=2,dz=2.4] run execute if score #s_incage s9 matches 0 run function station9:once/s_incage
execute if block 3 102 18 #minecraft:buttons[powered=true] run function station9:surface/b9
