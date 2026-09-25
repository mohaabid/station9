setblock 4 44 20 minecraft:redstone_lamp[lit=false]
execute as @a at @s run playsound minecraft:entity.warden.sniff hostile @s ^ ^ ^-1.5 1.2 0.6
title @a times 10 60 10
title @a title {"text": " "}
title @a subtitle {"text": "The lift is heavier than it should be.", "color": "dark_gray", "italic": true}
schedule function station9:end/6 80t
