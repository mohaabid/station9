scoreboard players add #ct s9 1
execute if score #ct s9 matches 10.. run function station9:chase/pulse
execute as @a[scores={s9_deaths=1..}] run function station9:chase/died
execute if score #steam s9 matches 0 if entity @a[x=44.3,y=41,z=34.3,dx=3.4,dy=2,dz=0.4] run function station9:event/steam
execute if entity @a[x=2.3,y=41,z=18.3,dx=1.4,dy=2,dz=2.4] run function station9:end/1
