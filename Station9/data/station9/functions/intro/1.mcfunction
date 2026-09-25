tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: Radio check. You're on the lift down to B9. The station's been dark for six weeks.", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
scoreboard players set #ride s9 0
schedule function station9:intro/ride 20t
