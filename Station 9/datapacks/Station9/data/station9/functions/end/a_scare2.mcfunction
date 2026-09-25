kill @e[tag=s9_final]
summon minecraft:wither_skeleton 2.7 101 20.0 {Tags:["s9","s9_ghost","s9_final"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",HandItems:[{},{}],ArmorItems:[{},{},{},{}],Rotation:[-90f,0f]}
execute as @a at @s run tp @s ~ ~ ~ facing entity @e[tag=s9_final,limit=1] eyes
effect give @a minecraft:slowness 2 255 true
setblock 4 104 20 minecraft:redstone_lamp[lit=true]
execute as @a at @s run playsound station9:sfx.scream hostile @s ~ ~ ~ 1 1
execute as @a at @s run playsound station9:sfx.sting_hit master @s ~ ~ ~ 1 1
schedule function station9:end/a_black 16t
