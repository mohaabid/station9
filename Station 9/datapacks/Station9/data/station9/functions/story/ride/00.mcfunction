scoreboard players set #stage s9 3
execute as @a at @s run tp @s ~ ~-50 ~
setblock 4 104 20 minecraft:redstone_lamp[lit=false]
setblock 4 54 20 minecraft:redstone_lamp[lit=true]
stopsound @a ambient
execute as @a at @s run playsound station9:amb.lift_ride ambient @s ~ ~ ~ 0.8 1
