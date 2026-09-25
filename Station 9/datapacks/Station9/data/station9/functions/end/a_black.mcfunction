setblock 4 104 20 minecraft:redstone_lamp[lit=false]
tp @e[tag=s9_final] 0 -60 0
kill @e[tag=s9_final]
effect give @a minecraft:blindness 5 0 true
title @a times 10 90 30
title @a subtitle {"text": "Ending 1 of 2:  Passenger", "color": "gray"}
title @a title {"text": "THE END", "color": "dark_red", "bold": true}
schedule function station9:end/stats 110t
