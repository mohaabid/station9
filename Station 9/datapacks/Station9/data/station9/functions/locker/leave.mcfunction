tag @s remove s9_hidden
scoreboard players set #hidden s9 0
execute if score #hmode s9 matches 4 if score #hwait s9 matches 1.. at @e[tag=s9_hunter] if entity @s[distance=..4] run function station9:ai/catch
