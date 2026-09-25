scoreboard players set #s_incage s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "Press B9 when you're ready. I'll talk you down.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a0_in_cage voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 69
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Press B9", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
