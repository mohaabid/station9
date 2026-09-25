function station9:tick/ambient
execute if score #stage s9 matches 2 run function station9:tick/footsteps
execute if score #stage s9 matches 2 if entity @a[nbt={Inventory:[{tag:{s9key:1b}}]}] run function station9:event/got_key
execute if score #stage s9 matches 4 if entity @a[nbt={Inventory:[{tag:{s9fuse:1b}}]}] run function station9:event/got_fuse
execute if block 28 42 20 minecraft:stone_button[powered=true] run function station9:event/keypad
execute if block 53 42 20 minecraft:lever[powered=true] run function station9:event/lever
# the mirror: look into it, then turn around
execute if score #mirror s9 matches 0 if entity @a[x=11.3,y=41,z=7.3,dx=1.4,dy=2,dz=1.4,y_rotation=140..180] run function station9:event/mirror_1
execute if score #mirror s9 matches 0 if entity @a[x=11.3,y=41,z=7.3,dx=1.4,dy=2,dz=1.4,y_rotation=-180..-140] run function station9:event/mirror_1
execute if score #mirror s9 matches 1 if entity @a[y_rotation=-100..100] run function station9:event/mirror_2
execute if score #mirror s9 matches 1 unless entity @a[x=11.3,y=41,z=7.3,dx=1.4,dy=2,dz=1.4] run function station9:event/mirror_2
execute if score #cstalk s9 matches 1 run function station9:tick/cstalk
execute if score #kscare s9 matches 0 if score #stage s9 matches 4.. if entity @a[x=26.3,y=41,z=23.3,dx=9.4,dy=2,dz=6.4] run function station9:event/k_scare_1
execute if score #ghint s9 matches 0 if score #stage s9 matches 2..3 if entity @a[x=50.3,y=41,z=15.3,dx=9.4,dy=2,dz=9.4] run function station9:event/gen_hint
