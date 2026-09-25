# look at it through the glass, or walk to its door, and it is gone
execute if entity @a[x=22.3,y=51,z=19.3,dx=8.4,dy=2,dz=5.4,y_rotation=-50..50] run scoreboard players add #wlook s9 1
execute if score #wlook s9 matches 30.. run function station9:b8/window_gone
execute if entity @a[x=29.3,y=51,z=25.3,dx=1.4,dy=2,dz=1.4] run function station9:b8/window_gone
execute unless entity @a[x=21.3,y=51,z=18.3,dx=10.4,dy=2,dz=14.4] run function station9:b8/window_gone_quiet
