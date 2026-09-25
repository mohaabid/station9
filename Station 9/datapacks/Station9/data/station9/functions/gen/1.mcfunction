scoreboard players set #stage s9 6
clear @a minecraft:blaze_rod{s9fuse:1b}
data modify block 53 43 20 front_text.messages[1] set value '{"text": "FUSE: OK"}'
data modify block 53 43 20 front_text.color set value "lime"
function station9:build/lamps_all_on
playsound minecraft:block.beacon.activate block @a 55 42 20 1.5 0.7 1
playsound minecraft:block.piston.extend block @a 55 42 20 1 0.5 1
playsound minecraft:block.respawn_anchor.charge block @a 55 42 20 1 0.6 1
title @a actionbar {"text": "POWER RESTORED", "color": "green"}
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: POWER'S UP! Every level is lighting up on my board -", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
schedule function station9:gen/2 70t
