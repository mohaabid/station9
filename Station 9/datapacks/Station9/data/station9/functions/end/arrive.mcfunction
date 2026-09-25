scoreboard players set #ride s9 0
stopsound @a ambient station9:amb.lift_ride
scoreboard players reset #o2 s9_hud
execute as @a at @s run tp @s ~ ~50 ~
execute if score #ending s9 matches 2 run setblock 4 104 20 minecraft:redstone_lamp[lit=false]
execute if score #ending s9 matches 1 run setblock 4 104 20 minecraft:redstone_lamp[lit=true]
playsound station9:sfx.gate_open block @a 6 102 20 1.2 1 0
schedule function station9:end/gate_up 40t
execute if score #ending s9 matches 1 run schedule function station9:end/a_scare 90t
execute if score #ending s9 matches 2 run schedule function station9:end/b_line 60t
