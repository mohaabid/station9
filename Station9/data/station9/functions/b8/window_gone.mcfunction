scoreboard players set #window s9 2
setblock 27 54 30 minecraft:redstone_lamp[lit=false]
tp @e[tag=s9_window] 0 -60 0
kill @e[tag=s9_window]
execute as @a at @s run playsound station9:sfx.sting_hit master @s ~ ~ ~ 0.35 1.0
schedule function station9:b8/window_lamp 8t
schedule function station9:b8/window_line 60t
