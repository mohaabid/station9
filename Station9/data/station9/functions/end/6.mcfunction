tp @a 5.3 41 20.0 90 -8
summon minecraft:wither_skeleton 2.6 41 20.0 {Tags:["s9","s9_stalker","s9_final"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",CustomName:'{"text": "Subject 9"}',Rotation:[-90f,0f]}
tp @e[tag=s9_final] 2.6 41 20.0 -90 0
setblock 4 44 20 minecraft:redstone_lamp[lit=true]
execute as @a at @s run playsound minecraft:entity.warden.roar hostile @s ~ ~ ~ 1.6 0.9
execute as @a at @s run playsound minecraft:entity.elder_guardian.curse hostile @s ~ ~ ~ 1 0.5
schedule function station9:end/7 14t
