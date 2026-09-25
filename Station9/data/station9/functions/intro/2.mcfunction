tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: -sshhk- ...lost the li- ...you there? ...B9? -kssht-", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
schedule function station9:intro/3 90t
