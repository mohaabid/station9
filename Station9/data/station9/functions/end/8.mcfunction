scoreboard players operation #sec s9 = #time s9
scoreboard players operation #sec s9 /= #20 s9
scoreboard players operation #min s9 = #sec s9
scoreboard players operation #min s9 /= #60 s9
scoreboard players operation #sec s9 %= #60 s9
tellraw @a ["",{"text": "\n  S T A T I O N   9\n", "color": "dark_red", "bold": true}]
tellraw @a ["",{"text": "  Time: ", "color": "gray"},{"score":{"name":"#min","objective":"s9"},"color":"white"},{"text": "m ", "color": "white"},{"score":{"name":"#sec","objective":"s9"},"color":"white"},{"text": "s", "color": "white"},{"text": "     Deaths: ", "color": "gray"},{"score":{"name":"#deaths","objective":"s9"},"color":"white"}]
tellraw @a ["",{"text": "  "},{"text": "[ Play again ]", "color": "gold", "bold": true, "clickEvent": {"action": "run_command", "value": "/function station9:start"}, "hoverEvent": {"action": "show_text", "contents": "Rebuild the station and start over"}}]
tellraw @a ""
