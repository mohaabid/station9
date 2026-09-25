scoreboard players set #stage s9 8
scoreboard players set #cscene s9 3
# the lights die, and when they come back it's gone
setblock 31 44 23 minecraft:redstone_lamp[lit=false]
setblock 31 44 28 minecraft:redstone_lamp[lit=false]
scoreboard players set #fried s9 1
execute as @a at @s run playsound station9:sfx.flash_buzz master @s ~ ~ ~ 0.7 1.0
tp @e[tag=s9_hunter] 59.0 41 24.0
scoreboard players set #hnode s9 35
scoreboard players set #hnext s9 -1
scoreboard players set #htarget s9 35
scoreboard players set #hwait s9 0
scoreboard players set #hmode s9 3
scoreboard players set #hspd s9 115
scoreboard players set #lost s9 60
scoreboard players set #hgrace s9 120
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "You've got it. Get out of there. Go!", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_fuse voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 52
schedule function station9:b9/fuse_lights 50t
schedule function station9:b9/fuse_line 122t
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Bring the fuse to Generator B", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  East end. It's waiting there.", "color": "gray", "italic": true}
