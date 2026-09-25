setblock 31 44 23 minecraft:redstone_lamp[lit=true]
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: You still with me? Your camera cut out for a second.", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
