stopsound @a ambient station9:amb.lift_ride
stopsound @a voice
execute as @a at @s run playsound station9:sfx.crash master @s ~ ~ ~ 1 1
setblock 4 54 20 minecraft:redstone_lamp[lit=false]
scoreboard players set #shake s9 22
schedule function station9:fx/shake 1t
effect give @a minecraft:darkness 7 0 true
effect give @a minecraft:blindness 3 0 true
scoreboard players reset #o2 s9_hud
