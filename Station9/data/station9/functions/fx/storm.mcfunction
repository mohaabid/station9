# lightning at random, while you're on the surface
execute if entity @a[y=95,dy=100] run function station9:fx/lightning
execute store result score #st s9 run random value 500..1500
execute store result storage station9:fx d.t int 1 run scoreboard players get #st s9
function station9:fx/storm_m with storage station9:fx d
