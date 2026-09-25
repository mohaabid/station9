function station9:build/lamps_off
function station9:build/emergency_on
playsound minecraft:entity.warden.roar hostile @a 47 42 20 1.5 0.8 0
stopsound @a block station9:sfx.gen_hum
scoreboard players set #fried s9 1
scoreboard players set #light s9 0
execute as @a at @s run playsound station9:sfx.flash_buzz master @s ~ ~ ~ 0.8 1.0
execute as @a at @s anchored eyes run particle minecraft:electric_spark ^ ^-0.3 ^0.6 0.1 0.1 0.1 0.3 20 force @s
effect give @a minecraft:darkness 3 0 true
fill 58 41 26 59 43 26 minecraft:air
playsound minecraft:block.piston.contract block @a 58.5 42 26 1.2 0.5 0
spawnpoint @a 58 41 24 0
scoreboard players set #tab s9 2
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "It's at the door! Maintenance tunnel, south side! Up the service stairs to B8, then the lift! Run!", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a3_run voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 125
title @a times 5 30 10
title @a subtitle {"text": "RUN", "color": "dark_red"}
title @a title {"text": " ", "color": "dark_red", "bold": true}
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Get to the lift", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Tunnel south, service stairs up to B8", "color": "gray", "italic": true}
