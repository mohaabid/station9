scoreboard players set #stage s9 5
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: A fuse? Good. Get it into Generator B.", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
execute as @a at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.9
title @a actionbar {"text": "Bring the fuse to Generator B", "color": "gold"}
