# something walks behind you in the corridor, and stops a moment after you do
execute as @a[x=7.3,y=41,z=19.3,dx=40.4,dy=2,dz=0.4] at @s run function station9:tick/footsteps_player
scoreboard players set @a s9_walk 0
scoreboard players set @a s9_sprint 0
