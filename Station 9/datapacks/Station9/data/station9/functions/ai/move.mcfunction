$execute as @e[tag=s9_hunter,limit=1] at @s if entity @e[tag=s9_next,distance=..$(spd)] run return run function station9:ai/snap
$execute as @e[tag=s9_hunter,limit=1] at @s facing entity @e[tag=s9_next,limit=1] feet run tp @s ^ ^ ^$(spd) ~ 0
