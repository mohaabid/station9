scoreboard players set #ghint s9 1
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: No fuse? There are spares in Containment. That door needs a Level 3 keycard.", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
