# Put the whole station back to its starting state
schedule clear station9:chase/release
schedule clear station9:end/2
schedule clear station9:end/3
schedule clear station9:end/5
schedule clear station9:end/6
schedule clear station9:end/7
schedule clear station9:end/8
schedule clear station9:end/ride
schedule clear station9:event/k_scare_2
schedule clear station9:event/k_scare_3
schedule clear station9:event/k_scare_4
schedule clear station9:event/office_slam
schedule clear station9:fx/alarm
schedule clear station9:fx/c1_on
schedule clear station9:fx/e1_on
schedule clear station9:fx/shake
schedule clear station9:gen/2
schedule clear station9:gen/3
schedule clear station9:gen/3b
schedule clear station9:gen/3c
schedule clear station9:gen/4
schedule clear station9:intro/1
schedule clear station9:intro/2
schedule clear station9:intro/3
schedule clear station9:intro/ride
schedule clear station9:start
kill @e[tag=s9]
function station9:build/all
function station9:rules
scoreboard players set #stage s9 0
scoreboard players set #time s9 0
scoreboard players set #deaths s9 0
scoreboard players set #mirror s9 0
scoreboard players set #cstalk s9 0
scoreboard players set #cs_seen s9 0
scoreboard players set #kscare s9 0
scoreboard players set #kdeny s9 0
scoreboard players set #ghint s9 0
scoreboard players set #steam s9 0
scoreboard players set #hunter s9 0
scoreboard players set #ct s9 0
scoreboard players set #ride s9 0
scoreboard players set #alarm s9 0
scoreboard players set #shake s9 0
scoreboard players set #echoes s9 0
scoreboard players set @a s9_deaths 0
scoreboard players reset @e s9_age
setworldspawn 4 41 20
spawnpoint @a 4 41 20
clear @a
effect clear @a
gamemode adventure @a
effect give @a minecraft:saturation infinite 0 true
summon minecraft:item 18.5 42.05 11.5 {Tags:["s9"],Age:-32768s,PickupDelay:0s,Item:{id:"minecraft:tripwire_hook",Count:1b,tag:{s9key:1b,display:{Name:'{"text": "Keycard - M. Marsh", "italic": false, "color": "aqua"}',Lore:['{"text": "Level 3 access", "color": "dark_gray"}']}}}}
summon minecraft:item 31.5 41.1 27.5 {Tags:["s9"],Age:-32768s,PickupDelay:0s,Item:{id:"minecraft:blaze_rod",Count:1b,tag:{s9fuse:1b,display:{Name:'{"text": "Fuse (30A)", "italic": false, "color": "gold"}',Lore:['{"text": "Generator B", "color": "dark_gray"}']}}}}
