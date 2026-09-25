scoreboard players add #ride s9 1
execute as @a at @s run playsound minecraft:entity.minecart.riding block @s ~ ~ ~ 0.5 0.6
execute as @a at @s run playsound minecraft:block.chain.step block @s ~ ~ ~ 0.6 0.5
execute if score #ride s9 matches 1 run title @a actionbar {"text": "v  B1", "color": "dark_gray"}
execute if score #ride s9 matches 2 run title @a actionbar {"text": "v  B2", "color": "dark_gray"}
execute if score #ride s9 matches 3 run title @a actionbar {"text": "v  B3", "color": "dark_gray"}
execute if score #ride s9 matches 4 run title @a actionbar {"text": "v  B4", "color": "dark_gray"}
execute if score #ride s9 matches 5 run title @a actionbar {"text": "v  B5", "color": "dark_gray"}
execute if score #ride s9 matches 6 run title @a actionbar {"text": "v  B6", "color": "dark_gray"}
execute if score #ride s9 matches 7 run title @a actionbar {"text": "v  B7", "color": "dark_gray"}
execute if score #ride s9 matches 8 run title @a actionbar {"text": "v  B8", "color": "dark_gray"}
execute if score #ride s9 matches 3 run tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: Get Generator B running - east end of the level. Then we bring you up.", "color": "gray", "italic": true}]
execute if score #ride s9 matches 3 run execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute if score #ride s9 matches 3 run execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
execute if score #ride s9 matches 6 run setblock 4 44 20 minecraft:redstone_lamp[lit=false]
execute if score #ride s9 matches 6 run schedule function station9:fx/e1_on 3t
execute if score #ride s9 matches 6 run playsound minecraft:entity.iron_golem.damage hostile @a 4 45 20 0.5 0.5 1
execute if score #ride s9 matches ..7 run schedule function station9:intro/ride 30t
execute if score #ride s9 matches 8.. run function station9:intro/crash
