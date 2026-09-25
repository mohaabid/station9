scoreboard players set #stage s9 2
scoreboard players set #time s9 0
gamemode adventure @a
tp @a 69.5 101 18.5 90 0
effect give @a minecraft:blindness 2 0 true
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Sign in at the security hut", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Through the gate, on the left", "color": "gray", "italic": true}
schedule function station9:fx/storm 400t
function station9:story/arrive
