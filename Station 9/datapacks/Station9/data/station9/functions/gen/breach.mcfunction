fill 49 41 19 49 43 20 minecraft:air
particle minecraft:explosion 49.5 42 20 0.3 0.8 0.5 0 6 force
playsound minecraft:entity.generic.explode hostile @a 49.5 42 20 1.2 0.6 0
playsound station9:sfx.scream hostile @a 49.5 42 20 1.0 0.8 0
kill @e[tag=s9_hunter]
summon minecraft:wither_skeleton 49.6 41 20.0 {Tags:["s9","s9_hunter"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",HandItems:[{},{}],ArmorItems:[{},{},{},{}],Rotation:[-90f,0f]}
tp @e[tag=s9_hunter] 49.6 41 20.0 -90 0
scoreboard players set #hnode s9 30
scoreboard players set #hnext s9 -1
scoreboard players set #htarget s9 30
scoreboard players set #hwait s9 0
scoreboard players set #hmode s9 5
scoreboard players set #hspd s9 232
scoreboard players set #hgrace s9 0
function station9:ai/to_player
