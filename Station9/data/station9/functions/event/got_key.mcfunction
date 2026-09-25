scoreboard players set #stage s9 3
tellraw @a ["",{"text": "[Radio] ", "color": "dark_aqua"},{"text": "Ops: That's Marsh's keycard. ...He never signed out.", "color": "gray", "italic": true}]
execute as @a at @s run playsound minecraft:block.note_block.bit master @s ~ ~ ~ 0.35 0.5
execute as @a at @s run playsound minecraft:ui.button.click master @s ~ ~ ~ 0.25 1.8
execute as @a at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.8
summon minecraft:wither_skeleton 8.5 41 19.5 {Tags:["s9","s9_stalker","s9_cstalk"],NoAI:1b,Silent:1b,Invulnerable:1b,PersistenceRequired:1b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",CustomName:'{"text": "Subject 9"}',Rotation:[-90f,0f]}
tp @e[tag=s9_cstalk] 8.5 41 19.5 -90 0
scoreboard players set #cstalk s9 1
scoreboard players set #cs_seen s9 0
schedule function station9:event/office_slam 50t
