execute unless score #stage s9 matches 4 run return 0
scoreboard players set #stage s9 5
spawnpoint @a 9 41 20 -90
function station9:build/b9_backup
setblock 7 43 25 minecraft:redstone_lamp[lit=false]
scoreboard players set #tab s9 0
kill @e[tag=s9_hunter]
summon minecraft:wither_skeleton 48.0 41 20.0 {Tags:["s9","s9_hunter"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",HandItems:[{},{}],ArmorItems:[{},{},{},{}],Rotation:[90f,0f]}
tp @e[tag=s9_hunter] 48.0 41 20.0 90 0
scoreboard players set #hnode s9 7
scoreboard players set #hnext s9 -1
scoreboard players set #htarget s9 7
scoreboard players set #hwait s9 0
scoreboard players set #hmode s9 6
scoreboard players set #teach s9 1
stopsound @a voice
tellraw @a ["", {"text": "[Radio] ", "color": "dark_aqua"}, {"text": "Reyes: ", "color": "dark_aqua"}, {"text": "B9. The generator room is at the east end of the main corridor. ...Wait. Your camera. There's someone at the end of the corridor.", "color": "gray", "italic": true}]
execute as @a at @s run playsound station9:voice.a2_arrive voice @s ~ ~ ~ 1 1
scoreboard players set #talk s9 156
scoreboard players reset * s9_hud
scoreboard players set #o1 s9_hud 2
scoreboard players display name #o1 s9_hud {"text": "> Restore Generator B", "color": "gold"}
execute as @a at @s run playsound minecraft:ui.toast.in master @s ~ ~ ~ 0.5 1.2
scoreboard players set #o2 s9_hud 1
scoreboard players display name #o2 s9_hud {"text": "  East end of the corridor", "color": "gray", "italic": true}
