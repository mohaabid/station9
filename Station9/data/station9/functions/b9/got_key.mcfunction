scoreboard players set #stage s9 6
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "That's Marsh's keycard. ...He never signed out.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_key voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 62
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Open Containment", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  Keycard lock, middle of the corridor", "color": "gray", "italic": true}
schedule function station9:b9/office_slam 50t
