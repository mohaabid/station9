scoreboard players set #stage s9 4
spawnpoint @a 8 51 19 -90
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Get out of the lift", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Press DOOR RELEASE", "color": "gray", "italic": true}
