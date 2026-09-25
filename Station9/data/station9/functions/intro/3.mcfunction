fill 6 41 19 6 43 20 minecraft:air
playsound minecraft:block.piston.contract block @a 6 42 20 1 0.5 1
playsound minecraft:block.iron_door.open block @a 6 42 20 1 0.6 1
scoreboard players set #stage s9 2
scoreboard players set #time s9 0
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: ...signal's bad. Generator B. East end. Go.", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
title @a actionbar {"text": "Restore power: find Generator B (east)", "color": "gold"}
