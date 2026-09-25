execute as @a at @s run playsound station9:sfx.roof_thump hostile @s ~ ~3 ~ 1 1
scoreboard players set #shake s9 10
schedule function station9:fx/shake 1t
setblock 4 54 20 minecraft:redstone_lamp[lit=false]
schedule function station9:fx/on_e8a 6t
