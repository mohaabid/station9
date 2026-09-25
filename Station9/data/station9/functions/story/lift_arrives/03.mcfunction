fill 6 101 19 6 103 20 minecraft:air
scoreboard players set #s_called s9 2
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Get in the lift", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
