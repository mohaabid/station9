clear @s minecraft:iron_nugget{s9batt:1b} 1
scoreboard players set #charge s9 3600
execute as @a at @s run playsound station9:sfx.flash_on master @s ~ ~ ~ 0.8 0.8
title @a actionbar {"text": "New battery", "color": "yellow"}
