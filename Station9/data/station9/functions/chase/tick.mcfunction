execute if entity @a[y=49,dy=6] run execute if score #s_b8chase s9 matches 0 run function station9:once/s_b8chase
execute if entity @a[x=46.3,y=51,z=16.3,dx=5.4,dy=2,dz=0.4] run execute if score #s_collapse s9 matches 0 run function station9:once/s_collapse
execute if entity @a[x=2.3,y=51,z=18.3,dx=1.4,dy=2,dz=2.4] run function station9:end/1
execute if score #siren s9 matches 1.. run scoreboard players remove #siren s9 1
execute if score #siren s9 matches 1 run execute as @a at @s run playsound station9:sfx.siren master @s ~ ~ ~ 0.6 0.95
