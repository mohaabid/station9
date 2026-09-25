scoreboard players set #kdeny s9 1
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: Keycard lock? Try the staff office - north side of the corridor.", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
