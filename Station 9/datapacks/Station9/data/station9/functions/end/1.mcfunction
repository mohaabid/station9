scoreboard players set #stage s9 10
scoreboard players set #hmode s9 0
tp @a[x=5.3,y=51,z=18.3,dx=2.4,dy=2,dz=2.4] 3.5 51 20 90 0
fill 6 51 19 6 53 20 minecraft:iron_block
playsound station9:sfx.gate_close block @a 6 52 20 1.5 1 0
tp @e[tag=s9_hunter] 0 -60 0
kill @e[tag=s9_hunter]
kill @e[tag=s9_node]
kill @e[tag=s9_locker]
setblock 5 52 18 minecraft:lever[face=wall,facing=south,powered=false]
setblock 4 54 20 minecraft:redstone_lamp[lit=true]
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Lift 2", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Going up", "color": "gray", "italic": true}
function station9:story/up
