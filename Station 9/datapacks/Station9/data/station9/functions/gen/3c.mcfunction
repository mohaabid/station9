playsound minecraft:entity.zombie.attack_iron_door hostile @a 48 42 20 2.0 0.6 1
playsound minecraft:entity.ravager.attack hostile @a 48 42 20 1.4 0.5 1
scoreboard players set #shake s9 6
schedule function station9:fx/shake 1t
function station9:build/lamps_all_off
function station9:build/emergency_on
playsound minecraft:entity.warden.roar hostile @a 47 42 20 1.5 0.8 1
effect give @a minecraft:darkness 3 0 true
fill 58 41 26 59 43 26 minecraft:air
fill 35 41 31 36 43 31 minecraft:air
playsound minecraft:block.piston.contract block @a 58.5 42 26 1.2 0.5 1
spawnpoint @a 58 41 24
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: IT'S AT THE DOOR! Maintenance tunnel - south side - get back to the lift! RUN!", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
title @a times 5 30 10
title @a title {"text": " "}
title @a subtitle {"text": "RUN", "color": "dark_red", "bold": true}
schedule function station9:gen/4 70t
