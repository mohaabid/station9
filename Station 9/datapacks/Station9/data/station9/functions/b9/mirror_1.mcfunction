scoreboard players set #mirror s9 1
kill @e[tag=s9_mirror]
summon minecraft:wither_skeleton 12.5 41 2.5 {Tags:["s9","s9_ghost","s9_mirror"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",HandItems:[{},{}],ArmorItems:[{},{},{},{}],Rotation:[0f,0f]}
playsound minecraft:entity.player.breath hostile @a 12.5 42 9.8 0.5 0.5 0
