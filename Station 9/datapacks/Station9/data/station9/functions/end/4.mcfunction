title @a times 20 80 20
title @a title {"text": "ESCAPED", "color": "green", "bold": true}
title @a subtitle {"text": "Station 9  -  Level B9", "color": "gray"}
execute as @a at @s run playsound minecraft:block.beacon.deactivate block @s ~ ~ ~ 1 0.8
schedule function station9:end/5 140t
