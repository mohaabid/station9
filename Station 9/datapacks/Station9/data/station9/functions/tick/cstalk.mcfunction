# it vanishes once you've had a good look, or if you walk up to it
execute if entity @a[x=7.3,y=41,z=19.3,dx=12.4,dy=2,dz=0.4,y_rotation=55..125] run scoreboard players add #cs_seen s9 1
execute if score #cstalk s9 matches 1 if score #cs_seen s9 matches 16.. run function station9:event/cstalk_vanish
execute if score #cstalk s9 matches 1 if entity @a[x=7.3,y=41,z=19.3,dx=4.4,dy=2,dz=0.4] run function station9:event/cstalk_vanish
execute if score #cstalk s9 matches 1 if score #stage s9 matches 4.. run function station9:event/cstalk_vanish
