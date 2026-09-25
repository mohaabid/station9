# lightning at random, while you're on the surface
execute if entity @a[x=-100,y=95,z=-100,dx=300,dy=100,dz=300] run function station9:fx/lightning
execute store result score #st s9 run random value 500..1500
execute store result storage station9:fx d.t int 1 run scoreboard players get #st s9
function station9:fx/storm_m with storage station9:fx d
