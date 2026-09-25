tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: ...wait. Containment B9 reads OPEN. It's read open for six weeks-", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
fill 49 41 19 49 43 20 minecraft:iron_block
playsound minecraft:block.iron_door.close block @a 49 42 20 1.5 0.5 1
playsound minecraft:block.anvil.land block @a 49 42 20 1 0.5 1
title @a actionbar {"text": "!! LOCKDOWN !!", "color": "red", "bold": true}
scoreboard players set #alarm s9 18
schedule function station9:fx/alarm 1t
schedule function station9:gen/3 50t
