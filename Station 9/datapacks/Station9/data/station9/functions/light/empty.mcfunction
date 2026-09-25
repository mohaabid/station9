# out of charge: swap in a spare if there is one
execute if score @s s9_bat matches 1.. run function station9:light/swap
execute if score @s s9_bat matches 0 run scoreboard players set #on s9 0
execute if score @s s9_bat matches 0 run scoreboard players set #light s9 0
execute if score @s s9_bat matches 0 run title @a actionbar {"text": "Flashlight: battery dead", "color": "red"}
