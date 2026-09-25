scoreboard players set #stage s9 1
tp @a 4 41 20.5 -90 0
effect give @a minecraft:blindness 5 0 true
setblock 4 44 20 minecraft:redstone_lamp[lit=true]
title @a times 30 80 30
title @a subtitle {"text": "Research Level B9  -  last contact 41 days ago", "color": "gray"}
title @a title {"text": "STATION 9", "color": "dark_red", "bold": true}
execute as @a at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 0.6
schedule function station9:intro/1 110t
