setblock 3 102 18 minecraft:stone_button[face=wall,facing=south,powered=false]
execute unless score #s_called s9 matches 2 run return 0
execute unless entity @a[x=2.3,y=101,z=18.3,dx=1.4,dy=2,dz=2.4] run return 0
scoreboard players set #s_called s9 3
playsound station9:sfx.beep_key block @a 3 102 18 1 1 0
tp @a[x=5.3,y=101,z=18.3,dx=2.4,dy=2,dz=2.4] 3.5 101 20 -90 0
fill 6 101 19 6 103 20 minecraft:iron_block
playsound station9:sfx.gate_close block @a 6 102 20 1.3 1 0
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Lift 2", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Going down", "color": "gray", "italic": true}
schedule function station9:story/descend 40t
