tag @s add s9_seen
execute if score #stage s9 matches 0 run tp @s 69.5 101 18.5 90 0
execute if score #stage s9 matches 0 run effect give @s minecraft:blindness 6 0 true
execute if score #stage s9 matches 0 run schedule function station9:start 40t
execute if score #stage s9 matches 1.. run tellraw @s ["",{"text": "[Station 9] ", "color": "dark_red"},{"text": "Click here to restart the map", "color": "gray", "underlined": true, "clickEvent": {"action": "run_command", "value": "/function station9:start"}}]
