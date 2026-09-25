stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "You're at the top. Walk away from the cage. Slowly. I'm sending it back down.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.e_out voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 104
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Walk away", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Leave the lift house", "color": "gray", "italic": true}
