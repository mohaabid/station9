setblock 31 44 23 minecraft:redstone_lamp[lit=true]
summon minecraft:wither_skeleton 31.5 41 29.5 {Tags:["s9","s9_stalker","s9_cell"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",CustomName:'{"text": "Subject 9"}',Rotation:[180f,0f]}
tp @e[tag=s9_cell] 31.5 41 29.5 180 0
schedule function station9:event/k_scare_3 35t
