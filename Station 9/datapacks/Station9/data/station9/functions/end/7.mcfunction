setblock 4 44 20 minecraft:redstone_lamp[lit=false]
tp @e[tag=s9_final] 0 -200 0
kill @e[tag=s9_final]
effect give @a minecraft:blindness 4 0 true
title @a times 10 80 30
title @a title {"text": "THE END", "color": "dark_red", "bold": true}
title @a subtitle {"text": ""}
schedule function station9:end/8 70t
