scoreboard players set #stage s9 9
scoreboard players set #hmode s9 0
tp @e[tag=s9_hunter] 0 -60 0
kill @e[tag=s9_hunter]
tp @e[tag=s9_ghost] 0 -60 0
kill @e[tag=s9_ghost]
clear @a minecraft:blaze_rod{s9fuse:1b}
data modify block 53 43 20 front_text.messages set value ['{"text": "GENERATOR B"}','{"text": "FUSE: OK"}','{"text": ""}','{"text": "RUNNING"}']
data modify block 53 43 20 front_text.color set value "lime"
stopsound @a ambient
function station9:build/b9_all_on
function station9:build/b8_all_on
execute as @a at @s run playsound station9:sfx.gen_start block @s ~ ~ ~ 1 1
execute as @a at @s run playsound station9:sfx.lights_on block @s ~ ~ ~ 1 1
playsound station9:sfx.gen_hum block @a 55 42 20 1.5 1 0
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> ...", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
function station9:story/lockdown
function station9:gen/sequence
