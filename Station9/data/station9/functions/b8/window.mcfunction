kill @e[tag=s9_window]
summon minecraft:wither_skeleton 26.5 51 30.5 {Tags:["s9","s9_ghost","s9_window"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",HandItems:[{},{}],ArmorItems:[{},{},{},{}],Rotation:[180f,0f]}
setblock 27 54 30 minecraft:redstone_lamp[lit=true]
scoreboard players set #window s9 1
