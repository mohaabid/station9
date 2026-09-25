scoreboard players remove #ride s9 1
execute as @a at @s run playsound minecraft:entity.minecart.riding block @s ~ ~ ~ 0.5 0.7
execute as @a at @s run playsound minecraft:block.chain.step block @s ~ ~ ~ 0.6 0.6
execute if score #ride s9 matches 1 run title @a actionbar {"text": "^  B1", "color": "dark_gray"}
execute if score #ride s9 matches 2 run title @a actionbar {"text": "^  B2", "color": "dark_gray"}
execute if score #ride s9 matches 3 run title @a actionbar {"text": "^  B3", "color": "dark_gray"}
execute if score #ride s9 matches 4 run title @a actionbar {"text": "^  B4", "color": "dark_gray"}
execute if score #ride s9 matches 5 run title @a actionbar {"text": "^  B5", "color": "dark_gray"}
execute if score #ride s9 matches 6 run title @a actionbar {"text": "^  B6", "color": "dark_gray"}
execute if score #ride s9 matches 7 run title @a actionbar {"text": "^  B7", "color": "dark_gray"}
execute if score #ride s9 matches 8 run title @a actionbar {"text": "^  B8", "color": "dark_gray"}
execute if score #ride s9 matches 9 run title @a actionbar {"text": "^  B9", "color": "dark_gray"}
execute if score #ride s9 matches 2.. run schedule function station9:end/ride 28t
execute if score #ride s9 matches ..1 run function station9:end/4
