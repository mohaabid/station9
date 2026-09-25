fill 49 41 19 49 43 20 minecraft:iron_block
fill 52 41 14 53 43 14 minecraft:iron_block
playsound minecraft:block.iron_door.close block @a 49 42 20 1.5 0.5 0
playsound station9:sfx.bang hostile @a 49 42 20 0.8 1.2 0
execute as @a at @s run playsound station9:sfx.siren master @s ~ ~ ~ 0.9 1
title @a times 5 40 10
title @a subtitle {"text": "!! LOCKDOWN !!", "color": "red"}
title @a title {"text": " ", "color": "dark_red", "bold": true}
