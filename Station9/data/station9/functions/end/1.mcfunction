scoreboard players set #stage s9 7
scoreboard players set #hunter s9 0
scoreboard players set #alarm s9 0
tp @a[x=5.3,y=41,z=18.3,dx=1.4,dy=2,dz=2.4] 3.5 41 20 90 0
fill 6 41 19 6 43 20 minecraft:iron_block
playsound minecraft:block.iron_door.close block @a 6 42 20 1.5 0.5 1
playsound minecraft:block.anvil.land block @a 6 42 20 1 0.6 1
tp @e[tag=s9_hunter] 0 -200 0
kill @e[tag=s9_hunter]
kill @e[tag=s9_trail]
setblock 4 44 20 minecraft:redstone_lamp[lit=true]
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: I've got you! Hold on - bringing you up!", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
schedule function station9:end/2 20t
