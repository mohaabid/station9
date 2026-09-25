setblock 7 102 21 minecraft:stone_button[face=wall,facing=east,powered=false]
playsound station9:sfx.beep_key block @a 7 102 21 1 1 0
execute if score #s_called s9 matches 1.. run return 0
execute if score #kit s9 matches 0 run return run function station9:surface/call_nokit
scoreboard players set #s_called s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "It's coming up. The lift still runs on the backup line, so that's something.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_called voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 95
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Wait for the lift", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
function station9:story/lift_arrives
