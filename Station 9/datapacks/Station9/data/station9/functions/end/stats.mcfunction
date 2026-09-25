scoreboard players set #stage s9 11
scoreboard players operation #sec s9 = #time s9
scoreboard players operation #sec s9 /= #20 s9
scoreboard players operation #min s9 = #sec s9
scoreboard players operation #min s9 /= #60 s9
scoreboard players operation #sec s9 %= #60 s9
tellraw @a ["",{"text": "\n  S T A T I O N   9\n", "color": "dark_red", "bold": true}]
tellraw @a ["",{"text": "  Time: ", "color": "gray"},{"score":{"name":"#min","objective":"s9"},"color":"white"},{"text": "m ", "color": "white"},{"score":{"name":"#sec","objective":"s9"},"color":"white"},{"text": "s", "color": "white"},{"text": "     Deaths: ", "color": "gray"},{"score":{"name":"#deaths","objective":"s9"},"color":"white"},{"text": "     Tapes: ", "color": "gray"},{"score":{"name":"#tapes","objective":"s9"},"color":"white"},{"text": "/3", "color": "white"}]
execute if score #ending s9 matches 1 run tellraw @a ["",{"text": "  Ending 1 of 2: Passenger.", "color": "gray"},{"text": "  (Marsh knew another way.)", "color": "dark_gray", "italic": true}]
execute if score #ending s9 matches 2 run tellraw @a ["",{"text": "  Ending 2 of 2: Lights Out.", "color": "gray"}]
tellraw @a ["",{"text": "  "},{"text": "[ Play again ]", "color": "gold", "bold": true, "clickEvent": {"action": "run_command", "value": "/function station9:start"}, "hoverEvent": {"action": "show_text", "contents": "Rebuild the station and start over"}}]
tellraw @a ""
